#include <stdio.h>

int main() {
    char str[256];  // 定义一个字符数组来存储输入的字符串

    printf("请输入一句话：");
    // 使用 fgets 读取整行输入（包括空格）
    if (fgets(str, sizeof(str), stdin) != NULL) {
        // 遍历字符串，替换空格为下划线
        for (int i = 0; str[i] != '\0'; i++) {
            if (str[i] == ' ') {
                str[i] = '_';
            }
        }
        printf("替换后的结果：%s", str);
    } else {
        printf("输入读取失败。\n");
    }

    return 0;
}
