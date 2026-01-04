/*
 * newline_compact.c
 *
 * 功能：
 *   读取指定的文本文件，执行等价于以下正则“全部替换”的操作，然后覆盖写回原文件：
 *
 *     查找:  \r?\n\r?\n(?!\r?\n)
 *     替换:  \n
 *
 * 解释（与实现一致）：
 *   将 CRLF(\r\n) 与 LF(\n) 都视为“一个换行”；
 *   对于任意连续换行段长度 N：
 *     - N <= 1：保持不变
 *     - N >= 2：写出 N-1 个 '\n'
 *
 * 文件覆盖策略（尽量降低损坏风险）：
 *   1) 写入临时文件 <原文件>.tmp
 *   2) 将原文件重命名为 <原文件>.bak
 *   3) 将临时文件重命名为原文件名
 *   4) 成功后删除 .bak
 *
 * 用法：
 *   Windows / Linux:
 *     gcc -std=c11 -O2 -Wall -Wextra newline_compact.c -o newline_compact
 *     ./newline_compact  yourfile.txt
 *
 * 注意：
 *   - 本程序按“字节”处理，不改变除换行规则以外的内容（编码如 UTF-8/GBK 均可）。
 *   - 输出换行统一为 '\n'（与替换填入 '\n' 一致）。
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

static int write_n_lf(FILE *out, size_t n) {
    for (size_t i = 0; i < n; i++) {
        if (fputc('\n', out) == EOF) return -1;
    }
    return 0;
}

/* 按给定规则冲刷累计的“换行段” */
static int flush_newline_run(FILE *out, size_t run_len) {
    if (run_len == 0) return 0;
    if (run_len == 1) return write_n_lf(out, 1);
    /* run_len >= 2 -> 输出 run_len - 1 个 '\n' */
    return write_n_lf(out, run_len - 1);
}

/* 将输入流按规则转换写入输出流 */
static int process_stream(FILE *in, FILE *out) {
    int c;
    size_t newline_run = 0;

    while ((c = fgetc(in)) != EOF) {
        if (c == '\n') {
            newline_run++;
            continue;
        }

        if (c == '\r') {
            int n = fgetc(in);
            if (n == '\n') {
                /* CRLF 视为一个换行 */
                newline_run++;
                continue;
            }
            /* 孤立 '\r'：回退读取并当普通字符处理 */
            if (n != EOF) ungetc(n, in);

            if (flush_newline_run(out, newline_run) != 0) return -1;
            newline_run = 0;

            if (fputc('\r', out) == EOF) return -1;
            continue;
        }

        /* 普通字符：先冲刷换行段，再写字符 */
        if (flush_newline_run(out, newline_run) != 0) return -1;
        newline_run = 0;

        if (fputc(c, out) == EOF) return -1;
    }

    /* EOF：冲刷尾部换行段 */
    if (flush_newline_run(out, newline_run) != 0) return -1;

    return 0;
}

static char *cat_suffix(const char *path, const char *suffix) {
    size_t lp = strlen(path), ls = strlen(suffix);
    char *buf = (char *)malloc(lp + ls + 1);
    if (!buf) return NULL;
    memcpy(buf, path, lp);
    memcpy(buf + lp, suffix, ls);
    buf[lp + ls] = '\0';
    return buf;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "用法: %s <file.txt>\n", argv[0]);
        return 2;
    }

    const char *path = argv[1];
    char *tmp_path = cat_suffix(path, ".tmp");
    char *bak_path = cat_suffix(path, ".bak");
    if (!tmp_path || !bak_path) {
        fprintf(stderr, "内存分配失败。\n");
        free(tmp_path);
        free(bak_path);
        return 1;
    }

    /* 以二进制方式打开，避免运行时对换行做隐式转换 */
    FILE *in = fopen(path, "rb");
    if (!in) {
        fprintf(stderr, "无法打开输入文件: %s\n原因: %s\n", path, strerror(errno));
        free(tmp_path);
        free(bak_path);
        return 1;
    }

    /* 若临时文件已存在，先尝试删除 */
    (void)remove(tmp_path);

    FILE *out = fopen(tmp_path, "wb");
    if (!out) {
        fprintf(stderr, "无法创建临时文件: %s\n原因: %s\n", tmp_path, strerror(errno));
        fclose(in);
        free(tmp_path);
        free(bak_path);
        return 1;
    }

    int rc = process_stream(in, out);

    if (fclose(out) != 0) rc = -1;
    if (fclose(in) != 0) rc = -1;

    if (rc != 0) {
        fprintf(stderr, "处理失败：写入临时文件时出错。\n");
        (void)remove(tmp_path);
        free(tmp_path);
        free(bak_path);
        return 1;
    }

    /* 备份原文件 -> .bak（若已存在则覆盖） */
    (void)remove(bak_path);
    if (rename(path, bak_path) != 0) {
        fprintf(stderr, "无法备份原文件到: %s\n原因: %s\n", bak_path, strerror(errno));
        (void)remove(tmp_path);
        free(tmp_path);
        free(bak_path);
        return 1;
    }

    /* 临时文件替换为原文件名 */
    if (rename(tmp_path, path) != 0) {
        fprintf(stderr, "无法用临时文件覆盖原文件: %s\n原因: %s\n", path, strerror(errno));
        /* 尝试恢复 */
        (void)rename(bak_path, path);
        (void)remove(tmp_path);
        free(tmp_path);
        free(bak_path);
        return 1;
    }

    /* 成功后删除备份 */
    (void)remove(bak_path);

    free(tmp_path);
    free(bak_path);
    return 0;
}
