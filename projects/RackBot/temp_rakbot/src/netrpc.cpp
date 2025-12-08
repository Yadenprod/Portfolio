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
#include "Events.h"
#include "SAMPDialog.h"
#include "Vehicle.h"

#include "AnimStuff.h"
#include "MathStuff.h"
#include "MiscFuncs.h"
#include "Funcs.h"
#include "SampRpFuncs.h"

#include "main.h"
#include "cmds.h"
#include "netgame.h"
#include "window.h"

#include "netrpc.h"

Checkpoint checkpoint;
GTAMenu gtaMenu;
GTAObject Objects[MAX_OBJECTS];
RaceCheckpoint raceCheckpoint;

bool spawnInfoExists = false;
SpawnInfo spawnInfo;

void ServerJoin(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	CHAR name[256];
	uint16_t playerId;
	uint8_t byteNameLen = 0;

	bsData.Read(playerId);
	int iUnk = 0;
	bsData.Read(iUnk);
	uint8_t unknown = 0;
	bsData.Read(unknown);
	bsData.Read(byteNameLen);

	if (byteNameLen > 20)
		return;

	bsData.Read(name, byteNameLen);
	name[byteNameLen] = '\0';

	Player *player = RakBot::app()->addPlayer(playerId);
	if (player == nullptr)
		return;

	printf("Player joined to the server: %s[%d]\n", name, playerId);

	player->setName(name);

	vars.adminsMutex.lock();
	for (int i = 0; i < static_cast<int>(vars.admins.size()); i++) {
		if (vars.admins[i] == name) {
			player->setAdmin(true);
			break;
		}
	}
	vars.adminsMutex.unlock();

	player->setActive(true);

	RakBot::app()->getEvents()->onPlayerJoin(player);
}

void ServerQuit(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);
	uint16_t playerId;
	uint8_t byteReason;

	bsData.Read(playerId);
	bsData.Read(byteReason);

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	printf("Player left the server: %s[%d]\n", player->getName().c_str(), playerId);

	RakBot::app()->getEvents()->onPlayerQuit(player, byteReason);
	RakBot::app()->deletePlayer(playerId);
}

