// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"
#include "RakNet.h"
#include "PlayerBase.h"
#include "Player.h"
#include "Bot.h"
#include "Settings.h"
#include "Pickup.h"
#include "Script.h"
#include "Server.h"
#include "SampRpFuncs.h"
#include "Funcs.h"
#include "MathStuff.h"
#include "cmds.h"
#include "netrpc.h"
#include "Vehicle.h"

#include "netgame.h"
#include "window.h"

#include "Events.h"

Events::Events() {}

Events::~Events() {}

void Events::reset() {

}

int Events::defCallAdd(uint32_t delay, bool repeat, std::function<void(DefCall *)> func) {
	if (delay < 1)
		return -1;

	int defCallIndex = -1;

	for (int i = 0; i < MAX_DEFCALLS; i++) {
		if (!_defCalls[i].active) {
			defCallIndex = i;
			break;
		}
	}

	if (defCallIndex == -1)
		return -1;

	_defCalls[defCallIndex].active = true;
	_defCalls[defCallIndex].startTime = GetTickCount();
	_defCalls[defCallIndex].delay = delay;
	_defCalls[defCallIndex].repeat = repeat;
	_defCalls[defCallIndex].func = func;
	return (defCallIndex + 1);
}

bool Events::defCallDelete(int defCallIndex) {
	if (defCallIndex < 1 || defCallIndex > MAX_DEFCALLS)
		return false;

	_defCalls[defCallIndex - 1].active = false;
	return false;
}

void Events::onUpdate() {
	for (int i = 0; i < MAX_DEFCALLS; i++) {
		DefCall *defCall = &_defCalls[i];

		if (!defCall->active)
			continue;

		static Timer timer;
		timer.setTimer(defCall->startTime);
		if (!timer.isElapsed(defCall->delay, false))
			continue;

		defCall->func(defCall);

		if (defCall->repeat) {
			defCall->startTime = Timer::getCurrentTime();
		} else {
			_defCalls[i].active = false;
		}
	}

	RakBot::app()->getServerInfo()->updateInfo();

	Bot *bot = RakBot::app()->getBot();

	KeepOnline();

	if (!bot->isConnectRequested() && vars.reconnectTimer.isElapsed(0, false) && !vars.keepOnlineWait) {
		bot->connect(RakBot::app()->getSettings()->getAddress()->getIp(), RakBot::app()->getSettings()->getAddress()->getPort());
	}

	FuncsLoop();
	UpdateInfo();
	AdminChecker();

	if (bot->isConnected() && RakBot::app()->getServer()->isGameInited()) {
		NoAfk();

		if (bot->isSpawned()) {
			CheckChangePos();
			AntiAFK();
		}
	}
}

bool Events::onRequestConnect() {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnRequestConnect())
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onRunCommand(std::string command) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnRunCommand(command))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onPrintLog(std::string text) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnPrintLog(text))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onSendInput(std::string input) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnSendInput(input))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onSync() {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnSync())
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onGameText(std::string gameText) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnGameText(gameText);
	}

	if (vars.botFarmerAutomated) {
		if (gameText.find("count") != std::string::npos) {
			FarmCount++;
			if (FarmCount >= 20) {
				FarmGetPay = 1;
				vect3_copy(FarmPos[FarmIndex], vars.coordMasterTarget);
				vars.coordMasterEnabled = 1;
				FarmWork = 0;
				FarmCount = 0;
			}
		}
	}

	return false;
}

void Events::onSpawned() {
	Bot *bot = RakBot::app()->getBot();

	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnSpawned(bot->getPosition(0), bot->getPosition(1), bot->getPosition(2));
	}

	if (vars.virtualWorld) {
		bot->requestClass(rand() % 299);
		return;
	}

	if (SampRpFuncs::onSpawned())
		return;

	if (vars.savedTeleportEnabled && !vars.checkPointMaster) {
		vect3_copy(vars.savedCoords, vars.coordMasterTarget);
		vars.coordMasterEnabled = false;
		RakBot::app()->log("[RAKBOT] Телепорт на сохраненные координаты");
		return;
	}
}

