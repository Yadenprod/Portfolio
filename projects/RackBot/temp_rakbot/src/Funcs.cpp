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
#include "Timer.h"
#include "Events.h"

#include "MiscFuncs.h"
#include "MathStuff.h"
#include "SampRpFuncs.h"

#include "cmds.h"
#include "main.h"
#include "mapwnd.h"
#include "netgame.h"
#include "netrpc.h"
#include "window.h"

#include "Funcs.h"

Funcs::Funcs() {}

Funcs::~Funcs() {}

void NoAfk() {
	if (!vars.noAfk || !vars.syncAllowed)
		return;

	if (vars.stickEnabled || vars.followEnabled)
		return;

	if (!vars.botSpawnedTimer.isElapsed(vars.afterSpawnDelay, false))
		return;

	static Timer timer;
	if (!timer.isElapsed(vars.noAfkDelay, true))
		return;

	Bot *bot = RakBot::app()->getBot();
	bot->sync();
}

void RoutePlay() {
	while (!RakBot::app()->isBotOff()) {
		Sleep(vars.routeUpdateDelay);

		if (!vars.routeEnabled)
			continue;

		Bot *bot = RakBot::app()->getBot();

		if (!bot->isSpawned())
			Sleep(100);

		if (vars.routeIndex >= vars.routeData.size()) {
			if (!vars.routeLoop) {
				vars.routeEnabled = false;
				vars.syncAllowed = true;
				bot->getKeys()->reset();
				bot->getAnimation()->reset();
				for (int i = 0; i < 3; i++)
					bot->setSpeed(i, 0.f);
				bot->sync();
				RakBot::app()->log("[RAKBOT] Сохраненный маршрут: остановлен");
				continue;
			} else {
				RakBot::app()->log("[RAKBOT] Сохраненный маршрут: повтор");
				vars.routeIndex = 0;
			}
		}

		for (int c = 0; c < vars.routeUpdateCount; c++) {
			if (vars.routeIndex >= vars.routeData.size())
				continue;

			for (int i = 0; i < 4; i++)
				bot->setQuaternion(i, vars.routeData[vars.routeIndex].quaternion[i]);

			for (int i = 0; i < 3; i++)
				bot->setPosition(i, vars.routeData[vars.routeIndex].position[i]);

			for (int i = 0; i < 3; i++)
				bot->setSpeed(i, vars.routeData[vars.routeIndex].speed[i]);

			bot->getAnimation()->setAnimFlags(vars.routeData[vars.routeIndex].animFlags);
			bot->getAnimation()->setAnimId(vars.routeData[vars.routeIndex].animId);
			bot->getKeys()->setKeyId(vars.routeData[vars.routeIndex].keys);
			bot->getKeys()->setLeftRightKey(vars.routeData[vars.routeIndex].leftRightKey);
			bot->getKeys()->setUpDownKey(vars.routeData[vars.routeIndex].upDownKey);
			bot->sync();
			vars.routeIndex++;
		}
	}
}

void CheckChangePos() {
	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned())
		return;

	static float fOldPos[3] = { 0, 0, 0 };
	for (int i = 0; i < 3; i++) {
		if (fOldPos[i] != bot->getPosition(i)) {
			if (vars.mapWindowOpened)
				UpdateMapWindow();

			vars.lastChangePos.setTimerFromCurrentTime();
			for (int i = 0; i < 3; i++)
				fOldPos[i] = bot->getPosition(i);
			break;
		}
	}
	if (raceCheckpoint.active) {
		static float fOldCP[3] = { 0, 0, 0 };
		for (int i = 0; i < 3; i++) {
			if (fOldCP[i] != raceCheckpoint.position[i]) {
				if (vars.mapWindowOpened)
					UpdateMapWindow();

				vect3_copy(raceCheckpoint.position, fOldCP);
				break;
			}
		}
	}
}

