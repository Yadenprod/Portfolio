// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"
#include "PlayerBase.h"
#include "Player.h"
#include "Bot.h"
#include "RakNet.h"
#include "Settings.h"
#include "Funcs.h"
#include "Script.h"
#include "Server.h"
#include "MiscFuncs.h"
#include "Timer.h"
#include "Events.h"
#include "ServerInfo.h"

#include "cmds.h"
#include "ini.h"
#include "window.h"
#include "keycheck.h"
#include "netrpc.h"
#include "netgame.h"
#include "resource.h"
#include "mapwnd.h"

#include "main.h"

void LoadAdmins();

LPTOP_LEVEL_EXCEPTION_FILTER OrigExceptionFilter;
void CreateMiniDump(EXCEPTION_POINTERS *ExceptionInfo);
LONG WINAPI unhandledExceptionFilter(EXCEPTION_POINTERS *ExceptionInfo);

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd) {
	char *locale = "RUSSIAN";
	setlocale(LC_COLLATE, locale);
	setlocale(LC_MONETARY, locale);
	setlocale(LC_TIME, locale);
	setlocale(LC_CTYPE, locale);

	// RunCommand("!debug");
	OrigExceptionFilter = SetUnhandledExceptionFilter(unhandledExceptionFilter);

	bool configLoaded = LoadConfig();
	bool customLoaded = LoadCustom();

	if (!configLoaded || !customLoaded)
		return 0;

	g_hInst = hInstance;
	g_hIcon = (HICON)LoadIcon(g_hInst, MAKEINTRESOURCE(IDI_ICON));

	CheckKey();
	if (!vars.keyAccepted)
		return 0;

	RegisterRPCs();

	HANDLE mainWindowThread = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(MainWindow), NULL, NULL, NULL);
	while (!vars.windowOpened || !g_hWndMain)
		SwitchToThread();

	SYSTEMTIME time;
	GetLocalTime(&time);
	RakBot::app()->log("* ===================================================== *");
	RakBot::app()->log("  RakBot " RAKBOT_VERSION " инициализирован");
	RakBot::app()->log("  Автор адаптации: " ADAPT_AUTHOR);
	RakBot::app()->log("  Автор перевода: " TRNSLT_AUTHOR);
	RakBot::app()->log("  Благодарность: " SPECIAL_THANKS);
	RakBot::app()->log("  RakBot.Ru");
	RakBot::app()->log("* ===================================================== *");

	if (vars.luaUpdateDelay < vars.mainDelay) {
		RakBot::app()->log("[WARNING] Задержка обновления скриптов (%d) не может быть меньше основной задержки обновления (%d)!", vars.luaUpdateDelay, vars.mainDelay);
	}

	if (vars.networkUpdateDelay < vars.mainDelay) {
		RakBot::app()->log("[WARNING] Задержка обновления сети (%d) не может быть меньше основной задержки обновления (%d)!", vars.networkUpdateDelay, vars.mainDelay);
	}

	if (vars.routeUpdateDelay < vars.mainDelay) {
		RakBot::app()->log("[WARNING] Задержка воспроизведения маршрута (%d) не может быть меньше основной задержки обновления (%d)!", vars.routeUpdateDelay, vars.mainDelay);
	}

	LoadScripts();

	RakBot::app()->log("[RAKBOT] IP сервера: %s:%d", RakBot::app()->getSettings()->getAddress()->getIp().c_str(), RakBot::app()->getSettings()->getAddress()->getPort());
	RakBot::app()->log("[RAKBOT] Ник игрока: %s", RakBot::app()->getSettings()->getName().c_str());
	RakBot::app()->log("[RAKBOT] Пароль игрока: %s", RakBot::app()->getSettings()->getLoginPassword().c_str());

	srand((unsigned int)GetTickCount());

	HANDLE loadAdminsThread = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(LoadAdmins), NULL, NULL, NULL);
	HANDLE routePlayThread = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(RoutePlay), NULL, NULL, NULL);
	HANDLE updateNetworkThread = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(UpdateNetwork), NULL, NULL, NULL);

	RakBot::app()->getServerInfo()->socketInit();

	while (!RakBot::app()->isBotOff()) {
		Sleep(vars.mainDelay);
		RakBot::app()->getEvents()->onUpdate();
	}

	RakBot::app()->log("[RAKBOT] Завершение работы...");

	UnloadScripts();

	CloseMapWindow();

	RakBot::app()->log("[RAKBOT] Ожидание завершения потока воспроизведения маршрута");
	WaitForSingleObject(routePlayThread, INFINITE);

	RakBot::app()->log("[RAKBOT] Ожидание завершения потока загрузки админов");
	WaitForSingleObject(loadAdminsThread, INFINITE);

	RakBot::app()->log("[RAKBOT] Ожидание завершения потока обновления сети");
	WaitForSingleObject(updateNetworkThread, INFINITE);

	RakBot::app()->log("[RAKBOT] Ожидание завершения потока главного окна");
	WaitForSingleObject(mainWindowThread, INFINITE);

	RakBot::app()->log("[RAKBOT] Ожидание завершения потока окна карты");
	WaitForSingleObject(vars.mapWindowThread, INFINITE);

	RakBot::app()->log("[RAKBOT] Ожидание завершения потока окна диалога");
	WaitForSingleObject(vars.dialogWindowThread, INFINITE);

	RakBot::app()->log("[RAKBOT] Работа завершена");

	if (vars.logFile != nullptr)
		fclose(vars.logFile);

	return 0;
}