void InitGame(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsInitGame(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t byteVehicleModels[212], m_byteWorldTime, m_byteWeather;
	uint16_t botId;
	bool m_bZoneNames, m_bUseCJWalk, m_bAllowWeapons, m_bLimitGlobalChatRadius, bLanMode, bStuntBonus;
	bool m_bDisableEnterExits, m_bNameTagLOS, m_bTirePopping, m_bShowPlayerTags, m_bInstagib;
	int m_iSpawnsAvailable, m_iShowPlayerMarkers, m_iDeathDropMoney;
	float m_fGravity, m_fGlobalChatRadius, m_fNameTagDrawDistance;
	int iNetModeNormalOnfootSendRate, iNetModeNormalIncarSendRate, iNetModeFiringSendRate, iNetModeSendMultiplier, iLagCompMode;

	bsInitGame.ReadCompressed(m_bZoneNames);
	bsInitGame.ReadCompressed(m_bUseCJWalk);
	bsInitGame.ReadCompressed(m_bAllowWeapons);
	bsInitGame.ReadCompressed(m_bLimitGlobalChatRadius);
	bsInitGame.Read(m_fGlobalChatRadius);
	bsInitGame.ReadCompressed(bStuntBonus);
	bsInitGame.Read(m_fNameTagDrawDistance);
	bsInitGame.ReadCompressed(m_bDisableEnterExits);
	bsInitGame.ReadCompressed(m_bNameTagLOS);
	bsInitGame.ReadCompressed(m_bTirePopping);
	bsInitGame.Read(m_iSpawnsAvailable);
	bsInitGame.Read(botId);
	bsInitGame.ReadCompressed(m_bShowPlayerTags);
	bsInitGame.Read(m_iShowPlayerMarkers);
	bsInitGame.Read(m_byteWorldTime);
	bsInitGame.Read(m_byteWeather);
	bsInitGame.Read(m_fGravity);
	bsInitGame.ReadCompressed(bLanMode);
	bsInitGame.Read(m_iDeathDropMoney);
	bsInitGame.ReadCompressed(m_bInstagib);
	bsInitGame.Read(iNetModeNormalOnfootSendRate);
	bsInitGame.Read(iNetModeNormalIncarSendRate);
	bsInitGame.Read(iNetModeFiringSendRate);
	bsInitGame.Read(iNetModeSendMultiplier);
	bsInitGame.Read(iLagCompMode);

	bot->setPlayerId(botId);

	uint8_t byteStrLen;
	char hostName[260];
	bsInitGame.Read(byteStrLen);
	bsInitGame.Read(hostName, byteStrLen);
	hostName[byteStrLen] = 0;
	RakBot::app()->getServer()->setServerName(hostName);

	bsInitGame.Read((char *)&byteVehicleModels[0], 212);

	char title[128];
	ZeroMemory(title, sizeof(title));
	snprintf(title, sizeof(title), "%s[%d] - %s",
		bot->getName().c_str(), bot->getPlayerId(),
		RakBot::app()->getServer()->getServerName().c_str());
	SetWindowText(g_hWndMain, title);
	RakBot::app()->log("[RAKBOT] Подключено к %.64s",
		RakBot::app()->getServer()->getServerName().c_str());
	UpdateWindow(g_hWndMain);

	RakBot::app()->getServer()->setGameInited(true);
	vars.gameInitedTimer.setTimerFromCurrentTime();

	RakBot::app()->getEvents()->onGameInited(hostName);

	if (m_iSpawnsAvailable != 0)
		bot->requestClass(0);
}

void WorldPlayerAdd(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t playerId;
	uint8_t fightStyle = 4;
	uint8_t team = 0;
	int skin = 0;
	float position[3];
	float rotation = 0;
	uint32_t color = 0;

	bsData.Read(playerId);
	bsData.Read(team);
	bsData.Read(skin);
	bsData.Read(position[0]);
	bsData.Read(position[1]);
	bsData.Read(position[2]);
	bsData.Read(rotation);
	bsData.Read(color);
	bsData.Read(fightStyle);

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	printf("Player entered the stream: %s[%d]\n", player->getName().c_str(), playerId);

	player->setPlayerState(PLAYER_STATE_ONFOOT);
	player->setInStream(true);
	player->setHealth(100);

	for (int i = 0; i < 3; i++)
		player->setPosition(i, position[i]);

	player->setSkin(skin);

	RakBot::app()->getEvents()->onPlayerAddInWorld(player);
}

void WorldPlayerDeath(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t playerId;
	bsData.Read(playerId);

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	RakBot::app()->getEvents()->onPlayerDeath(player);

	if (!player->isInStream())
		return;

	RakBot::app()->log("[RAKBOT] Умер игрок %s[%d]", player->getName().c_str(), playerId);
}

void WorldPlayerRemove(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t playerId = 0;
	bsData.Read(playerId);

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	printf("Player out of the stream: %s[%d]\n", player->getName().c_str(), playerId);

	player->setPlayerState(PLAYER_STATE_NONE);
	player->setInStream(false);
	player->setVehicle(nullptr);
	player->setVehicleSeat(0);

	for (int i = 0; i < 3; i++)
		player->setPosition(i, 0.f);

	for (int i = 0; i < 3; i++)
		player->setSpeed(i, 0.f);

	for (int i = 0; i < 4; i++)
		player->setQuaternion(i, 0.f);

	player->setHealth(0);
	player->setArmour(0);
	player->setWeapon(0);
	player->setSpecialAction(0);
	player->getKeys()->reset();
	player->getAnimation()->reset();
	player->getSurfing()->reset();

	RakBot::app()->getEvents()->onPlayerRemoveFromWorld(player);
}

void WorldVehicleAdd(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	NewVehicle newVehicle;
	bsData.Read((char *)&newVehicle, sizeof(NewVehicle));

	if (newVehicle.VehicleId < 1 || newVehicle.VehicleId >= MAX_VEHICLES)
		return;

	Vehicle *vehicle = RakBot::app()->addVehicle(newVehicle.VehicleId);
	if (vehicle == nullptr)
		return;

	for (int i = 0; i < 3; i++)
		vehicle->setPosition(i, newVehicle.position[i]);

	vehicle->setModel(newVehicle.iVehicleType);
	vehicle->setDoorsOpened((newVehicle.doorsLock == false));
	vehicle->setFirstColor(newVehicle.aColor1);
	vehicle->setSecondColor(newVehicle.aColor2);
	vehicle->setCarHealth(1000.f);
	vehicle->setActive(true);

	RakBot::app()->getEvents()->onCreateVehicle(vehicle);
}

void WorldVehicleRemove(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t VehicleID;

	bsData.Read(VehicleID);

	if (VehicleID < 1 || VehicleID >= MAX_VEHICLES)
		return;

	Vehicle *vehicle = RakBot::app()->getVehicle(VehicleID);
	if (vehicle == nullptr)
		return;

	RakBot::app()->getEvents()->onDestroyVehicle(vehicle);
	RakBot::app()->deleteVehicle(VehicleID);
}

void ConnectionRejected(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t byteRejectReason;
	bsData.Read(byteRejectReason);

	if (byteRejectReason == REJECT_REASON_BAD_NICKNAME) {
		RakBot::app()->log("[RAKBOT] Неправильный ник, либо игрок уже онлайн. Переподключение...");
		RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_PLAYER_ONLINE);
		bot->reconnect(0);
	} else if (byteRejectReason == REJECT_REASON_BAD_MOD) {
		RakBot::app()->log("[RAKBOT] Неправильная версия модификации");
	} else if (byteRejectReason == REJECT_REASON_BAD_PLAYERID) {
		RakBot::app()->log("[RAKBOT] Неправильный ID игрока");
	} else {
		RakBot::app()->log("[RAKBOT] Соединение отклонено по неизвестной причине");
	}
}

void ScrChatBubble(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t playerId;
	uint8_t len;
	uint32_t color, time;
	float dist;
	char msg[144];

	bsData.Read(playerId);
	bsData.Read(color);
	bsData.Read(dist);
	bsData.Read(time);
	bsData.Read(len);
	bsData.Read(msg, len);
	msg[len] = '\0';

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	if (time > 1500 && vars.farChatEnabled)
		RakBot::app()->log("[RAKBOT] %s[%d]: %s", player->getName().c_str(), playerId, msg);
}

void ClientMessage(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t byteAlpha, byteRed, byteGreen, byteBlue;
	uint32_t msgLen;

	bsData.Read(byteAlpha);
	bsData.Read(byteRed);
	bsData.Read(byteGreen);
	bsData.Read(byteBlue);
	bsData.Read(msgLen);

	char *msgBuf = new char[msgLen + 1];
	bsData.Read(msgBuf, msgLen);
	msgBuf[msgLen] = 0;
	std::string msg = msgBuf;
	delete[] msgBuf;
	msgBuf = nullptr;

	msg = std::regex_replace(msg, std::regex("\\{[0-9A-Fa-f]{6}\\}"), "");

	if (RakBot::app()->getEvents()->onServerMessage(msg))
		return;

	if (!vars.ignoreServerMessages)
		RakBot::app()->log("[СЕРВЕР] %s", msg.c_str());
}

