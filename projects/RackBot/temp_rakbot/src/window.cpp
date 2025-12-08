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
#include "Server.h"
#include "MiscFuncs.h"

#include "window.h"
#include "cmds.h"

// Code taken from http://www.rohitab.com/discuss/topic/37441-how-to-change-color-of-selected-text-in-listbox/page__view__findpost__p__10081946

// Child Window/Control IDs
#define IDC_LBLINFO             100
#define IDC_LSTCUSTOM           101
#define IDC_INPUTBOX			102
#define IDC_SENDBTN				103
#define IDC_AAFKBTN				105
#define IDC_NOAFKBTN			106
#define IDC_SPAWNBTN			107
#define IDC_TPBTN				108
#define IDC_COORDMASTERBTN		109
#define IDC_PARSEBTN			113
#define IDC_GOTOBTN				114
#define IDC_SPICBTN				115
#define IDC_FOLLOWBTN			116
#define IDC_STICKBTN			117
#define IDC_VWORLDBTN			118
#define IDC_WORKERBTN			119
#define IDC_SCOORDBTN			120
#define IDC_SKIPDIALOGBTN		125
#define IDC_CPMBTN				126
#define IDC_ANTIDEATHBTN		127
#define IDC_FARMBOTBTN			129
#define IDC_WRITESTATBTN		130
#define IDC_MAPBTN				131
#define IDC_FARCHATBTN			132
#define IDC_FLOODBTN			133
#define IDC_IGNOREMSGSBTN		134
#define IDC_AUTOLICBTN			136
#define IDC_AUTOQUEST			137
#define IDC_CHANGELAYOUT_BTN	138
#define IDC_SITE				228

#define IDC_ADMONLINE_IGNORE	1001
#define IDC_ADMONLINE_RELOG		1002
#define IDC_ADMONLINE_EXIT		1003

#define IDC_ADMNEAR_IGNORE		2001
#define IDC_ADMNEAR_RELOG		2002
#define IDC_ADMNEAR_EXIT		2003

enum BotMenu {
	MENU_EXIT = 10001,
	MENU_INFO,
	MENU_SITE,
	MENU_TRAY,
	MENU_DEBUG,
	MENU_LUA_SCRIPTSDIR,
	MENU_LUA_SCRIPTSRELOAD,
	MENU_OPENLOG,
	BotMenuItemsCount
};

#define IDH_CHANGELAYOUT		1001

#define WM_FLIPPED_TO_TRAY		(WM_APP + 1234)
#define ID_FLIPPED_TO_TRAY		1234

// Globals
HICON g_hIcon = NULL;

HWND g_hWndMain = NULL;
HWND g_hWndTitle = NULL;
HWND g_hWndLog = NULL;
HWND g_hWndInput = NULL;
HWND g_hWndAdmins = NULL, g_hWndAdminsTitle = NULL;
HWND g_hWndCoordX = NULL, g_hWndCoordY = NULL, g_hWndCoordZ = NULL;
HWND g_hWndPickupID = NULL;
HWND g_hWndPlayerID = NULL;

HINSTANCE g_hInst;
HFONT g_hfText, g_hfListBoxText;
NOTIFYICONDATA notifyIconData;
char szHint[64];

std::vector<std::string> commandHistory;
int currentCommand = 0;

void CommandHistoryPrev() {
	if (currentCommand > 0)
		currentCommand--;

	SendMessage(g_hWndInput, WM_SETTEXT, 0, (LPARAM)commandHistory[currentCommand].c_str());
	SetFocus(g_hWndInput);
}

void CommandHistoryNext() {
	if (currentCommand < (static_cast<int>(commandHistory.size()) - 1))
		currentCommand++;

	SendMessage(g_hWndInput, WM_SETTEXT, 0, (LPARAM)commandHistory[currentCommand].c_str());
	SetFocus(g_hWndInput);
}

