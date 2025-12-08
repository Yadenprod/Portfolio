// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#if defined(_COMPATIBILITY_1)
#include "Compatibility1Includes.h"
#elif defined(_WIN32)
#include <windows.h> // Sleep
#elif defined(_COMPATIBILITY_2)
#include "Compatibility2Includes.h"
#else
#include <unistd.h> // usleep
#endif

void RakSleep(unsigned int ms) {
#ifdef _WIN32
	Sleep(ms);
#else
	usleep(ms * 1000);
#endif
}
