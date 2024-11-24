// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include <Windows.h>
#include <iostream>
#include "logger.h"

void CreateConsole()
{
    // 分配新的控制台
    if (AllocConsole())
    {
        FILE* fp;
        freopen_s(&fp, "CONOUT$", "w", stdout);
        setlocale(LC_CTYPE, "zh-ch");
        // 设置控制台代码页为UTF-8
        //_setmode(_fileno(stdout), _O_U16TEXT);
        SetConsoleOutputCP(932);
    }
}

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        //CreateConsole();
		LoggerHook();
        break;
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

