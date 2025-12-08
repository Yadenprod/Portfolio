; AutoHotkey script to close "НОВЫЙ ЛАУНЧЕР" dialog
; This script waits for the dialog and clicks Close button

#NoEnv
#SingleInstance Force
SetTitleMatchMode, 2
SetControlDelay, 20

; Wait for НОВЫЙ ЛАУНЧЕР window (max 20 seconds)
WinWait, ЛАУНЧЕР, , 20

if ErrorLevel
{
    FileAppend, ERROR: ЛАУНЧЕР window not found`n, launcher_ahk.log
    ExitApp, 1
}

; Window found
FileAppend, OK: ЛАУНЧЕР window found`n, launcher_ahk.log

; Activate window
WinActivate, ЛАУНЧЕР
Sleep, 300

; Try to click "Закрыть" button
ControlClick, Закрыть, ЛАУНЧЕР
Sleep, 300

if ErrorLevel
{
    ; If button not found by text, try Tab + Enter
    FileAppend, WARN: Button not found, trying Tab+Enter`n, launcher_ahk.log
    Send, {Tab}
    Sleep, 200
    Send, {Enter}
    Sleep, 300
}
else
{
    FileAppend, OK: Закрыть button clicked`n, launcher_ahk.log
}

FileAppend, SUCCESS: Dialog closed`n, launcher_ahk.log
ExitApp, 0

