// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "MiscFuncs.h"
#include "RakNet.h"

#include "window.h"

#include "RakBot.h"

RakBot::RakBot() {
	for (int i = 0; i < MAX_PLAYERS; i++)
		_players[i].reset();

	for (int i = 0; i < MAX_VEHICLES; i++)
		_vehicles[i].reset();

	for (int i = 0; i < MAX_PICKUPS; i++)
		_pickups[i].reset();

	_bot.reset(true);
	_settings.reset();
	_server.reset();
	_events.reset();
	_sampDialog.reset();

	_rakClient = RakNetworkFactory::GetRakClientInterface();
	_rakClient->SetMTUSize(576);

	_botOff = false;
}

RakBot::~RakBot() {
	if (_rakClient != nullptr)
		RakNetworkFactory::DestroyRakClientInterface(_rakClient);
}

RakBot *RakBot::app() {
	static RakBot rakBot;
	return &rakBot;
}

bool RakBot::isBotOff() {
	std::lock_guard<std::mutex> lock(_botOffMutex);
	return _botOff;
}

void RakBot::exit() {
	log("[RAKBOT] Âûõîä èç áîòà...");

	Bot *bot = RakBot::app()->getBot();

	if (bot->isConnected()) {
		bot->disconnect(false);
	}

	std::lock_guard<std::mutex> lock(_botOffMutex);
	_botOff = true;
}

Player *RakBot::getPlayer(uint16_t playerId) {
	if (playerId < 0 || playerId >= MAX_PLAYERS)
		return nullptr;

	if (!_players[playerId].isActive())
		return nullptr;

	return &_players[playerId];
}

Player *RakBot::addPlayer(uint16_t playerId) {
	if (playerId < 0 || playerId >= MAX_PLAYERS)
		return nullptr;

	if (_players[playerId].isActive())
		return &_players[playerId];

	_players[playerId].setPlayerId(playerId);

	return &_players[playerId];
}

void RakBot::deletePlayer(uint16_t playerId) {
	if (playerId < 0 || playerId >= MAX_PLAYERS)
		return;

	if (!_players[playerId].isActive())
		return;

	_players[playerId].reset();
}

uint16_t RakBot::getPlayersCount() {
	if (!_bot.isConnected())
		return 0;

	uint16_t count = 1;

	for (int i = 0; i < MAX_PLAYERS; i++) {
		if (!_players[i].isActive())
			continue;
		count++;
	}

	return count;
}

Pickup *RakBot::getPickup(int pickupId) {
	if (pickupId < 0 || pickupId >= MAX_PICKUPS)
		return nullptr;

	if (!_pickups[pickupId].isActive())
		return nullptr;

	return &_pickups[pickupId];
}

Pickup *RakBot::addPickup(int pickupId) {
	if (pickupId < 0 || pickupId >= MAX_PICKUPS)
		return nullptr;

	if (_pickups[pickupId].isActive())
		return &_pickups[pickupId];

	_pickups[pickupId].setPickupId(pickupId);

	return &_pickups[pickupId];
}

void RakBot::deletePickup(int pickupId) {
	if (pickupId < 0 || pickupId >= MAX_PICKUPS)
		return;

	if (!_pickups[pickupId].isActive())
		return;

	_pickups[pickupId].reset();
}

Vehicle *RakBot::getVehicle(uint16_t vehicleId) {
	if (vehicleId < 1 || vehicleId >= MAX_VEHICLES)
		return nullptr;

	if (!_vehicles[vehicleId].isActive())
		return nullptr;

	return &_vehicles[vehicleId];
}

Vehicle *RakBot::addVehicle(uint16_t vehicleId) {
	if (vehicleId < 1 || vehicleId >= MAX_VEHICLES)
		return nullptr;

	if (_vehicles[vehicleId].isActive())
		return &_vehicles[vehicleId];

	_vehicles[vehicleId].setVehicleId(vehicleId);

	return &_vehicles[vehicleId];
}

void RakBot::deleteVehicle(uint16_t vehicleId) {
	if (vehicleId < 1 || vehicleId >= MAX_VEHICLES)
		return;

	if (!_vehicles[vehicleId].isActive())
		return;

	_vehicles[vehicleId].reset();
}

TextDraw *RakBot::getTextDraw(int textDrawId) {
	if (textDrawId < 0 || textDrawId >= MAX_TEXTDRAWS)
		return nullptr;

	if (!_textDraws[textDrawId].isActive())
		return nullptr;

	return &_textDraws[textDrawId];
}

