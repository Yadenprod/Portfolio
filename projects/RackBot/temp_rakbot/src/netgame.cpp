// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"
#include "PlayerBase.h"
#include "Player.h"
#include "Bot.h"
#include "RakNet.h"
#include "Script.h"
#include "Settings.h"
#include "Vehicle.h"
#include "Events.h"

#include "main.h"
#include "netrpc.h"

void BIG_NUM_MUL(unsigned long in[5], unsigned long out[6], unsigned long factor) {
	/*
	Based on TTMath library by Tomasz Sowa.
	*/

	unsigned long src[5] = { 0 };
	for (int i = 0; i < 5; i++)
		src[i] = ((in[4 - i] >> 24) | ((in[4 - i] << 8) & 0x00FF0000) | ((in[4 - i] >> 8) & 0x0000FF00) | (in[4 - i] << 24));

	unsigned long long tmp = 0;

	tmp = unsigned long long(src[0])*unsigned long long(factor);
	out[0] = tmp & 0xFFFFFFFF;
	out[1] = tmp >> 32;
	tmp = unsigned long long(src[1])*unsigned long long(factor) + unsigned long long(out[1]);
	out[1] = tmp & 0xFFFFFFFF;
	out[2] = tmp >> 32;
	tmp = unsigned long long(src[2])*unsigned long long(factor) + unsigned long long(out[2]);
	out[2] = tmp & 0xFFFFFFFF;
	out[3] = tmp >> 32;
	tmp = unsigned long long(src[3])*unsigned long long(factor) + unsigned long long(out[3]);
	out[3] = tmp & 0xFFFFFFFF;
	out[4] = tmp >> 32;
	tmp = unsigned long long(src[4])*unsigned long long(factor) + unsigned long long(out[4]);
	out[4] = tmp & 0xFFFFFFFF;
	out[5] = tmp >> 32;

	for (int i = 0; i < 12; i++) {
		unsigned char temp = ((unsigned char*)out)[i];
		((unsigned char*)out)[i] = ((unsigned char*)out)[23 - i];
		((unsigned char*)out)[23 - i] = temp;
	}
}

int gen_gpci(char buf[64], unsigned long factor) /* by bartekdvd */
{
	unsigned char out[6 * 4] = { 0 };

	static const char alphanum[] =
		"0123456789"
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ";

	for (int i = 0; i < 6 * 4; ++i)
		out[i] = alphanum[rand() % (sizeof(alphanum) - 1)];

	// out[6 * 4] = 0;

	BIG_NUM_MUL((unsigned long*)out, (unsigned long*)out, factor);

	unsigned int notzero = 0;
	buf[0] = '0'; buf[1] = '\0';

	if (factor == 0) return 1;

	int pos = 0;
	for (int i = 0; i < 24; i++) {
		unsigned char tmp = out[i] >> 4;
		unsigned char tmp2 = out[i] & 0x0F;

		if (notzero || tmp) {
			buf[pos++] = (char)((tmp > 9) ? (tmp + 55) : (tmp + 48));
			if (!notzero) notzero = 1;
		}

		if (notzero || tmp2) {
			buf[pos++] = (char)((tmp2 > 9) ? (tmp2 + 55) : (tmp2 + 48));
			if (!notzero) notzero = 1;
		}
	}
	buf[pos] = 0;

	return pos;
}