void LoadAdmins() {
	CreateDirectory(GetRakBotPath("admins").c_str(), NULL);

	vars.adminsMutex.lock();
	vars.admins.clear();
	vars.adminsMutex.unlock();

	Settings *settings = RakBot::app()->getSettings();

	std::stringstream serverAdminsFileName;
	serverAdminsFileName << settings->getAddress()->getIp() << ";" << settings->getAddress()->getPort() << ".txt";

	std::string serverAdminsFilePath = GetRakBotPath("admins\\" + serverAdminsFileName.str());

	if (!IsFileExists(serverAdminsFilePath))
		serverAdminsFilePath = GetRakBotPath("admins\\all.txt");

	std::ifstream adminsFile(serverAdminsFilePath);

	if (adminsFile.is_open()) {
		RakBot::app()->log(("[RAKBOT] Загрузка админов из файла " + serverAdminsFilePath + "...").c_str());
		while (!adminsFile.eof()) {
			std::string admin;
			adminsFile >> admin;
			Trim(admin);

			if (!admin.empty()) {
				vars.adminsMutex.lock();
				vars.admins.push_back(admin);
				vars.adminsMutex.unlock();
			}
		}
		adminsFile.close();

		vars.adminsMutex.lock();
		size_t adminsCount = vars.admins.size();
		vars.adminsMutex.unlock();

		RakBot::app()->log("[RAKBOT] Загружено %d админов из файла", adminsCount);
	} else {
		RakBot::app()->log("[RAKBOT] Загрузка админов с сервера...");

		CURLcode curlCode = OpenURL(vars.adminsUrl);
		if (curlCode == CURLE_OK) {
			char *pch = strtok(CurlBuffer, ":");
			while (pch != nullptr) {
				std::string admin(pch);
				Trim(admin);

				if (!admin.empty()) {
					vars.adminsMutex.lock();
					vars.admins.push_back(admin);
					vars.adminsMutex.unlock();
				}
				pch = strtok(NULL, ":");
			}

			vars.adminsMutex.lock();
			size_t adminsCount = vars.admins.size();
			vars.adminsMutex.unlock();

			RakBot::app()->log("[RAKBOT] Загружено %d админов с сервера", adminsCount);
		} else {
			RakBot::app()->log("[RAKBOT] Ошибка #%d при загрузке админов с сервера", curlCode);
		}
	}
	RakBot::app()->log("[RAKBOT] Загрузка админов завершена");
}

