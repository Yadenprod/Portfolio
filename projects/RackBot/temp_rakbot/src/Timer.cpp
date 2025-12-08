// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "Timer.h"

Timer::Timer() {
	_timer = GetTickCount();
}

Timer::Timer(uint32_t timer) {
	_timer = timer;
}

Timer::~Timer() {
}

void Timer::setTimer(uint32_t timer) {
	std::lock_guard<std::mutex> lock(_timerMutex);
	_timer = timer;
}

uint32_t Timer::getElapsed() {
	uint32_t tickCount = GetTickCount();

	_timerMutex.lock();
	uint32_t timer = _timer;
	_timerMutex.unlock();

	if (timer > tickCount)
		return 0;

	return (tickCount - timer);
}

bool Timer::isElapsed(uint32_t ms, bool resetIfTrue) {
	uint32_t tickCount = GetTickCount();

	_timerMutex.lock();
	uint32_t timer = _timer;
	_timerMutex.unlock();

	if (timer >= tickCount)
		return false;

	if ((tickCount - timer) < ms)
		return false;

	if (resetIfTrue) {
		_timerMutex.lock();
		_timer = tickCount;
		_timerMutex.unlock();
	}

	return true;
}

void Timer::setTimerFromCurrentTime() {
	std::lock_guard<std::mutex> lock(_timerMutex);
	_timer = GetTickCount();
}