void UpdateInfo() {
	Bot *bot = RakBot::app()->getBot();

	static Timer timer;
	if (!timer.isElapsed(500, true))
		return;

	if (bot->isConnected()) {
		char botInfo[1024];
		snprintf(botInfo, sizeof(botInfo),
			"Игроки: %d\nПинг: %d\nКоординаты:\n X: %0.2f\n Y: %0.2f\n Z: %0.2f\nЗдоровье: %d\nДеньги: %d\nАнимация: %d/%d\nУровень: %d\nСтатус: %s",
			RakBot::app()->getPlayersCount(), bot->getInfo()->getPing(), bot->getPosition(0), bot->getPosition(1), bot->getPosition(2),
			bot->getHealth(), bot->getMoney(),
			bot->getAnimation()->getAnimId(), bot->getAnimation()->getAnimFlags(), bot->getInfo()->getScore(),
			bot->getPlayerStateName().c_str());

		if ((bot->getPlayerState() == PLAYER_STATE_DRIVER) || (bot->getPlayerState() == PLAYER_STATE_PASSENGER)) {
			std::stringstream ss;
			ss << "\nТранспорт: " << bot->getVehicle()->getVehicleId();
			strcat(botInfo, ss.str().c_str());
		}

		SetWindowText(g_hWndTitle, botInfo);
	} else {
		SetWindowText(g_hWndTitle, "RakBot " RAKBOT_VERSION "\nАвтор: MishaN");
	}
}

void CheckOnlineAndId() {
	Bot *bot = RakBot::app()->getBot();

	if (bot->isConnected()) {
		if (vars.checkIdEnabled) {
			uint16_t playerId = bot->getPlayerId();
			if (playerId > vars.maxId || playerId < vars.minId) {
				RakBot::app()->log("[RAKBOT] Неподходящий ID (%d). Переподключение...", playerId);
				bot->disconnect(false);
				bot->reconnect(vars.reconnectDelay);
			}
		}

		if (!vars.gameInitedTimer.isElapsed(5000, false))
			return;

		if (vars.checkOnlineEnabled) {
			int playersCount = RakBot::app()->getPlayersCount();
			if (playersCount > vars.maxOnline || playersCount < vars.minOnline) {
				RakBot::app()->log("[RAKBOT] Неподходящий онлайн (%d). Переподключение...", playersCount);
				bot->disconnect(false);
				bot->reconnect(vars.reconnectDelay);
			}
		}
	}
}

void Follow() {
	Bot *bot = RakBot::app()->getBot();

	if (!vars.followEnabled || vars.coordMasterEnabled || vars.stickEnabled || !bot->isSpawned())
		return;

	Player *player = RakBot::app()->getPlayer(vars.followPlayerID);

	if (player->isInStream()) {
		bot->follow(player->getPlayerId());
		return;
	}
	bot->sync();
}

