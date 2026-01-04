#include <iostream>
#include <string>
#include <algorithm> // 用于 std::reverse
#include <cctype>    // 用于 toupper
#include <limits>    // 用于 std::numeric_limits，健壮地清空输入缓冲

// 只在 Windows 系统下需要包含此头文件以解决乱码问题
#ifdef _WIN32
#include <windows.h>
#endif

// 函数：将单个字符转换为其对应的数值
int charToValue(char c) {
    c = toupper(c);
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'A' && c <= 'Z') {
        return c - 'A' + 10;
    }
    return -1;
}

// 函数：将数值转换为对应的字符
char valueToChar(int v) {
    if (v >= 0 && v <= 9) {
        return v + '0';
    } else if (v >= 10 && v <= 35) {
        return v - 10 + 'A';
    }
    return '\0';
}

// 核心功能1：将任意进制的字符串转换为十进制整数
long long anyBaseToDecimal(const std::string& numStr, int sourceBase) {
    long long decimalValue = 0;
    long long power = 1;
    for (int i = numStr.length() - 1; i >= 0; i--) {
        int digitValue = charToValue(numStr[i]);
        if (digitValue < 0 || digitValue >= sourceBase) {
            std::cerr << "错误: 输入的数字 '" << numStr[i] << "' 对于 " << sourceBase << " 进制是无效的。" << std::endl;
            return -1;
        }
        decimalValue += digitValue * power;
        power *= sourceBase;
    }
    return decimalValue;
}

// 核心功能2：将十进制整数转换为任意进制的字符串
std::string decimalToAnyBase(long long decimalValue, int targetBase) {
    if (decimalValue == 0) return "0";
    std::string result = "";
    while (decimalValue > 0) {
        result += valueToChar(decimalValue % targetBase);
        decimalValue /= targetBase;
    }
    std::reverse(result.begin(), result.end());
    return result;
}

// 函数：从用户处获取一个合法的进制输入
int getValidBaseInput(const std::string& prompt) {
    int base;
    while (true) {
        std::cout << prompt;
        std::cin >> base;

        if (std::cin.good() && base >= 2 && base <= 36) {
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            return base;
        } else {
            std::cerr << "错误: 进制必须是一个介于 2 和 36 之间的整数。请重试。" << std::endl;
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
    }
}

int main() {
    // 解决 Windows 控制台中文乱码问题
    #ifdef _WIN32
        SetConsoleOutputCP(65001);
        SetConsoleCP(65001);
    #endif

    int sourceBase = 0; // 0 表示源进制未设置
    int targetBase = 0; // 0 表示目标进制未设置
    std::string numStr;

    std::cout << "--- 通用进制转换工具 ---" << std::endl;
    std::cout << "特殊指令:" << std::endl;
    std::cout << "  输入 '00' 退出程序。" << std::endl;
    std::cout << "  输入 '000' 重置当前和目标进制。" << std::endl;

    while (true) {
        // --- 步骤 1: 设置或确认源进制和目标进制 ---
        if (sourceBase == 0) { // 只要源进制未设置，就进入设置模式
            std::cout << "\n----------------------------------------" << std::endl;
            std::cout << "请设置转换模式。" << std::endl;
            sourceBase = getValidBaseInput("请输入要固定的【当前进制】 (2-36): ");
            targetBase = getValidBaseInput("请输入要固定的【目标进制】 (2-36): ");
            std::cout << "转换模式已固定: 从 " << sourceBase << " 进制 转换到 " << targetBase << " 进制。" << std::endl;
        }

        // --- 步骤 2: 获取要转换的数字 (并检查特殊指令) ---
        std::cout << "\n请输入一个 " << sourceBase << " 进制的数 (或输入 '00' 退出, '000' 重置): ";
        std::cin >> numStr;

        // 清理输入缓冲区
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        // 检查特殊指令
        if (numStr == "00") {
            break; // 退出主循环
        }
        if (numStr == "000") {
            sourceBase = 0; // 重置源进制
            targetBase = 0; // 重置目标进制
            std::cout << "当前和目标进制已解锁，下次将要求您重新设置。" << std::endl;
            continue; // 进入下一次循环
        }
        
        // --- 步骤 3: 执行转换 ---
        long long decimalResult = anyBaseToDecimal(numStr, sourceBase);

        if (decimalResult == -1) {
            std::cout << "请重试。" << std::endl;
            continue;
        }
        
        std::string finalResult = decimalToAnyBase(decimalResult, targetBase);

        // --- 步骤 4: 打印结果 ---
        std::cout << "\n>> 转换结果:" << std::endl;
        std::cout << "   " << numStr << " ( " << sourceBase << " 进制) => " << finalResult << " ( " << targetBase << " 进制)" << std::endl;
        std::cout << "----------------------------------------" << std::endl;
    }

    std::cout << "\n程序已退出。再见！" << std::endl;
    return 0;
}