void SendCommand() {
	int length = GetWindowTextLength(g_hWndInput);

	if (length < 1 || length > 128)
		return;

	char *text = new char[length + 1];
	SendMessage(g_hWndInput, WM_GETTEXT, (WPARAM)length + 1, (LPARAM)text);
	RunCommand(text);
	commandHistory[(commandHistory.size() - 1)] = text;
	commandHistory.push_back("");
	currentCommand = (commandHistory.size() - 1);
	delete[] text;

	SendMessage(g_hWndInput, WM_SETTEXT, 0, NULL);
	SetFocus(g_hWndInput);
}

void GetCoords(float *fCoords) {
	char szBuf[512];
	SendMessage(g_hWndCoordX, WM_GETTEXT, (WPARAM)sizeof(szBuf), (LPARAM)szBuf);
	fCoords[0] = (float)atof(szBuf);

	SendMessage(g_hWndCoordY, WM_GETTEXT, (WPARAM)sizeof(szBuf), (LPARAM)szBuf);
	fCoords[1] = (float)atof(szBuf);

	SendMessage(g_hWndCoordZ, WM_GETTEXT, (WPARAM)sizeof(szBuf), (LPARAM)szBuf);
	fCoords[2] = (float)atof(szBuf);
}

BOOL FlipToTray(HWND hWnd, HICON hIcon, BOOL bMinimize) {
	notifyIconData.cbSize = sizeof(NOTIFYICONDATA);
	notifyIconData.hWnd = hWnd;
	notifyIconData.uID = ID_FLIPPED_TO_TRAY;
	notifyIconData.uCallbackMessage = WM_FLIPPED_TO_TRAY;
	notifyIconData.uTimeout = 3000;

	sprintf(szHint, "%s\n%s",
		!RakBot::app()->getServer()->getServerName().empty() ? RakBot::app()->getServer()->getServerName().c_str() : "Инициализация...",
		RakBot::app()->getSettings()->getName().c_str());
	notifyIconData.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
	notifyIconData.hIcon = hIcon;
	lstrcpyn(notifyIconData.szTip, szHint, sizeof(notifyIconData.szTip));
	Shell_NotifyIcon(NIM_ADD, &notifyIconData);
	ShowWindow(g_hWndMain, SW_HIDE);
	return 1;
}

BOOL UnflipFromTray(HWND hWnd) {
	memset(&notifyIconData, 0, sizeof(NOTIFYICONDATA));
	notifyIconData.cbSize = sizeof(NOTIFYICONDATA);
	notifyIconData.hWnd = hWnd;
	notifyIconData.uID = ID_FLIPPED_TO_TRAY;

	Shell_NotifyIcon(NIM_DELETE, &notifyIconData);

	ShowWindow(hWnd, SW_RESTORE);
	SetForegroundWindow(hWnd);
	UpdateWindow(hWnd);
	return 1;
}

