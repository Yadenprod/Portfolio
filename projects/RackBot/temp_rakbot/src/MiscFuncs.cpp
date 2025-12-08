// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"
#include "PlayerBase.h"
#include "Player.h"
#include "Bot.h"
#include "RakNet.h"
#include "Settings.h"
#include "Pickup.h"
#include "Vehicle.h"
#include "Events.h"

#include "VehicleStuff.h"
#include "MiscFuncs.h"

// following functions

Pickup *FindNearestPickup(int model) {
	Bot *bot = RakBot::app()->getBot();
	Pickup *result = nullptr;

	if (!bot->isSpawned())
		return result;

	float fDist = -1.0f;

	for (int i = 1; i < MAX_PICKUPS; i++) {
		Pickup *pickup = RakBot::app()->getPickup(i);

		if (pickup == nullptr)
			continue;

		if (pickup->getModel() != model)
			continue;

		float fTempDist = bot->distanceTo(pickup);
		if (fTempDist < fDist || fDist < 0.0f) {
			result = pickup;
			fDist = fTempDist;
		}
	}

	return result;
}

Player *FindNearestPlayer(int skin) {
	Bot *bot = RakBot::app()->getBot();
	Player *result = nullptr;

	if (!bot->isSpawned())
		return result;

	float fDist = -1.0f;

	for (int i = 0; i < MAX_PLAYERS; i++) {
		Player *player = RakBot::app()->getPlayer(i);
		if (player == nullptr)
			continue;

		if (!player->isInStream())
			continue;

		if (skin != -1 && player->getSkin() != skin)
			continue;

		float fTempDist = bot->distanceTo(player);

		if (fTempDist < fDist || fDist < 0.0f) {
			result = player;
			fDist = fTempDist;
		}
	}

	return result;
}

Vehicle *FindNearestVehicle(int opened, int model, int color1, int color2) {
	Bot *bot = RakBot::app()->getBot();
	Vehicle *result = nullptr;

	if (!bot->isSpawned())
		return result;

	float fDist = -1.0f;

	for (int i = 1; i < MAX_VEHICLES; i++) {
		Vehicle *vehicle = RakBot::app()->getVehicle(i);
		if (vehicle == nullptr)
			continue;

		if ((opened != -1) && (static_cast<int>(vehicle->isDoorsOpened()) != opened))
			continue;

		if ((model != -1) && (vehicle->getModel() != model))
			continue;

		if ((color1 != -1) && (vehicle->getFirstColor() != color1))
			continue;

		if ((color2 != -1) && (vehicle->getSecondColor() != color2))
			continue;

		float fTempDist = bot->distanceTo(vehicle);

		if (fTempDist < fDist || fDist < 0.0f) {
			result = vehicle;
			fDist = fTempDist;
		}
	}

	return result;
}

Player *FindPlayerByName(std::string name) {
	for (int i = 0; i < MAX_PLAYERS; i++) {
		Player *player = RakBot::app()->getPlayer(i);
		if (player == nullptr)
			continue;

		if (player->getName() == name)
			return player;
	}

	return nullptr;
}

const char *GenRandomString(char *s, const int len, bool numbers) {
	char *charset = nullptr;

	if (numbers) {
		charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
	} else {
		charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	}

	for (int i = 0; i < len; ++i)
		s[i] = charset[rand() % (strlen(charset) - 1)];

	s[len] = 0;
	return s;
}

std::string GetRakBotPath() {
	static char rakBotPathBuffer[MAX_PATH];
	GetModuleFileName(NULL, rakBotPathBuffer, sizeof(rakBotPathBuffer));
	*(strrchr(rakBotPathBuffer, '\\') + 1) = 0;

	std::string rakBotPath = rakBotPathBuffer;
	return rakBotPath;
}

