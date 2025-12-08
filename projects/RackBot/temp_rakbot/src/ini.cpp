// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"

#include "MiscFuncs.h"

#include "Settings.h"
#include "ini.h"
#include "netrpc.h"

bool SetConfigString(const std::string &filePath, const std::string &section, const std::string &key, const std::string &value) {
	return WritePrivateProfileString(section.c_str(), key.c_str(), value.c_str(), filePath.c_str());
}

std::string GetConfigString(const std::string &filePath, const std::string &section, const std::string &key, const std::string &defaultValue) {
	char valueBuffer[4096];
	GetPrivateProfileString(section.c_str(), key.c_str(), defaultValue.c_str(), valueBuffer, sizeof(valueBuffer), filePath.c_str());
	std::string value = valueBuffer;
	if (value.empty())
		value = defaultValue;

	return value;
}

bool SetConfigInt(const std::string &filePath, const std::string &section, const std::string &key, int value) {
	return WritePrivateProfileString(section.c_str(), key.c_str(), std::to_string(value).c_str(), filePath.c_str());
}

int GetConfigInt(const std::string &filePath, const std::string &section, const std::string &key, int defaultValue) {
	char valueBuffer[64];
	GetPrivateProfileString(section.c_str(), key.c_str(), std::to_string(defaultValue).c_str(), valueBuffer, sizeof(valueBuffer), filePath.c_str());
	std::string value = valueBuffer;
	if (value.empty())
		return defaultValue;

	return std::stoi(value);
}

bool SetConfigFloat(const std::string &filePath, const std::string &section, const std::string &key, float value) {
	return WritePrivateProfileString(section.c_str(), key.c_str(), std::to_string(value).c_str(), filePath.c_str());
}

float GetConfigFloat(const std::string &filePath, const std::string &section, const std::string &key, float defaultValue) {
	char valueBuffer[64];
	GetPrivateProfileString(section.c_str(), key.c_str(), std::to_string(defaultValue).c_str(), valueBuffer, sizeof(valueBuffer), filePath.c_str());
	std::string value = valueBuffer;
	if (value.empty())
		return defaultValue;

	return std::stof(value);
}