void Chat(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);
	uint16_t playerId;
	uint8_t textLen;

	bsData.Read(playerId);
	bsData.Read(textLen);

	char *textBuf = new char[textLen + 1];
	bsData.Read((char*)textBuf, textLen);
	textBuf[textLen] = 0;
	std::string text = textBuf;
	delete[] textBuf;

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	if (RakBot::app()->getEvents()->onChatMessage(playerId, text))
		return;

	RakBot::app()->log("[СЕРВЕР] [ЧАТ] %s: %s", player->getName().c_str(), text.c_str());
}

void UpdateScoresPingsIPs(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();

	if (!bot->isConnected())
		return;

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t playerId;
	int  iPlayerScore;
	uint32_t dwPlayerPing;

	for (int i = 0; i < static_cast<int>(((rpcParams->numberOfBitsOfData / 8) + 1) / 9); i++) {
		bsData.Read(playerId);
		bsData.Read(iPlayerScore);
		bsData.Read(dwPlayerPing);

		if (playerId == bot->getPlayerId()) {
			bot->getInfo()->setScore(iPlayerScore);
			bot->getInfo()->setPing(dwPlayerPing);
		} else {
			Player *player = RakBot::app()->getPlayer(playerId);
			if (player == nullptr)
				continue;

			player->getInfo()->setScore(iPlayerScore);
			player->getInfo()->setPing(dwPlayerPing);
		}
	}
}

void ScrInitMenu(RPCParameters *rpcParams) {
	RakClientInterface *rakClient = RakBot::app()->getRakClient();

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	memset(&gtaMenu, 0, sizeof(GTAMenu));

	uint8_t byteMenuID;
	BOOL bColumns; // 0 = 1, 1 = 2
	CHAR cText[MAX_MENU_LINE];
	float fX;
	float fY;
	float fCol1;
	float fCol2 = 0.0;
	GTAMenuInt MenuInteraction;

	bsData.Read(byteMenuID);

	if (byteMenuID == 1 || byteMenuID == 3) {
		if (vars.autoRegEnabled && SampRpFuncs::isSampRpServer()) {
			RakNet::BitStream bsSend;
			bsSend.Write(2);
			rakClient->RPC(&RPC_MenuSelect, &bsSend, HIGH_PRIORITY, RELIABLE_ORDERED, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);
			RakBot::app()->log("[RAKBOT] Регистрация аккаунта завершена");
			return;
		}
	}

	if (byteMenuID == 7 && vars.bQuestEnabled && SampRpFuncs::isSampRpServer()) {
		RakNet::BitStream bsSend;
		bsSend.Write(2);
		rakClient->RPC(&RPC_MenuSelect, &bsSend, HIGH_PRIORITY, RELIABLE_ORDERED, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);
		return;
	}

	bsData.Read(bColumns);
	bsData.Read(cText, MAX_MENU_LINE);
	bsData.Read(fX);
	bsData.Read(fY);
	bsData.Read(fCol1);
	if (bColumns)
		bsData.Read(fCol2);
	bsData.Read(MenuInteraction.bMenu);
	for (uint8_t i = 0; i < MAX_MENU_ITEMS; i++)
		bsData.Read(MenuInteraction.bRow[i]);

	RakBot::app()->log("[RAKBOT] Меню: %s", cText);
	strcpy(gtaMenu.szTitle, cText);

	uint8_t byteColCount;
	bsData.Read(cText, MAX_MENU_LINE);
	RakBot::app()->log("[RAKBOT] Меню: %s", cText);
	strcpy(gtaMenu.szSeparator, cText);

	bsData.Read(byteColCount);
	gtaMenu.byteColCount = byteColCount;
	for (uint8_t i = 0; i < byteColCount; i++) {
		bsData.Read(cText, MAX_MENU_LINE);
		RakBot::app()->log("[RAKBOT] Меню: %s (!menu %d)", cText, i);
		strcpy(gtaMenu.szColumnContent[i], cText);
	}

	if (bColumns) {
		bsData.Read(cText, MAX_MENU_LINE);
		//RakBot::app()->log("4: %s", cText);

		bsData.Read(byteColCount);
		for (uint8_t i = 0; i < byteColCount; i++) {
			bsData.Read(cText, MAX_MENU_LINE);
			//RakBot::app()->log("5: %d %s", i, cText);
		}
	}
}

void ScrSetRaceCheckpoint(RPCParameters *rpcParams) {
	unsigned char * Data = reinterpret_cast<unsigned char *>(rpcParams->input);
	int iBitLength = rpcParams->numberOfBitsOfData;

	RakNet::BitStream bsData(Data, (iBitLength / 8) + 1, false);
	bsData.Read((char *)&raceCheckpoint, sizeof(RaceCheckpoint) - 1);

	raceCheckpoint.active = 1;
	RakBot::app()->getEvents()->onCreateRaceCheckpoint(&raceCheckpoint);
	/*char szBuf[256];
	snprintf(szBuf, sizeof(szBuf), "[RAKBOT] Установлен чекпоинт (%.2f; %.2f; %.2f). Чекпоинт мастер %s", g_RaceCheckpoint.fCurPos[0], g_RaceCheckpoint.fCurPos[1], g_RaceCheckpoint.fCurPos[2], g_settings.bCPM ? "включен" : "отключен");
	RakBot::app()->log(szBuf);*/
}

void ScrDisableRaceCheckpoint(RPCParameters *rpcParams) {
	RakBot::app()->getEvents()->onDestroyRaceCheckpoint(&raceCheckpoint);
	ZeroMemory(&raceCheckpoint, sizeof(RaceCheckpoint));
	//RakBot::app()->log("[RAKBOT] Удален чекпоинт");
}

