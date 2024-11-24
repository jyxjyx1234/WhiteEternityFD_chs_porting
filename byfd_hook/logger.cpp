#include <Windows.h>
#include <iostream>
#include "logger.h"
#include "detours.h"
#include <fstream>
#pragma comment(lib, "detours.lib")


DWORD OriginalAddress = 0x00444B29;
DWORD returnAddress = 0x00444B2f;

auto printMemoryContent = [](DWORD address) {
    if (IsBadReadPtr((void*)address, 1)) {
        std::cout << "Content: Invalid address" << std::endl;
    }
    else {
        char content[256];
        strncpy_s(content, (char*)address, sizeof(content) - 1);
        content[sizeof(content) - 1] = '\0';
        std::cout << "Content: " << content << std::endl;
    }
    };

void PrintRegisters(DWORD eax, DWORD ecx, DWORD edx, DWORD ebx, DWORD esi, DWORD edi, DWORD ebp, DWORD esp) {
    std::cout << "EAX: " << std::hex << eax << std::endl;
    std::cout << "ECX: " << std::hex << ecx << std::endl;
    std::cout << "EDX: " << std::hex << edx << std::endl;
    std::cout << "EBX: " << std::hex << ebx << std::endl;
    std::cout << "ESI: " << std::hex << esi << std::endl;
    std::cout << "EDI: " << std::hex << edi << std::endl;
    std::cout << "EBP: " << std::hex << ebp << std::endl;
    std::cout << "ESP: " << std::hex << esp << std::endl;

    std::cout << "EAX Content: "; printMemoryContent(eax);
    std::cout << "ECX Content: "; printMemoryContent(ecx);
    std::cout << "EDX Content: "; printMemoryContent(edx);
    std::cout << "EBX Content: "; printMemoryContent(ebx);
    std::cout << "ESI Content: "; printMemoryContent(esi);
    std::cout << "EDI Content: "; printMemoryContent(edi);
    std::cout << "EBP Content: "; printMemoryContent(ebp);
    std::cout << "ESP Content: "; printMemoryContent(esp);
}

void WriteToFile(const char* text)
{
    if (text == nullptr) return;
    std::ofstream file("output.txt", std::ios::app);
    if (file.is_open())
    {
        file << text << std::endl;
        file.close();
    }
}

void __declspec(naked) HookFunction() {
    __asm {
        // Save registers
        sub esp, 4
        pushad
        pushfd

        mov eax, [esp + 0x24]
        push eax
        call WriteToFile
		add esp, 4

        // Restore registers
        popfd
        popad
        add esp, 4
        mov dword ptr [edi + 4], ebp
        mov byte ptr[edi], 5
        // Jump back to original code
        jmp dword ptr[returnAddress]
    }
}

void LoggerHook() {
    DWORD oldProtect;
    VirtualProtect((LPVOID)OriginalAddress, 5, PAGE_EXECUTE_READWRITE, &oldProtect);
    *(BYTE*)OriginalAddress = 0xE9;
    *(DWORD*)(OriginalAddress + 1) = (DWORD)HookFunction - OriginalAddress - 5;
    VirtualProtect((LPVOID)OriginalAddress, 5, oldProtect, &oldProtect);
}
