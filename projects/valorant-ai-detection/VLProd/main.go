package main

/*
#include <windows.h>

void pressSpace() {
    INPUT input;
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = VK_SPACE;
    input.ki.wScan = 0;
    input.ki.dwFlags = 0;
    input.ki.time = 0;
    input.ki.dwExtraInfo = 0;
    SendInput(1, &input, sizeof(INPUT));

    input.ki.dwFlags = KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
}
*/
import "C"
import (
	"fmt"
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

func main() {
	rand.Seed(time.Now().UnixNano())
	targetR, targetG, targetB := uint8(250), uint8(195), uint8(248) // Фиолетовый контур Valorant
	tolerance := uint8(50)
	regionSize := 5

	for {
		screenW, screenH := robotgo.GetScreenSize()
		centerX, centerY := screenW/2, screenH/2

		found := false
		for x := 0; x < regionSize && !found; x++ {
			for y := 0; y < regionSize && !found; y++ {
				hex := robotgo.GetPixelColor(centerX-regionSize/2+x, centerY-regionSize/2+y)
				r, g, b := hexToRGB(hex)
				fmt.Printf("Pixel (%d,%d): R=%d G=%d B=%d\n", x, y, r, g, b)
				if colorMatch(r, g, b, targetR, targetG, targetB, tolerance) {
					fmt.Println("MATCH! -> SPACE (SendInput)")
					found = true
				}
			}
		}
		if found {
			C.pressSpace()
			time.Sleep(time.Duration(80+rand.Intn(60)) * time.Millisecond)
		}
		time.Sleep(time.Duration(8+rand.Intn(8)) * time.Millisecond)
	}
}
