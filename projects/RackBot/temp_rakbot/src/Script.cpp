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
#include "Server.h"
#include "Pickup.h"
#include "Vehicle.h"
#include "Events.h"

#include "MiscFuncs.h"

#include "main.h"
#include "cmds.h"
#include "keycheck.h"
#include "netgame.h"
#include "netrpc.h"
#include "window.h"

#include "Script.h"

std::vector<Script *> scripts;

void LuaPanic(sol::optional<std::string> maybe_msg) {
	RakBot::app()->log("[ERROR] Ошибка Lua!");
	if (maybe_msg) {
		const std::string& msg = maybe_msg.value();
		std::vector<std::string> lines = Split(msg, '\n');
		for each (std::string line in lines) {
			RakBot::app()->log("[ERROR] %s", line.c_str());
		}
	}
}

Script::Script(std::string scriptName) : _scriptName(scriptName) {
	try {
		_funcExecuting = false;
		_scriptClosing = false;

		for (int i = 0; i < LUA_MAXDEFCALLS; i++)
			_defCalls[i].active = false;

		std::string scriptsDir = GetRakBotPath("scripts");
		std::string scriptPath = scriptsDir + "\\" + _scriptName;

		// LOAD FILE
		std::ifstream scriptFile(scriptPath);
		if (!scriptFile.is_open()) {
			std::string s = "[ERROR] Ошибка загрузки скрипта \"" + _scriptName + "\": файл не найден";
			RakBot::app()->log(s.c_str());
			return;
		}
		scriptFile.close();

		// LOAD LUA LIBRARIES
		_scriptState.open_libraries();
		_scriptState.set_panic(sol::c_call<decltype(&LuaPanic), &LuaPanic>);

		_scriptState["package"]["path"] = scriptsDir + "\\libs\\?.lua;" + scriptsDir + "\\libs\\?\\init.lua;";
		_scriptState["package"]["cpath"] = scriptsDir + "\\libs\\?.dll;" + scriptsDir + "\\libs\\loadall.dll";

		// REGISTER LUA FUNCTIONS
		luaRegisterFunctions();

		// LOAD AND EXECUTE SCRIPT
		sol::load_result script = _scriptState.load_file(scriptPath);
		if (!script.valid())
			throw script.get<sol::error>();

		sol::protected_function_result result = script.get<sol::protected_function>()();
		if (!result.valid())
			throw result.get<sol::error>();

		std::string s = "[LUA] Скрипт \"" + _scriptName + "\" успешно загружен";
		RakBot::app()->log(s.c_str());
	} catch (const char *e) {
		std::string message = "Ошибка загрузки скрипта \"" + _scriptName + "\": " + e;
		luaError(message);
	} catch (const std::exception &e) {
		std::string message = "Ошибка загрузки скрипта \"" + _scriptName + "\": " + e.what();
		luaError(message);
	} catch (...) {
		std::string message = "Неизвестная ошибка при загрузке скрипта \"" + _scriptName + "\"";
		luaError(message);
	}

	// CALL ON_SCRIPT_START CALBACK
	luaOnScriptStart();
	_scriptThread = std::thread(&Script::luaUpdate, this);
}

Script::~Script() {
	_defCallsMutex.lock();
	for (int i = 0; i < LUA_MAXDEFCALLS; i++)
		_defCalls[i].active = false;
	_defCallsMutex.unlock();

	_scriptClosing = true;

	if (_scriptThread.joinable())
		_scriptThread.join();
}

Script *Script::load(std::string scriptName) {
	try {
		if (scriptName.empty())
			return nullptr;

		return new Script(scriptName);
	} catch (const char *e) {
		std::stringstream message;
		message << "[ERROR] Исключение при создании объекта скрипта: " << e;
		RakBot::app()->log(message.str().c_str());
		return nullptr;
	} catch (const std::exception &e) {
		std::stringstream message;
		message << "[ERROR] Исключение при создании объекта скрипта: " << e.what();
		RakBot::app()->log(message.str().c_str());
		return nullptr;
	} catch (...) {
		std::string message = "[ERROR] Необработанное исключение при создании объекта скрипта";
		RakBot::app()->log(message.c_str());
		return nullptr;
	}
}

void Script::unload(Script *script) {
	try {
		delete script;
	} catch (const char *e) {
		std::stringstream message;
		message << "[ERROR] Исключение при выгрузке скрипта: " << e;
		RakBot::app()->log(message.str().c_str());
	} catch (const std::exception &e) {
		std::stringstream message;
		message << "[ERROR] Исключение при выгрузке скрипта: " << e.what();
		RakBot::app()->log(message.str().c_str());
	} catch (...) {
		std::string message = "[ERROR] Необработанное исключение при выгрузке скрипта";
		RakBot::app()->log(message.c_str());
	}
}

// CALLBACKS

void Script::luaOnReset(uint8_t restart, uint32_t reconnectTime) {
	luaCallback("onReset", restart, reconnectTime);
}

bool Script::luaOnRecvPacket(uint8_t packetId, uint8_t *packetData, int packetSize) {
	return luaCallback("onRecvPacket", packetId, reinterpret_cast<int>(packetData), packetSize);
}

bool Script::luaOnSendPacket(uint8_t packetId, uint8_t *packetData, int packetSize) {
	return luaCallback("onSendPacket", packetId, reinterpret_cast<int>(packetData), packetSize);
}

bool Script::luaOnRecvRPC(uint8_t rpcId, uint8_t *packetData, int packetSize) {
	return luaCallback("onRecvRpc", rpcId, reinterpret_cast<int>(packetData), packetSize);
}

bool Script::luaOnSendRPC(uint8_t rpcId, uint8_t *packetData, int packetSize) {
	return luaCallback("onSendRpc", rpcId, reinterpret_cast<int>(packetData), packetSize);
}

void Script::luaOnGameText(std::string gameText) {
	luaCallback("onGameText", gameText);
}

void Script::luaOnSetSpawnPos(float positionX, float positionY, float positionZ) {
	luaCallback("onSetSpawnPos", positionX, positionY, positionZ);
}

bool Script::luaOnServerMessage(std::string message) {
	return luaCallback("onServerMessage", message);
}

bool Script::luaOnChatMessage(uint16_t playerId, std::string message) {
	return luaCallback("onChatMessage", playerId, message);
}

void Script::luaOnSetSkin(uint16_t playerid, uint16_t skinId) {
	luaCallback("onSetSkin", playerid, skinId);
}

void Script::luaOnCreateVehicle(uint16_t vehicleId) {
	luaCallback("onCreateVehicle", vehicleId);
}

void Script::luaOnDestroyVehicle(uint16_t vehicleId) {
	luaCallback("onDestroyVehicle", vehicleId);
}

void Script::luaOnSetVehicleParams(uint16_t vehicleId) {
	luaCallback("onSetVehicleParams", vehicleId);
}