void ScrSetCheckpoint(RPCParameters *rpcParams) {
	PCHAR Data = reinterpret_cast<PCHAR>(rpcParams->input);
	int iBitLength = rpcParams->numberOfBitsOfData;

	RakNet::BitStream bsData((unsigned char *)Data, (iBitLength / 8) + 1, false);

	bsData.Read(checkpoint.position[0]);
	bsData.Read(checkpoint.position[1]);
	bsData.Read(checkpoint.position[2]);
	bsData.Read(checkpoint.size);
	checkpoint.active = 1;
	RakBot::app()->getEvents()->onCreateCheckpoint(&checkpoint);
}

void ScrDisableCheckpoint(RPCParameters *rpcParams) {
	RakBot::app()->getEvents()->onDestroyCheckpoint(&checkpoint);
	ZeroMemory(&checkpoint, sizeof(Checkpoint));
}

void ScrCreatePickup(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	int pickupId;
	int model;
	int type;
	float position[3];

	bsData.Read(pickupId);
	bsData.Read(model);
	bsData.Read(type);

	for (int i = 0; i < 3; i++)
		bsData.Read(position[i]);

	Pickup *pickup = RakBot::app()->addPickup(pickupId);
	if (pickup == nullptr)
		return;

	pickup->setModel(model);
	pickup->setType(type);

	for (int i = 0; i < 3; i++)
		pickup->setPosition(i, position[i]);

	pickup->setActive(true);

	RakBot::app()->getEvents()->onCreatePickup(pickup);
}

void ScrDestroyPickup(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	int pickupId;
	bsData.Read(pickupId);

	Pickup *pickup = RakBot::app()->getPickup(pickupId);
	if (pickup == nullptr)
		return;

	RakBot::app()->getEvents()->onDestroyPickup(pickup);
	RakBot::app()->deletePickup(pickupId);
}

void ScrRemovePlayerFromVehicle(RPCParameters *rpcParams) {
	if (vars.botAutoSchoolActive)
		vars.botAutoSchoolActive = 0;

	Bot *bot = RakBot::app()->getBot();

	if (bot->getPlayerState() != PLAYER_STATE_PASSENGER
		&& bot->getPlayerState() != PLAYER_STATE_DRIVER) {
		RakBot::app()->log("[RAKBOT] Бот не находится в транспорте!");
		return;
	}

	if (RakBot::app()->getEvents()->onEjectFromVehicle())
		return;

	RakBot::app()->log("[RAKBOT] Бот выброшен из транспорта");
	bot->exitVehicle();
}

void ScrShowDialog(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t dialogId;
	bsData.Read(dialogId);
	RakBot::app()->getSampDialog()->setDialogId(dialogId);

	uint8_t dialogStyle;
	bsData.Read(dialogStyle);
	RakBot::app()->getSampDialog()->setDialogStyle(dialogStyle);

	uint8_t titleLen;
	bsData.Read(titleLen);
	char *titleBuf = new char[titleLen + 1];
	bsData.Read(titleBuf, titleLen);
	titleBuf[titleLen] = 0;
	RakBot::app()->getSampDialog()->setDialogTitle(titleBuf);
	delete[] titleBuf;

	uint8_t okButtonLen;
	bsData.Read(okButtonLen);
	char *okButtonBuf = new char[okButtonLen + 1];
	bsData.Read(okButtonBuf, okButtonLen);
	okButtonBuf[okButtonLen] = 0;
	RakBot::app()->getSampDialog()->setOkButtonText(okButtonBuf);
	delete[] okButtonBuf;

	uint8_t cancelButtonLen;
	bsData.Read(cancelButtonLen);
	char *cancelButtonBuf = new char[cancelButtonLen + 1];
	bsData.Read(cancelButtonBuf, cancelButtonLen);
	cancelButtonBuf[cancelButtonLen] = 0;
	RakBot::app()->getSampDialog()->setCancelButtonText(cancelButtonBuf);
	delete[] cancelButtonBuf;

	int dialogTextSize = 10000;
	char *dialogTextBuf = new char[dialogTextSize + 1];
	stringCompressor->DecodeString(dialogTextBuf, dialogTextSize, &bsData);
	RakBot::app()->getSampDialog()->setDialogText(dialogTextBuf);
	delete[] dialogTextBuf;

	RakBot::app()->getSampDialog()->setDialogOffline(false);

	std::string s;

	s = std::regex_replace(RakBot::app()->getSampDialog()->getDialogTitle(), std::regex("\\{[0-9A-Fa-f]{6}\\}"), "");
	RakBot::app()->getSampDialog()->setDialogTitle(s);

	s = std::regex_replace(RakBot::app()->getSampDialog()->getDialogText(), std::regex("\\{[0-9A-Fa-f]{6}\\}"), "");
	RakBot::app()->getSampDialog()->setDialogText(s);

	s = std::regex_replace(RakBot::app()->getSampDialog()->getDialogText(), std::regex("\t"), " ");
	RakBot::app()->getSampDialog()->setDialogText(s);

	if (RakBot::app()->getEvents()->onDialogShow(
		RakBot::app()->getSampDialog()->getDialogId(),
		RakBot::app()->getSampDialog()->getDialogStyle(),
		RakBot::app()->getSampDialog()->getDialogTitle(),
		RakBot::app()->getSampDialog()->getOkButtonText(),
		RakBot::app()->getSampDialog()->getCancelButtonText(),
		RakBot::app()->getSampDialog()->getDialogText()
	)) {
		return;
	}

	RakBot::app()->log("[RAKBOT] Получен диалог %d с заголовком \"%s\"", RakBot::app()->getSampDialog()->getDialogId(), RakBot::app()->getSampDialog()->getDialogTitle().c_str());

	RakBot::app()->getSampDialog()->showDialog();
}