LRESULT CALLBACK MainWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
	switch (uMsg) {
		case WM_FLIPPED_TO_TRAY:
		{
			if (wParam == ID_FLIPPED_TO_TRAY && lParam == WM_LBUTTONDOWN) {
				UnflipFromTray(g_hWndMain);
				Sleep(500);
			}
			if (wParam == ID_FLIPPED_TO_TRAY && lParam == WM_MOUSEMOVE) {
				sprintf(szHint, "%s\n%s",
					!RakBot::app()->getServer()->getServerName().empty() ? RakBot::app()->getServer()->getServerName().c_str() : "Инициализация...",
					RakBot::app()->getSettings()->getName().c_str());
				strncpy(notifyIconData.szTip, szHint, sizeof(notifyIconData.szTip));
				Shell_NotifyIcon(NIM_MODIFY, &notifyIconData);
			}
			break;
		}

		case WM_DELETEITEM:
		{
			if (wParam == IDC_LSTCUSTOM) {
				LPDELETEITEMSTRUCT deleteItem = reinterpret_cast<LPDELETEITEMSTRUCT>(lParam);
				char *buf = reinterpret_cast<char *>(deleteItem->itemData);
				delete[] buf;
			}
			break;
		}

		case WM_CREATE:
		{
			HWND hWndTemp;

			SendMessage(g_hWndMain, WM_SETICON, ICON_BIG, (LPARAM)g_hIcon);
			SendMessage(g_hWndMain, WM_SETICON, ICON_SMALL, (LPARAM)g_hIcon);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTON, "Админы онлайн",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				573, 208, 205, 185, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);
			g_hWndAdminsTitle = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_STATIC, "Загрузка игроков...",
				WS_CHILD | WS_VISIBLE,
				583, 228, 185, 155, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfListBoxText, FALSE);
			g_hWndAdmins = hWndTemp;

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTON, "Информация",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				573, 2, 205, 205, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_STATIC, "RakBot " RAKBOT_VERSION "\nАвтор: MishaN",
				WS_CHILD | WS_VISIBLE,
				583, 20, 185, 180, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfListBoxText, FALSE);
			g_hWndTitle = hWndTemp;

			hWndTemp = CreateWindowEx(WS_EX_CLIENTEDGE, WC_LISTBOX, "",
				LBS_NOINTEGRALHEIGHT | LBS_OWNERDRAWFIXED |
				WS_VSCROLL | WS_HSCROLL | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				5, 10, 560, 310, hWnd, (HMENU)(IDC_LSTCUSTOM), g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfListBoxText, FALSE);
			SendMessage(hWndTemp, LB_SETITEMHEIGHT, NULL, 15);
			SendMessage(hWndTemp, LB_SETHORIZONTALEXTENT, (WPARAM)1600, FALSE);
			g_hWndLog = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_EDIT, NULL,
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL,
				5, 325, 430, 20, hWnd, (HMENU)IDC_INPUTBOX, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfListBoxText, FALSE);
			commandHistory.push_back("");
			currentCommand = 0;
			g_hWndInput = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "L",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				440, 324, 22, 22, hWnd, (HMENU)IDC_CHANGELAYOUT_BTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Отправить",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				464, 324, 102, 22, hWnd, (HMENU)IDC_SENDBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTONA, "Телепорт",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				5, 350, 196, 96, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_EDIT, "0,00",
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER | SS_CENTER | ES_AUTOHSCROLL,
				15, 370, 55, 20, hWnd, (HMENU)IDC_INPUTBOX, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);
			g_hWndCoordX = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_EDIT, "0,00",
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER | SS_CENTER | ES_AUTOHSCROLL,
				75, 370, 55, 20, hWnd, (HMENU)IDC_INPUTBOX, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);
			g_hWndCoordY = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_EDIT, "0,00",
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER | SS_CENTER | ES_AUTOHSCROLL,
				135, 370, 55, 20, hWnd, (HMENU)IDC_INPUTBOX, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);
			g_hWndCoordZ = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Телепорт",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				14, 394, 72, 22, hWnd, (HMENU)IDC_TPBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "КоордМастер",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				89, 394, 102, 22, hWnd, (HMENU)IDC_COORDMASTERBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Сохранить координаты",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE | BS_AUTOCHECKBOX,
				24, 419, 170, 20, hWnd, (HMENU)IDC_SCOORDBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTONA, "Админ в сети",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				206, 350, 105, 96, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTONA, "Игнор",
				WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON,
				216, 369, 60, 22, hWnd, (HMENU)IDC_ADMONLINE_IGNORE, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTONA, "Релог",
				WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON,
				216, 394, 60, 22, hWnd, (HMENU)IDC_ADMONLINE_RELOG, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTONA, "Выход",
				WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON,
				216, 419, 60, 22, hWnd, (HMENU)IDC_ADMONLINE_EXIT, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			CheckRadioButton(hWnd, IDC_ADMONLINE_IGNORE, IDC_ADMONLINE_EXIT, IDC_ADMONLINE_IGNORE + vars.adminOnlineAction);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTONA, "Админ рядом",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				316, 350, 104, 96, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTONA, "Игнор",
				WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON,
				326, 369, 60, 22, hWnd, (HMENU)IDC_ADMNEAR_IGNORE, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTONA, "Релог",
				WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON,
				326, 394, 60, 22, hWnd, (HMENU)IDC_ADMNEAR_RELOG, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTONA, "Выход",
				WS_CHILD | WS_VISIBLE | BS_RADIOBUTTON,
				326, 419, 60, 22, hWnd, (HMENU)IDC_ADMNEAR_EXIT, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			CheckRadioButton(hWnd, IDC_ADMNEAR_IGNORE, IDC_ADMNEAR_EXIT, IDC_ADMNEAR_IGNORE + vars.adminNearAction);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTONA, "Отправка пикапа",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				5, 446, 120, 50, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_EDIT, "ID",
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER | SS_CENTER | ES_AUTOHSCROLL,
				15, 466, 45, 20, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);
			g_hWndPickupID = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_BUTTON, ">>>",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				64, 465, 52, 22, hWnd, (HMENU)IDC_SPICBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTON, "Игрок",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				130, 446, 290, 50, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_EDIT, "ID",
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER | SS_CENTER,
				140, 466, 40, 20, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);
			g_hWndPlayerID = hWndTemp;

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Cледить",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				184, 465, 62, 22, hWnd, (HMENU)IDC_FOLLOWBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Прицепиться",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				249, 465, 87, 22, hWnd, (HMENU)IDC_STICKBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Телепорт",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				339, 465, 72, 22, hWnd, (HMENU)IDC_GOTOBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTON, "Боты",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				425, 350, 140, 96, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Грузчик",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				434, 369, 60, 22, hWnd, (HMENU)IDC_WORKERBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Фермер",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				497, 369, 60, 22, hWnd, (HMENU)IDC_FARMBOTBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Автобус",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				434, 394, 60, 22, hWnd, (HMENU)IDC_CPMBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Квест",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				497, 394, 60, 22, hWnd, (HMENU)IDC_AUTOQUEST, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Автошкола",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				434, 419, 123, 22, hWnd, (HMENU)IDC_AUTOLICBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTON, "Пропуск",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				425, 446, 140, 50, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Диалоги",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				434, 465, 70, 22, hWnd, (HMENU)IDC_SKIPDIALOGBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Чат",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE | BS_AUTOCHECKBOX,
				513, 465, 40, 22, hWnd, (HMENU)IDC_IGNOREMSGSBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(WS_EX_TRANSPARENT, WC_BUTTON, "Функции",
				WS_CHILD | WS_VISIBLE | BS_GROUPBOX,
				573, 394, 205, 101, hWnd, NULL, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "АнтиAFK",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				582, 413, 62, 22, hWnd, (HMENU)IDC_AAFKBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "NoAFK",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				647, 413, 52, 22, hWnd, (HMENU)IDC_NOAFKBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Вирт. мир",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				702, 413, 72, 22, hWnd, (HMENU)IDC_VWORLDBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Спавн",
				WS_TABSTOP | BS_TEXT | WS_VISIBLE | WS_CHILD,
				582, 438, 52, 22, hWnd, (HMENU)IDC_SPAWNBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Парсер",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				637, 438, 57, 22, hWnd, (HMENU)IDC_PARSEBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Антисмерть",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				697, 438, 77, 22, hWnd, (HMENU)IDC_ANTIDEATHBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Карта",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				582, 463, 47, 22, hWnd, (HMENU)IDC_MAPBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Данные",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				632, 463, 57, 22, hWnd, (HMENU)IDC_WRITESTATBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			hWndTemp = CreateWindowEx(0, WC_BUTTON, "Дальний чат",
				BS_TEXT | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
				692, 463, 82, 22, hWnd, (HMENU)IDC_FARCHATBTN, g_hInst, NULL);
			SendMessage(hWndTemp, WM_SETFONT, (WPARAM)g_hfText, FALSE);

			HMENU hMenu = CreateMenu();
			HMENU hMenuFuncs = CreatePopupMenu();
			HMENU hMenuInfo = CreatePopupMenu();
			HMENU hMenuLua = CreatePopupMenu();

			AppendMenu(hMenu, MF_POPUP, (uint32_t)hMenuFuncs, "Сервис");
			AppendMenu(hMenu, MF_POPUP, (uint32_t)hMenuInfo, "Справка");
			AppendMenu(hMenu, MF_POPUP, (uint32_t)hMenuLua, "Lua");
			AppendMenu(hMenu, MF_STRING, MENU_DEBUG, "Отладка");

			AppendMenu(hMenuFuncs, MF_STRING, MENU_OPENLOG, "Показать файл лога");
			AppendMenu(hMenuFuncs, MF_STRING, MENU_TRAY, "Свернуть в трей");
			AppendMenu(hMenuFuncs, MF_SEPARATOR, NULL, "");
			AppendMenu(hMenuFuncs, MF_STRING, MENU_EXIT, "Выход");

			AppendMenu(hMenuInfo, MF_STRING, MENU_SITE, "Перейти на Cheat-Master.Ru");
			AppendMenu(hMenuInfo, MF_SEPARATOR, NULL, "");
			AppendMenu(hMenuInfo, MF_STRING, MENU_INFO, "О программе RakBot");

			AppendMenu(hMenuLua, MF_STRING, MENU_LUA_SCRIPTSRELOAD, "Перезагрузить скрипты");
			AppendMenu(hMenuLua, MF_SEPARATOR, NULL, "");
			AppendMenu(hMenuLua, MF_STRING, MENU_LUA_SCRIPTSDIR, "Открыть папку скриптов");

			SetMenu(hWnd, hMenu);
			SetFocus(g_hWndInput);
			vars.windowOpened = true;
			break;
		}

		case WM_KEYDOWN:
		{
			switch (wParam) {
				case VK_RETURN:
				{
					if (GetFocus() == g_hWndInput)
						SendCommand();
					return true;
				}

				case VK_UP:
				{
					CommandHistoryPrev();
					return true;
				}

				case VK_DOWN:
				{
					CommandHistoryNext();
					return true;
				}
			}
			break;
		}

		case WM_COMMAND:
		{
			switch (wParam) {
				case IDC_CHANGELAYOUT_BTN:
					ActivateKeyboardLayout((HKL)HKL_NEXT, NULL);
					break;

				case IDC_SENDBTN:
					SendCommand();
					break;

				case IDC_AAFKBTN:
					RunCommand("!aafk");
					break;

				case IDC_NOAFKBTN:
					RunCommand("!noafk");
					break;

				case IDC_SPAWNBTN:
					RunCommand("!spawn");
					break;

				case IDC_TPBTN:
				{
					float pos[3];
					GetCoords(pos);

					char buf[64];
					snprintf(buf, sizeof(buf), "!tp %f %f %f", pos[0], pos[1], pos[2]);
					RunCommand(buf);
					break;
				}

				case IDC_SCOORDBTN:
				{
					float pos[3];
					GetCoords(pos);

					char buf[128];
					snprintf(buf, sizeof(buf), "!scoords %f %f %f", pos[0], pos[1], pos[2]);
					RunCommand(buf);
					break;
				}

				case IDC_COORDMASTERBTN:
				{
					float pos[3];
					GetCoords(pos);

					char buf[64];
					snprintf(buf, sizeof(buf), "!coord %f %f %f", pos[0], pos[1], pos[2]);
					RunCommand(buf);
					break;
				}

				case IDC_PARSEBTN:
					RunCommand("!parsenicks");
					break;

				case IDC_SPICBTN:
				{
					char buf[64];
					SendMessage(g_hWndPickupID, WM_GETTEXT, (WPARAM)sizeof(buf), (LPARAM)buf);
					int pickupId = atoi(buf);

					snprintf(buf, sizeof(buf), "!sendpick %d", pickupId);
					RunCommand(buf);
					break;
				}

				case IDC_ADMONLINE_IGNORE:
				{
					RakBot::app()->log("[RAKBOT] Бездействие, если админ в сети");
					vars.adminOnlineAction = 0;
					CheckRadioButton(g_hWndMain, IDC_ADMONLINE_IGNORE, IDC_ADMONLINE_EXIT, LOWORD(wParam));
					break;
				}

				case IDC_ADMONLINE_RELOG:
				{
					RakBot::app()->log("[RAKBOT] Переподключение, если админ в сети");
					vars.adminOnlineAction = 1;
					CheckRadioButton(g_hWndMain, IDC_ADMONLINE_IGNORE, IDC_ADMONLINE_EXIT, LOWORD(wParam));
					break;
				}

				case IDC_ADMONLINE_EXIT:
				{
					RakBot::app()->log("[RAKBOT] Выход, если админ в сети");
					vars.adminOnlineAction = 2;
					CheckRadioButton(g_hWndMain, IDC_ADMONLINE_IGNORE, IDC_ADMONLINE_EXIT, LOWORD(wParam));
					break;
				}

				case IDC_ADMNEAR_IGNORE:
				{
					RakBot::app()->log("[RAKBOT] Бездействие, если админ рядом");
					vars.adminNearAction = 0;
					CheckRadioButton(g_hWndMain, IDC_ADMNEAR_IGNORE, IDC_ADMNEAR_EXIT, LOWORD(wParam));
					break;
				}

				case IDC_ADMNEAR_RELOG:
				{
					RakBot::app()->log("[RAKBOT] Переподключение, если админ рядом");
					vars.adminNearAction = 1;
					CheckRadioButton(g_hWndMain, IDC_ADMNEAR_IGNORE, IDC_ADMNEAR_EXIT, LOWORD(wParam));
					break;
				}

				case IDC_ADMNEAR_EXIT:
				{
					RakBot::app()->log("[RAKBOT] Выход, если админ рядом");
					vars.adminNearAction = 2;
					CheckRadioButton(g_hWndMain, IDC_ADMNEAR_IGNORE, IDC_ADMNEAR_EXIT, LOWORD(wParam));
					break;
				}

				case IDC_FOLLOWBTN:
				{
					char buf[64];
					SendMessage(g_hWndPlayerID, WM_GETTEXT, (WPARAM)sizeof(buf), (LPARAM)buf);
					uint32_t playerId = atol(buf);

					snprintf(buf, sizeof(buf), "!follow %d", playerId);
					RunCommand(buf);
					break;
				}

				case IDC_GOTOBTN:
				{
					char buf[64];
					SendMessage(g_hWndPlayerID, WM_GETTEXT, (WPARAM)sizeof(buf), (LPARAM)buf);
					uint32_t playerId = atol(buf);

					snprintf(buf, sizeof(buf), "!goto %d", playerId);
					RunCommand(buf);
					break;
				}

				case IDC_STICKBTN:
				{
					char buf[64];
					SendMessage(g_hWndPlayerID, WM_GETTEXT, (WPARAM)sizeof(buf), (LPARAM)buf);
					uint32_t playerId = atol(buf);

					snprintf(buf, sizeof(buf), "!stick %d", playerId);
					RunCommand(buf);
					break;
				}
				break;

				case IDC_VWORLDBTN:
					RunCommand("!virtualworld");
					break;

				case IDC_WORKERBTN:
					RunCommand("!botloader");
					break;

				case IDC_SKIPDIALOGBTN:
				{
					switch (vars.skipDialog) {
						case 0:
							RakBot::app()->log("[RAKBOT] Автоматическая отправка нажатия 1й кнопки(ENTER)");
							vars.skipDialog = 1;
							break;

						case 1:
							RakBot::app()->log("[RAKBOT] Автоматическая отправка нажатия 2й кнопки(ESC)");
							vars.skipDialog = 2;
							break;

						case 2:
							RakBot::app()->log("[RAKBOT] Игнорирование диалогов");
							vars.skipDialog = 3;
							break;

						case 3:
							RakBot::app()->log("[RAKBOT] Нормальное отображение диалогов");
							vars.skipDialog = 0;
							break;
					}
				}
				break;

				case IDC_CPMBTN:
					RunCommand("!cpm");
					break;

				case IDC_ANTIDEATHBTN:
					RunCommand("!antideath");
					break;

				case IDC_FARMBOTBTN:
					RunCommand("!botfarmer");
					break;

				case IDC_WRITESTATBTN:
					RunCommand("!parsestat");
					break;

				case IDC_MAPBTN:
					RunCommand("!map");
					break;

				case IDC_FARCHATBTN:
					RunCommand("!farchat");
					break;

				case IDC_FLOODBTN:
					RakBot::app()->log("[RAKBOT] !flood 1 <задержка> <текст> - флуд в чат с указанной задержкой");
					RakBot::app()->log("[RAKBOT] !flood 2 <задержка> <текст> - флуд в SMS с указанной задержкой");
					RakBot::app()->log("[RAKBOT] !flood 3 <задержка> <текст> - флуд в репорт с указанной задержкой");
					RakBot::app()->log("[RAKBOT] !flood 4 <задержка> <текст> - флуд в саппорт с указанной задержкой");
					RakBot::app()->log("[RAKBOT] !flood - отключить флудер");
					break;

				case IDC_IGNOREMSGSBTN:
					RunCommand("!skipmsg");
					break;

				case IDC_AUTOLICBTN:
					RunCommand("!autoschool");
					break;

				case IDC_AUTOQUEST:
					RunCommand("!quest");
					break;

				case MENU_DEBUG:
					RunCommand("!debug");
					break;

				case MENU_OPENLOG:
					RunCommand("!openlog");
					break;

				case MENU_TRAY:
					FlipToTray(g_hWndMain, g_hIcon, FALSE);
					break;

					// СПРАВКА
				case MENU_EXIT:
					RakBot::app()->exit();
					break;

				case MENU_INFO:
					ShellExecute(g_hWndMain, "open", "http://rakbot.ru", 0, 0, SW_SHOWNORMAL);
					break;

				case MENU_SITE:
					ShellExecute(g_hWndMain, "open", "http://cheat-master.ru", 0, 0, SW_SHOWNORMAL);
					break;

				case MENU_LUA_SCRIPTSRELOAD:
					RunCommand("!reloadscripts");
					break;

				case MENU_LUA_SCRIPTSDIR:
					ShellExecute(g_hWndMain, "open", GetRakBotPath("//scripts").c_str(), 0, 0, SW_SHOWNORMAL);
					break;
			}
			break;
		}

		case WM_MEASUREITEM:
		{
			LPMEASUREITEMSTRUCT lpMeasureItem = (LPMEASUREITEMSTRUCT)lParam;
			// Is this measure request for our control?
			if (lpMeasureItem->CtlID == IDC_LSTCUSTOM) {
				TEXTMETRIC tm;
				HWND hWndItem = GetDlgItem(hWnd, IDC_LSTCUSTOM);
				HDC hdcItem = GetDC(hWndItem);

				if (GetTextMetrics(hdcItem, &tm))
					// Set the item height to that of the font + 10px padding
					lpMeasureItem->itemHeight = tm.tmHeight + 1;

				ReleaseDC(hWndItem, hdcItem);
				break;
			}
			break;
		}

		case WM_GETMINMAXINFO:
		{
			int windowWidth = 800;
			int windowHeight = 560;

			LPMINMAXINFO minMaxInfo = reinterpret_cast<LPMINMAXINFO>(lParam);
			minMaxInfo->ptMinTrackSize.x = windowWidth;
			minMaxInfo->ptMinTrackSize.y = windowHeight;
			minMaxInfo->ptMaxTrackSize.x = windowWidth;
			minMaxInfo->ptMaxTrackSize.y = windowHeight;
			break;
		}

		case WM_DRAWITEM:
		{
			LPDRAWITEMSTRUCT lpDrawItem = (LPDRAWITEMSTRUCT)lParam;

			switch (lpDrawItem->CtlID) {
				case IDC_LSTCUSTOM:
				{
					LPTSTR lpText = (LPTSTR)lpDrawItem->itemData;
					COLORREF textColor = RGB(0, 0, 0);
					COLORREF bkColor = RGB(255, 255, 255);

					if (lpText == NULL)
						return 0;

					if (!strncmp(&lpText[11], "[RAKBOT] ", 9) || !strncmp(lpText, "[RAKBOT] ", 9))
						textColor = RGB(0, 0, 130);

					if (!strncmp(&lpText[11], "[СЕРВЕР] ", 9) || !strncmp(lpText, "[СЕРВЕР] ", 9))
						textColor = RGB(0, 130, 0);

					if (!strncmp(&lpText[11], "[ERROR] ", 8) || !strncmp(lpText, "[ERROR] ", 8))
						textColor = RGB(130, 0, 0);

					if (!strncmp(&lpText[11], "[WARNING] ", 10) || !strncmp(lpText, "[WARNING] ", 10))
						textColor = RGB(204, 85, 0);

					if (!strncmp(&lpText[11], "[LUA] ", 6) || !strncmp(lpText, "[LUA] ", 6))
						textColor = RGB(0, 130, 130);

					SetBkColor(lpDrawItem->hDC, bkColor);
					SetTextColor(lpDrawItem->hDC, textColor);

					ExtTextOut(lpDrawItem->hDC,
						lpDrawItem->rcItem.left + 3, lpDrawItem->rcItem.top,
						ETO_OPAQUE | ETO_CLIPPED, &lpDrawItem->rcItem,
						lpText, lstrlen(lpText), NULL);
					break;
				}

				default:
					break;
			}
			break;
		}

		case WM_DESTROY:
		{
			PostQuitMessage(0);
			break;
		}

		default:
			break;
	}

	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

