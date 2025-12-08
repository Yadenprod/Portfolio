// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "Settings.h"

Vars vars;
std::mutex Vars::adminsMutex;
TeleportPlace Vars::teleportPlaces[300];
Timer Vars::botConnectedTimer;
Timer Vars::botSpawnedTimer;
Timer Vars::gameInitedTimer;
Timer Vars::reconnectTimer;
Timer Vars::lastChangePos;
std::queue<std::string> commandQueue;
std::mutex commandQueueMutex;

Settings::Settings() {}

Settings::~Settings() {}

void Settings::reset() {
	std::lock_guard<std::mutex> lock(_settingsMutex);

	_address.reset();
}

Address *Settings::getAddress() {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	return &_address;
}

void Settings::setName(std::string name) {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	_name = name;
}

std::string Settings::getName() {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	return _name;
}

void Settings::setLoginPassword(std::string loginPassword) {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	_loginPassword = loginPassword;
}

std::string Settings::getLoginPassword() {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	return _loginPassword;
}

void Settings::setServerPassword(std::string serverPassword) {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	_serverPassword = serverPassword;
}

std::string Settings::getServerPassword() {
	std::lock_guard<std::mutex> lock(_settingsMutex);
	return _serverPassword;
}