void AdminChecker() {
	static Timer timer;
	if (!timer.isElapsed(500, true))
		return;

	if (g_hWndAdmins == NULL || g_hWndAdminsTitle == NULL)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!bot->isConnected()) {
		SetWindowText(g_hWndAdmins, "Загрузка игроков...");
		SetWindowText(g_hWndAdminsTitle, "Админы онлайн");
		return;
	}

	char szAdminList[2048];
	ZeroMemory(szAdminList, sizeof(szAdminList));
	int iCount = 0, iCountNear = 0;

	for (int i = 0; i < MAX_PLAYERS; i++) {
		Player *player = RakBot::app()->getPlayer(i);
		if (player == nullptr)
			continue;

		if (player->getInfo()->getScore() < 1)
			continue;

		if (player->isAdmin()) {
			switch (vars.adminOnlineAction) {
				case 1:
					RakBot::app()->log("[RAKBOT] Админ в сети, ПЕРЕПОДКЛЮЧЕНИЕ");
					bot->disconnect(false);
					bot->reconnect(vars.adminReconnectDelay);
					return;

				case 2:
					RakBot::app()->log("[RAKBOT] Админ в сети, ВЫХОД");
					bot->disconnect(false);
					RakBot::app()->exit();
					return;
			}

			char szBuf[128];
			ZeroMemory(szBuf, sizeof(szBuf));

			if (player->isInStream()) {
				switch (vars.adminNearAction) {
					case 1:
						RakBot::app()->log("[RAKBOT] Админ рядом, ПЕРЕПОДКЛЮЧЕНИЕ");
						bot->disconnect(false);
						bot->reconnect(vars.adminReconnectDelay);
						return;

					case 2:
						RakBot::app()->log("[RAKBOT] Админ рядом, ВЫХОД");
						bot->disconnect(false);
						RakBot::app()->exit();
						return;
				}

				strncat(szBuf, "!", sizeof(szBuf) - 1);
				iCountNear++;
			}
			snprintf(szBuf, sizeof(szBuf), "%s[%d] | L:%d\n", player->getName().c_str(), i, player->getInfo()->getScore());
			strncat(szAdminList, szBuf, sizeof(szAdminList) - 1);
			iCount++;
		}
	}

	if (iCount < 1) {
		SetWindowText(g_hWndAdmins, "Нет админов онлайн");
		SetWindowText(g_hWndAdminsTitle, "Админы онлайн");
	} else {
		SetWindowText(g_hWndAdmins, szAdminList);
		char szAdminListTitle[256];
		snprintf(szAdminListTitle, sizeof(szAdminListTitle), "Админы онлайн (%d/%d)", iCountNear, iCount);
		SetWindowText(g_hWndAdminsTitle, szAdminListTitle);
	}
}

int BotLoaderBagCount = 0;
bool BotLoaderWithBag = false;
bool BotLoaderWaitDialog = false;
bool BotLoaderWaitAfterPay = false;
Timer BotLoaderTakenBagTimer = UINT32_MAX;

void BotLoader() {
	static Timer timer;
	if (!timer.isElapsed(1000, true))
		return;

	if (!vars.botLoaderEnabled || vars.coordMasterEnabled)
		return;

	if (BotLoaderWaitDialog || BotLoaderWaitAfterPay)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned() || SampRpFuncs::isBotSuspended())
		return;

	if (!vars.sendBadSync)
		vars.sendBadSync = true;

	float botPosition[3];
	for (int i = 0; i < 3; i++)
		botPosition[i] = bot->getPosition(i);

	float loaderPosition[3] = { 2126.78f, -2281.03f, 24.88f };

	if (vect3_dist(botPosition, loaderPosition) > 120.f)
		return;

	if ((bot->getSkin() == 260 || bot->getSkin() == 16 || bot->getSkin() == 27) && BotLoaderBagCount < vars.botLoaderLimit) {
		if (BotLoaderWithBag) {
			if (!BotLoaderTakenBagTimer.isElapsed(vars.botLoaderDelay, false))
				return;

			// RakBot::app()->log("[RAKBOT] Бот грузчика: сдаем мешок...");
			SampRpFuncs::takeCheckpoint([bot]() {
				srand(static_cast<uint32_t>(time(NULL)));
				float offsetX = (-0.5f) + (static_cast<float>(rand() % 101) / 100.f);
				float offsetY = 0.5f - (static_cast<float>(rand() % 101) / 100.f);
				bot->teleport(2201.f + offsetX, -2271.f + offsetY, 14.f);
			});
		} else {
			// RakBot::app()->log("[RAKBOT] Бот грузчика: поднимаем мешок...");
			SampRpFuncs::takeCheckpoint([bot]() {
				srand(static_cast<uint32_t>(time(NULL)));
				float offsetX = (-0.5f) + (static_cast<float>(rand() % 101) / 100.f);
				float offsetY = 0.5f - (static_cast<float>(rand() % 101) / 100.f);
				bot->teleport(2201.f + offsetX, -2271.f + offsetY, 14.f);
			});
		}
		return;
	}

	Pickup *pickup = FindNearestPickup(1275);
	if (pickup == nullptr)
		return;

	RakBot::app()->log("[RAKBOT] Бот грузчика: поднятие пикапа раздевалки...");
	SampRpFuncs::pickUpPickup(pickup);
	BotLoaderWaitDialog = true;
	BotLoaderBagCount = 0;
}