void Packet_ConnectionSucceeded(Packet *p) {
	RakClientInterface *rakClient = RakBot::app()->getRakClient();
	RakNet::BitStream bsSuccAuth((unsigned char *)p->data, p->length, false);

	bsSuccAuth.IgnoreBits(8);
	bsSuccAuth.IgnoreBits(32);
	bsSuccAuth.IgnoreBits(16);

	uint16_t localPlayerId;
	bsSuccAuth.Read(localPlayerId);
	bsSuccAuth.Read(vars.uiChallenge);

	Bot *bot = RakBot::app()->getBot();
	if (bot == nullptr)
		return;

	bot->setConnected(true);
	bot->setName(RakBot::app()->getSettings()->getName());
	bot->setPlayerId(localPlayerId);

	/*if (!VMProtectIsValidImageCRC()) {
		VMProtectBeginUltra(__FUNCTION__);
		DWORD tickCount = GetTickCount();
		while (GetTickCount() - tickCount > 10000) { }
		VMProtectEnd();
	}*/

	RakBot::app()->log("[RAKBOT] Подключено. Вход в игру...");
	bot->setConnected(true);
	vars.botConnectedTimer.setTimerFromCurrentTime();
	RakBot::app()->getEvents()->onConnect(localPlayerId);

	char authBS[64];
	memset(authBS, 0, sizeof(authBS));
	gen_gpci(authBS, 0x3e9);

	int iVersion = NETGAME_VERSION;
	uint8_t byteMod = 1;
	uint8_t byteAuthBSLen = static_cast<uint8_t>(strlen(authBS));
	uint8_t byteNameLen = static_cast<uint8_t>(RakBot::app()->getSettings()->getName().length());

	unsigned int uiClientChallengeResponse = vars.uiChallenge ^ iVersion;

	RakNet::BitStream bsSend;
	bsSend.Write(iVersion);
	bsSend.Write(byteMod);
	bsSend.Write(byteNameLen);
	bsSend.Write(RakBot::app()->getSettings()->getName().c_str(), byteNameLen);

	bsSend.Write(uiClientChallengeResponse);
	bsSend.Write(byteAuthBSLen);
	bsSend.Write(authBS, byteAuthBSLen);
	char szClientVer[] = "0.3.7";
	uint8_t byteClientVerLen = sizeof(szClientVer) - 1;
	bsSend.Write(byteClientVerLen);
	bsSend.Write(szClientVer, byteClientVerLen);
	bsSend.Write(uiClientChallengeResponse);

	rakClient->RPC(&RPC_ClientJoin, &bsSend, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);
}

void Packet_PlayerSync(Packet *p) {
	RakNet::BitStream bsPlayerSync((unsigned char *)p->data, p->length, false);
	uint16_t playerId;

	//Log("Packet_PlayerSync: %d \n%s\n", p->length, DumpMem((unsigned char *)p->data, p->length));

	bool bHasLR, bHasUD;
	bool bHasSurfInfo, bAnimation;

	bsPlayerSync.IgnoreBits(8);
	bsPlayerSync.Read(playerId);

	OnfootData ofd;
	memset(&ofd, 0, sizeof(OnfootData));

	// LEFT/RIGHT KEYS
	bsPlayerSync.Read(bHasLR);
	if (bHasLR) bsPlayerSync.Read(ofd.leftRightKey);

	// UP/DOWN KEYS
	bsPlayerSync.Read(bHasUD);
	if (bHasUD) bsPlayerSync.Read(ofd.upDownKey);

	// GENERAL KEYS
	bsPlayerSync.Read(ofd.keys);

	// VECTOR POS
	bsPlayerSync.Read(ofd.position[0]);
	bsPlayerSync.Read(ofd.position[1]);
	bsPlayerSync.Read(ofd.position[2]);

	// ROTATION
	bsPlayerSync.ReadNormQuat(
		ofd.quaternion[0],
		ofd.quaternion[1],
		ofd.quaternion[2],
		ofd.quaternion[3]);


	// HEALTH/ARMOUR (COMPRESSED INTO 1 uint8_t)
	uint8_t byteHealthArmour;
	uint8_t health, armour;
	uint8_t byteArmTemp = 0, byteHlTemp = 0;

	bsPlayerSync.Read(byteHealthArmour);
	byteArmTemp = (byteHealthArmour & 0x0F);
	byteHlTemp = (byteHealthArmour >> 4);

	if (byteArmTemp == 0xF) armour = 100;
	else if (byteArmTemp == 0) armour = 0;
	else armour = byteArmTemp * 7;

	if (byteHlTemp == 0xF) health = 100;
	else if (byteHlTemp == 0) health = 0;
	else health = byteHlTemp * 7;

	ofd.health = health;
	ofd.armour = armour;

	// CURRENT WEAPON
	bsPlayerSync.Read(ofd.weapon);

	// Special Action
	bsPlayerSync.Read(ofd.specialAction);

	// READ MOVESPEED VECTORS
	bsPlayerSync.ReadVector(
		ofd.speed[0],
		ofd.speed[1],
		ofd.speed[2]);

	bsPlayerSync.Read(bHasSurfInfo);
	if (bHasSurfInfo) {
		bsPlayerSync.Read(ofd.surfVehicleId);
		bsPlayerSync.Read(ofd.surfOffsets[0]);
		bsPlayerSync.Read(ofd.surfOffsets[1]);
		bsPlayerSync.Read(ofd.surfOffsets[2]);
	} else
		ofd.surfVehicleId = -1;

	bsPlayerSync.Read(bAnimation);
	if (bAnimation) {
		bsPlayerSync.Read(ofd.animId);
		bsPlayerSync.Read(ofd.animFlags);
	}

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	player->setPlayerState(PLAYER_STATE_ONFOOT);
	player->setPosition(0, ofd.position[0]);
	player->setPosition(1, ofd.position[1]);
	player->setPosition(2, ofd.position[2]);

	player->setQuaternion(0, ofd.quaternion[0]);
	player->setQuaternion(1, ofd.quaternion[1]);
	player->setQuaternion(2, ofd.quaternion[2]);
	player->setQuaternion(3, ofd.quaternion[3]);

	player->setSpeed(0, ofd.speed[0]);
	player->setSpeed(1, ofd.speed[1]);
	player->setSpeed(2, ofd.speed[2]);

	player->setHealth(ofd.health);
	player->setArmour(ofd.armour);
	player->setWeapon(ofd.weapon);
	player->setSpecialAction(ofd.specialAction);

	PlayerKeys *keys = player->getKeys();
	keys->setLeftRightKey(ofd.leftRightKey);
	keys->setUpDownKey(ofd.upDownKey);
	keys->setKeyId(ofd.keys);

	PlayerAnimation *anim = player->getAnimation();
	anim->setAnimId(ofd.animId);
	anim->setAnimFlags(ofd.animFlags);

	PlayerSurfing *surfing = player->getSurfing();
	surfing->setOffsets(0, ofd.surfOffsets[0]);
	surfing->setOffsets(1, ofd.surfOffsets[1]);
	surfing->setOffsets(2, ofd.surfOffsets[2]);
}

