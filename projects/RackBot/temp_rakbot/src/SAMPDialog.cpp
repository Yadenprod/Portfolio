// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"
#include "MiscFuncs.h"

#include "window.h"

#include "SAMPDialog.h"

SAMPDialog::SAMPDialog() {}

SAMPDialog::~SAMPDialog() {}

void SAMPDialog::reset() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogActive = false;
	_dialogOffline = false;
	_dialogStyle = 0;
	_dialogId = 0;
}

void SAMPDialog::setDialogActive(bool dialogActive) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogActive = dialogActive;
}

bool SAMPDialog::isDialogActive() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _dialogActive;
}

void SAMPDialog::setDialogOffline(bool dialogOffline) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogOffline = dialogOffline;
}

bool SAMPDialog::isDialogOffline() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _dialogOffline;
}

void SAMPDialog::setDialogStyle(uint8_t dialogStyle) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogStyle = dialogStyle;
}

uint8_t SAMPDialog::getDialogStyle() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _dialogStyle;
}

void SAMPDialog::setDialogId(uint16_t dialogId) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogId = dialogId;
}

uint16_t SAMPDialog::getDialogId() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _dialogId;
}

void SAMPDialog::setDialogTitle(std::string dialogTitle) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogTitle = dialogTitle;
}

std::string SAMPDialog::getDialogTitle() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _dialogTitle;
}

void SAMPDialog::setOkButtonText(std::string okButtonText) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_okButtonText = okButtonText;
}

std::string SAMPDialog::getOkButtonText() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _okButtonText;
}

void SAMPDialog::setCancelButtonText(std::string cancelButtonText) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_cancelButtonText = cancelButtonText;
}

std::string SAMPDialog::getCancelButtonText() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _cancelButtonText;
}

void SAMPDialog::setDialogText(std::string dialogText) {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	_dialogText = dialogText;
}

std::string SAMPDialog::getDialogText() {
	std::lock_guard<std::mutex> lock(_sampDialogMutex);
	return _dialogText;
}

HWND hwndSAMPDlg = NULL;