void BusBot() {
	static Timer timer;
	if (!timer.isElapsed(1000, true))
		return;

	if (!vars.busWorkerRoute)
		return;

	if (vars.coordMasterEnabled)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (bot->getPlayerState() == PLAYER_STATE_DRIVER)
		return;

	if (bot->getPlayerState() == PLAYER_STATE_ENTERING_VEHICLE)
		return;

	Vehicle *vehicle = FindNearestVehicle(1, vars.busWorkerBusModel);
	if (vehicle == nullptr)
		return;

	bot->enterVehicle(vehicle, 0);
}

float FarmFieldPos[5][3] =
{
	{ -281.77f, -1369.35f, 9.68f },
	{ -200.11f, 45.97f, 3.12f },
	{ -1022.36f, -1025.35f, 129.22f },
	{ 50.33f, -40.53f, 0.88f },
	{ 1922.23f, 194.19f, 34.25f }
};

float FarmPos[5][3] =
{
	{ -398.97f, -1425.89f, 26.32f },
	{ -108.58f, -3.05f, 3.12f },
	{ -1060.43f, -1195.93f, 129.56f },
	{ -2.98f, 74.82f, 3.12f },
	{ 1918.44f, 173.35f, 37.27f }
};

bool FarmWork = false;
int FarmCount = 0;
int FarmIndex = 0;
bool ChangeFarm = false;
bool FarmGetPay = 0;

#define FARM_FIRST_PICK 901

void FarmerBot() {
	static Timer timer;
	if (!timer.isElapsed(1000, true))
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!vars.botFarmerEnabled || vars.coordMasterEnabled || !bot->isSpawned() || SampRpFuncs::isBotSuspended())
		return;

	if (!vars.sendBadSync)
		vars.sendBadSync = true;

	if (FarmWork) {
		if (!checkpoint.active) {
			Pickup *pickup = FindNearestPickup(19197);
			if (pickup != nullptr) {
				if (bot->distanceTo(pickup) < 50.0f) {
					bot->pickUpPickup(pickup, FALSE);
					RakBot::app()->log("[RAKBOT] Сдача куста в машину %d", pickup->getPickupId());
				} else {
					for (int i = 0; i < 3; i++)
						vars.coordMasterTarget[i] = pickup->getPosition(i);
					vars.coordMasterTarget[2] -= 5.0f;
					vars.coordMasterEnabled = true;
					RakBot::app()->log("[RAKBOT] Телепорт к машине");
				}
			} else {
				static Timer notFoundCarsTimer;
				if (vars.botFarmerAutomated && vars.bQuestEnabled) {
					RakBot::app()->log("[RAKBOT] Не удается найти машины! Смена фермы...");

					FarmGetPay = 1;
					vect3_copy(FarmPos[FarmIndex], vars.coordMasterTarget);
					vars.coordMasterEnabled = 1;
					FarmWork = 0;
					FarmCount = 0;
					ChangeFarm = 1;
				} else if (notFoundCarsTimer.isElapsed(8000, true)) {
					RakBot::app()->log("[RAKBOT] Не удается найти машины!");
					notFoundCarsTimer.setTimerFromCurrentTime();
				}
				return;
			}
		} else {
			bot->takeCheckpoint();
			srand(static_cast<uint32_t>(time(NULL)));
			float offsetX = (-0.5f) + (static_cast<float>(rand() % 101) / 100.f);
			float offsetY = 0.5f - (static_cast<float>(rand() % 101) / 100.f);
			bot->teleport(bot->getPosition(0) + offsetX, bot->getPosition(1) + offsetY, bot->getPosition(2));
		}
	} else {
		int pickupId = FARM_FIRST_PICK + (FarmIndex * 2);
		Pickup *pickup = RakBot::app()->getPickup(pickupId);

		if (pickup) {
			if (bot->distanceTo(pickup) < 50.0f) {
				bot->pickUpPickup(pickup, FALSE);
				RakBot::app()->log("[RAKBOT] Пользуемся раздевалкой...");
			} else {
				for (int i = 0; i < 3; i++)
					vars.coordMasterTarget[i] = pickup->getPosition(i);
				vars.coordMasterTarget[2] -= 5.0f;
				vars.coordMasterEnabled = 1;
				RakBot::app()->log("[RAKBOT] Телепорт к раздевалке");
			}
		} else {
			vect3_copy(FarmPos[FarmIndex], vars.coordMasterTarget);
			vars.coordMasterTarget[2] -= 5.0f;
			vars.coordMasterEnabled = 1;
			RakBot::app()->log("[RAKBOT] Телепорт к раздевалке");
		}
	}
}