void MainWindow() {
	INITCOMMONCONTROLSEX icex;
	icex.dwSize = sizeof(INITCOMMONCONTROLSEX);
	icex.dwICC = ICC_WIN95_CLASSES | ICC_COOL_CLASSES | ICC_BAR_CLASSES | ICC_USEREX_CLASSES;
	InitCommonControlsEx(&icex);

	WNDCLASSEX cWndClass;
	HDC hdcScreen;
	MSG msg;

	ZeroMemory(&msg, sizeof(MSG));
	ZeroMemory(&cWndClass, sizeof(WNDCLASSEX));

	// Register our Main Window class.
	cWndClass.cbSize = sizeof(WNDCLASSEX);
	cWndClass.hInstance = g_hInst;
	cWndClass.lpszClassName = "mainWindowClass";
	cWndClass.lpfnWndProc = MainWindowProc;
	cWndClass.hCursor = LoadCursor(g_hInst, IDC_ARROW);
	cWndClass.hIcon = g_hIcon;
	cWndClass.hIconSm = cWndClass.hIcon;
	cWndClass.hbrBackground = (HBRUSH)(COLOR_BTNFACE + 1);
	//cWndClass.hbrBackground = (HBRUSH)COLOR_BACKGROUND;

	if (!RegisterClassEx(&cWndClass))
		return;

	// Create a font we can later use on our controls. We use MulDiv and GetDeviceCaps to convert
	// our point size to match the users DPI setting.
	hdcScreen = GetDC(HWND_DESKTOP);

	g_hfText = CreateFont(15,
		0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, RUSSIAN_CHARSET, OUT_TT_PRECIS,
		CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, FF_DONTCARE, "Arial");

	g_hfListBoxText = CreateFont(15,
		0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, RUSSIAN_CHARSET, OUT_TT_PRECIS,
		CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, FF_DONTCARE, "Consolas");

	ReleaseDC(HWND_DESKTOP, hdcScreen);

	// Create an instance of the Main Window.
	g_hWndMain = CreateWindowEx(WS_EX_APPWINDOW, cWndClass.lpszClassName, "RakBot " RAKBOT_VERSION,
		WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, 0, 0, 0, 0,
		HWND_DESKTOP, NULL, g_hInst, NULL);

	if (g_hWndMain) {
		// Show the main window and enter the message loop.
		ShowWindow(g_hWndMain, SW_SHOW);
		UpdateWindow(g_hWndMain);

		while (GetMessage(&msg, NULL, 0, 0) && !RakBot::app()->isBotOff()) {
			if (msg.message == WM_KEYDOWN || msg.message == WM_KEYUP)
				SendMessage(g_hWndMain, msg.message, msg.wParam, msg.lParam);

			if (IsDialogMessage(g_hWndMain, &msg) == 0) {
				TranslateMessage(&msg);
				DispatchMessage(&msg);
			}
		}
	}

	g_hWndAdmins = NULL;
	g_hWndTitle = NULL;
	g_hWndLog = NULL;
	g_hWndMain = NULL;

	RakBot::app()->exit();
	DeleteObject(g_hfText);
}
