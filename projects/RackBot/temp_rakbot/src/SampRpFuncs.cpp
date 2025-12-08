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

#include "AnimStuff.h"
#include "MathStuff.h"
#include "Funcs.h"

#include "cmds.h"
#include "netrpc.h"

#include "SampRpFuncs.h"

bool SampRpFuncs::_botSuspended = false;

SampRpFuncs::SampRpFuncs() {}

SampRpFuncs::~SampRpFuncs() {}

void SampRpFuncs::takeCheckpoint(std::function<void()> afterAction) {
	static bool takeCheckpointReady = true;

	if (!checkpoint.active && !raceCheckpoint.active)
		return;

	float *position = checkpoint.active ? checkpoint.position : raceCheckpoint.position;
	Bot *bot = RakBot::app()->getBot();

	if (bot->distanceTo(position) >= 120.0f) {
		RakBot::app()->log("[RAKBOT] Расстояние до чекпоинта больше 120 метров!");
		return;
	}

	if (!takeCheckpointReady)
		return;
	takeCheckpointReady = false;

	srand(static_cast<uint32_t>(time(NULL)));
	float offsetX = (-1.f) + (static_cast<float>(rand() % 201) / 100.f);
	float offsetY = 1.f - (static_cast<float>(rand() % 201) / 100.f);

	_botSuspended = true;
	bot->teleport(position[0] + offsetX, position[1] + offsetY, position[2] - 2.5f);

	RakBot::app()->getEvents()->defCallAdd(1500, false, [bot, afterAction](DefCall *) {
		bot->takeCheckpoint();
		if (afterAction)
			afterAction();
		_botSuspended = false;
		takeCheckpointReady = true;
	});
}

void SampRpFuncs::pickUpPickup(Pickup *pickup, std::function<void()> afterAction) {
	static bool pickUpReady = true;

	if (pickup == nullptr)
		return;

	Bot *bot = RakBot::app()->getBot();

	if (bot->distanceTo(pickup) >= 120.0f) {
		RakBot::app()->log("[RAKBOT] Расстояние до пикапа %d(%d) больше 120 метров!", pickup->getPickupId(), pickup->getModel());
		return;
	}

	if (!pickUpReady)
		return;
	pickUpReady = false;

	_botSuspended = true;
	bot->teleport(pickup->getPosition(0), pickup->getPosition(1), pickup->getPosition(2) - 2.5f);

	RakBot::app()->getEvents()->defCallAdd(1500, false, [bot, pickup, afterAction](DefCall *) {
		bot->pickUpPickup(pickup);
		if (afterAction)
			afterAction();
		_botSuspended = false;
		pickUpReady = true;
	});
}

bool SampRpFuncs::isSampRpServer() {
	if (RakBot::app()->getServer()->getServerName().find("Samp-Rp.Ru") != std::string::npos)
		return true;

	return false;
}