bool Events::onSpawn() {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnSpawn())
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onSetSpawnPos(float positionX, float positionY, float positionZ) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnSetSpawnPos(positionX, positionY, positionZ);
	}
}

bool Events::onSetPosition(float positionX, float positionY, float positionZ) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnSetPosition(positionX, positionY, positionZ))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onSetHealth(uint8_t health) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnSetHealth(health))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onSetArmour(uint8_t armour) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnSetArmour(armour))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onServerMessage(std::string message) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnServerMessage(message))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return SampRpFuncs::onServerMessage(message);
}

bool Events::onChatMessage(uint16_t playerId, std::string message) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnChatMessage(playerId, message))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onDialogShow(uint16_t dialogId, uint8_t dialogStyle, std::string dialogTitle, std::string okButtonText, std::string cancelButtonText, std::string dialogText) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr) {
			if (script->luaOnDialogShow(dialogId, dialogStyle, dialogTitle, okButtonText, cancelButtonText, dialogText))
				luaResult = true;
		}
	}
	if (luaResult)
		return true;

	Bot *bot = RakBot::app()->getBot();

	if (dialogId == vars.dialogIdBan) {
		RakBot::app()->log("[RAKBOT] Аккаунт заблокирован!");
		bot->disconnect(false);
		RakBot::app()->exit();
		return true;
	}

	if (dialogId == vars.dialogIdPassword) {
		RakBot::app()->log("[RAKBOT] Ввод пароля...");
		bot->dialogResponse(dialogId, 1, -1, RakBot::app()->getSettings()->getLoginPassword());
		return true;
	}

	if (SampRpFuncs::onDialogShow(dialogId, dialogStyle, dialogTitle, okButtonText, cancelButtonText, dialogText))
		return true;

	switch (vars.skipDialog) {
		case 1:
			RakBot::app()->log("[RAKBOT] Пропуск диалога %d с нижатием 1й кнопки(ENTER)", dialogId);
			bot->dialogResponse(dialogId, 1, -1);
			return true;

		case 2:
			RakBot::app()->log("[RAKBOT] Пропуск диалога %d с нижатием 2й кнопки(ESC)", dialogId);
			bot->dialogResponse(dialogId, 0, -1);
			return true;

		case 3:
			RakBot::app()->log("[RAKBOT] Пропуск диалога %d", dialogId);
			return true;
	}

	return false;
}

bool Events::onDialogResponse(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput, bool isOffline) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnDialogResponse(dialogId, dialogButton, dialogItem, dialogInput, isOffline))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onDialogResponseSent(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDialogResponseSent(dialogId, dialogButton, dialogItem, dialogInput);
	}

	SampRpFuncs::onDialogResponseSent(dialogId, dialogButton, dialogItem, dialogInput);
}

void Events::onSetSkin(uint16_t playerid, uint16_t skinId) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnSetSkin(playerid, skinId);
	}
}

void Events::onApplyAnimation(uint16_t playerId, uint16_t animId) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnApplyAnimation(playerId, animId);
	}
}

void Events::onConnect(uint16_t playerId) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnConnect(playerId);
	}
}

void Events::onDisconnect(uint8_t reason) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDisconnect(reason);
	}
}

void Events::onReconnect(int delay) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnReconnect(delay);
	}
}

void Events::onSetMoney(int money) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnSetMoney(money);
	}
}

void Events::onGameInited(std::string serverName) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnGameInited();
	}
}

void Events::onCreateVehicle(Vehicle * vehicle) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCreateVehicle(vehicle->getVehicleId());
	}
}

void Events::onDestroyVehicle(Vehicle *vehicle) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDestroyVehicle(vehicle->getVehicleId());
	}
}

void Events::onSetVehicleParams(Vehicle * vehicle) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnSetVehicleParams(vehicle->getVehicleId());
	}
}

void Events::onPlayerJoin(Player *player) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnPlayerJoin(player->getPlayerId(), player->getName());
	}
}

void Events::onPlayerQuit(Player *player, uint8_t reason) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnPlayerQuit(player->getPlayerId(), reason);
	}
}

