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

#include "ServerInfo.h"

ServerInfo::ServerInfo() {
	_socket = NULL;
	_timer.setTimer(0);
}

ServerInfo::~ServerInfo() {
	if (_socket != NULL)
		closesocket(_socket);
}

void ServerInfo::sendPacket(const char *data, const int size) {
	RakNet::BitStream bsSend;
	bsSend.Write("SAMP", 4);
	bsSend.Write(_addr.sin_addr.s_addr);
	bsSend.Write(RakBot::app()->getSettings()->getAddress()->getPort());
	bsSend.Write(data, size);

	sendto(_socket, (char *)bsSend.GetData(), bsSend.GetNumberOfBytesUsed(), NULL, (SOCKADDR *)&_addr, sizeof(_addr));
}

void ServerInfo::socketInit() {
	_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

	DWORD adapterAddress = inet_addr(vars.adapterAddress.c_str());
	if (adapterAddress != 0) {
		sockaddr_in adapter_addr;
		adapter_addr.sin_family = AF_INET;
		adapter_addr.sin_addr.s_addr = adapterAddress;
		adapter_addr.sin_port = 0;
		bind(_socket, (sockaddr *)&adapter_addr, sizeof(adapter_addr));
		RakBot::app()->log("[RAKBOT] Выбран адаптер с адресом: %s (ServerInfo)", vars.adapterAddress.c_str());
	}

	u_long arg = 1;
	ioctlsocket(_socket, FIONBIO, &arg);

	_addr.sin_family = AF_INET;
	_addr.sin_addr.s_addr = inet_addr(RakBot::app()->getSettings()->getAddress()->getIp().c_str());
	_addr.sin_port = htons(RakBot::app()->getSettings()->getAddress()->getPort());
}

void ServerInfo::updateInfo() {
	if (!_timer.isElapsed(1000, true))
		return;

	sendPacket("p4150", 5);
	sendPacket("i", 1);
	sendPacket("c", 1);
	sendPacket("r", 1);
}