void Script::luaOnPlayerAddInWorld(uint16_t playerId) {
	luaCallback("onPlayerAddInWorld", playerId);
}

void Script::luaOnPlayerRemoveFromWorld(uint16_t playerId) {
	luaCallback("onPlayerRemoveFromWorld", playerId);
}

void Script::luaOnPlayerDeath(uint16_t playerId) {
	luaCallback("onPlayerDeath", playerId);
}

void Script::luaOnTextDrawHide(uint16_t textDrawId) {
	luaCallback("onTextDrawHide", textDrawId);
}

void Script::luaOnTextDrawSetString(uint16_t textDrawId, std::string textDrawString) {
	luaCallback("onTextDrawSetString", textDrawId, textDrawString);
}

void Script::luaOnTextDrawShow(uint16_t textDrawId, float positionX, float positionY, std::string textDrawString) {
	luaCallback("onTextDrawShow", textDrawId, positionX, positionY, textDrawString);
}

void Script::luaOnToggleSpectating(bool state) {
	luaCallback("onToggleSpectating", state);
}

bool Script::luaOnPutInVehicle(uint16_t vehicleId, uint16_t seatId) {
	return luaCallback("onPlayerPutInVehicle", vehicleId, seatId);
}

bool Script::luaOnEjectFromVehicle() {
	return luaCallback("onPlayerEjectFromVehicle");
}

void Script::luaOnCreateCheckpoint() {
	luaCallback("onCreateCheckpoint");
}

void Script::luaOnDestroyCheckpoint() {
	luaCallback("onDestroyCheckpoint");
}

void Script::luaOnCreateRaceCheckpoint() {
	luaCallback("onCreateRaceCheckpoint");
}

void Script::luaOnDestroyRaceCheckpoint() {
	luaCallback("onDestroyRaceCheckpoint");
}

void Script::luaOnCreatePickup(uint16_t pickupId) {
	luaCallback("onCreatePickup", pickupId);
}

void Script::luaOnDestroyPickup(uint16_t pickupId) {
	luaCallback("onDestroyPickup", pickupId);
}

bool Script::luaOnSetInteriorId(uint8_t interiorId) {
	return luaCallback("onSetInteriorId", interiorId);
}

void Script::luaOnCreateObject(uint16_t objectId) {
	luaCallback("onCreateObject", objectId);
}

void Script::luaOnDestroyObject(uint16_t objectId) {
	luaCallback("onDestroyObject", objectId);
}

void Script::luaOnAttachObjectToPlayer(uint16_t playerId, uint32_t slotId, bool attach) {
	luaCallback("onAttachObjectToPlayer", playerId, slotId, attach);
}

bool Script::luaOnTakeCheckpoint(float positionX, float positionY, float positionZ) {
	return luaCallback("onTakeCheckpoint", positionX, positionY, positionZ);
}

bool Script::luaOnPickUpPickup(uint16_t pickupId) {
	return luaCallback("onPickUpPickup", pickupId);
}

bool Script::luaOnTextDrawClick(uint16_t textDrawId) {
	return luaCallback("onTextDrawClick", textDrawId);
}

void Script::luaOnApplyAnimation(uint16_t playerId, uint16_t animId) {
	luaCallback("onApplyAnimation", playerId, animId);
}

bool Script::luaOnDialogResponse(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput, bool isOffline) {
	return luaCallback("onDialogResponse", dialogId, dialogButton, dialogItem, dialogInput, isOffline);
}

void Script::luaOnDialogResponseSent(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput) {
	luaCallback("onDialogResponseSent", dialogId, dialogButton, dialogItem, dialogInput);
}

bool Script::luaOnSpawn() {
	return luaCallback("onSpawn");
}

bool Script::luaOnSendInput(std::string input) {
	return luaCallback("onSendInput", input);
}

bool Script::luaOnSync() {
	return luaCallback("onSync");
}

void Script::luaOnTextLabelShow(uint16_t labelId, float positionX, float positionY, float positionZ, std::string labelString) {
	luaCallback("onTextLabelShow", labelId, positionX, positionY, positionZ, labelString);
}

bool Script::luaOnTeleport(float positionX, float positionY, float positionZ) {
	return luaCallback("onTeleport", positionX, positionY, positionZ);
}

bool Script::luaOnCoordMasterStart(float targetX, float targetY, float targetZ) {
	return luaCallback("onCoordMasterStart", targetX, targetY, targetZ);
}

bool Script::luaOnCoordMasterStop() {
	return luaCallback("onCoordMasterStop");
}

void Script::luaOnCoordMasterComplete() {
	luaCallback("onCoordMasterComplete");
}

bool Script::luaOnSetHealth(uint8_t health) {
	return luaCallback("onSetHealth", health);
}

bool Script::luaOnSetArmour(uint8_t armour) {
	return luaCallback("onSetArmour", armour);
}

void Script::luaOnSetMoney(int money) {
	luaCallback("onSetMoney", money);
}

void Script::luaOnPlayerQuit(uint16_t playerId, uint8_t reasonId) {
	luaCallback("onPlayerQuit", playerId, reasonId);
}

void Script::luaOnPlayerJoin(uint16_t playerId, std::string playerName) {
	luaCallback("onPlayerJoin", playerId, playerName);
}

void Script::luaOnGameInited() {
	luaCallback("onGameInited");
}

bool Script::luaOnRequestConnect() {
	return luaCallback("onRequestConnect");
}

void Script::luaOnConnect(uint16_t playerId) {
	luaCallback("onConnect", playerId);
}

void Script::luaOnDisconnect(uint8_t reason) {
	luaCallback("onDisconnect", reason);
}

void Script::luaOnReconnect(int delay) {
	luaCallback("onReconnect", delay);
}

bool Script::luaOnSetPosition(float positionX, float positionY, float positionZ) {
	return luaCallback("onSetPosition", positionX, positionY, positionZ);
}

void Script::luaOnSpawned(float positionX, float positionY, float positionZ) {
	luaCallback("onSpawned", positionX, positionY, positionZ);
}

bool Script::luaOnDialogShow(uint16_t dialogId, uint8_t dialogStyle, std::string dialogTitle, std::string okButtonText, std::string cancelButtonText, std::string dialogText) {
	return luaCallback("onDialogShow", dialogId, dialogStyle, dialogTitle, okButtonText, cancelButtonText, dialogText);
}

bool Script::luaOnPrintLog(std::string msg) {
	return luaCallback("onPrintLog", msg);
}

bool Script::luaOnRunCommand(std::string cmd) {
	return luaCallback("onRunCommand", cmd);
}

void Script::luaOnScriptStart() {
	luaCallback("onScriptStart");
}

void Script::luaOnScriptExit() {
	luaCallback("onScriptExit");
}