void Packet_VehicleSync(Packet *p) {
	RakNet::BitStream bsSync((unsigned char *)p->data, p->length, false);

	uint16_t playerId;
	bool bLandingGear;
	bool bHydra, bTrain, bTrailer;
	bool bSiren;

	//Log("Packet_VehicleSync: %d \n%s\n", p->length, DumpMem((unsigned char *)p->data, p->length));

	bsSync.IgnoreBits(8);
	bsSync.Read(playerId);

	IncarData icd;
	memset(&icd, 0, sizeof(IncarData));

	// VEHICLE ID
	bsSync.Read(icd.sVehicleId);

	// LEFT/RIGHT KEYS
	bsSync.Read(icd.lrAnalog);

	// UP/DOWN KEYS
	bsSync.Read(icd.udAnalog);

	// GENERAL KEYS
	bsSync.Read(icd.sKeys);

	// ROLL / DIRECTION
	// ROTATION
	bsSync.ReadNormQuat(
		icd.quaternion[0],
		icd.quaternion[1],
		icd.quaternion[2],
		icd.quaternion[3]);

	// POSITION
	bsSync.Read(icd.position[0]);
	bsSync.Read(icd.position[1]);
	bsSync.Read(icd.position[2]);

	// SPEED
	bsSync.ReadVector(
		icd.vecMoveSpeed[0],
		icd.vecMoveSpeed[1],
		icd.vecMoveSpeed[2]);

	// VEHICLE HEALTH
	uint16_t wTempVehicleHealth;
	bsSync.Read(wTempVehicleHealth);
	icd.fCarHealth = (float)wTempVehicleHealth;

	// HEALTH/ARMOUR (COMPRESSED INTO 1 uint8_t)
	uint8_t byteHealthArmour;
	uint8_t bytePlayerHealth, bytePlayerArmour;
	uint8_t byteArmTemp = 0, byteHlTemp = 0;

	bsSync.Read(byteHealthArmour);
	byteArmTemp = (byteHealthArmour & 0x0F);
	byteHlTemp = (byteHealthArmour >> 4);

	if (byteArmTemp == 0xF)
		bytePlayerArmour = 100;

	else if (byteArmTemp == 0)
		bytePlayerArmour = 0;

	else bytePlayerArmour = byteArmTemp * 7;

	if (byteHlTemp == 0xF)
		bytePlayerHealth = 100;

	else if (byteHlTemp == 0)
		bytePlayerHealth = 0;

	else bytePlayerHealth = byteHlTemp * 7;

	icd.bytePlayerHealth = bytePlayerHealth;
	icd.bytePlayerArmour = bytePlayerArmour;

	// CURRENT WEAPON
	bsSync.Read(icd.weapon);

	// SIREN
	bsSync.ReadCompressed(bSiren);
	if (bSiren)
		icd.byteSirenOn = 1;

	// LANDING GEAR
	bsSync.ReadCompressed(bLandingGear);
	if (bLandingGear)
		icd.byteLandingGearState = 1;

	// HYDRA THRUST ANGLE AND TRAILER ID
	bsSync.ReadCompressed(bHydra);
	bsSync.ReadCompressed(bTrailer);

	uint32_t dwTrailerID_or_ThrustAngle;
	bsSync.Read(dwTrailerID_or_ThrustAngle);
	icd.TrailerID_or_ThrustAngle = (uint16_t)dwTrailerID_or_ThrustAngle;

	// TRAIN SPECIAL
	uint16_t wSpeed;
	bsSync.ReadCompressed(bTrain);
	if (bTrain) {
		bsSync.Read(wSpeed);
		icd.fTrainSpeed = (float)wSpeed;
	}

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	player->setPlayerState(PLAYER_STATE_DRIVER);
	player->setPosition(0, icd.position[0]);
	player->setPosition(1, icd.position[1]);
	player->setPosition(2, icd.position[2]);

	player->setQuaternion(0, icd.quaternion[0]);
	player->setQuaternion(1, icd.quaternion[1]);
	player->setQuaternion(2, icd.quaternion[2]);
	player->setQuaternion(3, icd.quaternion[3]);

	player->setSpeed(0, icd.vecMoveSpeed[0]);
	player->setSpeed(1, icd.vecMoveSpeed[1]);
	player->setSpeed(2, icd.vecMoveSpeed[2]);

	player->setHealth(icd.bytePlayerHealth);
	player->setArmour(icd.bytePlayerArmour);
	player->setWeapon(icd.weapon);
	player->setVehicleSeat(0);

	PlayerKeys *keys = player->getKeys();
	keys->setLeftRightKey(icd.lrAnalog);
	keys->setUpDownKey(icd.udAnalog);
	keys->setKeyId(icd.sKeys);

	Vehicle *vehicle = RakBot::app()->getVehicle(icd.sVehicleId);
	if (vehicle == nullptr)
		return;

	player->setVehicle(vehicle);
	vehicle->setDriver(player);
	vehicle->setPassenger(0, player);
	vehicle->setCarHealth(icd.fCarHealth);
	vehicle->setTrainSpeed(icd.fTrainSpeed);
	vehicle->setVehicleId(icd.sVehicleId);
	vehicle->setTrailerId(icd.TrailerID_or_ThrustAngle);
	vehicle->setGearState(icd.byteLandingGearState);
	vehicle->setSirenEnabled(icd.byteSirenOn);

	vehicle->setPosition(0, icd.position[0]);
	vehicle->setPosition(1, icd.position[1]);
	vehicle->setPosition(2, icd.position[2]);

	vehicle->setQuaternion(0, icd.quaternion[0]);
	vehicle->setQuaternion(1, icd.quaternion[1]);
	vehicle->setQuaternion(2, icd.quaternion[2]);
	vehicle->setQuaternion(3, icd.quaternion[3]);

	vehicle->setSpeed(0, icd.vecMoveSpeed[0]);
	vehicle->setSpeed(1, icd.vecMoveSpeed[1]);
	vehicle->setSpeed(2, icd.vecMoveSpeed[2]);
}