std::string GetRakBotPath(const std::string& append) {
	static char rakBotPathBuffer[MAX_PATH];
	GetModuleFileName(NULL, rakBotPathBuffer, sizeof(rakBotPathBuffer));
	*(strrchr(rakBotPathBuffer, '\\') + 1) = 0;

	std::string rakBotPath = rakBotPathBuffer;
	rakBotPath = rakBotPath + append;
	return rakBotPath;
}

std::string UrlEncode(const std::string &s) {
	std::ostringstream escaped;
	escaped.fill('0');
	escaped << std::hex;

	// for (std::string::const_iterator i = s.begin(), n = s.end(); i != n; ++i) {
	for (size_t i = 0; i < s.length(); i++) {
		// std::string::value_type c = *i;
		std::string::value_type c = s[i];

		// Keep alphanumeric and other accepted characters intact
		if (isalnum(c) || c == '-' || c == '_' || c == '.' || c == '~') {
			escaped << c;
			continue;
		}

		// Any other characters are percent-encoded
		escaped << std::uppercase;
		escaped << '%' << std::setw(2) << int((unsigned char)c);
		escaped << std::nouppercase;
	}

	return escaped.str();
}

void LTrim(std::string &s) {
	s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch) {
		return !std::isspace(ch);
	}));
}

void RTrim(std::string &s) {
	s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) {
		return !std::isspace(ch);
	}).base(), s.end());
}

void Trim(std::string &s) {
	LTrim(s);
	RTrim(s);
}

std::vector<std::string> Split(const std::string &s, char delim) {
	std::stringstream ss(s);
	std::string item;
	std::vector<std::string> elems;
	while (std::getline(ss, item, delim)) {
		elems.push_back(item);
		// elems.push_back(std::move(item)); // if C++11 (based on comment from @mchiasson)
	}
	return elems;
}

void DoCoordMaster(bool state, float x, float y, float z) {
	if (state) {
		if (RakBot::app()->getEvents()->onCoordMasterStart(x, y, z))
			return;

		vars.coordMasterTarget[0] = x;
		vars.coordMasterTarget[1] = y;
		vars.coordMasterTarget[2] = z;

		if (vars.coordMasterEnabled)
			return;

		vars.coordMasterEnabled = true;
		RakBot::app()->log("[RAKBOT] CoordMaster: телепорт на координаты (%.2f; %.2f; %.2f)", x, y, z);
	} else {
		if (RakBot::app()->getEvents()->onCoordMasterStop())
			return;

		vars.coordMasterTarget[0] = 0.f;
		vars.coordMasterTarget[1] = 0.f;
		vars.coordMasterTarget[2] = 0.f;

		if (!vars.coordMasterEnabled)
			return;

		vars.coordMasterEnabled = false;
		RakBot::app()->log("[RAKBOT] CoordMaster: телепорт остановлен");
	}
}

bool IsDirExists(const std::string& dirPath) {
	DWORD ftyp = GetFileAttributesA(dirPath.c_str());
	if (ftyp == INVALID_FILE_ATTRIBUTES)
		return false;

	if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
		return true;

	return false;
}

bool IsFileExists(const std::string &filePath) {
	FILE *f;
	if (fopen_s(&f, filePath.c_str(), "rb") == 0) {
		fclose(f);
		return true;
	}
	return false;
}

int vasprintf(char **strp, const char *fmt, va_list ap) {
	// _vscprintf tells you how big the buffer needs to be
	int len = _vscprintf(fmt, ap);
	if (len == -1) {
		return -1;
	}
	size_t size = (size_t)len + 1;
	char *str = new char[size];
	if (!str) {
		return -1;
	}
	// _vsprintf_s is the "secure" version of vsprintf
	int r = vsprintf_s(str, len + 1, fmt, ap);
	if (r == -1) {
		delete[] str;
		return -1;
	}
	*strp = str;
	return r;
}

int asprintf(char **strp, const char *fmt, ...) {
	va_list ap;
	va_start(ap, fmt);
	int r = vasprintf(strp, fmt, ap);
	va_end(ap);
	return r;
}