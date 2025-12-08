; AutoHotkey script to click Yes on Sandboxie UAC dialog
; This script waits for Sandboxie window and clicks Yes button

#NoEnv
#SingleInstance Force
SetTitleMatchMode, 2
SetControlDelay, 20

; Wait for Sandboxie window (max 20 seconds)
WinWait, Sandboxie, , 20

if ErrorLevel
{
    FileAppend, ERROR: Sandboxie window not found`n, sandboxie_ahk.log
    ExitApp, 1
}

; Window found
FileAppend, OK: Sandboxie window found`n, sandboxie_ahk.log

; Activate window
WinActivate, Sandboxie
Sleep, 300

; Press Left arrow to select Yes (default is No)
Send, {Left}
FileAppend, OK: Pressed Left arrow`n, sandboxie_ahk.log
Sleep, 200

; Press Enter to confirm
Send, {Enter}
FileAppend, OK: Pressed Enter`n, sandboxie_ahk.log
Sleep, 500

FileAppend, SUCCESS: Yes clicked`n, sandboxie_ahk.log
ExitApp, 0