void Packet_PassengerSync(Packet *p) {
	RakNet::BitStream bsSync((unsigned char *)p->data, p->length, false);

	uint16_t playerId;

	//Log("Packet_VehicleSync: %d \n%s\n", p->length, DumpMem((unsigned char *)p->data, p->length));

	bsSync.IgnoreBits(8);
	bsSync.Read(playerId);

	PassengerData pd;
	memset(&pd, 0, sizeof(PassengerData));

	bsSync.Read(pd.sVehicleID);
	bsSync.Read(pd.byteSeatID);
	bsSync.Read(pd.byteCurrentWeapon);

	// HEALTH/ARMOUR (COMPRESSED INTO 1 uint8_t)
	uint8_t byteHealthArmour;
	uint8_t bytePlayerHealth, bytePlayerArmour;
	uint8_t byteArmTemp = 0, byteHlTemp = 0;

	bsSync.Read(byteHealthArmour);
	byteArmTemp = (byteHealthArmour & 0x0F);
	byteHlTemp = (byteHealthArmour >> 4);

	if (byteArmTemp == 0xF)
		bytePlayerArmour = 100;

	else if (byteArmTemp == 0)
		bytePlayerArmour = 0;

	else bytePlayerArmour = byteArmTemp * 7;

	if (byteHlTemp == 0xF)
		bytePlayerHealth = 100;

	else if (byteHlTemp == 0)
		bytePlayerHealth = 0;

	else bytePlayerHealth = byteHlTemp * 7;

	pd.byteHealth = bytePlayerHealth;
	pd.byteArmor = bytePlayerArmour;

	bsSync.Read(pd.sLeftRightKeys);
	bsSync.Read(pd.sUpDownKeys);
	bsSync.Read(pd.sKeys);

	bsSync.Read(pd.fPosition[0]);
	bsSync.Read(pd.fPosition[1]);
	bsSync.Read(pd.fPosition[2]);

	Player *player = RakBot::app()->getPlayer(playerId);
	if (player == nullptr)
		return;

	player->setPlayerState(PLAYER_STATE_PASSENGER);
	player->setPosition(0, pd.fPosition[0]);
	player->setPosition(1, pd.fPosition[1]);
	player->setPosition(2, pd.fPosition[2]);

	player->setQuaternion(0, 0.f);
	player->setQuaternion(1, 0.f);
	player->setQuaternion(2, 0.f);
	player->setQuaternion(3, 0.f);

	player->setSpeed(0, 0.f);
	player->setSpeed(1, 0.f);
	player->setSpeed(2, 0.f);

	player->setHealth(pd.byteHealth);
	player->setArmour(pd.byteArmor);
	player->setWeapon(pd.byteCurrentWeapon);

	PlayerKeys *keys = player->getKeys();
	keys->setLeftRightKey(pd.sLeftRightKeys);
	keys->setUpDownKey(pd.sUpDownKeys);
	keys->setKeyId(pd.sKeys);

	Vehicle *vehicle = RakBot::app()->getVehicle(pd.sVehicleID);
	if (vehicle == nullptr)
		return;

	player->setVehicle(vehicle);
	player->setVehicleSeat(pd.byteSeatID);
	vehicle->setPassenger(pd.byteSeatID, player);

	player->setPosition(0, vehicle->getPosition(0));
	player->setPosition(1, vehicle->getPosition(1));
	player->setPosition(2, vehicle->getPosition(2));

	player->setQuaternion(0, vehicle->getQuaternion(0));
	player->setQuaternion(1, vehicle->getQuaternion(1));
	player->setQuaternion(2, vehicle->getQuaternion(2));
	player->setQuaternion(3, vehicle->getQuaternion(3));

	player->setSpeed(0, vehicle->getSpeed(0));
	player->setSpeed(1, vehicle->getSpeed(0));
	player->setSpeed(2, vehicle->getSpeed(0));
}

