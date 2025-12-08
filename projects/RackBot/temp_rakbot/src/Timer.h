#pragma once

#include <Windows.h>

class Timer {
private:
	uint32_t _timer;
	std::mutex _timerMutex;

public:
	Timer();
	Timer(uint32_t timer);
	~Timer();

	void setTimerFromCurrentTime();
	void setTimer(uint32_t timer);
	uint32_t getTimer() { return _timer; }

	uint32_t getElapsed();
	bool isElapsed(uint32_t ms, bool resetIfTrue);

	static uint32_t getCurrentTime() { return GetTickCount(); }
};