void Script::luaOnScriptUpdate() {
	luaCallback("onScriptUpdate");
}

void Script::luaOnCrash() {
	luaCallback("onCrash");
}

void Script::luaOnEnterVehicle(uint16_t playerId, uint16_t vehicleId, uint8_t seatId) {
	luaCallback("onEnterVehicle", playerId, vehicleId, seatId);
}

void Script::luaRegisterFunctions() {
	_scriptState.set_function("isBotConnected", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->isConnected();
	});

	_scriptState.set_function("isBotSpawned", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->isSpawned();
	});

	_scriptState.set_function("isGameInited", [this]() {
		Server *server = RakBot::app()->getServer();
		return server->isGameInited();
	});

	_scriptState.set_function("isConnectRequested", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->isConnectRequested();
	});

	_scriptState.set_function("connect", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->connect(
			RakBot::app()->getSettings()->getAddress()->getIp(),
			RakBot::app()->getSettings()->getAddress()->getPort()
		);
	});

	_scriptState.set_function("disconnect", [this](bool timeOut) {
		Bot *bot = RakBot::app()->getBot();
		return bot->disconnect(timeOut);
	});

	_scriptState.set_function("reset", [this](bool reconnect) {
		Bot *bot = RakBot::app()->getBot();
		return bot->reset(reconnect);
	});

	_scriptState.set_function("reconnect", [this](int reconnectDelay) {
		Bot *bot = RakBot::app()->getBot();
		return bot->reconnect(reconnectDelay);
	});

	_scriptState.set_function("getMoney", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getMoney();
	});

	_scriptState.set_function("enterVehicle", [this](int vehicleId, int seatId) {
		Bot *bot = RakBot::app()->getBot();
		Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
		return bot->enterVehicle(vehicle, seatId);
	});

	_scriptState.set_function("exitVehicle", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->exitVehicle();
	});

	_scriptState.set_function("sendSync", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->sync();
	});

	_scriptState.set_function("sendInput", [this](std::string input) {
		Bot *bot = RakBot::app()->getBot();
		return bot->sendInput(input);
	});

	_scriptState.set_function("requestClass", [this](int classId) {
		Bot *bot = RakBot::app()->getBot();
		return bot->requestClass(classId);
	});

	_scriptState.set_function("requestSpawn", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->requestSpawn();
	});

	_scriptState.set_function("sendPickup", [this](int pickupId, bool checkDist) {
		Bot *bot = RakBot::app()->getBot();
		Pickup *pickup = RakBot::app()->getPickup(pickupId);
		return bot->pickUpPickup(pickup, checkDist);
	});

	_scriptState.set_function("sendDialog", [this](int dialogId, int button, int item, std::string input) {
		Bot *bot = RakBot::app()->getBot();
		return bot->dialogResponse(dialogId, button, item, input);
	});

	_scriptState.set_function("sendSpawn", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->spawn();
	});

	_scriptState.set_function("getHealth", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getHealth();
	});

	_scriptState.set_function("setHealth", [this](int health) {
		Bot *bot = RakBot::app()->getBot();
		return bot->setHealth(health);
	});

	_scriptState.set_function("getArmour", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getArmour();
	});

	_scriptState.set_function("setArmour", [this](int armour) {
		Bot *bot = RakBot::app()->getBot();
		return bot->setArmour(armour);
	});

	_scriptState.set_function("getWeapon", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getWeapon();
	});

	_scriptState.set_function("setWeapon", [this](int weapon) {
		Bot *bot = RakBot::app()->getBot();
		return bot->setWeapon(weapon);
	});

	_scriptState.set_function("getBotId", [this]() {
		Bot *bot = RakBot::app()->getBot();
		uint16_t playerId = bot->getPlayerId();
		if (playerId == PLAYER_ID_NONE)
			return sol::make_object(_scriptState, sol::nil);
		return sol::make_object(_scriptState, playerId);
	});

	_scriptState.set_function("getSkin", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getSkin();
	});

	_scriptState.set_function("getBotState", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getPlayerState();
	});

	_scriptState.set_function("getPosition", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return std::make_tuple(bot->getPosition(0), bot->getPosition(1), bot->getPosition(2));
	});

	_scriptState.set_function("setPosition", [this](float x, float y, float z) {
		Bot *bot = RakBot::app()->getBot();
		bot->setPosition(0, x);
		bot->setPosition(1, y);
		bot->setPosition(2, z);
		return true;
	});

	_scriptState.set_function("getSpeed", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return std::make_tuple(bot->getSpeed(0), bot->getSpeed(1), bot->getSpeed(2));
	});

	_scriptState.set_function("setSpeed", [this](float x, float y, float z) {
		Bot *bot = RakBot::app()->getBot();
		bot->setSpeed(0, x);
		bot->setSpeed(1, y);
		bot->setSpeed(2, z);
		return true;
	});

	_scriptState.set_function("getQuaternion", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return std::make_tuple(bot->getQuaternion(0), bot->getQuaternion(1), bot->getQuaternion(2), bot->getQuaternion(3));
	});

	_scriptState.set_function("setQuaternion", [this](float w, float x, float y, float z) {
		Bot *bot = RakBot::app()->getBot();
		bot->setQuaternion(0, w);
		bot->setQuaternion(1, x);
		bot->setQuaternion(2, y);
		bot->setQuaternion(3, z);
		return true;
	});

	_scriptState.set_function("getBotVehicle", [this]() {
		Bot *bot = RakBot::app()->getBot();
		Vehicle *vehicle = bot->getVehicle();
		if (vehicle == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		return sol::make_object(_scriptState, vehicle->getVehicleId());
	});

	_scriptState.set_function("getAnimation", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return std::make_tuple(bot->getAnimation()->getAnimId(), bot->getAnimation()->getAnimFlags());
	});

	_scriptState.set_function("getInteriorId", [this]() {
		return vars.interiorId;
	});

	_scriptState.set_function("setAnimation", [this](int animId, int animFlags) {
		Bot *bot = RakBot::app()->getBot();
		bot->getAnimation()->setAnimId(animId);
		bot->getAnimation()->setAnimFlags(animFlags);
		return true;
	});

	_scriptState.set_function("getKeys", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return std::make_tuple(bot->getKeys()->getKeyId(), bot->getKeys()->getLeftRightKey(), bot->getKeys()->getUpDownKey());
	});

	_scriptState.set_function("setKeys", [this](int keys, int lrAnalog, int udAnalog) {
		Bot *bot = RakBot::app()->getBot();
		bot->getKeys()->setKeyId(keys);
		bot->getKeys()->setLeftRightKey(lrAnalog);
		bot->getKeys()->setUpDownKey(udAnalog);
		return true;
	});

	_scriptState.set_function("getScore", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getInfo()->getScore();
	});

	_scriptState.set_function("getPing", [this]() {
		Bot *bot = RakBot::app()->getBot();
		return bot->getInfo()->getPing();
	});

	_scriptState.set_function("clickTextDraw", [this](int textdrawId) {
		Bot *bot = RakBot::app()->getBot();
		bot->clickTextdraw(textdrawId);
		return true;
	});

	_scriptState.set_function("teleport", [this](float x, float y, float z) {
		Bot *bot = RakBot::app()->getBot();
		bot->setPosition(0, x);
		bot->setPosition(1, y);
		bot->setPosition(2, z);
		bot->sync();
		return true;
	});

	_scriptState.set_function("takeCheckpoint", [this]() {
		Bot *bot = RakBot::app()->getBot();
		bot->takeCheckpoint();
		return true;
	});

	_scriptState.set_function("coordMasterState", [this]() {
		return vars.coordMasterEnabled;
	});

	_scriptState.set_function("coordMasterStart", [this](float x, float y, float z) {
		Bot *bot = RakBot::app()->getBot();
		DoCoordMaster(true, x, y, z);
		return true;
	});

	_scriptState.set_function("coordMasterStop", [this]() {
		Bot *bot = RakBot::app()->getBot();
		DoCoordMaster(false);
		return true;
	});

	// RAKNET
	_scriptState.set_function("sendPacket", [this](int bsPtr) {
		BitStream *bsData = reinterpret_cast<BitStream *>(bsPtr);
		if (bsData == nullptr)
			return;

		RakBot::app()->getRakClient()->Send(bsData, HIGH_PRIORITY, UNRELIABLE_SEQUENCED, 0);
	});

	_scriptState.set_function("sendRpc", [this](int rpcId, int bsPtr) {
		if (rpcId < 0 || rpcId > 255)
			return;

		BitStream *bsData = reinterpret_cast<BitStream *>(bsPtr);
		if (bsData == nullptr)
			return;

		RakBot::app()->getRakClient()->RPC(&rpcId, bsData, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);
	});

	_scriptState.set_function("bitStreamNew", [this]() {
		BitStream *bitStream = new BitStream();
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		return sol::make_object(_scriptState, reinterpret_cast<int>(bitStream));
	});

	_scriptState.set_function("bitStreamInit", [this](int dataPtr, int dataSize) {
		BitStream *bitStream = new BitStream(reinterpret_cast<uint8_t *>(dataPtr), dataSize, false);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		return sol::make_object(_scriptState, reinterpret_cast<int>(bitStream));
	});

	_scriptState.set_function("bitStreamDelete", [this](int bsPtr) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		delete bitStream;
		return true;
	});

	_scriptState.set_function("bitStreamData", [this](int bsPtr) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		return sol::make_object(_scriptState, reinterpret_cast<int>(bitStream->GetData()));
	});

	_scriptState.set_function("bitStreamSize", [this](int bsPtr) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return 0;
		return bitStream->GetNumberOfBytesUsed();
	});

	_scriptState.set_function("bitStreamIgnoreBytes", [this](int bsPtr, int amount) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		bitStream->IgnoreBits(BYTES_TO_BITS(amount));
		return true;
	});

	_scriptState.set_function("bitStreamIgnoreBits", [this](int bsPtr, int amount) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		bitStream->IgnoreBits(amount);
		return true;
	});

	_scriptState.set_function("bitStreamReset", [this](int bsPtr) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		bitStream->Reset();
		return true;
	});

	_scriptState.set_function("bitStreamSetWriteOffset", [this](int bsPtr, int offset) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		bitStream->SetWriteOffset(BYTES_TO_BITS(offset));
		return true;
	});

	_scriptState.set_function("bitStreamSetReadOffset", [this](int bsPtr, int offset) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		bitStream->SetReadOffset(BYTES_TO_BITS(offset));
		return true;
	});

	_scriptState.set_function("bitStreamReadBool", [this](int bsPtr, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		bool value;
		if (compressed)
			bitStream->ReadCompressed(value);
		else
			bitStream->Read(value);
		return sol::make_object(_scriptState, value);
	});

	_scriptState.set_function("bitStreamReadByte", [this](int bsPtr, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		uint8_t value;
		if (compressed)
			bitStream->ReadCompressed(value);
		else
			bitStream->Read(value);
		return sol::make_object(_scriptState, static_cast<int>(value));
	});

	_scriptState.set_function("bitStreamReadWord", [this](int bsPtr, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		uint16_t value;
		if (compressed)
			bitStream->ReadCompressed(value);
		else
			bitStream->Read(value);
		return sol::make_object(_scriptState, static_cast<int>(value));
	});

	_scriptState.set_function("bitStreamReadDWord", [this](int bsPtr, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		uint32_t value;
		if (compressed)
			bitStream->ReadCompressed(value);
		else
			bitStream->Read(value);
		return sol::make_object(_scriptState, static_cast<int>(value));
	});

	_scriptState.set_function("bitStreamReadFloat", [this](int bsPtr, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		float value;
		if (compressed)
			bitStream->ReadCompressed(value);
		else
			bitStream->Read(value);
		return sol::make_object(_scriptState, value);
	});

	_scriptState.set_function("bitStreamReadString", [this](int bsPtr, int strSize, sol::optional<bool> encode) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr || strSize < 1)
			return sol::make_object(_scriptState, sol::nil);
		char *strBuf = new char[strSize + 1];
		if (encode)
			stringCompressor->DecodeString(strBuf, strSize, bitStream);
		else
			bitStream->Read(strBuf, strSize);
		strBuf[strSize] = 0;
		return sol::make_object(_scriptState, strBuf);
	});

	_scriptState.set_function("bitStreamWriteBool", [this](int bsPtr, bool val, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		bool value = val;
		if (compressed)
			bitStream->WriteCompressed(value);
		else
			bitStream->Write(value);
		return true;
	});

	_scriptState.set_function("bitStreamWriteByte", [this](int bsPtr, int val, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		uint8_t value = static_cast<uint8_t>(val);
		if (compressed)
			bitStream->WriteCompressed(value);
		else
			bitStream->Write(value);
		return true;
	});

	_scriptState.set_function("bitStreamWriteWord", [this](int bsPtr, int val, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		uint16_t value = static_cast<uint16_t>(val);
		if (compressed)
			bitStream->WriteCompressed(value);
		else
			bitStream->Write(value);
		return true;
	});

	_scriptState.set_function("bitStreamWriteDWord", [this](int bsPtr, int val, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		uint32_t value = static_cast<uint32_t>(val);
		if (compressed)
			bitStream->WriteCompressed(value);
		else
			bitStream->Write(value);
		return true;
	});

	_scriptState.set_function("bitStreamWriteFloat", [this](int bsPtr, float val, sol::optional<bool> compressed) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		float value = val;
		if (compressed)
			bitStream->WriteCompressed(value);
		else
			bitStream->Write(value);
		return true;
	});

	_scriptState.set_function("bitStreamWriteString", [this](int bsPtr, std::string str, int strSize, sol::optional<bool> encode) {
		BitStream *bitStream = reinterpret_cast<BitStream *>(bsPtr);
		if (bitStream == nullptr)
			return false;
		if (encode)
			stringCompressor->EncodeString(str.c_str(), strSize, bitStream);
		else
			bitStream->Write(str.c_str(), strSize);
		return true;
	});

	// MISC
	_scriptState.set_function("getScriptPath", [this]() {
		std::string scriptPath = GetRakBotPath("scripts") + "\\" + _scriptName;
		return scriptPath;
	});

	_scriptState.set_function("getScriptsDir", [this]() {
		std::string scriptsDir = GetRakBotPath("scripts");
		return scriptsDir;
	});

	_scriptState.set_function("getLicenseKey", [this]() {
		return vars.regKey;
	});

	_scriptState.set_function("defCallAdd", [this](int delay, bool repeat, sol::protected_function func, sol::optional<sol::table> maybe_params) {
		if (delay < 1)
			return sol::make_object(_scriptState, sol::nil);
		if (!func.valid())
			return sol::make_object(_scriptState, sol::nil);

		_defCallsMutex.lock();
		int defCallIndex = -1;
		for (int i = 0; i < LUA_MAXDEFCALLS; i++) {
			if (!_defCalls[i].active) {
				defCallIndex = i;
				break;
			}
		}

		if (defCallIndex == -1)
			return sol::make_object(_scriptState, sol::nil);

		_defCalls[defCallIndex].active = true;
		_defCalls[defCallIndex].startTime = GetTickCount();
		_defCalls[defCallIndex].callDelay = delay;
		_defCalls[defCallIndex].repeat = repeat;
		_defCalls[defCallIndex].func = func;

		if (maybe_params) {
			_defCalls[defCallIndex].params = maybe_params.value();
		} else {
			_defCalls[defCallIndex].params = _scriptState.create_table();
		}
		_defCallsMutex.unlock();

		return sol::make_object(_scriptState, (defCallIndex + 1));
	});

	_scriptState.set_function("defCallDelete", [this](int defCallId) {
		if (defCallId < 1 || defCallId > LUA_MAXDEFCALLS)
			return false;
		_defCallsMutex.lock();
		_defCalls[defCallId - 1].active = false;
		_defCallsMutex.unlock();
		return false;
	});

	_scriptState.set_function("printLog", [this](std::string log) {
		std::vector<std::string> lines = Split(log, '\n');
		if (lines.size() < 1)
			return false;
		for each (std::string line in lines) {
			std::string s = "[LUA] " + line;
			RakBot::app()->log(s.c_str());
		}
		return true;
	});

	_scriptState.set_function("runCommand", [this](std::string cmd) {
		std::vector<std::string> lines = Split(cmd, '|');
		if (lines.size() < 1)
			return false;
		for each (std::string line in lines) {
			RunCommand(line.c_str());
		}
		return true;
	});

	_scriptState.set_function("exit", [this]() {
		RakBot::app()->exit();
		return true;
	});

	_scriptState.set_function("randomString", [this](int len, bool numbers) {
		char *buf = new char[len + 1];
		GenRandomString(buf, len, numbers);
		buf[len] = 0;
		std::string s = buf;
		delete[] buf;
		return s;
	});

	_scriptState.set_function("messageBox", [this](std::string message) {
		std::thread msgBoxThread([message] {
			MessageBox(NULL, message.c_str(), "Сообщение Lua!", MB_ICONASTERISK);
		});
		msgBoxThread.detach();
		return true;
	});

	_scriptState.set_function("dumpMem", [this](int address, int size) {
		return DumpMem(reinterpret_cast<uint8_t *>(address), size);
	});

	_scriptState.set_function("openUrl", [this](std::string url) {
		char safeUrlBuf[1024];
		DWORD safeUrlLength = sizeof(safeUrlBuf);
		InternetCanonicalizeUrl(url.c_str(), safeUrlBuf, &safeUrlLength, NULL);
		std::string safeUrl = safeUrlBuf;
		CURLcode code = OpenURL(safeUrl);
		return std::make_tuple(CurlBuffer, static_cast<int>(code));
	});

	_scriptState.set_function("downloadFile", [this](std::string url, std::string file) {
		return static_cast<int>(URLDownloadToFile(NULL, url.c_str(), file.c_str(), NULL, NULL));
	});

	_scriptState.set_function("getRakBotPath", [this](sol::optional<std::string> maybe_path) {
		if (maybe_path) {
			std::string &path = maybe_path.value();
			return GetRakBotPath(path);
		}
		return GetRakBotPath();
	});

	_scriptState.set_function("getIniString", [this](std::string file, std::string section, std::string key, sol::optional<std::string> maybe_default) {
		char buf[256];
		GetPrivateProfileString(section.c_str(), key.c_str(), "nil", buf, sizeof(buf), file.c_str());
		std::string result = buf;
		if (result == "nil")
			return sol::make_object(_scriptState, sol::nil);
		return sol::make_object(_scriptState, result);
	});

	_scriptState.set_function("setIniString", [this](std::string file, std::string section, std::string key, std::string value) {
		return WritePrivateProfileString(section.c_str(), key.c_str(), value.c_str(), file.c_str());
	});

	// TEXTDRAW
	_scriptState.set_function("getTextDraw", [this](int textDrawId) {
		TextDraw *textDraw = RakBot::app()->getTextDraw(textDrawId);
		if (textDraw == nullptr)
			return sol::make_object(_scriptState, sol::nil);

		if (!textDraw->isActive())
			return sol::make_object(_scriptState, sol::nil);

		sol::table textDrawInfo = _scriptState.create_table();
		textDrawInfo["id"] = textDraw->getTextDrawId();
		textDrawInfo["model"] = textDraw->getModelId();
		textDrawInfo["flags"] = textDraw->getFlags();
		textDrawInfo["style"] = textDraw->getStyle();

		textDrawInfo["shadow"] = textDraw->isHasShadow();
		textDrawInfo["outline"] = textDraw->isHasOutline();
		textDrawInfo["selectable"] = textDraw->isSelectable();

		textDrawInfo["letterColor"] = textDraw->getLetterColor();
		textDrawInfo["boxColor"] = textDraw->getBoxColor();
		textDrawInfo["backgroundColor"] = textDraw->getBackgroundColor();
		textDrawInfo["color"] = textDraw->getColor();

		textDrawInfo["zoom"] = textDraw->getZoom();

		textDrawInfo["lineSize"] = _scriptState.create_table();
		textDrawInfo["lineSize"]["width"] = textDraw->getLineSize(0);
		textDrawInfo["lineSize"]["height"] = textDraw->getLineSize(1);

		textDrawInfo["letterSize"] = _scriptState.create_table();
		textDrawInfo["letterSize"]["width"] = textDraw->getLetterSize(0);
		textDrawInfo["letterSize"]["height"] = textDraw->getLetterSize(1);

		textDrawInfo["rotation"] = _scriptState.create_table();
		textDrawInfo["rotation"]["x"] = textDraw->getRotation(0);
		textDrawInfo["rotation"]["y"] = textDraw->getRotation(1);
		textDrawInfo["rotation"]["z"] = textDraw->getRotation(2);

		textDrawInfo["position"] = _scriptState.create_table();
		textDrawInfo["position"]["x"] = textDraw->getPosition(0);
		textDrawInfo["position"]["y"] = textDraw->getPosition(1);

		textDrawInfo["string"] = textDraw->getString();

		return sol::make_object(_scriptState, textDrawInfo);
	});

	// CHECKPOINT
	_scriptState.set_function("getCheckpoint", [this]() {
		sol::table cpInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		if (!checkpoint.active)
			return sol::make_object(_scriptState, sol::nil);
		cpInfo["size"] = checkpoint.size;
		cpInfo["distance"] = bot->distanceTo(checkpoint.position);
		cpInfo["position"] = _scriptState.create_table();
		cpInfo["position"]["x"] = checkpoint.position[0];
		cpInfo["position"]["y"] = checkpoint.position[1];
		cpInfo["position"]["z"] = checkpoint.position[2];
		return sol::make_object(_scriptState, cpInfo);
	});

	// CHECKPOINT
	_scriptState.set_function("getRaceCheckpoint", [this]() {
		sol::table cpInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		if (!raceCheckpoint.active)
			return sol::make_object(_scriptState, sol::nil);

		cpInfo["size"] = raceCheckpoint.size;
		cpInfo["type"] = raceCheckpoint.type;
		cpInfo["distance"] = bot->distanceTo(raceCheckpoint.position);
		cpInfo["position"] = _scriptState.create_table();
		cpInfo["position"]["x"] = raceCheckpoint.position[0];
		cpInfo["position"]["y"] = raceCheckpoint.position[1];
		cpInfo["position"]["z"] = raceCheckpoint.position[2];
		cpInfo["nextPosition"] = _scriptState.create_table();
		cpInfo["nextPosition"]["x"] = raceCheckpoint.fNextPos[0];
		cpInfo["nextPosition"]["y"] = raceCheckpoint.fNextPos[1];
		cpInfo["nextPosition"]["z"] = raceCheckpoint.fNextPos[2];
		return sol::make_object(_scriptState, cpInfo);
	});

	// PICKUPS
	_scriptState.set_function("getPickup", [this](int pickupId) {
		sol::table pickupInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		Pickup *pickup = RakBot::app()->getPickup(pickupId);
		if (pickup == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		pickupInfo["id"] = pickup->getPickupId();
		pickupInfo["model"] = pickup->getModel();
		pickupInfo["type"] = pickup->getType();
		pickupInfo["distance"] = bot->distanceTo(pickup);
		pickupInfo["position"] = _scriptState.create_table();
		pickupInfo["position"]["x"] = pickup->getPosition(0);
		pickupInfo["position"]["y"] = pickup->getPosition(1);
		pickupInfo["position"]["z"] = pickup->getPosition(2);
		return sol::make_object(_scriptState, pickupInfo);
	});

	// VEHICLES
	_scriptState.set_function("getVehicle", [this](int vehicleId) {
		sol::table vehicleInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
		if (vehicle == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		vehicleInfo["id"] = vehicleId;
		vehicleInfo["model"] = vehicle->getModel();
		vehicleInfo["name"] = vehicle->getName();
		vehicleInfo["class"] = vehicle->getVehicleClass();
		vehicleInfo["health"] = vehicle->getCarHealth();
		vehicleInfo["firstColor"] = vehicle->getFirstColor();
		vehicleInfo["secondColor"] = vehicle->getSecondColor();
		vehicleInfo["lights"] = vehicle->isLightsEnabled();
		vehicleInfo["engine"] = vehicle->isEngineEnabled();
		vehicleInfo["siren"] = vehicle->isSirenEnabled();
		vehicleInfo["seatsAmount"] = vehicle->getSeatsAmount();
		vehicleInfo["gearState"] = vehicle->getGearState();
		vehicleInfo["distance"] = bot->distanceTo(vehicle);
		vehicleInfo["position"] = _scriptState.create_table();
		vehicleInfo["position"]["x"] = vehicle->getPosition(0);
		vehicleInfo["position"]["y"] = vehicle->getPosition(1);
		vehicleInfo["position"]["z"] = vehicle->getPosition(2);
		vehicleInfo["speed"] = _scriptState.create_table();
		vehicleInfo["speed"]["x"] = vehicle->getSpeed(0);
		vehicleInfo["speed"]["y"] = vehicle->getSpeed(1);
		vehicleInfo["speed"]["z"] = vehicle->getSpeed(2);
		vehicleInfo["quaternion"] = _scriptState.create_table();
		vehicleInfo["quaternion"]["w"] = vehicle->getQuaternion(0);
		vehicleInfo["quaternion"]["x"] = vehicle->getQuaternion(1);
		vehicleInfo["quaternion"]["y"] = vehicle->getQuaternion(2);
		vehicleInfo["quaternion"]["z"] = vehicle->getQuaternion(3);
		sol::table passengersTable = _scriptState.create_table();
		for (int i = 0; i < vehicle->getSeatsAmount(); i++) {
			Player *player = vehicle->getPassenger(i);
			if (player == nullptr)
				continue;
			passengersTable[i] = player->getPlayerId();
		}
		vehicleInfo["passengers"] = passengersTable;
		vehicleInfo["trailerId"] = vehicle->getTrailerId();
		vehicleInfo["trainSpeed"] = vehicle->getTrainSpeed();
		return sol::make_object(_scriptState, vehicleInfo);
	});

	_scriptState.set_function("getDialog", [this]() {
		sol::table dialogInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		SAMPDialog *sampDialog = RakBot::app()->getSampDialog();
		dialogInfo["id"] = sampDialog->getDialogId();
		dialogInfo["style"] = sampDialog->getDialogStyle();
		dialogInfo["isActive"] = sampDialog->isDialogActive();
		dialogInfo["isOffline"] = sampDialog->isDialogOffline();
		dialogInfo["title"] = sampDialog->getDialogTitle();
		dialogInfo["okButtonText"] = sampDialog->getOkButtonText();
		dialogInfo["cancelButtonText"] = sampDialog->getCancelButtonText();
		dialogInfo["text"] = sampDialog->getDialogText();
		return sol::make_object(_scriptState, dialogInfo);
	});

	// OBJECTS
	_scriptState.set_function("getObject", [this](int objectId) {
		sol::table objectInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		GTAObject object = Objects[objectId];
		if (!object.active)
			return sol::make_object(_scriptState, sol::nil);
		objectInfo["id"] = objectId;
		objectInfo["model"] = object.ulModelId;
		objectInfo["objectId"] = object.usObjectId;
		objectInfo["drawDistance"] = object.fDrawDistance;
		objectInfo["distance"] = bot->distanceTo(object.position);
		objectInfo["rotation"] = _scriptState.create_table();
		objectInfo["rotation"]["x"] = object.fRotation[0];
		objectInfo["rotation"]["y"] = object.fRotation[1];
		objectInfo["rotation"]["z"] = object.fRotation[2];
		objectInfo["position"] = _scriptState.create_table();
		objectInfo["position"]["x"] = object.position[0];
		objectInfo["position"]["y"] = object.position[1];
		objectInfo["position"]["z"] = object.position[2];
		return sol::make_object(_scriptState, objectInfo);
	});

	// PLAYERS
	_scriptState.set_function("getPlayer", [this](int playerId) {
		sol::table playerInfo = _scriptState.create_table();
		Bot *bot = RakBot::app()->getBot();
		Player *player = RakBot::app()->getPlayer(playerId);
		if (player == nullptr)
			return sol::make_object(_scriptState, sol::nil);
		playerInfo["id"] = player->getPlayerId();
		playerInfo["state"] = player->getPlayerState();
		playerInfo["health"] = player->getHealth();
		playerInfo["isAdmin"] = player->isAdmin();
		playerInfo["inStream"] = player->isInStream();
		playerInfo["inCar"] = ((player->getPlayerState() == PLAYER_STATE_DRIVER) || (player->getPlayerState() == PLAYER_STATE_PASSENGER));
		playerInfo["armour"] = player->getArmour();
		playerInfo["weapon"] = player->getWeapon();
		playerInfo["name"] = player->getName();
		playerInfo["distance"] = bot->distanceTo(player);
		playerInfo["score"] = player->getInfo()->getScore();
		playerInfo["ping"] = player->getInfo()->getPing();
		playerInfo["keys"] = _scriptState.create_table();
		playerInfo["keys"]["keys"] = player->getKeys()->getKeyId();
		playerInfo["keys"]["lrAnalog"] = player->getKeys()->getLeftRightKey();
		playerInfo["keys"]["udAnalog"] = player->getKeys()->getUpDownKey();
		playerInfo["anim"] = _scriptState.create_table();
		playerInfo["anim"]["animId"] = player->getAnimation()->getAnimId();
		playerInfo["anim"]["animFlags"] = player->getAnimation()->getAnimFlags();
		playerInfo["position"] = _scriptState.create_table();
		playerInfo["position"]["x"] = player->getPosition(0);
		playerInfo["position"]["y"] = player->getPosition(1);
		playerInfo["position"]["z"] = player->getPosition(2);
		playerInfo["speed"] = _scriptState.create_table();
		playerInfo["speed"]["x"] = player->getSpeed(0);
		playerInfo["speed"]["y"] = player->getSpeed(1);
		playerInfo["speed"]["z"] = player->getSpeed(2);
		playerInfo["quaternion"] = _scriptState.create_table();
		playerInfo["quaternion"]["w"] = player->getQuaternion(0);
		playerInfo["quaternion"]["x"] = player->getQuaternion(1);
		playerInfo["quaternion"]["y"] = player->getQuaternion(2);
		playerInfo["quaternion"]["z"] = player->getQuaternion(3);
		Vehicle *vehicle = player->getVehicle();
		if (vehicle != nullptr) {
			playerInfo["vehicleId"] = vehicle->getVehicleId();
			playerInfo["vehicleSeat"] = player->getVehicleSeat();
		}
		return sol::make_object(_scriptState, playerInfo);
	});

	_scriptState.set_function("getPlayersCount", [this]() {
		return RakBot::app()->getPlayersCount();
	});

	// SERVER
	_scriptState.set_function("getServerName", [this]() {
		Server *server = RakBot::app()->getServer();
		return server->getServerName();
	});

	// ADMINS
	_scriptState.set_function("adminsAdd", [this](std::string admin) {
		vars.admins.push_back(admin);
		return true;
	});

	_scriptState.set_function("adminsClear", [this]() {
		vars.admins.clear();
		return true;
	});

	// AUTO REG
	_scriptState.set_function("setOwnAutoReg", [this](bool state) {
		vars.autoRegEnabled = (state == false);
		return true;
	});

	_scriptState.set_function("setMail", [this](std::string mail) {
		vars.autoRegMail = mail;
		return true;
	});

	_scriptState.set_function("getMail", [this]() {
		return vars.autoRegMail;
	});

	_scriptState.set_function("setReconnectDelay", [this](int delay) {
		if (delay < 0)
			return false;
		vars.reconnectDelay = delay;
		return true;
	});

	_scriptState.set_function("getReconnectDelay", [this]() {
		return vars.reconnectDelay;
	});

	_scriptState.set_function("setReferer", [this](std::string referer) {
		vars.autoRegReferer = referer;
		return true;
	});

	_scriptState.set_function("getReferer", [this]() {
		return vars.autoRegReferer;
	});
	_scriptState.set_function("setSex", [this](int sex) {
		vars.autoRegSex = sex;
		return true;
	});

	_scriptState.set_function("getSex", [this]() {
		return vars.autoRegSex;
	});

	// SETTINGS
	_scriptState.set_function("getNickName", [this]() {
		Settings *settings = RakBot::app()->getSettings();
		return settings->getName();
	});

	_scriptState.set_function("setNickName", [this](std::string name) {
		Settings *settings = RakBot::app()->getSettings();
		settings->setName(name);
		return true;
	});

	_scriptState.set_function("getPassword", [this]() {
		Settings *settings = RakBot::app()->getSettings();
		return settings->getLoginPassword();
	});

	_scriptState.set_function("setPassword", [this](std::string password) {
		Settings *settings = RakBot::app()->getSettings();
		settings->setLoginPassword(password);
		return true;
	});

	_scriptState.set_function("getServerPassword", [this]() {
		Settings *settings = RakBot::app()->getSettings();
		return settings->getServerPassword();
	});

	_scriptState.set_function("setServerPassword", [this](std::string password) {
		Settings *settings = RakBot::app()->getSettings();
		settings->setServerPassword(password);
		return true;
	});

	_scriptState.set_function("getRegKey", [this]() {
		return vars.regKey;
	});

	_scriptState.set_function("getServerAddress", [this]() {
		std::stringstream ss;
		ss << RakBot::app()->getSettings()->getAddress()->getIp() << ":" << RakBot::app()->getSettings()->getAddress()->getPort();
		return ss.str();
	});

	_scriptState.set_function("setServerAddress", [this](std::string address) {
		std::vector<std::string> parts = Split(address, ':');
		if (parts.size() != 2)
			return false;
		std::string ip = parts[0];
		uint16_t port = static_cast<uint16_t>(std::stoi(parts[1]));
		if (port < 1 || port > 65535)
			return false;
		RakBot::app()->getSettings()->getAddress()->setIp(ip);
		RakBot::app()->getSettings()->getAddress()->setPort(port);
		return true;
	});

	_scriptState.set_function("sleep", [this](int ms) {
		RakBot::app()->log("[WARNING] Использование функции \"sleep()\" в скриптах не рекомендуется!");
		RakBot::app()->log("[WARNING] Предпочительнее использование \"defCallAdd()\"");
		Sleep(ms);
	});

	_scriptState.set_function("hideDialog", [this]() {
		RakBot::app()->getSampDialog()->hideDialog();
	});

	_scriptState.set_function("showDialog", [this]() {
		RakBot::app()->getSampDialog()->showDialog();
	});

	_scriptState.set_function("createDialog", [this](int dialogId, int dialogStyle, std::string title, std::string btn1, std::string btn2, std::string text) {
		SAMPDialog *sampDialog = RakBot::app()->getSampDialog();
		if (sampDialog->isDialogActive())
			return false;

		if (dialogId < 0 || dialogId >= 65536)
			return false;
		sampDialog->setDialogId(dialogId);

		if (dialogStyle < 1 || dialogStyle >= 5)
			return false;
		sampDialog->setDialogStyle(dialogStyle);

		sampDialog->setDialogTitle(title);
		sampDialog->setOkButtonText(btn1);
		sampDialog->setCancelButtonText(btn2);
		sampDialog->setDialogText(text);
		sampDialog->setDialogActive(false);
		sampDialog->setDialogOffline(true);
		return true;
	});

	_scriptState.set_function("sendVkNotify", [this](const std::string& message) {
		const char *vkNotifyUrlFormat = VMProtectDecryptStringA("https://rakbot.ru/panel/action/vk-notify?key=%s&hwid=%u&message=%s");

		std::string regKeyEncoded = UrlEncode(vars.regKey);
		std::string messageEncoded = UrlEncode(message);

		char *vkNotifyUrl;
		int vkNotifyUrlLength = asprintf(&vkNotifyUrl, vkNotifyUrlFormat, regKeyEncoded.c_str(), GetDeviceID(), messageEncoded.c_str());

		VMProtectFreeString(vkNotifyUrlFormat);

		if (vkNotifyUrlLength < 1)
			return sol::make_object(_scriptState, false);

		CURLcode curlCode = OpenURL(vkNotifyUrl);

		delete[] vkNotifyUrl;

		if (curlCode != CURLE_OK)
			return sol::make_object(_scriptState, curlCode);

		std::string result = CurlBuffer;
		return sol::make_object(_scriptState, result);
	});
}

void Script::luaError(std::string error) {
	std::vector<std::string> lines = Split(error, '\n');

	for each (std::string line in lines) {
		std::string s = "[ERROR] " + line;
		RakBot::app()->log(s.c_str());
	}
}

void Script::luaUpdate() {
	while (!_scriptClosing) {
		Sleep(vars.luaUpdateDelay);

		_defCallsMutex.lock();
		for (int i = 0; i < LUA_MAXDEFCALLS; i++) {
			LuaDefCall *defCall = &_defCalls[i];

			if (!defCall->active)
				continue;

			static Timer timer;
			timer.setTimer(defCall->startTime);
			if (!timer.isElapsed(defCall->callDelay, false))
				continue;

			_scriptMutex.lock();
			try {
				_funcExecuting = true;
				sol::protected_function_result result = defCall->func(defCall->params);
				if (!result.valid())
					throw result.get<sol::error>();
				_funcExecuting = false;
			} catch (const char *e) {
				std::string message = "Ошибка скрипта \"" + _scriptName + "\": " + e;
				luaError(message);
				_funcExecuting = false;
			} catch (const std::exception &e) {
				std::string message = "Ошибка скрипта \"" + _scriptName + "\": " + e.what();
				luaError(message);
				_funcExecuting = false;
			} catch (...) {
				std::string message = "Неизвестная ошибка скрипта \"" + _scriptName + "\"";
				luaError(message);
				_funcExecuting = false;
			}
			_scriptMutex.unlock();

			if (defCall->repeat) {
				defCall->startTime = Timer::getCurrentTime();
			} else {
				_defCalls[i].active = false;
			}
		}
		_defCallsMutex.unlock();

		luaOnScriptUpdate();
	}
}

void LoadScripts() {
	CreateDirectory(GetRakBotPath("scripts").c_str(), NULL);
	CreateDirectory(GetRakBotPath("scripts\\libs").c_str(), NULL);

	WIN32_FIND_DATA wfd;
	HANDLE hFind = FindFirstFile(GetRakBotPath("scripts\\*.lua").c_str(), &wfd);
	setlocale(LC_ALL, "");

	bool scriptsExists = false;
	if (INVALID_HANDLE_VALUE != hFind) {
		do {
			scripts.push_back(Script::load(wfd.cFileName));
			scriptsExists = true;
		} while (NULL != FindNextFile(hFind, &wfd));
		FindClose(hFind);
	}
}

void UnloadScripts() {
	while (scripts.size() > 0) {
		Script *script = scripts.back();
		script->luaOnScriptExit();
		Script::unload(script);
		scripts.pop_back();
	}
}

template<typename ...Args>
bool Script::luaCallback(std::string funcName, Args && ...args) {
	std::lock_guard<std::recursive_mutex> lock(_scriptMutex);

	try {
		if (_scriptClosing)
			return false;

		if (_funcExecuting)
			return false;

		_funcExecuting = true;

		sol::protected_function func = _scriptState[funcName];
		if (!func.valid()) {
			_funcExecuting = false;
			return false;
		}

		sol::protected_function_result result = func(std::forward<Args>(args)...);
		if (!result.valid())
			throw result.get<sol::error>();

		if (result.get_type() != sol::type::boolean) {
			_funcExecuting = false;
			return false;
		}

		_funcExecuting = false;
		return result.get<bool>();
	} catch (const char *e) {
		std::string message = "Ошибка скрипта \"" + _scriptName + "\": " + e;
		luaError(message);
		_funcExecuting = false;
		return false;
	} catch (const std::exception &e) {
		std::string message = "Ошибка скрипта \"" + _scriptName + "\": " + e.what();
		luaError(message);
		_funcExecuting = false;
		return false;
	} catch (...) {
		std::string message = "Неизвестная ошибка скрипта \"" + _scriptName + "\"";
		luaError(message);
		_funcExecuting = false;
		return false;
	}
}