void CreateMiniDump(EXCEPTION_POINTERS *ExceptionInfo) {
	char *dumpFileName = new char[MAX_PATH];
	_snprintf_s(dumpFileName, MAX_PATH, MAX_PATH, "\\excepts\\%08x.dmp", (uint32_t)ExceptionInfo->ExceptionRecord->ExceptionAddress);

	char *dumpFilePath = new char[MAX_PATH];
	GetModuleFileName(NULL, dumpFilePath, MAX_PATH);
	*strrchr(dumpFilePath, '\\') = 0;
	strcat_s(dumpFilePath, MAX_PATH, dumpFileName);

	HANDLE dumpFile = CreateFile(dumpFilePath, GENERIC_READ | GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

	delete[] dumpFileName;
	delete[] dumpFilePath;

	if (dumpFile == NULL)
		return;

	MINIDUMP_EXCEPTION_INFORMATION *mdei = new MINIDUMP_EXCEPTION_INFORMATION;

	mdei->ThreadId = GetCurrentThreadId();
	mdei->ExceptionPointers = ExceptionInfo;
	mdei->ClientPointers = TRUE;

	MINIDUMP_TYPE mdt = MiniDumpNormal;

	MiniDumpWriteDump(GetCurrentProcess(), GetCurrentProcessId(), dumpFile, MiniDumpNormal, (ExceptionInfo != 0) ? mdei : 0, 0, 0);
	CloseHandle(dumpFile);
	delete mdei;
}

LONG WINAPI unhandledExceptionFilter(EXCEPTION_POINTERS *ExceptionInfo) {
	RakBot::app()->getEvents()->onCrash();

	CreateDirectory(GetRakBotPath("excepts").c_str(), NULL);

	CreateMiniDump(ExceptionInfo);

	char *exceptionLogFileName = new char[MAX_PATH];
	_snprintf_s(exceptionLogFileName, MAX_PATH, MAX_PATH, "\\excepts\\%08x.log", (uint32_t)ExceptionInfo->ExceptionRecord->ExceptionAddress);

	char *exceptionLogFilePath = new char[MAX_PATH];
	GetModuleFileName(NULL, exceptionLogFilePath, MAX_PATH);
	*strrchr(exceptionLogFilePath, '\\') = 0;
	strcat_s(exceptionLogFilePath, MAX_PATH, exceptionLogFileName);

	FILE *exceptionLogFile = fopen(exceptionLogFilePath, "w");

	delete[] exceptionLogFileName;
	delete[] exceptionLogFilePath;

	if (exceptionLogFile == NULL) {
		if (OrigExceptionFilter)
			return OrigExceptionFilter(ExceptionInfo);

		return EXCEPTION_CONTINUE_SEARCH;
	}

	MODULEINFO *moduleinfo = new MODULEINFO;
	GetModuleInformation(GetCurrentProcess(), GetModuleHandle(NULL), moduleinfo, sizeof(MODULEINFO));

	SYSTEMTIME *time = new SYSTEMTIME;
	GetLocalTime(time);
	fprintf_s(exceptionLogFile, "Время: %02d:%02d:%02d\n", time->wHour, time->wMinute, time->wSecond);
	fprintf_s(exceptionLogFile, "Дата: %02d/%02d/%04d\n", time->wDay, time->wMonth, time->wYear);
	fprintf_s(exceptionLogFile, "Версия RakBot: %s\n", RAKBOT_VERSION);
	fprintf_s(exceptionLogFile, "Исключение по адресу: 0x%p\n", ExceptionInfo->ExceptionRecord->ExceptionAddress);
	fprintf_s(exceptionLogFile, "Базовый адрес: 0x%08X-0x%08X\n", (DWORD)moduleinfo->lpBaseOfDll, (DWORD)moduleinfo->lpBaseOfDll + moduleinfo->SizeOfImage);

	delete time;
	delete moduleinfo;

	int m_ExceptionCode = ExceptionInfo->ExceptionRecord->ExceptionCode;
	int m_exceptionInfo_0 = ExceptionInfo->ExceptionRecord->ExceptionInformation[0];
	int m_exceptionInfo_1 = ExceptionInfo->ExceptionRecord->ExceptionInformation[1];
	int m_exceptionInfo_2 = ExceptionInfo->ExceptionRecord->ExceptionInformation[2];

	switch (m_ExceptionCode) {
		case EXCEPTION_ACCESS_VIOLATION:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_ACCESS_VIOLATION\n");
			if (m_exceptionInfo_0 == 0) {
				fprintf_s(exceptionLogFile, "Ошибка чтения по адресу: 0x%08X\n", m_exceptionInfo_1);
			} else if (m_exceptionInfo_0 == 1) {
				fprintf_s(exceptionLogFile, "Ошибка записи по адресу: 0x%08X\n", m_exceptionInfo_1);
			} else if (m_exceptionInfo_0 == 8) {
				fprintf_s(exceptionLogFile, "Предотвращение выполнение данных по адресу: 0x%08X", m_exceptionInfo_1);
			} else {
				fprintf_s(exceptionLogFile, "Неизвестная ошибка доступа: 0x%08X\n", m_exceptionInfo_1);
			}
			break;

		case EXCEPTION_ARRAY_BOUNDS_EXCEEDED:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_ARRAY_BOUNDS_EXCEEDED\n");
			break;

		case EXCEPTION_BREAKPOINT:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_BREAKPOINT\n");
			break;

		case EXCEPTION_DATATYPE_MISALIGNMENT:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_DATATYPE_MISALIGNMENT\n");
			break;

		case EXCEPTION_FLT_DENORMAL_OPERAND:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_DENORMAL_OPERAND\n");
			break;

		case EXCEPTION_FLT_DIVIDE_BY_ZERO:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_DIVIDE_BY_ZERO\n");
			break;

		case EXCEPTION_FLT_INEXACT_RESULT:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_INEXACT_RESULT\n");
			break;

		case EXCEPTION_FLT_INVALID_OPERATION:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_INVALID_OPERATION\n");
			break;

		case EXCEPTION_FLT_OVERFLOW:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_OVERFLOW\n");
			break;

		case EXCEPTION_FLT_STACK_CHECK:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_STACK_CHECK\n");
			break;

		case EXCEPTION_FLT_UNDERFLOW:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_FLT_UNDERFLOW\n");
			break;

		case EXCEPTION_ILLEGAL_INSTRUCTION:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_ILLEGAL_INSTRUCTION\n");
			break;

		case EXCEPTION_IN_PAGE_ERROR:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_IN_PAGE_ERROR\n");
			if (m_exceptionInfo_0 == 0) {
				fprintf_s(exceptionLogFile, "Ошибка чтения по адресу: 0x%08X\n", m_exceptionInfo_1);
			} else if (m_exceptionInfo_0 == 1) {
				fprintf_s(exceptionLogFile, "Ошибка записи по адресу: 0x%08X\n", m_exceptionInfo_1);
			} else if (m_exceptionInfo_0 == 8) {
				fprintf_s(exceptionLogFile, "Предотвращение выполнения данных по адресу: 0x%08X\n", m_exceptionInfo_1);
			} else {
				fprintf_s(exceptionLogFile, "Неизвестая ошибка досупа по адресу: 0x%08X\n", m_exceptionInfo_1);
			}

			fprintf_s(exceptionLogFile, "Статус ядра: 0x%08X\n", m_exceptionInfo_2);
			break;

		case EXCEPTION_INT_DIVIDE_BY_ZERO:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_INT_DIVIDE_BY_ZERO\n");
			break;

		case EXCEPTION_INT_OVERFLOW:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_INT_OVERFLOW\n");
			break;

		case EXCEPTION_INVALID_DISPOSITION:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_INVALID_DISPOSITION\n");
			break;

		case EXCEPTION_NONCONTINUABLE_EXCEPTION:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_NONCONTINUABLE_EXCEPTION\n");
			break;

		case EXCEPTION_PRIV_INSTRUCTION:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_PRIV_INSTRUCTION\n");
			break;

		case EXCEPTION_SINGLE_STEP:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_SINGLE_STEP\n");
			break;

		case EXCEPTION_STACK_OVERFLOW:
			fprintf_s(exceptionLogFile, "Причина: EXCEPTION_STACK_OVERFLOW\n");
			break;

		case DBG_CONTROL_C:
			fprintf_s(exceptionLogFile, "Причина: DBG_CONTROL_C (WTF!)\n");
			break;

		default:
			fprintf_s(exceptionLogFile, "Причина: %08x\n", m_ExceptionCode);
	}

	fprintf_s(exceptionLogFile, "EAX: 0x%08X || ESI: 0x%08X\n", ExceptionInfo->ContextRecord->Eax, ExceptionInfo->ContextRecord->Esi);
	fprintf_s(exceptionLogFile, "EBX: 0x%08X || EDI: 0x%08X\n", ExceptionInfo->ContextRecord->Ebx, ExceptionInfo->ContextRecord->Edi);
	fprintf_s(exceptionLogFile, "ECX: 0x%08X || EBP: 0x%08X\n", ExceptionInfo->ContextRecord->Ecx, ExceptionInfo->ContextRecord->Ebp);
	fprintf_s(exceptionLogFile, "EDX: 0x%08X || ESP: 0x%08X\n", ExceptionInfo->ContextRecord->Edx, ExceptionInfo->ContextRecord->Esp);

	for (int i = 0; i < 320; i += 16)
		fprintf_s(exceptionLogFile, "ESP+%04X: 0x%08X 0x%08X 0x%08X 0x%08X\n",
			i, *(DWORD *)(ExceptionInfo->ContextRecord->Esp + (i + 0)), *(DWORD *)(ExceptionInfo->ContextRecord->Esp + (i + 4)),
			*(DWORD *)(ExceptionInfo->ContextRecord->Esp + (i + 8)), *(DWORD *)(ExceptionInfo->ContextRecord->Esp + (i + 12)));

	fclose(exceptionLogFile);

	if (OrigExceptionFilter)
		return OrigExceptionFilter(ExceptionInfo);

	return EXCEPTION_CONTINUE_SEARCH;
}