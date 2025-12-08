package main

/*
#include <windows.h>
int isKeyDown(int vk) {
    return (GetAsyncKeyState(vk) & 0x8000) != 0;
}
void pressEqualDown() {
    INPUT input;
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = 0xBB; // VK_OEM_PLUS (равно)
    input.ki.wScan = 0;
    input.ki.dwFlags = 0; // key down
    input.ki.time = 0;
    input.ki.dwExtraInfo = 0;
    SendInput(1, &input, sizeof(INPUT));
}
void pressEqualUp() {
    INPUT input;
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = 0xBB; // VK_OEM_PLUS (равно)
    input.ki.wScan = 0;
    input.ki.dwFlags = KEYEVENTF_KEYUP; // key up
    input.ki.time = 0;
    input.ki.dwExtraInfo = 0;
    SendInput(1, &input, sizeof(INPUT));
}
*/
import "C"
import (
	"math"
	"math/rand"
	"strconv"
	"time"

	"github.com/go-vgo/robotgo"
)

func hexToRGB(hex string) (uint8, uint8, uint8) {
	r, _ := strconv.ParseUint(hex[0:2], 16, 8)
	g, _ := strconv.ParseUint(hex[2:4], 16, 8)
	b, _ := strconv.ParseUint(hex[4:6], 16, 8)
	return uint8(r), uint8(g), uint8(b)
}

func colorMatch(r, g, b, tr, tg, tb, tol uint8) bool {
	return math.Abs(float64(r)-float64(tr)) <= float64(tol) &&
		math.Abs(float64(g)-float64(tg)) <= float64(tol) &&
		math.Abs(float64(b)-float64(tb)) <= float64(tol)
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	rand.Seed(time.Now().UnixNano())
	targetR, targetG, targetB := uint8(255), uint8(115), uint8(255)   // светлый фиолетовый
	targetR2, targetG2, targetB2 := uint8(200), uint8(80), uint8(200) // чуть более тёмный фиолетовый
	tolerance := uint8(42)
	toleranceDark := uint8(24) // для тёмного оттенка — меньше допуск
	// --- Настройки ---
	regionSize := 7                     // размер квадрата (рамки)
	thickness := 14                     // толщина рамки
	circleRadius := 8                   // радиус круга
	circlePoints := 16                  // количество точек на круге
	crossOffsets := []int{-8, -4, 4, 8} // смещения для креста
	// --- Конец настроек ---
	half := regionSize / 2

	aimEnabled := true
	tabWasDown := false
	wasTriggering := false

	for {
		// Глобальное переключение по Tab (VK_TAB = 0x09)
		tabDown := C.isKeyDown(0x09) != 0
		if tabDown && !tabWasDown {
			aimEnabled = !aimEnabled
		}
		tabWasDown = tabDown

		// Проверка: если зажата W/A/S/D — не срабатываем
		if C.isKeyDown(0x57) != 0 || // W
			C.isKeyDown(0x41) != 0 || // A
			C.isKeyDown(0x53) != 0 || // S
			C.isKeyDown(0x44) != 0 { // D
			if wasTriggering {
				C.pressEqualUp()
				wasTriggering = false
			}
			continue
		}
		if !aimEnabled {
			if wasTriggering {
				C.pressEqualUp()
				wasTriggering = false
			}
			continue
		}
		screenW, screenH := robotgo.GetScreenSize()
		centerX, centerY := screenW/2, screenH/2

		// Проверяем центр
		hex := robotgo.GetPixelColor(centerX, centerY)
		r, g, b := hexToRGB(hex)
		if colorMatch(r, g, b, targetR, targetG, targetB, tolerance) ||
			colorMatch(r, g, b, targetR2, targetG2, targetB2, toleranceDark) {
			if wasTriggering {
				C.pressEqualUp()
				wasTriggering = false
			}
			continue
		}

		foundFrame := false
		// Проверяем рамку (frame)
		for dx := -half; dx <= half && !foundFrame; dx++ {
			for dy := -half; dy <= half && !foundFrame; dy++ {
				if dx == 0 && dy == 0 {
					continue // не проверяем центр второй раз
				}
				if !(abs(dx) >= half-thickness+1 || abs(dy) >= half-thickness+1) {
					continue
				}
				hex := robotgo.GetPixelColor(centerX+dx, centerY+dy)
				r, g, b := hexToRGB(hex)
				if colorMatch(r, g, b, targetR, targetG, targetB, tolerance) ||
					colorMatch(r, g, b, targetR2, targetG2, targetB2, toleranceDark) {
					foundFrame = true
				}
			}
		}

		foundCircle := false
		// Проверяем круг (circle)
		for i := 0; i < circlePoints && !foundCircle; i++ {
			angle := 2 * math.Pi * float64(i) / float64(circlePoints)
			dx := int(float64(circleRadius) * math.Cos(angle))
			dy := int(float64(circleRadius) * math.Sin(angle))
			hex := robotgo.GetPixelColor(centerX+dx, centerY+dy)
			r, g, b := hexToRGB(hex)
			if colorMatch(r, g, b, targetR, targetG, targetB, tolerance) ||
				colorMatch(r, g, b, targetR2, targetG2, targetB2, toleranceDark) {
				foundCircle = true
			}
		}

		foundCross := false
		// Проверяем крест (cross)
		for _, offset := range crossOffsets {
			if foundCross {
				break
			}
			// Горизонталь
			hex := robotgo.GetPixelColor(centerX+offset, centerY)
			r, g, b := hexToRGB(hex)
			if colorMatch(r, g, b, targetR, targetG, targetB, tolerance) ||
				colorMatch(r, g, b, targetR2, targetG2, targetB2, toleranceDark) {
				foundCross = true
				break
			}
			// Вертикаль
			hex = robotgo.GetPixelColor(centerX, centerY+offset)
			r, g, b = hexToRGB(hex)
			if colorMatch(r, g, b, targetR, targetG, targetB, tolerance) ||
				colorMatch(r, g, b, targetR2, targetG2, targetB2, toleranceDark) {
				foundCross = true
				break
			}
		}

		if foundFrame || foundCircle || foundCross {
			if !wasTriggering {
				C.pressEqualDown()
				wasTriggering = true
			}
		} else {
			if wasTriggering {
				C.pressEqualUp()
				wasTriggering = false
			}
		}
	}
}