void ScrGameText(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	int type, time, textLen;
	bsData.Read(type);
	bsData.Read(time);
	bsData.Read(textLen);

	char *textBuf = new char[textLen + 1];
	bsData.Read(textBuf, textLen);
	textBuf[textLen] = 0;
	std::string gameText = textBuf;
	delete[] textBuf;

	gameText = std::regex_replace(gameText, std::regex("~n~"), "\n");
	gameText = std::regex_replace(gameText, std::regex("~.~"), "");

	if (RakBot::app()->getEvents()->onGameText(gameText))
		return;

	std::vector<std::string> lines = Split(gameText, '\n');
	for (std::string line : lines)
		RakBot::app()->log("[RAKBOT] Геймтекст: %s", line.c_str());
}

void ScrSetPos(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();

	if (vars.sendBadSync)
		return;

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	float position[3];
	bsData.Read(position[0]);
	bsData.Read(position[1]);
	bsData.Read(position[2]);

	if (RakBot::app()->getEvents()->onSetPosition(position[0], position[1], position[2]))
		return;

	bot->teleport(position[0], position[1], position[2]);

	char szBuf[256];
	snprintf(szBuf, 256, "[RAKBOT] Ваша позиция изменена на: (%.2f; %.2f; %.2f)", position[0], position[1], position[2]);
	RakBot::app()->log(szBuf);
}

void ScrSetMoney(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	int moneyAmount;
	bsData.Read(moneyAmount);
	bot->setMoney(bot->getMoney() + moneyAmount);

	RakBot::app()->log("[RAKBOT] Количество денег изменено на %d", bot->getMoney());

	RakBot::app()->getEvents()->onSetMoney(bot->getMoney());
}

void ScrResetMoney(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	bot->setMoney(0);
	RakBot::app()->log("[RAKBOT] Сервер забрал у Вас все деньги");

	RakBot::app()->getEvents()->onSetMoney(0);
}

void ScrSetSpawnInfo(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	bsData.Read((char *)&spawnInfo, sizeof(SpawnInfo));
	spawnInfoExists = true;

	char buf[256];
	snprintf(buf, sizeof(buf), "[RAKBOT] Установлена позиция спавна: (%.2f; %.2f; %.2f)",
		spawnInfo.position[0], spawnInfo.position[1], spawnInfo.position[2]);
	RakBot::app()->log(buf);

	RakBot::app()->getEvents()->onSetSpawnPos(spawnInfo.position[0], spawnInfo.position[1], spawnInfo.position[2]);
}

void SetHealth(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	float fHealth;
	bsData.Read(fHealth);

	uint8_t byteHealth = static_cast<uint8_t>(fHealth);

	if (RakBot::app()->getEvents()->onSetHealth(byteHealth))
		return;

	if (fHealth <= 0.0f && !vars.antiDeath) {
		bot->kill();
		return;
	}

	if (((fHealth + 5.0f >= bot->getHealth()) && (fHealth < 90.0f)) && vars.bAntiSat)
		return;

	bot->setHealth(byteHealth);
	bot->sync();

	char szBuf[256];
	snprintf(szBuf, 256, "[RAKBOT] Ваш уровень здоровья изменен на %d", bot->getHealth());
	RakBot::app()->log(szBuf);
}

void SetPlayerArmour(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	float fArmour;
	bsData.Read(fArmour);
	uint8_t byteArmour = static_cast<uint8_t>(fArmour);

	if (RakBot::app()->getEvents()->onSetArmour(byteArmour))
		return;

	bot->setHealth(byteArmour);
	bot->sync();

	char szBuf[256];
	snprintf(szBuf, 256, "[RAKBOT] Ваш уровень брони изменен на %d", bot->getArmour());
	RakBot::app()->log(szBuf);
}

void RequestClass(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	int requestOutcome;
	bsData.Read(requestOutcome);

	if (requestOutcome) {
		RakBot::app()->log("[RAKBOT] Конечный класс получен");
		bsData.Read((char *)&spawnInfo, sizeof(SpawnInfo));
		spawnInfoExists = true;

		char buf[256];
		snprintf(buf, sizeof(buf), "[RAKBOT] Установлена позиция спавна: (%.2f; %.2f; %.2f)",
			spawnInfo.position[0], spawnInfo.position[1], spawnInfo.position[2]);
		RakBot::app()->log(buf);
	} else {
		RakBot::app()->log("[RAKBOT] Класс запрошен");
	}
}

void RequestSpawn(RPCParameters *rpcParams) {
	if (vars.virtualWorld)
		return;

	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	int requestOutcome;
	bsData.Read(requestOutcome);

	RakBot::app()->log("[RAKBOT] Сервер запросил спавн");

	if (requestOutcome == 2 || (requestOutcome && vars.waitForRequestSpawnReply))
		bot->spawn();
	else
		vars.waitForRequestSpawnReply = false;
}

