#pragma once

#include "Timer.h"

class ServerInfo {
private:
	SOCKET _socket;
	sockaddr_in _addr;
	Timer _timer;

	void sendPacket(const char *data, const int size);

public:
	ServerInfo();
	~ServerInfo();

	void socketInit();
	void updateInfo();
};