bool SampRpFuncs::onServerMessage(std::string msg) {
	if (!SampRpFuncs::isSampRpServer())
		return false;
	Bot *bot = RakBot::app()->getBot();

	if (msg.find("Припаркуйте автомобиль и пройдите в здание автошколы") != std::string::npos) {
		bot->exitVehicle();
		vars.botAutoSchoolActive = false;
		vars.botAutoSchoolFinished = true;
	}

	if (vars.busWorkerRoute != 0) {
		if (msg.find("Вы арендовали транспортное средство") != std::string::npos) {
			RakBot::app()->log("[RAKBOT] Заводим двигатель...");
			bot->sendInput("/en");
		}

		if (msg.find(" Транспорт недоступен") != std::string::npos) {
			vars.checkPointMaster = false;
			vars.busWorkerRoute = 0;
			RakBot::app()->log("[RAKBOT] Бот-автобусник: транспорт недоступен, бот отключен!");
		}
	}

	if (msg.find("Сдача на права стоит 500 вирт") != std::string::npos)
		vars.botAutoSchoolActive = 0;

	std::smatch matches;
	if (std::regex_search(msg, matches, std::regex("Мешков перетащено: (\\d+)"))) {
		BotLoaderBagCount = std::stoul(matches[1], nullptr, 10);
	}

	if (vars.botFarmerAutomated) {
		if (msg.find("Сначала начните работу на этой ферме") != std::string::npos ||
			msg.find("На поле недостаточно урожая") != std::string::npos ||
			msg.find("В машине нет места") != std::string::npos) {
			FarmGetPay = true;
			vect3_copy(FarmPos[FarmIndex], vars.coordMasterTarget);
			vars.coordMasterEnabled = true;
			FarmWork = false;
			FarmCount = 0;
			if (vars.bQuestEnabled)
				ChangeFarm = true;
		}
	}

	if (msg.find("Сменить скин можно в магазинах \"Victim\"") != std::string::npos)
		return true;

	if (vars.botFarmerAutomated) {
		if (msg.find("Рабочий день начат") != std::string::npos) {
			vect3_copy(FarmFieldPos[FarmIndex], vars.coordMasterTarget);
			vars.coordMasterEnabled = true;
			FarmWork = 1;
			return true;
		}

		if (msg.find("Рабочий день окончен") != std::string::npos) {
			if (ChangeFarm) {
				FarmIndex++;
				if (FarmIndex > 4)
					FarmIndex = 0;
				vect3_copy(FarmPos[FarmIndex], vars.coordMasterTarget);
				vars.coordMasterEnabled = 1;
				RakBot::app()->log("[RAKBOT] Телепорт на ферму %d", FarmIndex);
			} else
				bot->pickUpPickup(RakBot::app()->getPickup(900 + (FarmIndex * 2)));
			return true;
		}
	}

	//if (vars.botLoaderEnabled) {
	//	if (msg.find("Вы ничего не заработали") != std::string::npos)
	//		return true;

	//	if (msg.find("Вы не начинали работу") != std::string::npos) {
	//		LoaderStep = 6;
	//		return true;
	//	}
	//}

	if (msg.find("Необходимо авторизироваться") != std::string::npos)
		return true;

	if (msg.find("Ваш IP адрес заблокирован") != std::string::npos) {
		RakBot::app()->log("[RAKBOT] IP адрес заблокирован");
		bot->disconnect(false);
		RakBot::app()->exit();
		return true;
	}

	return false;
}

bool SampRpFuncs::onAttachObjectToPlayer(uint16_t playerId, uint32_t slotId, bool attach) {
	if (!SampRpFuncs::isSampRpServer())
		return false;

	Bot *bot = RakBot::app()->getBot();

	if (vars.botLoaderEnabled && playerId == bot->getPlayerId()) {
		if (!attach) {
			BotLoaderWithBag = false;
			// RakBot::app()->log("[RAKBOT] Бот грузчика: мешок сдан!");
		} else {
			BotLoaderWithBag = true;
			// RakBot::app()->log("[RAKBOT] Бот грузчика: мешок поднят!");
			BotLoaderTakenBagTimer.setTimerFromCurrentTime();
		}
	}

	return false;
}

