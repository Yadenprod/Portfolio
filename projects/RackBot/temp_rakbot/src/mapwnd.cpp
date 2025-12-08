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
#include "MiscFuncs.h"

#include "netrpc.h"
#include "resource.h"
#include "window.h"
#include "mapwnd.h"

HWND MapWindow;
HANDLE BitmapHandle;

LRESULT CALLBACK MapWindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
	switch (uMsg) {
		case WM_CREATE:
		{
			HICON hIcon = LoadIcon(g_hInst, MAKEINTRESOURCE(IDI_ICON));
			SendMessage(hWnd, WM_SETICON, ICON_BIG, (LPARAM)hIcon);
			SendMessage(hWnd, WM_SETICON, ICON_SMALL, (LPARAM)hIcon);
			break;
		}

		case WM_PAINT:
		{
			PAINTSTRUCT ps;
			RECT Rect;
			HDC hdc, hCmpDC, hMapDC;
			HBITMAP hBmp;
			HANDLE hOldBitmap;
			HPEN hEllipsePen, hPenOld;
			BITMAP Bitmap;

			GetClientRect(hWnd, &Rect);
			hdc = BeginPaint(hWnd, &ps);

			hCmpDC = CreateCompatibleDC(hdc);
			hBmp = CreateCompatibleBitmap(hdc, Rect.right - Rect.left,
				Rect.bottom - Rect.top);
			SelectObject(hCmpDC, hBmp);

			GetObject(BitmapHandle, sizeof(BITMAP), &Bitmap);
			hMapDC = CreateCompatibleDC(hCmpDC);
			hOldBitmap = SelectObject(hMapDC, BitmapHandle);
			StretchBlt(hCmpDC, 0, 0, 480, 456, hMapDC, 0, 0, 480, 456, SRCCOPY);
			SelectObject(hMapDC, hOldBitmap);

			if (raceCheckpoint.active) {
				hEllipsePen = CreatePen(PS_SOLID, 3, RGB(255, 0, 0));
				hPenOld = (HPEN)SelectObject(hCmpDC, hEllipsePen);
				int x = 251 + (int)(raceCheckpoint.position[0] / 13.2f);
				int y = 228 - (int)(raceCheckpoint.position[1] / 13.2f);
				Ellipse(hCmpDC, x, y, x + 4, y + 4);
				SelectObject(hCmpDC, hPenOld);
				DeleteObject(hEllipsePen);
			}

			Bot *bot = RakBot::app()->getBot();
			if (bot == nullptr)
				break;

			if (bot->isSpawned()) {
				hEllipsePen = CreatePen(PS_SOLID, 3, RGB(0, 0, 255));
				hPenOld = (HPEN)SelectObject(hCmpDC, hEllipsePen);
				int x = 251 + (int)(bot->getPosition(0) / 13.2f);
				int y = 228 - (int)(bot->getPosition(1) / 13.2f);
				Ellipse(hCmpDC, x, y, x + 4, y + 4);
				SelectObject(hCmpDC, hPenOld);
				DeleteObject(hEllipsePen);
			}

			SetStretchBltMode(hdc, COLORONCOLOR);
			BitBlt(hdc, 0, 0, Rect.right - Rect.left, Rect.bottom - Rect.top, hCmpDC, 0, 0, SRCCOPY);

			DeleteDC(hCmpDC);
			DeleteObject(hBmp);
			EndPaint(hWnd, &ps);
			break;
		}

		case WM_GETMINMAXINFO:
		{
			int windowWidth = 496;
			int windowHeight = 494;

			LPMINMAXINFO minMaxInfo = reinterpret_cast<LPMINMAXINFO>(lParam);
			minMaxInfo->ptMinTrackSize.x = windowWidth;
			minMaxInfo->ptMinTrackSize.y = windowHeight;
			minMaxInfo->ptMaxTrackSize.x = windowWidth;
			minMaxInfo->ptMaxTrackSize.y = windowHeight;
			break;
		}
		break;

		case WM_DESTROY:
			PostQuitMessage(0);
			break;
	}

	if (hWnd == NULL)
		return FALSE;

	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

void MapWindowThread() {
	WNDCLASSEX wcex;
	MSG msg;

	InitCommonControls();

	ZeroMemory(&msg, sizeof(MSG));
	ZeroMemory(&wcex, sizeof(WNDCLASSEX));

	wcex.cbSize = sizeof(WNDCLASSEX);
	wcex.hInstance = g_hInst;
	wcex.lpszClassName = TEXT("MapWindow");
	wcex.lpfnWndProc = MapWindowProc;
	wcex.hCursor = LoadCursor(NULL, IDC_ARROW);
	wcex.hIcon = LoadIcon(NULL, MAKEINTRESOURCE(IDI_ICON));
	wcex.hIconSm = wcex.hIcon;
	wcex.hbrBackground = (HBRUSH)(COLOR_BTNFACE + 1);
	//wcex.hbrBackground = (HBRUSH)COLOR_BACKGROUND;
	if (!RegisterClassEx(&wcex)) {
		return;
	}

	BitmapHandle = LoadImage(NULL, GetRakBotPath("map.bmp").c_str(), IMAGE_BITMAP, 0, 0, LR_LOADFROMFILE);

	MapWindow = CreateWindowEx(WS_EX_APPWINDOW, wcex.lpszClassName, "San Andreas",
		WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0,
		HWND_DESKTOP, NULL, g_hInst, NULL);

	if (MapWindow) {
		vars.mapWindowOpened = true;

		ShowWindow(MapWindow, 1);
		UpdateWindow(MapWindow);
		while (GetMessage(&msg, NULL, 0, 0) && !RakBot::app()->isBotOff()) {
			if (!IsDialogMessage(MapWindow, &msg)) {
				TranslateMessage(&msg);
				DispatchMessage(&msg);
			}
		}
	}

	DeleteObject(BitmapHandle);

	DestroyWindow(MapWindow);
	MapWindow = NULL;
	UnregisterClass("MapWindow", GetModuleHandle(NULL));
	RakBot::app()->log("[RAKBOT] Карта закрыта");
	vars.mapWindowOpened = false;
}

void ShowMapWindow() {
	if (!vars.mapWindowOpened)
		vars.mapWindowThread = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(MapWindowThread), NULL, NULL, NULL);
}

void CloseMapWindow() {
	if (vars.mapWindowOpened) {
		SendMessage(MapWindow, WM_DESTROY, 0, 0);
		WaitForSingleObject(vars.mapWindowThread, INFINITE);
		vars.mapWindowThread = nullptr;
	}
}

void UpdateMapWindow() {
	InvalidateRect(MapWindow, NULL, 0);
}