void CoordMaster() {
	static Timer timer;
	if (!timer.isElapsed(vars.coordMasterDelay, true))
		return;

	if (!vars.coordMasterEnabled || !vars.syncAllowed)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!vars.botSpawnedTimer.isElapsed(vars.afterSpawnDelay, false))
		return;

	if (!bot->isSpawned())
		return;

	bot->sync();

	float position[3];
	for (int i = 0; i < 3; i++)
		position[i] = bot->getPosition(i);

	float fDist = vect3_dist(position, vars.coordMasterTarget);
	float fDistXY = vect2_dist(position, vars.coordMasterTarget);

	if (fDist == 0.f)
		return;

	if (fDist > vars.coordMasterDist) {
		if (fDistXY > vars.coordMasterDist) {
			if (position[2] != vars.coordMasterHeight) {
				if (abs(vars.coordMasterHeight - position[2]) > vars.coordMasterDist)
					position[2] +=
					(vars.coordMasterDist * (position[2] > vars.coordMasterHeight ? -1.0f : 1.0f));
				else
					position[2] = vars.coordMasterHeight;
			} else {
				float fDistSin = (vars.coordMasterTarget[0] - position[0]) / fDistXY;
				float fDistCos = (vars.coordMasterTarget[1] - position[1]) / fDistXY;

				position[0] += fDistSin * vars.coordMasterDist;
				position[1] += fDistCos * vars.coordMasterDist;
			}
		} else if (fDistXY != 0.0f) {
			position[0] = vars.coordMasterTarget[0];
			position[1] = vars.coordMasterTarget[1];
		} else {
			if (abs(vars.coordMasterTarget[2] - position[2]) > vars.coordMasterDist)
				position[2] +=
				(vars.coordMasterDist * (position[2] > vars.coordMasterTarget[2] ? -1.0f : 1.0f));
			else
				position[2] = vars.coordMasterTarget[2];
		}
	} else {
		vect3_copy(vars.coordMasterTarget, position);
		RakBot::app()->log("[RAKBOT] Вы достигли места назначения!");
		RakBot::app()->getEvents()->defCallAdd(vars.coordMasterDelay, false, [bot](DefCall *) {
			if (!bot->isSpawned())
				return;

			vars.coordMasterEnabled = false;
			RakBot::app()->log("[RAKBOT] Коордмастер завершил работу");
			RakBot::app()->getEvents()->onCoordMasterComplete();
		});
	}

	bot->teleport(position[0], position[1], position[2]);
}

void GetBalance() {
	static Timer timer;
	if (!timer.isElapsed(3000, true))
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!vars.getBalanceEnabled || vars.coordMasterEnabled)
		return;

	bot->sendInput("/atm");
}

void Stick() {
	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned())
		return;

	if (!vars.stickEnabled || vars.followEnabled)
		return;

	Player *player = RakBot::app()->getPlayer(vars.followPlayerID);
	if (player == nullptr)
		return;

	if (!player->isInStream())
		return;

	for (int i = 0; i < 4; i++)
		bot->setQuaternion(i, player->getQuaternion(i));

	for (int i = 0; i < 3; i++)
		bot->setPosition(i, player->getPosition(i));

	/* for (int i = 0; i < 3; i++)
		bot->setSpeed(i, player->getSpeed(i)); */

	bot->sync();
}