bool SampRpFuncs::onDialogShow(uint16_t dialogId, uint8_t dialogStyle, std::string dialogTitle, std::string okButtonText, std::string cancelButtonText, std::string dialogText) {
	if (!SampRpFuncs::isSampRpServer())
		return false;

	Bot *bot = RakBot::app()->getBot();

	if (vars.botFarmerEnabled) {
		if (dialogId == 135) {
			bot->dialogResponse(dialogId, FarmGetPay ? 0 : 1, -1, "");
			if (FarmGetPay)
				FarmGetPay = 0;
			return true;
		}
		if (dialogId == 126)
			return true;
	}

	if (vars.iSetWorkIndex) {
		if (dialogId == 6) {
			RakBot::app()->log("[RAKBOT] Устройство на работу...");
			bot->dialogResponse(dialogId, 1, -1, "");
			return true;
		}
		if (dialogId == 7) {
			RakBot::app()->log("[RAKBOT] Выбор работы...");
			bot->dialogResponse(dialogId, 1, vars.iSetWorkIndex - 1);
			vars.iSetWorkIndex = 0;
			Sleep(1500);
			if (vars.bQuestEnabled) {
				vars.bQuestEnabled = 0;
				vars.iQuestStep = 0;
				vars.busWorkerRoute = 6;
			}
			bot->spawn();
			return true;
		}
	}

	if (vars.botAutoSchoolEnabled) {
		if (dialogId == 96 || dialogId == 97) {
			bot->dialogResponse(dialogId, 1, -1);
			vars.botAutoSchoolActive = 1;
			return true;
		}
	}

	if (vars.busWorkerRoute) {
		switch (dialogId) {
			case 276:
				bot->dialogResponse(dialogId, 1, -1);
				return true;

			case 169:
				bot->dialogResponse(dialogId, 1, -1);
				return true;

			case 17:
				bot->dialogResponse(dialogId, 1, -1);
				return true;

			case 18:
				bot->dialogResponse(dialogId, 1, vars.busWorkerRouteItem);
				return true;
		}
	}

	if (vars.botLoaderEnabled && dialogId == 128) {
		if (bot->getSkin() == 260 || bot->getSkin() == 16 || bot->getSkin() == 27) {
			bot->dialogResponse(dialogId, 0, -1);
		} else {
			bot->dialogResponse(dialogId, 1, -1);
		}
		return true;
	}

	if (vars.autoRegEnabled) {
		switch (dialogId) {
			case 2:
				RakBot::app()->log("[RAKBOT] Регистрация аккаунта...");
				bot->dialogResponse(dialogId, 1, -1, RakBot::app()->getSettings()->getLoginPassword());
				return true;

			case 3:
				bot->dialogResponse(dialogId, 1, -1);
				return true;

			case 21:
				bot->dialogResponse(dialogId, 1, -1, vars.autoRegMail);
				return true;

			case 109:
				bot->dialogResponse(dialogId, 1, -1, vars.autoRegReferer);
				return true;

			case 4:
				bot->dialogResponse(dialogId, vars.autoRegSex);
				return true;
		}
	}

	if (vars.bQuestEnabled) {
		if (dialogId == 259) {
			bot->dialogResponse(dialogId);
			return true;
		}
		if (dialogId == 225 || dialogId == 228) {
			bot->dialogResponse(dialogId);
			return true;
		}
		if (dialogId == 229) {
			if (dialogText.find("скин") != std::string::npos) {
				vars.botFarmerEnabled = 0;
				vars.bQuestSpawn = 1;
				vars.iQuestStep = 4;
				vars.iBankPutMoney = 1500;
				bot->spawn();
				return true;
			}
			if (dialogText.find("20 мешков") != std::string::npos) {
				vars.iQuestStep = 1;
				RunCommand("!botloader");
				return true;
			}
			if (dialogText.find("50 единиц") != std::string::npos) {
				vars.botAutoSchoolEnabled = 0;
				vars.bQuestSpawn = 1;
				vars.botFarmerAutomated = 1;
				vars.iQuestStep = 3;
				vars.botFarmerEnabled = 1;
				bot->spawn();
				return true;
			}
			if (dialogText.find("права") != std::string::npos) {
				vars.botLoaderEnabled = 0;
				vars.iQuestStep = 2;
				vars.bQuestSpawn = 1;
				vars.botAutoSchoolEnabled = 1;
				bot->spawn();
				return true;
			}
			if (dialogText.find("в мэрию") != std::string::npos) {
				vars.iQuestStep = 5;
				vars.bQuestSpawn = 1;
				bot->spawn();
				return true;
			}
			bot->dialogResponse(dialogId);
			return true;
		}
	}

	if (vars.getBalanceEnabled) {
		switch (dialogId) {
			case 22:
			{
				if (dialogText.find("ATM") != std::string::npos) {
					if (!vars.getBalanceFinished) {
						bot->dialogResponse(dialogId);
						vars.getBalanceFinished = true;
					} else {
						bot->dialogResponse(dialogId);
						vars.getBalanceFinished = false;
						vars.getBalanceEnabled = false;
					}
					return true;
				}
			}
		}
	}

	if (vars.parseStatistic) {
		switch (dialogId) {
			case 22:
			{
				if (dialogTitle.find("MainMenu") != std::string::npos) {
					bot->dialogResponse(dialogId, 1, 3);
					return true;
				}

				if (dialogTitle.find("Информация") != std::string::npos) {
					bot->dialogResponse(dialogId);
					return true;
				}
				if (dialogTitle.find("Статистика персонажа") != std::string::npos) {
					char path[MAX_PATH], buf[256];

					Settings *settings = RakBot::app()->getSettings();
					GetModuleFileName(NULL, buf, sizeof(buf));
					strcpy(strrchr(buf, '\\') + 1, "stats");
					CreateDirectoryA(buf, NULL);
					snprintf(path, MAX_PATH, "%s\\%s;%s;%d.log",
						buf, settings->getName().c_str(), settings->getAddress()->getIp().c_str(), settings->getAddress()->getPort());

					FILE *f = fopen(path, "w");
					std::stringstream ss;
					ss << dialogText << "\nПароль: " << RakBot::app()->getSettings()->getLoginPassword() << std::endl;
					::fwrite(ss.str().c_str(), ss.str().length(), 1, f);
					::fclose(f);

					RakBot::app()->log("[RAKBOT] Информация аккаунта записана в файл");
					bot->dialogResponse(dialogId);
					return true;
				}
			}
		}
	}

	return false;
}