void Packet_UnoccupiedSync(Packet *p) {
	RakNet::BitStream bsUnocSync((unsigned char *)p->data, p->length, false);

	bsUnocSync.IgnoreBits(8);

	uint16_t playerId;
	bsUnocSync.Read(playerId);

	UnoccupiedData ud;
	memset(&ud, 0, sizeof(UnoccupiedData));
	bsUnocSync.Read((char *)&ud, sizeof(UnoccupiedData));

	Vehicle *vehicle = RakBot::app()->getVehicle(ud.sVehicleID);
	if (vehicle == nullptr)
		return;

	vehicle->setCarHealth(ud.fHealth);
	vehicle->setDriver(nullptr);

	for (int i = 0; i < vehicle->getSeatsAmount(); i++)
		vehicle->setPassenger(i, nullptr);

	for (int i = 0; i < 3; i++)
		vehicle->setPosition(i, ud.fPosition[i]);

	for (int i = 0; i < 3; i++)
		vehicle->setSpeed(i, ud.fMoveSpeed[i]);
}

void UpdatePlayerScoresAndPings(int iWait, int iMS) {
	static uint32_t dwLastUpdateTick = 0;

	if ((GetTickCount() - dwLastUpdateTick) > (uint32_t)iMS || !iWait) {
		dwLastUpdateTick = GetTickCount();

		RakClientInterface *rakClient = RakBot::app()->getRakClient();
		RakNet::BitStream bsParams;
		rakClient->RPC(&RPC_UpdateScoresPingsIPs, &bsParams, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);
	}
}