void ScrApplyAnimation(RPCParameters *rpcParams) {
	if (!vars.sleepEnabled)
		return;

	uint16_t wPlayerID;
	float fDelta;
	uint8_t byteAnimLibLen, byteAnimNameLen;
	char szAnimLib[256], szAnimName[260];
	uint8_t byteLoop, byteLockx, byteLocky, byteFreeze;
	int iTime;

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	ZeroMemory(szAnimLib, sizeof(szAnimLib));
	ZeroMemory(szAnimName, sizeof(szAnimName));

	bsData.Read(wPlayerID);
	bsData.Read(byteAnimLibLen);
	bsData.Read(szAnimLib, byteAnimLibLen);
	bsData.Read(byteAnimNameLen);
	bsData.Read(szAnimName, byteAnimNameLen);
	bsData.Read(fDelta);
	bsData.Read(byteLoop);
	bsData.Read(byteLockx);
	bsData.Read(byteLocky);
	bsData.Read(byteFreeze);
	bsData.Read(iTime);

	int animFlags = 33000;
	int animId = GetAnimationID(szAnimLib, szAnimName);
	if (animId < 1 || animId > 1811) {
		animId = 1189;
	}

	RakBot::app()->getEvents()->onApplyAnimation(wPlayerID, animId);

	Bot *bot = RakBot::app()->getBot();
	if (wPlayerID == bot->getPlayerId()) {
		bot->getAnimation()->setAnimId(animId);
		bot->getAnimation()->setAnimFlags(animFlags);
		return;
	}

	Player *player = RakBot::app()->getPlayer(wPlayerID);
	if (player == nullptr)
		return;

	player->getAnimation()->setAnimId(animId);
	player->getAnimation()->setAnimFlags(animId);
}

void SetPlayerSkin(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);
	int playerId, skinId;
	bsData.Read(playerId);
	bsData.Read(skinId);

	RakBot::app()->getEvents()->onSetSkin(playerId, skinId);

	if (playerId == bot->getPlayerId()) {
		bot->setSkin(skinId);
		RakBot::app()->log("[RAKBOT] Установлен скин %d", bot->getSkin());
	} else {
		Player *player = RakBot::app()->getPlayer(playerId);
		if (player == nullptr)
			return;
		player->setSkin(skinId);
	}
}

void SetInteriorId(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t interiorId;
	bsData.Read(interiorId);

	if (RakBot::app()->getEvents()->onSetInteriorId(interiorId))
		return;

	RakNet::BitStream bsSend;
	bsSend.Write(interiorId);
	RakBot::app()->getRakClient()->RPC(&RPC_SetInteriorId, &bsSend, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);

	RakBot::app()->log("[RAKBOT] Бот перемещен в интерьер %d", vars.interiorId);
	vars.interiorId = interiorId;
}

void SetPlayerAttachedObject(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t byteAttach;
	uint16_t wPlayerID;
	uint32_t dwSlot;

	bsData.Read(wPlayerID);
	bsData.Read(dwSlot);
	bsData.Read(byteAttach);

	RakBot::app()->getEvents()->onAttachObjectToPlayer(wPlayerID, dwSlot, byteAttach);
}

void CreateObject(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t usObjectId;
	bsData.Read(usObjectId);

	bsData.Read(Objects[usObjectId].ulModelId);
	bsData.Read((char *)Objects[usObjectId].position, sizeof(float) * 3);
	bsData.Read((char *)Objects[usObjectId].fRotation, sizeof(float) * 3);
	bsData.Read(Objects[usObjectId].fDrawDistance);
	Objects[usObjectId].active = 1;

	RakBot::app()->getEvents()->onCreateObject(&Objects[usObjectId]);
}

void DestroyObject(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t usObjectId;
	bsData.Read(usObjectId);
	RakBot::app()->getEvents()->onDestroyObject(&Objects[usObjectId]);

	ZeroMemory(&Objects[usObjectId], sizeof(GTAObject));
}

void ClickTextDraw(RPCParameters *rpcParams) {
	RakClientInterface *rakClient = RakBot::app()->getRakClient();

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t data[5];
	bsData.Read((char *)data, sizeof(data));

	if (!memcmp(data, "\x00\x00\x00\x00\x00", 5)) {
		RakNet::BitStream bsSend;
		bsSend.Write<uint16_t>(0xFFFF);
		rakClient->RPC(&RPC_ClickTextDraw, &bsSend, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);
	}
}

void SetVehicleParamsEx(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t vehicleId;
	uint8_t engine, lights, alarm, doors, bonnet, boot, objective;

	bsData.Read(vehicleId);
	bsData.Read(engine);
	bsData.Read(lights);
	bsData.Read(alarm);
	bsData.Read(doors);
	bsData.Read(bonnet);
	bsData.Read(boot);
	bsData.Read(objective);

	Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
	if (vehicle == nullptr)
		return;

	vehicle->setEngineEnabled(engine);
	vehicle->setLightsEnabled(lights);
	vehicle->setDoorsOpened((doors == false));
	vehicle->setSirenEnabled(alarm);

	if (vehicle == bot->getVehicle()) {
		RakBot::app()->log("[RAKBOT] Состояние автомобиля изменено (двигатель: %s; фары: %s; двери: %s)",
			engine == 1 ? "Вкл" : "Выкл",
			lights == 1 ? "Вкл" : "Выкл",
			doors == 1 ? "Откр" : "Закр"
		);
	}

	if (vars.busWorkerRoute != 0 && engine == 1 && lights == 1) {
		vars.checkPointMaster = true;
	}

	RakBot::app()->getEvents()->onSetVehicleParams(vehicle);
}

void PutPlayerInVehicle(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakClientInterface *rakClient = RakBot::app()->getRakClient();

	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t vehicleId;
	uint8_t seatId;

	bsData.Read(vehicleId);
	bsData.Read(seatId);

	Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
	if (vehicle == nullptr)
		return;

	if (RakBot::app()->getEvents()->onPutInVehicle(vehicle, seatId))
		return;

	bot->enterVehicle(vehicle, seatId);
	RakBot::app()->log("[RAKBOT] Бот посажен в транспорт с ID %d", vehicleId);
}