bool SampRpFuncs::onSpawned() {
	if (!SampRpFuncs::isSampRpServer())
		return false;

	Bot *bot = RakBot::app()->getBot();

	if (vars.bQuestEnabled && !vars.coordMasterEnabled) {
		if (!vars.bQuestSpawn) {
			vars.bQuestEnabled = 1;
			bot->sendInput("/quest");
			return true;
		} else {
			vars.bQuestSpawn = 0;
		}

		if (vars.iQuestStep == 4) {
			if (vars.iBankPutMoney == 1500) {
				vars.botFarmerEnabled = 0;
				vars.coordMasterTarget[0] = 1414.69f;
				vars.coordMasterTarget[1] = -1700.48f;
				vars.coordMasterTarget[2] = 13.54f;
				vars.coordMasterEnabled = 1;
				RakBot::app()->log("[RAKBOT] Автоматическое пополнение баланса на 1500 вирт", vars.iBankPutMoney);
				return true;
			} else {
				vars.coordMasterTarget[0] = 459.09f;
				vars.coordMasterTarget[1] = -1500.35f;
				vars.coordMasterTarget[2] = 31.04f;
				vars.coordMasterEnabled = 1;
				vars.bBuySkin = 1;
				RakBot::app()->log("[RAKBOT] Покупка скина. Телепорт к магазину...");
				return true;
			}
		}
		if (vars.iQuestStep == 5) {
			vars.iSetWorkIndex = 1;
			RakBot::app()->log("[RAKBOT] Устройство на работу водителя автобуса", vars.iSetWorkIndex);
			vars.coordMasterTarget[0] = 1480.00f;
			vars.coordMasterTarget[1] = -1771.00f;
			vars.coordMasterTarget[2] = 18.00f;
			vars.coordMasterEnabled = 1;
			return true;
		}
	}

	if (vars.botAutoSchoolEnabled) {
		vars.coordMasterTarget[0] = -2026.00f;
		vars.coordMasterTarget[1] = -101.00f;
		vars.coordMasterTarget[2] = 35.00f;
		vars.coordMasterEnabled = 1;
		RakBot::app()->log("[RAKBOT] Начало сдачи экзамена на права. Телепорт к автошколе...");
		return true;
	}

	if (vars.botFarmerEnabled) {
		vect3_copy(FarmPos[FarmIndex], vars.coordMasterTarget);
		vars.coordMasterEnabled = 1;
		vars.botFarmerEnabled = 1;
		RakBot::app()->log("[RAKBOT] Телепорт на ферму %d", FarmIndex);
		return true;
	}

	if (vars.botLoaderEnabled) {
		vars.coordMasterTarget[0] = 2126.78f;
		vars.coordMasterTarget[1] = -2281.03f;
		vars.coordMasterTarget[2] = 24.88f;
		vars.coordMasterEnabled = 1;
		RakBot::app()->log("[RAKBOT] Бот грузчика включен");
		return true;
	}

	switch (vars.busWorkerRoute) {
		case 1:
			vars.coordMasterTarget[0] = 1258.83f;
			vars.coordMasterTarget[1] = -1810.54f;
			vars.coordMasterTarget[2] = 10.07f;
			vars.busWorkerBusModel = 437;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: городской ЛС");
			vars.coordMasterEnabled = 1;
			return true;

		case 2:
			vars.coordMasterTarget[0] = -1985.03f;
			vars.coordMasterTarget[1] = 96.93f;
			vars.coordMasterTarget[2] = 23.82f;
			vars.busWorkerBusModel = 437;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: городской СФ");
			vars.coordMasterEnabled = 1;
			return true;

		case 3:
			vars.coordMasterTarget[0] = 2778.17f;
			vars.coordMasterTarget[1] = 1290.91f;
			vars.coordMasterTarget[2] = 6.73f;
			vars.busWorkerBusModel = 437;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: городской ЛВ");
			vars.coordMasterEnabled = 1;
			return true;

		case 4:
			vars.busWorkerRouteItem = 0;
			vars.coordMasterTarget[0] = 1654.91f;
			vars.coordMasterTarget[1] = -1050.12f;
			vars.coordMasterTarget[2] = 21.13f;
			vars.busWorkerBusModel = 431;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: междугородний ЛС-СФ");
			vars.coordMasterEnabled = 1;
			return true;

		case 5:
			vars.busWorkerRouteItem = 1;
			vars.coordMasterTarget[0] = 1654.91f;
			vars.coordMasterTarget[1] = -1050.12f;
			vars.coordMasterTarget[2] = 21.13f;
			vars.busWorkerBusModel = 431;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: междугородний ЛС-ЛВ");
			vars.coordMasterEnabled = 1;
			return true;

		case 6:
			vars.busWorkerRouteItem = 2;
			vars.coordMasterTarget[0] = 1654.91f;
			vars.coordMasterTarget[1] = -1050.12f;
			vars.coordMasterTarget[2] = 21.13f;
			vars.busWorkerBusModel = 431;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: междугородний СФ-ЛВ");
			vars.coordMasterEnabled = 1;
			return true;

		case 7:
			vars.busWorkerRouteItem = 3;
			vars.coordMasterTarget[0] = 1654.91f;
			vars.coordMasterTarget[1] = -1050.12f;
			vars.coordMasterTarget[2] = 21.13f;
			vars.busWorkerBusModel = 431;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: пригородный ЛС-ФК");
			vars.coordMasterEnabled = 1;
			return true;

		case 8:
			vars.busWorkerRouteItem = 4;
			vars.coordMasterTarget[0] = 1654.91f;
			vars.coordMasterTarget[1] = -1050.12f;
			vars.coordMasterTarget[2] = 21.13f;
			vars.busWorkerBusModel = 431;
			RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: пригородный ЛС-ЗАВОД");
			vars.coordMasterEnabled = false;
			return true;
	}
	return false;
}

void SampRpFuncs::onCreateObject(GTAObject * object) {
	if (!SampRpFuncs::isSampRpServer())
		return;

	if (object->ulModelId == 1317) {
		vect3_copy(object->position, checkpoint.position);
		checkpoint.position[2] += 1.5f;
		checkpoint.size = 1.0f;
		checkpoint.active = 1;
	}
}

void SampRpFuncs::onDestroyObject(GTAObject * object) {
	if (!SampRpFuncs::isSampRpServer())
		return;

	if (object->ulModelId == 1317) {
		checkpoint.active = 0;
	}
}

void SampRpFuncs::onDialogResponseSent(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput) {
	if (!SampRpFuncs::isSampRpServer())
		return;

	if (vars.botLoaderEnabled && dialogId == 128) {
		BotLoaderWaitAfterPay = true;
		RakBot::app()->getEvents()->defCallAdd(5500, false, [](DefCall *) {
			BotLoaderWaitAfterPay = false;
		});
		BotLoaderWaitDialog = false;
	}
}