void UpdateNetwork() {
	while (!RakBot::app()->isBotOff()) {
		Sleep(vars.networkUpdateDelay);

		Bot *bot = RakBot::app()->getBot();
		RakClientInterface *rakClient = RakBot::app()->getRakClient();

		if (rakClient == nullptr)
			return;

		while (Packet *pkt = rakClient->Receive()) {
			if (pkt->data == NULL)
				break;

			uint8_t packetIdentifier = pkt->data[0];

			switch (packetIdentifier) {
				case ID_DISCONNECTION_NOTIFICATION:
					RakBot::app()->log("[RAKBOT] Сервер закрыл соединение. Переподключение через %d секунд", vars.reconnectDelay / 1000);
					RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_KICK);
					bot->reconnect(vars.reconnectDelay);
					break;
				case ID_CONNECTION_BANNED:
					RakBot::app()->log("[RAKBOT] Вы забанены на этом сервере. Переподключение...");
					RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_BANNED);
					bot->reconnect(3000);
					break;
				case ID_CONNECTION_ATTEMPT_FAILED:
					RakBot::app()->log("[RAKBOT] Не удалось подключиться к серверу. Переподключение...");
					RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_SERVER_OFFLINE);
					bot->reconnect(1000);
					break;
				case ID_NO_FREE_INCOMING_CONNECTIONS:
					RakBot::app()->log("[RAKBOT] Сервер заполнен. Переподключение...");
					RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_SERVER_FULL);
					bot->reconnect(0);
					break;
				case ID_INVALID_PASSWORD:
					RakBot::app()->log("[RAKBOT] Неверный пароль сервера.");
					RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_WRONG_PASSWORD);
					bot->disconnect(false);
					break;
				case ID_CONNECTION_LOST:
					RakBot::app()->log("[RAKBOT] Соединение было потеряно. Переподключение через %d секунд", vars.reconnectDelay / 1000);
					RakBot::app()->getEvents()->onDisconnect(DISCONNECT_REASON_CONNECTION_LOST);
					bot->reconnect(vars.reconnectDelay);
					break;
				case ID_CONNECTION_REQUEST_ACCEPTED:
					Packet_ConnectionSucceeded(pkt);
					break;
				case ID_PLAYER_SYNC:
					Packet_PlayerSync(pkt);
					break;
				case ID_VEHICLE_SYNC:
					Packet_VehicleSync(pkt);
					break;
				case ID_PASSENGER_SYNC:
					Packet_PassengerSync(pkt);
					break;
				case ID_UNOCCUPIED_SYNC:
					Packet_UnoccupiedSync(pkt);
					break;
			}
			rakClient->DeallocatePacket(pkt);
		}

		if (bot->isConnected())
			UpdatePlayerScoresAndPings(1, 500);
	}
}