void ShowTextDraw(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	// printf("%s\n\n", DumpMem(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1));

	uint16_t id;
	bsData.Read(id);

	uint8_t flags;
	bsData.Read(flags);

	float letterSize[2];
	bsData.Read(letterSize[0]);
	bsData.Read(letterSize[1]);

	uint32_t letterColor;
	bsData.Read(((uint8_t *)&letterColor)[3]);
	bsData.Read(((uint8_t *)&letterColor)[2]);
	bsData.Read(((uint8_t *)&letterColor)[1]);
	bsData.Read(((uint8_t *)&letterColor)[0]);

	float lineSize[2];
	bsData.Read(lineSize[0]);
	bsData.Read(lineSize[1]);

	uint32_t boxColor;
	bsData.Read(((uint8_t *)&boxColor)[3]);
	bsData.Read(((uint8_t *)&boxColor)[2]);
	bsData.Read(((uint8_t *)&boxColor)[1]);
	bsData.Read(((uint8_t *)&boxColor)[0]);

	uint8_t shadow;
	bsData.Read(shadow);

	uint8_t outline;
	bsData.Read(outline);

	uint32_t backgroundColor;
	bsData.Read(((uint8_t *)&backgroundColor)[3]);
	bsData.Read(((uint8_t *)&backgroundColor)[2]);
	bsData.Read(((uint8_t *)&backgroundColor)[1]);
	bsData.Read(((uint8_t *)&backgroundColor)[0]);

	uint8_t style;
	bsData.Read(style);

	uint8_t selectable;
	bsData.Read(selectable);

	float position[2];
	bsData.Read(position[0]);
	bsData.Read(position[1]);

	uint16_t modelId;
	bsData.Read(modelId);

	float rotation[3];
	bsData.Read(rotation[0]);
	bsData.Read(rotation[1]);
	bsData.Read(rotation[2]);

	float zoom;
	bsData.Read(zoom);

	uint32_t color;
	bsData.Read(((uint8_t *)&color)[3]);
	bsData.Read(((uint8_t *)&color)[2]);
	bsData.Read(((uint8_t *)&color)[1]);
	bsData.Read(((uint8_t *)&color)[0]);

	uint16_t stringLength;
	bsData.Read(stringLength);

	char *textDrawStringBuf = new char[stringLength + 1];
	bsData.Read(textDrawStringBuf, stringLength);
	textDrawStringBuf[stringLength] = 0;

	std::string string = textDrawStringBuf;
	delete[] textDrawStringBuf;

	TextDraw *textDraw = RakBot::app()->addTextDraw(id);
	if (textDraw == nullptr)
		return;

	textDraw->setHasShadow(shadow);
	textDraw->setHasOutline(outline);
	textDraw->setSelectable(selectable);
	textDraw->setFlags(flags);
	textDraw->setStyle(style);
	textDraw->setModelId(modelId);
	textDraw->setLetterColor(letterColor);
	textDraw->setBoxColor(boxColor);
	textDraw->setBackgroundColor(backgroundColor);
	textDraw->setColor(color);
	textDraw->setZoom(zoom);
	textDraw->setString(string);

	for (int i = 0; i < 2; i++)
		textDraw->setLetterSize(i, letterSize[i]);

	for (int i = 0; i < 2; i++)
		textDraw->setLineSize(i, lineSize[i]);

	for (int i = 0; i < 2; i++)
		textDraw->setPosition(i, position[i]);

	for (int i = 0; i < 3; i++)
		textDraw->setRotation(i, rotation[i]);

	textDraw->setActive(true);

	if (vars.textDrawCreateLogging) {
		RakBot::app()->log("[RAKBOT] Показан текстдрав с ID %d (модель: %d; клик: %s; X: %.2f; Y: %.2f; текст: %s)",
			id, modelId, selectable ? "да" : "нет", position[0], position[1], string.c_str());
	}

	RakBot::app()->getEvents()->onTextDrawShow(id, position[0], position[1], string);
}

void TextDrawHideForPlayer(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t textDrawId;
	bsData.Read(textDrawId);

	if (vars.textDrawHideLogging)
		RakBot::app()->log("[RAKBOT] Скрыт текстдрав с ID %d", textDrawId);

	RakBot::app()->getEvents()->onTextDrawHide(textDrawId);
	RakBot::app()->deleteTextDraw(textDrawId);
}

void TextDrawSetString(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t textDrawId, textDrawStringLen;

	bsData.Read(textDrawId);
	bsData.Read(textDrawStringLen);

	char *textDrawStringBuf = new char[textDrawStringLen + 1];
	bsData.Read(textDrawStringBuf, textDrawStringLen);
	textDrawStringBuf[textDrawStringLen] = 0;
	std::string textDrawString = textDrawStringBuf;
	delete[] textDrawStringBuf;

	TextDraw *textDraw = RakBot::app()->getTextDraw(textDrawId);
	if (textDraw == nullptr)
		return;

	textDraw->setString(textDrawString);

	if (vars.textDrawSetStringLogging)
		RakBot::app()->log("[RAKBOT] Изменен текст текстдрава с ID %d (текст: %s)", textDrawId, textDrawString.c_str());

	RakBot::app()->getEvents()->onTextDrawSetString(textDrawId, textDrawString);
}

void TogglePlayerSpectating(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint32_t specState;
	bsData.Read(specState);
	uint8_t playerState = bot->getPlayerState();

	if (specState == 1 && playerState != PLAYER_STATE_SPECTATE) {
		bot->setPlayerState(PLAYER_STATE_SPECTATE);
		RakBot::app()->log("[RAKBOT] Режим наблюдения включен сервером");
	} else if (specState == 0) {
		RakBot::app()->log("[RAKBOT] Режим наблюдения отключен сервером");
		bot->spawn();
	}

	RakBot::app()->getEvents()->onToggleSpectating(static_cast<bool>(specState));
}