void AntiAFK() {
	static Timer timer;
	if (!timer.isElapsed(vars.antiAfkDelay, true))
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!vars.antiAfkEnabled)
		return;

	static float k = 1.f;
	static float n = 1.f;

	float offset = (vars.antiAfkOffset != 0.f) ? vars.antiAfkOffset : 0.1f;
	bot->setPosition(0, bot->getPosition(0) + (offset * (k * n)));
	bot->sync();

	if (k <= -2.f || k >= 2.f)
		n *= -1.f;
	else
		k += (1.f * n);

	if (k == 0.f)
		k += (1.f * n);
}

void AutoLicensePass() {
	static Timer timer;
	if (!timer.isElapsed(3000, true))
		return;

	if (!vars.botAutoSchoolEnabled || vars.coordMasterEnabled)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned())
		return;

	if (bot->getPlayerState() != PLAYER_STATE_ONFOOT)
		return;

	if (!raceCheckpoint.active) {
		Pickup *doorPickup = FindNearestPickup(1318);
		if (doorPickup == nullptr)
			return;

		if (bot->distanceTo(doorPickup) < 50.f) {
			if (doorPickup->getPosition(2) < 1000.f) {
				if (vars.botAutoSchoolActive) {
					Vehicle *vehicle = FindNearestVehicle(1, 426, 79, 79);
					if (vehicle != nullptr) {
						bot->enterVehicle(vehicle, 0);
					}
				} else {
					RakBot::app()->log("[RAKBOT] Вход в здание автошколы...");
					bot->pickUpPickup(doorPickup, true);
				}
				return;
			}

			if ((vars.botAutoSchoolActive == 1) || (vars.botAutoSchoolEnabled == 0)) {
				RakBot::app()->log("[RAKBOT] Выход из здания автошколы...");
				bot->pickUpPickup(doorPickup, true);
				return;
			}

			if (checkpoint.active) {
				RakBot::app()->log("[RAKBOT] Начало сдачи экзамена...");
				bot->takeCheckpoint();

				if (vars.botAutoSchoolFinished)
					vars.botAutoSchoolEnabled = 0;

				return;
			}
		}
	}
}

void Flood() {
	static Timer timer;
	if (!timer.isElapsed(vars.floodDelay, true))
		return;

	Bot *bot = RakBot::app()->getBot();

	if (vars.floodEnabled) {
		static int id = 0;
		switch (vars.floodMode) {
			case 1:
				RunCommand(vars.floodText.c_str());
				break;

			case 2:
				char buf[256];
				snprintf(buf, sizeof(buf), "/sms %d %s", id, vars.floodText.c_str());
				bot->sendInput(buf);
				id = id < 1000 ? id + 1 : 0;
				break;
		}
	}
}

void CheckPickUp() {
	Bot *bot = RakBot::app()->getBot();

	if (!vars.autoPickEnabled || vars.coordMasterEnabled)
		return;

	if (!bot->isSpawned())
		return;

	static int iLastPickup = -1;
	for (int i = 0; i < MAX_PICKUPS; i++) {
		Pickup *pickup = RakBot::app()->getPickup(i);
		if (pickup == nullptr)
			continue;

		if (bot->distanceTo(pickup) < 1.0f) {
			if (i != iLastPickup) {
				if (vars.lastChangePos.isElapsed(1500, false)) {
					bot->pickUpPickup(pickup, true);
					RakBot::app()->log("[RAKBOT] Автоматическое поднятие пикапа %d", i);
					iLastPickup = i;
				}
			}
			return;
		}
	}
	iLastPickup = -1;
}

void CheckPointMaster() {
	Bot *bot = RakBot::app()->getBot();

	if (!vars.checkPointMaster || vars.coordMasterEnabled)
		return;

	if (!raceCheckpoint.active && !checkpoint.active)
		return;

	float *pos = checkpoint.active ? checkpoint.position : raceCheckpoint.position;
	DoCoordMaster(true, pos[0], pos[1], pos[2] - 5.f);
}