bool LoadCustom() {
	bool result = true;

	std::string section, stringValue;
	std::string filePath = GetRakBotPath("settings\\custom.ini");

	if (IsFileExists(filePath)) {
		section = "Log";
		
		vars.logFileMode = GetConfigString(filePath, section, "FileMode", "a");

		section = "Bot";

		vars.mainDelay = GetConfigInt(filePath, section, "MainUpdateDelay", 50);
		if (vars.mainDelay < 1)
			vars.mainDelay = 1;

		vars.luaUpdateDelay = GetConfigInt(filePath, section, "LuaUpdateDelay", 50);
		if (vars.luaUpdateDelay < 1)
			vars.luaUpdateDelay = 1;

		vars.networkUpdateDelay = GetConfigInt(filePath, section, "NetworkUpdateDelay", 50);
		if (vars.networkUpdateDelay < 1)
			vars.networkUpdateDelay = 1;

		vars.spawnDelay = GetConfigInt(filePath, section, "SpawnDelay", 500);
		if (vars.spawnDelay < 1)
			vars.spawnDelay = 1;

		vars.dialogResponseDelay = GetConfigInt(filePath, section, "DialogResponseDelay", 500);
		if (vars.dialogResponseDelay < 1)
			vars.dialogResponseDelay = 1;

		vars.noAfkDelay = GetConfigInt(filePath, section, "NoAfkDelay", 100);
		if (vars.noAfkDelay < 1)
			vars.noAfkDelay = 1;

		vars.afterSpawnDelay = GetConfigInt(filePath, section, "AfterSpawnDelay", 1000);
		if (vars.afterSpawnDelay < 1)
			vars.afterSpawnDelay = 1;

		vars.enterVehicleDelay = GetConfigInt(filePath, section, "EnterVehicleDelay", 2000);
		if (vars.enterVehicleDelay < 1)
			vars.enterVehicleDelay = 1;

		section = "Sync";

		vars.syncSpeedOffset[0] = GetConfigFloat(filePath, section, "SpeedOffsetX", 0.f);
		vars.syncSpeedOffset[1] = GetConfigFloat(filePath, section, "SpeedOffsetY", 0.f);
		vars.syncSpeedOffset[2] = GetConfigFloat(filePath, section, "SpeedOffsetZ", 0.f);

		vars.syncPositionOffset[0] = GetConfigFloat(filePath, section, "PositionOffsetX", 0.f);
		vars.syncPositionOffset[1] = GetConfigFloat(filePath, section, "PositionOffsetY", 0.f);
		vars.syncPositionOffset[2] = GetConfigFloat(filePath, section, "PositionOffsetZ", 0.f);

		section = "AdminChecker";
		vars.adminsUrl = GetConfigString(filePath, section, "URL", "http://api.sanek.love/al_list.php?responseType=colon&from=RakBot");

		section = "Route";

		vars.routeLoop = static_cast<bool>(GetConfigInt(filePath, section, "Loop", 1));

		vars.routeUpdateDelay = GetConfigInt(filePath, section, "Delay", 50);
		if (vars.routeUpdateDelay < 1)
			vars.routeUpdateDelay = 1;

		vars.routeUpdateCount = GetConfigInt(filePath, section, "Count", 2);
		if (vars.routeUpdateCount < 1)
			vars.routeUpdateCount = 1;

		section = "TextDraw";

		vars.textDrawCreateLogging = static_cast<bool>(GetConfigInt(filePath, section, "CreateLog", 0));
		vars.textDrawHideLogging = static_cast<bool>(GetConfigInt(filePath, section, "HideLog", 0));
		vars.textDrawSetStringLogging = static_cast<bool>(GetConfigInt(filePath, section, "SetStringLog", 0));

		section = "3DTextLabel";
		vars.textLabelCreateLogging = static_cast<bool>(GetConfigInt(filePath, section, "CreateLog", 0));

		section = "NetworkAdapter";
		vars.adapterAddress = GetConfigString(filePath, section, "Address", "0.0.0.0");

		section = "BadSync";
		vars.badSyncSurfId = GetConfigInt(filePath, section, "SurfId", 2002);
		vars.badSyncNanOffset = static_cast<bool>(GetConfigInt(filePath, section, "NanOffsets", 0));
	} else {
		section = "Log";
		SetConfigString(filePath, section, "FileMode", "a");

		section = "Bot";
		SetConfigString(filePath, section, "MainUpdateDelay", "50");
		SetConfigString(filePath, section, "LuaUpdateDelay", "50");
		SetConfigString(filePath, section, "NetworkUpdateDelay", "50");
		SetConfigString(filePath, section, "SpawnDelay", "500");
		SetConfigString(filePath, section, "DialogResponseDelay", "500");
		SetConfigString(filePath, section, "NoAfkDelay", "100");
		SetConfigString(filePath, section, "AfterSpawnDelay", "1000");
		SetConfigString(filePath, section, "EnterVehicleDelay", "2000");

		section = "Sync";
		SetConfigString(filePath, section, "SpeedOffsetX", "0.0");
		SetConfigString(filePath, section, "SpeedOffsetY", "0.0");
		SetConfigString(filePath, section, "SpeedOffsetZ", "0.0");
		SetConfigString(filePath, section, "PositionOffsetX", "0.0");
		SetConfigString(filePath, section, "PositionOffsetY", "0.0");
		SetConfigString(filePath, section, "PositionOffsetZ", "0.0");

		section = "AdminChecker";
		SetConfigString(filePath, section, "URL", "http://api.sanek.love/al_list.php?responseType=colon&from=RakBot");

		section = "Route";
		SetConfigString(filePath, section, "Loop", "1");
		SetConfigString(filePath, section, "Delay", "50");
		SetConfigString(filePath, section, "Count", "2");

		section = "TextDraw";
		SetConfigString(filePath, section, "CreateLog", "0");
		SetConfigString(filePath, section, "HideLog", "0");
		SetConfigString(filePath, section, "SetStringLog", "0");

		section = "3DTextLabel";
		SetConfigString(filePath, section, "CreateLog", "0");

		section = "NetworkAdapter";
		SetConfigString(filePath, section, "Address", "0.0.0.0");

		section = "BadSync";
		SetConfigString(filePath, section, "SurdId", "2002");
		SetConfigString(filePath, section, "NanOffsets", "0");

		MessageBox(NULL, "Файл \"settings\\custom.ini\" создан! Перезапустите бота.", "Первая настройка", MB_ICONASTERISK);
		result = false;
	}

	return result;
}