LRESULT CALLBACK SAMPDialogBoxProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
	Bot *bot = RakBot::app()->getBot();

	RECT rect;
	HWND hwndButton1, hwndButton2;
	HWND hwndEditBox = GetDlgItem(hwnd, IDE_INPUTEDIT);
	HWND hwndListBox = GetDlgItem(hwnd, IDL_LISTBOX);
	uint16_t wSelection = 65535;
	char szResponse[512];

	switch (msg) {
		case WM_CREATE:
		{
			HINSTANCE hInst = GetModuleHandle(NULL);
			switch (RakBot::app()->getSampDialog()->getDialogStyle()) {
				case DIALOG_STYLE_MSGBOX:
					hwndButton1 = CreateWindowEx(NULL, "BUTTON",
						(!RakBot::app()->getSampDialog()->getOkButtonText().empty()) ? RakBot::app()->getSampDialog()->getOkButtonText().c_str() : "(не задано)",
						WS_TABSTOP | WS_VISIBLE | WS_CHILD,
						10, 425, 180, 30, hwnd, (HMENU)IDB_BUTTON1, hInst, NULL);
					SendMessage(hwndButton1, WM_SETFONT, (WPARAM)g_hfText, FALSE);
					if (RakBot::app()->getSampDialog()->getOkButtonText().empty())
						EnableWindow(hwndButton1, FALSE);

					hwndButton2 = CreateWindowEx(NULL, "BUTTON",
						(!RakBot::app()->getSampDialog()->getCancelButtonText().empty()) ? RakBot::app()->getSampDialog()->getCancelButtonText().c_str() : "(не задано)",
						WS_TABSTOP | WS_VISIBLE | WS_CHILD,
						195, 425, 180, 30, hwnd, (HMENU)IDB_BUTTON2, hInst, NULL);
					SendMessage(hwndButton2, WM_SETFONT, (WPARAM)g_hfText, FALSE);
					if (RakBot::app()->getSampDialog()->getCancelButtonText().empty())
						EnableWindow(hwndButton2, FALSE);
					break;

				case DIALOG_STYLE_INPUT:
				case DIALOG_STYLE_PASSWORD:
				{
					hwndEditBox = CreateWindowEx(NULL, "EDIT", "", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL,
						10, 400, 365, 20, hwnd, (HMENU)IDE_INPUTEDIT, hInst, NULL);
					SendMessage(hwndEditBox, WM_SETFONT, (WPARAM)g_hfText, FALSE);

					hwndButton1 = CreateWindowEx(NULL, "BUTTON",
						(!RakBot::app()->getSampDialog()->getOkButtonText().empty()) ? RakBot::app()->getSampDialog()->getOkButtonText().c_str() : "(не задано)",
						WS_TABSTOP | WS_VISIBLE | WS_CHILD,
						10, 425, 180, 30, hwnd, (HMENU)IDB_BUTTON1, hInst, NULL);
					SendMessage(hwndButton1, WM_SETFONT, (WPARAM)g_hfText, FALSE);
					if (RakBot::app()->getSampDialog()->getOkButtonText().empty())
						EnableWindow(hwndButton1, FALSE);

					hwndButton2 = CreateWindowEx(NULL, "BUTTON",
						(!RakBot::app()->getSampDialog()->getCancelButtonText().empty()) ? RakBot::app()->getSampDialog()->getCancelButtonText().c_str() : "(не задано)",
						WS_TABSTOP | WS_VISIBLE | WS_CHILD,
						195, 425, 180, 30, hwnd, (HMENU)IDB_BUTTON2, hInst, NULL);
					SendMessage(hwndButton2, WM_SETFONT, (WPARAM)g_hfText, FALSE);
					if (RakBot::app()->getSampDialog()->getCancelButtonText().empty())
						EnableWindow(hwndButton2, FALSE);
				}

				break;

				case DIALOG_STYLE_LIST:
				case DIALOG_STYLE_TABLIST:
				{
					hwndListBox = CreateWindowEx(WS_EX_CLIENTEDGE, "LISTBOX", "",
						LBS_NOINTEGRALHEIGHT | WS_VSCROLL | WS_HSCROLL | WS_CHILD | WS_TABSTOP | WS_VISIBLE,
						10, 10, 365, 410, hwnd, (HMENU)IDL_LISTBOX, g_hInst, NULL);
					SendMessage(hwndListBox, WM_SETFONT, (WPARAM)g_hfListBoxText, FALSE);
					SendMessage(hwndListBox, LB_SETCURSEL, 1, FALSE);

					std::vector<std::string> lines = Split(RakBot::app()->getSampDialog()->getDialogText(), '\n');
					for (std::string line : lines) {
						int id = SendMessage(hwndListBox, LB_ADDSTRING, 0, (LPARAM)line.c_str());
						SendMessage(hwndListBox, LB_SETITEMDATA, id, (LPARAM)id);
					}

					hwndButton1 = CreateWindowEx(NULL, "BUTTON",
						(!RakBot::app()->getSampDialog()->getOkButtonText().empty()) ? RakBot::app()->getSampDialog()->getOkButtonText().c_str() : "(не задано)",
						WS_TABSTOP | WS_VISIBLE | WS_CHILD,
						10, 425, 180, 30, hwnd, (HMENU)IDB_BUTTON1, hInst, NULL);
					SendMessage(hwndButton1, WM_SETFONT, (WPARAM)g_hfText, FALSE);
					if (RakBot::app()->getSampDialog()->getOkButtonText().empty())
						EnableWindow(hwndButton1, FALSE);

					hwndButton2 = CreateWindowEx(NULL, "BUTTON",
						(!RakBot::app()->getSampDialog()->getCancelButtonText().empty()) ? RakBot::app()->getSampDialog()->getCancelButtonText().c_str() : "(не задано)",
						WS_TABSTOP | WS_VISIBLE | WS_CHILD,
						195, 425, 180, 30, hwnd, (HMENU)IDB_BUTTON2, hInst, NULL);
					SendMessage(hwndButton2, WM_SETFONT, (WPARAM)g_hfText, FALSE);
					if (RakBot::app()->getSampDialog()->getCancelButtonText().empty())
						EnableWindow(hwndButton2, FALSE);
				}

				break;
			}
		}
		break;

		case WM_COMMAND:
		{
			switch (LOWORD(wParam)) {
				case IDB_BUTTON1:
					if (RakBot::app()->getSampDialog()->getDialogStyle() == DIALOG_STYLE_LIST) {
						wSelection = (uint16_t)SendMessage(hwndListBox, LB_GETCURSEL, 0, 0);
						if (wSelection != (uint16_t)-1) {
							SendMessage(hwndListBox, LB_GETTEXT, wSelection, (LPARAM)szResponse);
							bot->dialogResponse(RakBot::app()->getSampDialog()->getDialogId(), 1, wSelection, szResponse), RakBot::app()->getSampDialog()->isDialogOffline();
							PostQuitMessage(0);
						}
						break;
					}

					GetWindowText(hwndEditBox, szResponse, 512);
					bot->dialogResponse(RakBot::app()->getSampDialog()->getDialogId(), 1, wSelection, szResponse), RakBot::app()->getSampDialog()->isDialogOffline();
					PostQuitMessage(0);
					break;

				case IDB_BUTTON2:
					GetWindowText(hwndEditBox, szResponse, 512);
					bot->dialogResponse(RakBot::app()->getSampDialog()->getDialogId(), 0, wSelection, szResponse), RakBot::app()->getSampDialog()->isDialogOffline();
					PostQuitMessage(0);
					break;
			}
		}

		break;

		case WM_PAINT:
		{
			PAINTSTRUCT ps;
			HDC hdc = NULL, hdcMem = NULL;
			if (RakBot::app()->getSampDialog()->getDialogStyle() == DIALOG_STYLE_LIST) {
				GetClientRect(hwnd, &rect);
				hdc = BeginPaint(hwnd, &ps);
				SetBkMode(hdc, 1);
				hdcMem = CreateCompatibleDC(hdc);
			} else {
				GetClientRect(hwnd, &rect);
				if (RakBot::app()->getSampDialog()->getDialogStyle() == DIALOG_STYLE_INPUT || RakBot::app()->getSampDialog()->getDialogStyle() == DIALOG_STYLE_PASSWORD)
					rect.bottom -= 79;
				else
					rect.bottom -= 49;
				rect.left = 10;
				rect.top = 10;
				rect.right = rect.right -= 10;
				hdc = BeginPaint(hwnd, &ps);
				SetBkMode(hdc, 1);
				hdcMem = CreateCompatibleDC(hdc);
				SelectObject(hdc, g_hfText);
				DrawText(hdc, RakBot::app()->getSampDialog()->getDialogText().c_str(), RakBot::app()->getSampDialog()->getDialogText().length(), &rect, DT_VCENTER | DT_CENTER | DT_WORDBREAK);
			}

			if (hdcMem)
				DeleteDC(hdcMem);

			if (hdc)
				EndPaint(hwnd, &ps);
		}
		break;

		case WM_GETMINMAXINFO:
		{
			int windowWidth = 400;
			int windowHeight = 500;

			LPMINMAXINFO minMaxInfo = reinterpret_cast<LPMINMAXINFO>(lParam);
			minMaxInfo->ptMinTrackSize.x = windowWidth;
			minMaxInfo->ptMinTrackSize.y = windowHeight;
			minMaxInfo->ptMaxTrackSize.x = windowWidth;
			minMaxInfo->ptMaxTrackSize.y = windowHeight;
			break;
		}

		case WM_DESTROY:
			// bot->dialogResponse(RakBot::app()->getSampDialog()->getDialogId(), 0, wSelection, szResponse);
			PostQuitMessage(0);
			break;

		default:
			return DefWindowProc(hwnd, msg, wParam, lParam);
	}

	return 0;
}