void SetWork() {
	static Timer timer;
	if (!timer.isElapsed(1000, true))
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!vars.iSetWorkIndex || vars.coordMasterEnabled)
		return;

	if (!bot->isSpawned())
		return;

	Pickup *pickup = FindNearestPickup(1318);
	if (pickup != nullptr) {
		if (pickup->getPosition(2) < 1000.0f)
			bot->pickUpPickup(pickup);
	} else {
		bot->takeCheckpoint();
	}
}

void Bank() {
	static Timer timer;
	if (!timer.isElapsed(1000, true))
		return;

	if (!vars.iBankPutMoney || vars.coordMasterEnabled)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned())
		return;

	Pickup *pickup = FindNearestPickup(1318);
	if (pickup == nullptr)
		return;

	if (pickup->getPosition(1) < -1500.0f) {
		bot->pickUpPickup(pickup, true);
		return;
	}

	std::string cmd = "/bank " + std::to_string(vars.iBankPutMoney);
	bot->sendInput(cmd);
	vars.iBankPutMoney = 0;
	if (vars.bQuestEnabled)
		vars.bQuestSpawn = 1;
	bot->spawn();
}

void GetSkin() {
	static Timer timer;
	if (!timer.isElapsed(1000, true))
		return;

	if (!vars.bBuySkin || vars.coordMasterEnabled)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned())
		return;

	Pickup *pickup;

	pickup = FindNearestPickup(1275);
	if (pickup != nullptr) {
		bot->pickUpPickup(pickup, true);
		return;
	}

	pickup = FindNearestPickup(1318);
	if (pickup != nullptr) {
		bot->pickUpPickup(RakBot::app()->getPickup(pickup->getPickupId() - 1), true);
		return;
	}
}

void KeepOnline() {
	Bot *bot = RakBot::app()->getBot();

	if (vars.keepOnlineEnabled) {
		SYSTEMTIME sysTime;
		GetLocalTime(&sysTime);

		if (!vars.keepOnlineBeginAfterEnd &&
			(sysTime.wMinute >= vars.keepOnlineBegin && sysTime.wMinute < vars.keepOnlineEnd)) {
			if (vars.keepOnlineWait) {
				vars.keepOnlineWait = false;
			}
		} else if (vars.keepOnlineBeginAfterEnd &&
			(sysTime.wMinute >= vars.keepOnlineBegin || sysTime.wMinute < vars.keepOnlineEnd)) {
			if (vars.keepOnlineWait) {
				vars.keepOnlineWait = false;
			}
		} else {
			if (!vars.keepOnlineWait) {
				vars.keepOnlineWait = true;
				bot->disconnect(false);
				bot->reconnect(vars.reconnectDelay);
			}
		}
	}
}

void SleepAnim() {
	Bot *bot = RakBot::app()->getBot();

	if (!bot->isSpawned() || !vars.sleepEnabled)
		return;

	bot->getAnimation()->setAnimId(390);
	bot->getAnimation()->setAnimFlags(4356);
}

void FuncsLoop() {
	Flood();
	CoordMaster();
	CheckPointMaster();
	BusBot();
	BotLoader();
	FarmerBot();
	GetBalance();
	AutoLicensePass();
	Bank();
	CheckPickUp();
	SetWork();
	Follow();
	Stick();
	GetSkin();
	CheckOnlineAndId();
	SleepAnim();
}

void FuncsOff() {
	BotLoaderBagCount = 0;
	FarmCount = 0;
	FarmGetPay = 0;
	FarmWork = 0;

	vars.sendBadSync = false;
	vars.smartInvis = false;
	raceCheckpoint.active = false;
	checkpoint.active = false;
	vars.coordMasterEnabled = false;
	vars.stickEnabled = false;
	vars.followEnabled = false;
	vars.routeEnabled = false;
	vars.syncAllowed = false;
}