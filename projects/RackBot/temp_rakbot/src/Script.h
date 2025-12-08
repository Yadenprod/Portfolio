#pragma once

#include <thread>

#include <lua.hpp>
#pragma comment(lib, "lua51.lib")

#define SOL_CHECK_ARGUMENTS 1
#include <sol.hpp>

#define LUA_MAXDEFCALLS 100

class Timer;

struct LuaDefCall {
	bool active;
	bool repeat;
	uint32_t startTime;
	uint32_t callDelay;
	sol::protected_function func;
	sol::table params;
};

class Script {
private:
	bool _funcExecuting;
	bool _scriptClosing;

	std::string _scriptName;
	sol::state _scriptState;
	std::thread _scriptThread;
	std::recursive_mutex _scriptMutex;

	LuaDefCall _defCalls[LUA_MAXDEFCALLS];
	std::recursive_mutex _defCallsMutex;

	Script(std::string scriptName);
	~Script();

	Script(Script const&);
	Script& operator=(Script const&);

public:
	// LUA CALLBACKS
	void luaOnReset(uint8_t restart, uint32_t reconnectTime);
	bool luaOnSetHealth(uint8_t health);
	bool luaOnSetArmour(uint8_t armour);
	void luaOnSetMoney(int money);
	void luaOnPlayerQuit(uint16_t playerId, uint8_t reasonId);
	void luaOnPlayerJoin(uint16_t playerId, std::string playerName);
	void luaOnGameInited();
	bool luaOnRequestConnect();
	void luaOnConnect(uint16_t playerId);
	void luaOnDisconnect(uint8_t reason);
	void luaOnReconnect(int delay);
	bool luaOnSetPosition(float positionX, float positionY, float positionZ);
	void luaOnSpawned(float positionX, float positionY, float positionZ);
	bool luaOnDialogShow(uint16_t dialogId, uint8_t dialogStyle, std::string dialogTitle, std::string okButtonText, std::string cancelButtonText, std::string dialogText);
	bool luaOnPrintLog(std::string msg);
	bool luaOnRunCommand(std::string cmd);
	void luaOnScriptStart();
	void luaOnScriptExit();
	void luaOnScriptUpdate();
	bool luaOnRecvPacket(uint8_t packetId, uint8_t *packetData, int packetSize);
	bool luaOnSendPacket(uint8_t packetId, uint8_t *packetData, int packetSize);
	bool luaOnRecvRPC(uint8_t rpcId, uint8_t *packetData, int packetSize);
	bool luaOnSendRPC(uint8_t rpcId, uint8_t *packetData, int packetSize);
	void luaOnGameText(std::string gameText);
	void luaOnSetSpawnPos(float positionX, float positionY, float positionZ);
	bool luaOnServerMessage(std::string message);
	bool luaOnChatMessage(uint16_t playerId, std::string message);
	void luaOnSetSkin(uint16_t playerid, uint16_t skinId);
	void luaOnCreateVehicle(uint16_t vehicleId);
	void luaOnDestroyVehicle(uint16_t vehicleId);
	void luaOnSetVehicleParams(uint16_t vehicleId);
	void luaOnPlayerAddInWorld(uint16_t playerId);
	void luaOnPlayerRemoveFromWorld(uint16_t playerId);
	void luaOnPlayerDeath(uint16_t playerId);
	void luaOnTextDrawHide(uint16_t textDrawId);
	void luaOnTextDrawSetString(uint16_t textDrawId, std::string textDrawString);
	void luaOnTextDrawShow(uint16_t textDrawId, float positionX, float positionY, std::string textDrawString);
	void luaOnToggleSpectating(bool state);
	bool luaOnPutInVehicle(uint16_t vehicleId, uint16_t seatId);
	bool luaOnEjectFromVehicle();
	void luaOnCreateCheckpoint();
	void luaOnDestroyCheckpoint();
	void luaOnCreateRaceCheckpoint();
	void luaOnDestroyRaceCheckpoint();
	void luaOnCreatePickup(uint16_t pickupId);
	void luaOnDestroyPickup(uint16_t pickupId);
	bool luaOnSetInteriorId(uint8_t interiorId);
	void luaOnCreateObject(uint16_t objectId);
	void luaOnDestroyObject(uint16_t objectId);
	void luaOnAttachObjectToPlayer(uint16_t playerId, uint32_t slotId, bool attach);
	bool luaOnTakeCheckpoint(float positionX, float positionY, float positionZ);
	bool luaOnPickUpPickup(uint16_t pickupId);
	bool luaOnTextDrawClick(uint16_t textDrawId);
	void luaOnApplyAnimation(uint16_t playerId, uint16_t animId);
	bool luaOnDialogResponse(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput, bool isOffline);
	void luaOnDialogResponseSent(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput);
	bool luaOnSpawn();
	bool luaOnSendInput(std::string input);
	bool luaOnSync();
	void luaOnTextLabelShow(uint16_t labelId, float positionX, float positionY, float positionZ, std::string labelString);
	bool luaOnTeleport(float positionX, float positionY, float positionZ);
	bool luaOnCoordMasterStart(float targetX, float targetY, float targetZ);
	bool luaOnCoordMasterStop();
	void luaOnCoordMasterComplete();
	void luaOnCrash();
	void luaOnEnterVehicle(uint16_t playerId, uint16_t vehicleId, uint8_t seatId);

	// LUA STUFF
	std::string getScriptName() { return _scriptName; }

	static Script *load(std::string scriptName);
	static void unload(Script *script);

	void luaRegisterFunctions();
	void luaError(std::string funcName);
	void luaUpdate();

	template <typename... Args>
	bool luaCallback(std::string funcName, Args&&... args);
};

extern std::vector<Script *> scripts;

void LoadScripts();
void UnloadScripts();