void DialogWindowThread() {
	WNDCLASSEX wc;
	MSG msg;
	HINSTANCE hInstance = GetModuleHandle(NULL);
	RECT conRect;
	GetWindowRect(g_hWndMain, &conRect);

	wc.cbSize = sizeof(WNDCLASSEX);
	wc.style = 0;
	wc.lpfnWndProc = SAMPDialogBoxProc;
	wc.cbClsExtra = 0;
	wc.cbWndExtra = 0;
	wc.hInstance = hInstance;
	wc.hIcon = g_hIcon;
	wc.hIconSm = wc.hIcon;
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = (HBRUSH)(COLOR_BTNFACE + 1);
	wc.lpszMenuName = NULL;
	wc.lpszClassName = "sampDialogWindowClass";

	if (!RegisterClassEx(&wc))
		return;

	hwndSAMPDlg = CreateWindowEx(WS_EX_APPWINDOW, wc.lpszClassName, RakBot::app()->getSampDialog()->getDialogTitle().c_str(),
		WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, (conRect.right + conRect.left) / 2 - 200, 0, 400, 500,
		g_hWndMain, NULL, g_hInst, NULL);

	if (hwndSAMPDlg == NULL)
		return;

	ShowWindow(hwndSAMPDlg, 1);
	UpdateWindow(hwndSAMPDlg);
	SetForegroundWindow(hwndSAMPDlg);

	while (GetMessage(&msg, NULL, 0, 0) > 0 && !RakBot::app()->isBotOff()) {
		if (msg.message == WM_KEYDOWN || msg.message == WM_KEYUP)
			SendMessage(hwndSAMPDlg, msg.message, msg.wParam, msg.lParam);

		if (IsDialogMessage(hwndSAMPDlg, &msg) == 0) {
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	RakBot::app()->getSampDialog()->setDialogActive(false);
	SendMessage(hwndSAMPDlg, WM_DESTROY, 0, 0);
	DestroyWindow(hwndSAMPDlg);
	UnregisterClass("sampDialogWindowClass", GetModuleHandle(NULL));
	hwndSAMPDlg = NULL;
}

void SAMPDialog::showDialog() {
	if (hwndSAMPDlg != NULL)
		hideDialog();

	std::lock_guard<std::mutex> lock(_sampDialogMutex);

	if (_dialogId == DIALOG_ID_NONE)
		return;

	switch (_dialogStyle) {
		case DIALOG_STYLE_MSGBOX:
		case DIALOG_STYLE_INPUT:
		case DIALOG_STYLE_PASSWORD:
		case DIALOG_STYLE_LIST:
		case DIALOG_STYLE_TABLIST:
			if (!_dialogActive) {
				_dialogActive = true;
				vars.dialogWindowThread = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(DialogWindowThread), NULL, NULL, NULL);
			}
			break;

		default:
			if (_dialogActive) {
				SendMessage(hwndSAMPDlg, WM_DESTROY, 0, 0);
			}
			break;
	}
}

void SAMPDialog::hideDialog() {
	SendMessage(hwndSAMPDlg, WM_DESTROY, 0, 0);
	// RakBot::app()->log("[RAKBOT] Ожидание закрытия окна диалога...");
	WaitForSingleObject(vars.dialogWindowThread, INFINITE);
	RakBot::app()->log("[RAKBOT] Окно диалога закрыто");
}