TextDraw *RakBot::addTextDraw(int textDrawId) {
	if (textDrawId < 0 || textDrawId >= MAX_TEXTDRAWS)
		return nullptr;

	if (_textDraws[textDrawId].isActive())
		return &_textDraws[textDrawId];

	_textDraws[textDrawId].setTextDrawId(textDrawId);

	return &_textDraws[textDrawId];
}

void RakBot::deleteTextDraw(int textDrawId) {
	if (textDrawId < 0 || textDrawId >= MAX_TEXTDRAWS)
		return;

	if (!_textDraws[textDrawId].isActive())
		return;

	_textDraws[textDrawId].reset();
}

Bot *RakBot::getBot() {
	return &_bot;
}

Settings *RakBot::getSettings() {
	return &_settings;
}

RakClientInterface *RakBot::getRakClient() {
	return _rakClient;
}

Server *RakBot::getServer() {
	return &_server;
}

Events *RakBot::getEvents() {
	return &_events;
}

SAMPDialog *RakBot::getSampDialog() {
	return &_sampDialog;
}

ServerInfo *RakBot::getServerInfo() {
	return &_serverInfo;
}

void RakBot::log(const char *format, ...) {
	if (format == nullptr)
		return;

	if (strlen(format) < 1)
		return;

	/*int formatLength = format.length();
	char *fmt = new char[formatLength + 1];
	strncpy(fmt, format.c_str(), formatLength);
	fmt[formatLength] = 0;*/

	// char *buf = new char[MAX_LOGLEN + 1];

	std::va_list args;
	va_start(args, format);
	
	char *buf;
	int bufLen = vasprintf(&buf, format, args);
	buf[bufLen] = 0;
	va_end(args);

	// delete[] fmt;

	if (RakBot::app()->getEvents()->onPrintLog(buf)) {
		delete[] buf;
		return;
	}

	logToFile(buf);

	if (g_hWndMain) {
		if (vars.timeStamp) {
			SYSTEMTIME time;
			GetLocalTime(&time);

			char *tempBuf;
			bufLen = asprintf(&tempBuf, "[%02d:%02d:%02d] %s", time.wHour, time.wMinute, time.wSecond, buf);
			delete[] buf;
			buf = tempBuf;
		}

		if (g_hWndLog) {
			int lbCount = SendMessage(g_hWndLog, LB_GETCOUNT, 0, 0);
			if (lbCount >= MAX_LOGLINES)
				SendMessage(g_hWndLog, LB_DELETESTRING, 0, 0);

			WPARAM idx = SendMessage(g_hWndLog, LB_ADDSTRING, 0, (LPARAM)buf);
			SendMessage(g_hWndLog, LB_SETTOPINDEX, idx, 0);
			return;
		}
	}
	delete[] buf;
}

void RakBot::logToFile(std::string line) {
	std::lock_guard<std::mutex> lock(_logToFileMutex);

	if (vars.logFile == nullptr) {
		Settings *settings = RakBot::app()->getSettings();

		if (settings->getAddress()->getIp().empty())
			return;

		if (settings->getAddress()->getPort() < 0 || settings->getAddress()->getPort() > 65535)
			return;

		if (settings->getName().empty())
			return;

		char currentDirBuf[MAX_PATH];
		GetModuleFileName(NULL, currentDirBuf, sizeof(currentDirBuf));
		*strrchr(currentDirBuf, '\\') = 0;

		std::stringstream ss;
		ss << currentDirBuf << "\\logs";
		CreateDirectory(ss.str().c_str(), NULL);

		ss << "\\" << settings->getAddress()->getIp() << ";" << settings->getAddress()->getPort();
		CreateDirectory(ss.str().c_str(), NULL);

		ss << "\\" << settings->getName() << ".log";

		// MessageBox(NULL, ss.str().c_str(), "", NULL);

		vars.logFile = fopen(ss.str().c_str(), vars.logFileMode.c_str());
		if (vars.logFile == nullptr)
			return;

		fprintf(vars.logFile, "==================================[ÍÎÂÀß ÑÅÑÑÈß]==================================\n");
	}

	SYSTEMTIME time;
	GetLocalTime(&time);

	char timeBuf[64];
	_snprintf(timeBuf, sizeof(timeBuf), "[%02d:%02d:%02d]", time.wHour, time.wMinute, time.wSecond);

	fprintf(vars.logFile, "%s %s\n", timeBuf, line.c_str());
	fflush(vars.logFile);
}