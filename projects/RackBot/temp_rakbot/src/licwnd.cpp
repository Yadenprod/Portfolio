// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "MiscFuncs.h"
#include "Settings.h"

#include "keycheck.h"
#include "resource.h"
#include "window.h"

#define IDC_ACCEPT 1

HWND LicenseWindow, KeyArea;
HFONT TextFont;

LRESULT CALLBACK licWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
	switch (uMsg) {
		case WM_CREATE:
		{
			HWND tempWindow;

			tempWindow = CreateWindow("STATIC", "Введите ключ активации программы в текстовое поле ниже.",
				WS_VISIBLE | WS_CHILD | SS_CENTER,
				10, 10, 380, 20, hWnd, NULL, g_hInst, NULL);
			SendMessage(tempWindow, WM_SETFONT, (WPARAM)TextFont, FALSE);

			tempWindow = CreateWindow("EDIT", NULL,
				WS_CHILD | WS_TABSTOP | WS_VISIBLE | WS_BORDER,
				10, 35, 380, 20, hWnd, NULL, g_hInst, NULL);
			SendMessage(tempWindow, WM_SETFONT, (WPARAM)TextFont, FALSE);
			KeyArea = tempWindow;

			tempWindow = CreateWindow("BUTTON", "Активировать!",
				BS_DEFPUSHBUTTON | BS_TEXT | WS_CHILD | WS_VISIBLE,
				120, 60, 150, 24, hWnd, (HMENU)IDC_ACCEPT, g_hInst, NULL);
			SendMessage(tempWindow, WM_SETFONT, (WPARAM)TextFont, FALSE);

			HICON hIcon = LoadIcon(g_hInst, MAKEINTRESOURCE(IDI_ICON));
			SendMessage(hWnd, WM_SETICON, ICON_BIG, (LPARAM)hIcon);
			SendMessage(hWnd, WM_SETICON, ICON_SMALL, (LPARAM)hIcon);
			break;

			SetFocus(KeyArea);
			break;
		}

		case WM_COMMAND:
		{
			if (wParam == MAKELONG(IDC_ACCEPT, BN_CLICKED)) {
				char regKey[64];
				SendMessage(KeyArea, WM_GETTEXT, (WPARAM)sizeof(regKey), (LPARAM)regKey);
				vars.regKey = regKey;
				Trim(vars.regKey);

				if (IsWrongKey()) {
					MessageBoxA(LicenseWindow, "Неверный формат ключа!", "Ошибка!", MB_ICONERROR);
				} else {
					std::fstream keyFile(GetRakBotPath("settings\\license.key"), std::ios::out | std::ios::trunc | std::ios::binary);

					if (keyFile.is_open()) {
						keyFile << vars.regKey;
						keyFile.close();
					}

					CheckKey();
				}
				PostQuitMessage(0);
			}
			break;
		}

		case WM_GETMINMAXINFO:
		{
			LPMINMAXINFO minMaxInfo = reinterpret_cast<LPMINMAXINFO>(lParam);
			minMaxInfo->ptMinTrackSize.x = 416;
			minMaxInfo->ptMinTrackSize.y = 130;
			minMaxInfo->ptMaxTrackSize.x = 416;
			minMaxInfo->ptMaxTrackSize.y = 130;
			break;
		}

		case WM_DESTROY:
			PostQuitMessage(0);
			break;
	}
	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

void showLicenseWindow() {
	INITCOMMONCONTROLSEX icex;
	icex.dwSize = sizeof(INITCOMMONCONTROLSEX);
	icex.dwICC = ICC_WIN95_CLASSES | ICC_COOL_CLASSES | ICC_BAR_CLASSES | ICC_USEREX_CLASSES;
	InitCommonControlsEx(&icex);

	WNDCLASSEX wcex;
	HDC hdcScreen;
	MSG msg;

	ZeroMemory(&msg, sizeof(MSG));
	ZeroMemory(&wcex, sizeof(WNDCLASSEX));

	wcex.cbSize = sizeof(WNDCLASSEX);
	wcex.hInstance = g_hInst;
	wcex.lpszClassName = "LicenseWindow";
	wcex.lpfnWndProc = licWindowProc;
	wcex.hCursor = LoadCursor(g_hInst, IDC_ARROW);
	wcex.hIcon = LoadIcon(NULL, MAKEINTRESOURCE(IDI_ICON));
	wcex.hIconSm = wcex.hIcon;
	wcex.hbrBackground = (HBRUSH)(COLOR_BTNFACE + 1);
	//wcex.hbrBackground = (HBRUSH)COLOR_BACKGROUND;

	if (!RegisterClassEx(&wcex)) {
		return;
	}

	hdcScreen = GetDC(HWND_DESKTOP);
	TextFont = CreateFont(-MulDiv(11, GetDeviceCaps(hdcScreen, LOGPIXELSY), 81), // 11pt
		0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, RUSSIAN_CHARSET, OUT_TT_PRECIS,
		CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, FF_DONTCARE, "Arial");
	ReleaseDC(HWND_DESKTOP, hdcScreen);

	LicenseWindow = CreateWindowEx(WS_EX_APPWINDOW, wcex.lpszClassName, "Активация RakBot",
		WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0,
		HWND_DESKTOP, NULL, g_hInst, NULL);

	if (LicenseWindow) {
		ShowWindow(LicenseWindow, 1);
		UpdateWindow(LicenseWindow);

		while (GetMessage(&msg, NULL, 0, 0)) {
			if (!IsDialogMessage(LicenseWindow, &msg)) {
				TranslateMessage(&msg);
				DispatchMessage(&msg);
			}
		}
	}

	DeleteObject(TextFont);
	DestroyWindow(LicenseWindow);
	UnregisterClass("LicenseWindow", g_hInst);
	LicenseWindow = 0;
}