void LoadRoute(char *routeName) {
	vars.routeData.clear();

	OnfootData onfootData;

	char buf[512];
	snprintf(buf, sizeof(buf), "routes\\%s.route", routeName);
	std::string routePath = GetRakBotPath(buf);
	std::fstream routeFile(routePath, std::ios::in | std::ios::binary);

	if (routeFile.is_open()) {
		while (!routeFile.eof()) {
			routeFile.read((char *)&onfootData, sizeof(OnfootData));
			vars.routeData.push_back(onfootData);
		}

		routeFile.close();
		vars.routeIndex = 0;

		RakBot::app()->log("[RAKBOT] Маршрут '%s' успешно загружен", routeName);
	} else {
		RakBot::app()->log("[RAKBOT] Маршрут '%s' не найден", routeName);
	}
}

bool LoadConfig() {
	bool result = true;

	ZeroMemory(&vars, sizeof(Vars));
	CreateDirectory(GetRakBotPath("settings").c_str(), NULL);

	int intValue;
	std::string section, stringValue;
	std::string filePath = GetRakBotPath("settings\\settings.ini");

	if (IsFileExists(filePath)) {
		section = "Account";
		stringValue = GetConfigString(filePath, section, "Server", "127.0.0.1:7777");

		std::smatch matches;
		std::regex_search(stringValue, matches, std::regex("(\\S+):(\\d+)"));

		if (matches.size() != 3) {
			RakBot::app()->getSettings()->getAddress()->setIp("127.0.0.1");
			RakBot::app()->getSettings()->getAddress()->setPort(7777);
		} else {
			std::string ip = matches[1];
			RakBot::app()->getSettings()->getAddress()->setIp(ip);

			int port = std::stoi(matches[2]);
			if (port < 1 || port > 65535)
				port = 7777;

			RakBot::app()->getSettings()->getAddress()->setPort(static_cast<uint16_t>(port));
		}

		stringValue = GetConfigString(filePath, section, "NickName", "MishaN");
		RakBot::app()->getSettings()->setName(stringValue);

		stringValue = GetConfigString(filePath, section, "Password", "qwerty");
		RakBot::app()->getSettings()->setLoginPassword(stringValue);

		section = "AutoReg";
		stringValue = GetConfigString(filePath, section, "Enabled", "0");
		vars.autoRegEnabled = static_cast<bool>(std::stoul(stringValue));

		vars.autoRegMail = GetConfigString(filePath, section, "Mail", "mail@mail.ru");
		vars.autoRegReferer = GetConfigString(filePath, section, "NickName", "MishaN");

		stringValue = GetConfigString(filePath, section, "Sex", "1");
		vars.autoRegSex = std::stoi(stringValue);
		if (vars.autoRegSex < 0 || vars.autoRegSex > 1)
			vars.autoRegSex = 1;

		section = "CoordMaster";
		stringValue = GetConfigString(filePath, section, "Distance", "80.0");
		vars.coordMasterDist = std::stof(stringValue);
		if (vars.coordMasterDist < 1.f)
			vars.coordMasterDist = 1.f;

		stringValue = GetConfigString(filePath, section, "Height", "-40.0");
		vars.coordMasterHeight = std::stof(stringValue);

		stringValue = GetConfigString(filePath, section, "Delay", "1500");
		vars.coordMasterDelay = std::stoi(stringValue);
		if (vars.coordMasterDelay < 1000)
			vars.coordMasterDelay = 1000;

		section = "Loader";
		stringValue = GetConfigString(filePath, section, "Delay", "10000");
		vars.botLoaderDelay = std::stoi(stringValue);
		if (vars.botLoaderDelay < 1000)
			vars.botLoaderDelay = 1000;

		stringValue = GetConfigString(filePath, section, "Limit", "20");
		vars.botLoaderLimit = std::stoi(stringValue);
		if (vars.botLoaderLimit < 1)
			vars.botLoaderLimit = 1;

		stringValue = GetConfigString(filePath, section, "Enabled", "0");
		vars.botLoaderEnabled = static_cast<bool>(std::stoul(stringValue));

		section = "Settings";
		stringValue = GetConfigString(filePath, section, "KickReconnect", "15");
		intValue = std::stoi(stringValue);
		if (intValue < 0)
			intValue = 0;
		vars.reconnectDelay = (intValue * 1000) + 500;

		stringValue = GetConfigString(filePath, section, "AdminReconnect", "300");
		intValue = std::stoi(stringValue);
		if (intValue < 0)
			intValue = 0;
		vars.adminReconnectDelay = (intValue * 1000) + 500;

		stringValue = GetConfigString(filePath, section, "PasswordDialog", "1");
		intValue = std::stoi(stringValue);
		if (intValue < 0)
			intValue = 0;
		vars.dialogIdPassword = intValue;

		stringValue = GetConfigString(filePath, section, "BanDialog", "58");
		intValue = std::stoi(stringValue);
		if (intValue < 0)
			intValue = 0;
		vars.dialogIdBan = intValue;

		stringValue = GetConfigString(filePath, section, "AdminOnline", "0");
		intValue = std::stoi(stringValue);
		if (intValue < 0 || intValue > 2)
			intValue = 0;
		vars.adminOnlineAction = intValue;

		stringValue = GetConfigString(filePath, section, "AdminNear", "0");
		intValue = std::stoi(stringValue);
		if (intValue < 0 || intValue > 2)
			intValue = 0;
		vars.adminNearAction = intValue;

		stringValue = GetConfigString(filePath, section, "BusRoute", "0");
		intValue = std::stoi(stringValue);
		if (intValue < 0 || intValue > 8)
			intValue = 0;
		vars.busWorkerRoute = intValue;

		stringValue = GetConfigString(filePath, section, "AntiAfkDelay", "1");
		if (intValue < 1)
			intValue = 1;
		vars.antiAfkDelay = intValue * 1000;

		stringValue = GetConfigString(filePath, section, "AntiAfkOffset", "0.001");
		vars.antiAfkOffset = std::stof(stringValue);
		if (vars.antiAfkOffset < 0.001f)
			vars.antiAfkOffset = 0.001f;
	} else {
		section = "Account";
		SetConfigString(filePath, section, "Server", "127.0.0.1:7777");
		SetConfigString(filePath, section, "NickName", "MishaN");
		SetConfigString(filePath, section, "Password", "qwerty");

		section = "AutoReg";
		SetConfigString(filePath, section, "Enabled", "1");
		SetConfigString(filePath, section, "Mail", "mail@mail.ru");
		SetConfigString(filePath, section, "NickName", "MishaN");
		SetConfigString(filePath, section, "Sex", "1");

		section = "CoordMaster";
		SetConfigString(filePath, section, "Distance", "80.0");
		SetConfigString(filePath, section, "Height", "-40.0");
		SetConfigString(filePath, section, "Delay", "1500");

		section = "Loader";
		SetConfigString(filePath, section, "Delay", "10000");
		SetConfigString(filePath, section, "Limit", "20");
		SetConfigString(filePath, section, "Enabled", "0");

		section = "Settings";
		SetConfigString(filePath, section, "KickReconnect", "15");
		SetConfigString(filePath, section, "AdminReconnect", "300");
		SetConfigString(filePath, section, "PasswordDialog", "1");
		SetConfigString(filePath, section, "BanDialog", "58");
		SetConfigString(filePath, section, "AdminOnline", "0");
		SetConfigString(filePath, section, "AdminNear", "0");
		SetConfigString(filePath, section, "BusRoute", "0");
		SetConfigString(filePath, section, "AntiAfkDelay", "1");
		SetConfigString(filePath, section, "AntiAfkOffset", "0.001");

		std::string message = "Файл настроек был создан, так как отсутствовал!\nПуть: " + filePath + "\nПерезапустите приложение";
		MessageBox(NULL, message.c_str(), "Предупреждение", MB_ICONASTERISK);
		result = false;
	}

	if (vars.busWorkerRoute > 0 && vars.busWorkerRoute < 9)
		vars.checkPointMaster = 1;

	vars.noAfk = true;
	vars.timeStamp = true;
	vars.logFile = nullptr;

	ZeroMemory(Objects, sizeof(GTAObject) * MAX_OBJECTS);
	ZeroMemory(&checkpoint, sizeof(Checkpoint));
	ZeroMemory(&raceCheckpoint, sizeof(RaceCheckpoint));
	spawnInfoExists = false;
	ZeroMemory(&spawnInfo, sizeof(SpawnInfo));
	ZeroMemory(&gtaMenu, sizeof(GTAMenu));

	vars.botConnectedTimer.setTimer(UINT32_MAX);
	vars.botSpawnedTimer.setTimer(UINT32_MAX);
	vars.gameInitedTimer.setTimer(UINT32_MAX);
	vars.reconnectTimer.setTimer(0);

	return result;
}