void Events::onPlayerRemoveFromWorld(Player * player) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnPlayerRemoveFromWorld(player->getPlayerId());
	}
}

void Events::onPlayerDeath(Player * player) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnPlayerDeath(player->getPlayerId());
	}
}

void Events::onDeath() {
	Bot *bot = RakBot::app()->getBot();

	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnPlayerDeath(bot->getPlayerId());
	}
}

void Events::onPlayerAddInWorld(Player * player) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnPlayerAddInWorld(player->getPlayerId());
	}
}

void Events::onTextDrawHide(uint16_t textDrawId) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnTextDrawHide(textDrawId);
	}
}

void Events::onTextDrawShow(uint16_t textDrawId, float positionX, float positionY, std::string textDrawString) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnTextDrawShow(textDrawId, positionX, positionY, textDrawString);
	}
}

void Events::onTextDrawSetString(uint16_t textDrawId, std::string string) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnTextDrawSetString(textDrawId, string);
	}
}

bool Events::onTextDrawClick(uint16_t textDrawId) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnTextDrawClick(textDrawId))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onTextLabelShow(uint16_t labelId, float positionX, float positionY, float positionZ, std::string labelString) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnTextLabelShow(labelId, positionX, positionY, positionZ, labelString);
	}
}

void Events::onToggleSpectating(bool state) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnToggleSpectating(state);
	}
}

bool Events::onPutInVehicle(Vehicle *vehicle, uint8_t seatId) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnPutInVehicle(vehicle->getVehicleId(), seatId))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onEjectFromVehicle() {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnEjectFromVehicle())
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onCreatePickup(Pickup * pickup) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCreatePickup(pickup->getPickupId());
	}
}

void Events::onDestroyPickup(Pickup * pickup) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDestroyPickup(pickup->getPickupId());
	}
}

bool Events::onPickUpPickup(Pickup * pickup) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnPickUpPickup(pickup->getPickupId()))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onCreateCheckpoint(Checkpoint * checkpoint) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCreateCheckpoint();
	}
}

void Events::onDestroyCheckpoint(Checkpoint * checkpoint) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDestroyCheckpoint();
	}
}

void Events::onCreateRaceCheckpoint(RaceCheckpoint * raceCheckpoint) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCreateRaceCheckpoint();
	}
}

void Events::onDestroyRaceCheckpoint(RaceCheckpoint * raceCheckpoint) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDestroyRaceCheckpoint();
	}
}

bool Events::onSetInteriorId(uint8_t interiorId) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnSetInteriorId(interiorId))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onCreateObject(GTAObject * object) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCreateObject(object->usObjectId);
	}

	SampRpFuncs::onCreateObject(object);
}

void Events::onDestroyObject(GTAObject * object) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnDestroyObject(object->usObjectId);
	}

	SampRpFuncs::onDestroyObject(object);
}

void Events::onAttachObjectToPlayer(uint16_t playerId, uint32_t slotId, bool attach) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnAttachObjectToPlayer(playerId, slotId, attach);
	}

	if (SampRpFuncs::onAttachObjectToPlayer(playerId, slotId, attach))
		return;
}

bool Events::onTakeCheckpoint(float positionX, float positionY, float positionZ) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnTakeCheckpoint(positionX, positionY, positionZ))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onTeleport(float positionX, float positionY, float positionZ) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnTeleport(positionX, positionY, positionZ))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onCoordMasterStart(float targetX, float targetY, float targetZ) {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnCoordMasterStart(targetX, targetY, targetZ))
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

bool Events::onCoordMasterStop() {
	bool luaResult = false;
	for each (Script *script in scripts) {
		if (script != nullptr)
			if (script->luaOnCoordMasterStop())
				luaResult = true;
	}
	if (luaResult)
		return true;

	return false;
}

void Events::onCoordMasterComplete() {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCoordMasterComplete();
	}
}

void Events::onCrash() {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnCrash();
	}
}

void Events::onEnterVehicle(uint16_t playerId, uint16_t vehicleId, uint8_t seatId) {
	for each (Script *script in scripts) {
		if (script != nullptr)
			script->luaOnEnterVehicle(playerId, vehicleId, seatId);
	}
}
