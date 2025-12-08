package main

import (
	"bytes"
	"encoding/json"
	"image/png"
	"mime/multipart"
	"net/http"

	"github.com/go-vgo/robotgo"
)

// #include <windows.h>
// void pressEqualDown() {
//     INPUT input;
//     input.type = INPUT_KEYBOARD;
//     input.ki.wVk = 0xBB;
//     input.ki.wScan = 0;
//     input.ki.dwFlags = 0;
//     input.ki.time = 0;
//     input.ki.dwExtraInfo = 0;
//     SendInput(1, &input, sizeof(INPUT));
// }
// void pressEqualUp() {
//     INPUT input;
//     input.type = INPUT_KEYBOARD;
//     input.ki.wVk = 0xBB;
//     input.ki.wScan = 0;
//     input.ki.dwFlags = KEYEVENTF_KEYUP;
//     input.ki.time = 0;
//     input.ki.dwExtraInfo = 0;
//     SendInput(1, &input, sizeof(INPUT));
// }
// #include <windows.h>
// int isMouseDown() {
//     return (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0 ||
//            (GetAsyncKeyState(VK_RBUTTON) & 0x8000) != 0 ||
//            (GetAsyncKeyState(VK_XBUTTON1) & 0x8000) != 0 ||
//            (GetAsyncKeyState(VK_XBUTTON2) & 0x8000) != 0;
// }
import "C"

func main() {
	screenW, screenH := robotgo.GetScreenSize()
	regionW := 1280
	regionH := 960
	wasTriggering := false
	for {
		x := screenW/2 - regionW/2
		y := screenH/2 - regionH/2
		bmp := robotgo.CaptureScreen(x, y, regionW, regionH)
		img := robotgo.ToImage(bmp)
		bufImg := new(bytes.Buffer)
		_ = png.Encode(bufImg, img)
		robotgo.FreeBitmap(bmp)

		// Лог: отправка скриншота
		println("[LOG] Отправляю скриншот на сервер...")

		buf, contentType, err := createMultipart(bufImg.Bytes())
		if err != nil {
			println("[LOG] Ошибка формирования multipart:", err.Error())
			continue
		}
		resp, err := http.Post("http://127.0.0.1:5001/predict", contentType, buf)
		if err == nil && resp.StatusCode == 200 {
			var result struct {
				Enemy bool `json:"enemy"`
			}
			errDecode := json.NewDecoder(resp.Body).Decode(&result)
			resp.Body.Close()
			if errDecode == nil && result.Enemy {
				// Проверяем, не нажата ли физически мышь (любая кнопка)
				if C.isMouseDown() == 0 {
					if !wasTriggering {
						C.pressEqualDown()
						wasTriggering = true
					}
				}
			} else {
				if wasTriggering {
					C.pressEqualUp()
					wasTriggering = false
				}
			}
		} else {
			if err != nil {
				println("[LOG] Ошибка отправки запроса:", err.Error())
			} else {
				println("[LOG] Сервер вернул статус:", resp.StatusCode)
			}
			if wasTriggering {
				println("[LOG] Потеря связи с сервером. Отпускаю кнопку =")
				C.pressEqualUp()
				wasTriggering = false
			}
		}
		// Убрана задержка для максимальной скорости
	}
}

// createMultipart формирует multipart/form-data с файлом image и возвращает buffer и content-type
func createMultipart(img []byte) (*bytes.Buffer, string, error) {
	var b bytes.Buffer
	w := multipart.NewWriter(&b)
	f, err := w.CreateFormFile("image", "img.png")
	if err != nil {
		return nil, "", err
	}
	_, err = f.Write(img)
	if err != nil {
		return nil, "", err
	}
	w.Close()
	return &b, w.FormDataContentType(), nil
}