void SaveConfig(const std::string &filePath) {
	Settings *settings = RakBot::app()->getSettings();

	std::stringstream serverFullAddress;
	serverFullAddress << settings->getAddress()->getIp() << ":" << settings->getAddress()->getPort();

	std::string section;

	section = "Account";
	SetConfigString(filePath, section, "Server", serverFullAddress.str());
	SetConfigString(filePath, section, "NickName", settings->getName());
	SetConfigString(filePath, section, "Password", settings->getLoginPassword());

	section = "AutoReg";
	SetConfigString(filePath, section, "Enabled", std::to_string(vars.autoRegEnabled));
	SetConfigString(filePath, section, "Mail", vars.autoRegMail);
	SetConfigString(filePath, section, "NickName", vars.autoRegReferer);
	SetConfigString(filePath, section, "Sex", std::to_string(vars.autoRegSex));

	section = "CoordMaster";
	SetConfigString(filePath, section, "Distance", std::to_string(vars.coordMasterDist));
	SetConfigString(filePath, section, "Height", std::to_string(vars.coordMasterHeight));
	SetConfigString(filePath, section, "Delay", std::to_string(vars.coordMasterDelay));

	section = "Loader";
	SetConfigString(filePath, section, "Enabled", std::to_string(vars.botLoaderEnabled));
	SetConfigString(filePath, section, "Delay", std::to_string(vars.botLoaderDelay));
	SetConfigString(filePath, section, "Limit", std::to_string(vars.botLoaderLimit));

	section = "Settings";
	SetConfigString(filePath, section, "KickReconnect", std::to_string(vars.reconnectDelay));
	SetConfigString(filePath, section, "AdminReconnect", std::to_string(vars.adminReconnectDelay));
	SetConfigString(filePath, section, "PasswordDialog", std::to_string(vars.dialogIdPassword));
	SetConfigString(filePath, section, "BanDialog", std::to_string(vars.dialogIdBan));
	SetConfigString(filePath, section, "AdminOnline", std::to_string(vars.adminOnlineAction));
	SetConfigString(filePath, section, "AdminNear", std::to_string(vars.adminNearAction));
	SetConfigString(filePath, section, "BusRoute", std::to_string(vars.busWorkerRoute));
	SetConfigString(filePath, section, "AntiAfkDelay", std::to_string(vars.antiAfkDelay));
	SetConfigString(filePath, section, "AntiAfkOffset", std::to_string(vars.antiAfkOffset));
}