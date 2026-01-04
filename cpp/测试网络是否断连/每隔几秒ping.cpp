#include <iostream>
#include <string>
#include <cstdlib>   // 用于 system()
#include <thread>    // 用于 std::this_thread::sleep_for
#include <chrono>    // 用于 std::chrono::seconds
#include <ctime>     // 用于获取和格式化时间

// 函数：获取当前时间的字符串格式
std::string getCurrentTimestamp() {
    time_t now = time(0);
    tm ltm;
#ifdef _WIN32
    localtime_s(&ltm, &now); // Windows下的安全版本
#else
    localtime_r(&now, &ltm); // Linux/macOS下的线程安全版本
#endif
    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &ltm);
    return std::string(buffer);
}

int main() {
    // ---------- 配置区 ----------
    // 要 ping 的目标地址。使用IP地址可以避免DNS解析失败带来的误判。
    // 8.8.8.8 是 Google 的公共 DNS 服务器，非常稳定。
    std::string targetHost = "8.8.8.8";

    // 检测间隔时间（秒）
    int pingIntervalSeconds = 5;
    // --------------------------

    std::cout << "网络连接检测已启动..." << std::endl;
    std::cout << "检测目标: " << targetHost << std::endl;
    std::cout << "检测间隔: " << pingIntervalSeconds << " 秒" << std::endl;
    std::cout << "------------------------------------" << std::endl;

    while (true) {
        std::string command;

        // 根据操作系统平台构建不同的 ping 命令
#ifdef _WIN32
        // Windows 系统:
        // -n 1: 只发送1个数据包
        // -w 1000: 等待响应的超时时间为 1000 毫秒 (1秒)
        // > nul: 将命令的输出重定向到空设备，不显示在屏幕上
        command = "ping -n 1 -w 1000 " + targetHost + " > nul";
#else
        // Linux 或 macOS 系统:
        // -c 1: 只发送1个数据包
        // -W 1: 等待响应的超时时间为 1 秒
        // > /dev/null: 将命令的输出重定向到空设备
        command = "ping -c 1 -W 1 " + targetHost + " > /dev/null";
#endif

        // 执行命令并获取返回值
        int exitCode = system(command.c_str());

        // 获取当前时间戳
        std::string timestamp = getCurrentTimestamp();

        // 检查返回值
        if (exitCode == 0) {
            std::cout << "[" << timestamp << "] 网络连接正常 (Connected)" << std::endl;
        } else {
            std::cout << "[" << timestamp << "] >> 网络连接断开或目标不可达 (Disconnected!) <<" << std::endl;
        }
        
        // 程序休眠，等待下一个检测周期
        std::this_thread::sleep_for(std::chrono::seconds(pingIntervalSeconds));
    }

    return 0;
}