void SetPlayerFacingAngle(RPCParameters *rpcParams) {
	Bot *bot = RakBot::app()->getBot();
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	bsData.Read(vars.faceAngle);

	bot->setQuaternion(0, -cosf((vars.faceAngle / 2.f) * M_PI / 180.f));
	bot->setQuaternion(0, 0.f);
	bot->setQuaternion(0, 0.f);
	bot->setQuaternion(0, 1.f * sinf((vars.faceAngle / 2.f) * M_PI / 180.f));
}

void Create3DTextLabel(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint8_t hideBehindWalls;
	uint16_t labelId;
	uint16_t labelPlayerId;
	uint16_t labelVehicleId;
	uint32_t labelColor;
	float labelPosition[3];
	float labelDrawDistance;

	bsData.Read(labelId);
	bsData.Read(labelColor);
	bsData.Read(labelPosition[0]);
	bsData.Read(labelPosition[1]);
	bsData.Read(labelPosition[2]);
	bsData.Read(labelDrawDistance);
	bsData.Read(hideBehindWalls);
	bsData.Read(labelPlayerId);
	bsData.Read(labelVehicleId);

	char labelTextBuf[2049];
	ZeroMemory(labelTextBuf, sizeof(labelTextBuf));
	stringCompressor->DecodeString(labelTextBuf, sizeof(labelTextBuf) - 1, &bsData);

	std::string labelText = labelTextBuf;
	RakBot::app()->getEvents()->onTextLabelShow(labelId, labelPosition[0], labelPosition[1], labelPosition[2], labelText);

	labelText = std::regex_replace(labelText, std::regex("\\{[0-9A-Fa-f]{6}\\}"), "");

	if (vars.textLabelCreateLogging) {
		RakBot::app()->log("[RAKBOT] Показана 3D метка с ID %d (X: %.2f; Y: %.2f; Z: %.2f; текст: %s)",
			labelId, labelPosition[0], labelPosition[1], labelPosition[2], labelText.c_str());
	}
}

/* void Update3DTextLabel(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	std::string dump = DumpMem(bsData.GetData(), bsData.GetNumberOfBytesUsed());
	std::vector<std::string> dumpLines = Split(dump, '\n');
	for (std::string line : dumpLines) {
		RakBot::app()->log(line.c_str());
	}
} */

void EnterVehicle(RPCParameters *rpcParams) {
	RakNet::BitStream bsData(rpcParams->input, (rpcParams->numberOfBitsOfData / 8) + 1, false);

	uint16_t playerId;
	uint16_t vehicleId;
	uint8_t seatId;

	bsData.Read(playerId);
	bsData.Read(vehicleId);
	bsData.Read(seatId);

	RakBot::app()->getEvents()->onEnterVehicle(playerId, vehicleId, seatId);

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
	if (vehicle == nullptr)
		return;

	RakBot::app()->log("[RAKBOT] Игрок %s[%d] садится в транспорт %s[%d] на место %d",
		player->getName(), playerId, vehicle->getName(), vehicleId, seatId);
}

void RegisterRPCs() {
	RakClientInterface *rakClient = RakBot::app()->getRakClient();
	rakClient->RegisterAsRemoteProcedureCall(&RPC_RequestSpawn, RequestSpawn);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_UpdateScoresPingsIPs, UpdateScoresPingsIPs);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_Chat, Chat);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_RequestClass, RequestClass);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrServerJoin, ServerJoin);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrServerQuit, ServerQuit);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetPlayerPos, ScrSetPos);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetSpawnInfo, ScrSetSpawnInfo);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetRaceCheckpoint, ScrSetRaceCheckpoint);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrDisableRaceCheckpoint, ScrDisableRaceCheckpoint);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrRemovePlayerFromVehicle, ScrRemovePlayerFromVehicle);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetPlayerHealth, SetHealth);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrInitGame, InitGame);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrWorldPlayerAdd, WorldPlayerAdd);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrWorldPlayerDeath, WorldPlayerDeath);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrWorldPlayerRemove, WorldPlayerRemove);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrWorldVehicleAdd, WorldVehicleAdd);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrWorldVehicleRemove, WorldVehicleRemove);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrConnectionRejected, ConnectionRejected);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrClientMessage, ClientMessage);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrGivePlayerMoney, ScrSetMoney);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrResetPlayerMoney, ScrResetMoney);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetCheckpoint, ScrSetCheckpoint);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrDisableCheckpoint, ScrDisableCheckpoint);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrCreatePickup, ScrCreatePickup);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrDestroyPickup, ScrDestroyPickup);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrChatBubble, ScrChatBubble);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrInitMenu, ScrInitMenu);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrShowDialog, ScrShowDialog);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrDisplayGameText, ScrGameText);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrApplyAnimation, ScrApplyAnimation);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetPlayerSkin, SetPlayerSkin);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetPlayerInterior, SetInteriorId);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetPlayerAttachedObject, SetPlayerAttachedObject);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrCreateObject, CreateObject);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrDestroyObject, DestroyObject);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ClickTextDraw, ClickTextDraw);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetVehicleParamsEx, SetVehicleParamsEx);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrPutPlayerInVehicle, PutPlayerInVehicle);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrShowTextDraw, ShowTextDraw);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrTextDrawHideForPlayer, TextDrawHideForPlayer);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrTextDrawSetString, TextDrawSetString);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrTogglePlayerSpectating, TogglePlayerSpectating);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrSetPlayerFacingAngle, SetPlayerFacingAngle);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrCreate3DTextLabel, Create3DTextLabel);
	rakClient->RegisterAsRemoteProcedureCall(&RPC_EnterVehicle, EnterVehicle);
	// rakClient->RegisterAsRemoteProcedureCall(&RPC_ScrUpdate3DTextLabel, Update3DTextLabel);
}
