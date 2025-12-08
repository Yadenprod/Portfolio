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
#include "Pickup.h"
#include "Vehicle.h"
#include "Events.h"

#include "Funcs.h"
#include "MathStuff.h"
#include "VehicleStuff.h"
#include "MiscFuncs.h"
#include "SampRpFuncs.h"

#include "main.h"
#include "ini.h"
#include "netrpc.h"
#include "mapwnd.h"
#include "netgame.h"
#include "window.h"

#define cmdcmp(command) !strnicmp(cmd, command, strlen(command))

void RunCommand(const char *cmdstr) {
	static std::mutex mutex;
	std::lock_guard<std::mutex> lock(mutex);

	std::string command = cmdstr;

	if (command.empty())
		return;

	if (RakBot::app()->getEvents()->onRunCommand(command))
		return;

	RakClientInterface *rakClient = RakBot::app()->getRakClient();
	Bot *bot = RakBot::app()->getBot();

	if (command[0] != '!') {
		bot->sendInput(command);
		return;
	}

	std::string s = command.substr(1, command.length() - 1);
	const char *cmd = s.c_str();

	// ВЫЙТИ ИЗ КЛИЕНТА
	if (cmdcmp("quit")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда выхода из бота, не требует аргументов",
				"Помощь",
				MB_ICONASTERISK);
			return;
		}

		RakBot::app()->exit();
		return;
	}

	if (cmdcmp("keeponline")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда контроля онлайна бота (сколько времени в часу бот работает и когда).\n"
				"Требует 2 аргумента: минута старта и время работы в минутах. То есть, если ввести \n"
				"\"!keeponline 10 30\", бот будет заходить каждый час в 10-ю минуту и работать 30 минут (до 40-й минуты).",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int keepOnlineTime;

		if (sscanf(cmd, "%*s%d%d", &vars.keepOnlineBegin, &keepOnlineTime) < 2) {
			vars.keepOnlineEnabled = false;
			RakBot::app()->log("[RAKBOT] Введите: !keeponline [минута старта] [время работы в минутах]");
			return;
		}

		if (keepOnlineTime < 0 || keepOnlineTime > 60) {
			vars.keepOnlineEnabled = false;
			RakBot::app()->log("[RAKBOT] Время работы может быть максимум 60 минут!");
			return;
		}

		vars.keepOnlineEnd = vars.keepOnlineBegin + keepOnlineTime;

		if (vars.keepOnlineEnd > 59) {
			vars.keepOnlineEnd %= 60;
			vars.keepOnlineBeginAfterEnd = true;
		}

		vars.keepOnlineEnabled ^= true;

		if (vars.keepOnlineEnabled) {
			char msg[512];
			snprintf(msg, sizeof(msg), "[RAKBOT] Бот будет работать с %d до %d минуты%s",
				vars.keepOnlineBegin, vars.keepOnlineEnd, vars.keepOnlineBeginAfterEnd ? " следующего часа" : "");
			RakBot::app()->log(msg);
		} else {
			RakBot::app()->log("[RAKBOT] Диапазон онлайна отключен");
		}

		return;
	}

	// ANTIAFK
	if (cmdcmp("aafk")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения АнтиАФК, не требует аргументов",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.antiAfkEnabled ^= 1;

		if (vars.antiAfkEnabled)
			RakBot::app()->log("[RAKBOT] AntiAFK включен");
		else
			RakBot::app()->log("[RAKBOT] AntiAFK отключен");
		return;
	}

	// NOAFK
	if (cmdcmp("noafk")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения NoAFK, не требует аргументов",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.noAfk ^= 1;
		if (vars.noAfk)
			RakBot::app()->log("[RAKBOT] NoAFK включен");
		else
			RakBot::app()->log("[RAKBOT] NoAFK отключен");
		return;
	}

	// SPAWN

	if (cmdcmp("reqspawn")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда запроса спавна бота, не требует аргументов",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		bot->requestSpawn();
		vars.waitForRequestSpawnReply = true;
		return;
	}

	if (cmdcmp("spawn")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда спавна бота, не требует аргументов",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		bot->spawn();
		return;
	}

	if (cmdcmp("reqclass")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда выбора класса, требует 1 аргумент: ID класса",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int classId;
		if (sscanf(cmd, "%*s%d", &classId) < 1) {
			RakBot::app()->log("[RAKBOT] Введите ID класса");
			return;
		}

		bot->requestClass(classId);
		RakBot::app()->log("[RAKBOT] Выбран класс %d", classId);
		return;
	}

	if (cmdcmp("sendpick")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда поднятия пикапа, требует 1 аргумент: ID пикапа",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int pickupId;
		if (sscanf(cmd, "%*s%d", &pickupId) < 1) {
			RakBot::app()->log("[RAKBOT] Отправка пикапа: введите ID пикапа");
			return;
		}

		RakBot::app()->log("[RAKBOT] Отправка пикапа с ID %d", pickupId);
		Pickup *pickup = RakBot::app()->getPickup(pickupId);
		bot->pickUpPickup(pickup, false);
		return;
	}

	if (cmdcmp("reloadscripts")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда перезагрузки Lua скриптов",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		UnloadScripts();
		LoadScripts();
		return;
	}

	if (cmdcmp("sleep")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения анимации сна, работает после спавна и переподключения",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		Bot *bot = RakBot::app()->getBot();
		PlayerAnimation *botAnim = bot->getAnimation();

		vars.sleepEnabled ^= true;

		if (vars.sleepEnabled) {
			botAnim->setAnimId(390);
			botAnim->setAnimFlags(4356);
			RakBot::app()->log("[RAKBOT] Сон включен");
		} else {
			botAnim->setAnimId(1189);
			botAnim->setAnimFlags(33000);
			RakBot::app()->log("[RAKBOT] Сон отключен");
		}

		return;
	}

	// SPAWN CAR
	if (cmdcmp("spawncar")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда спавна автомобиля (палится админам, да и по сути бесполезна, но пусть будет).\n"
				"Требует 1 аргумент: ID транспортного средства",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int carid = std::strtoul(&cmd[5], nullptr, 10);

		RakNet::BitStream bsData;
		bsData.Write(carid);
		rakClient->RPC(&RPC_VehicleDestroyed, &bsData, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);

		RakBot::app()->log("[RAKBOT] Запрос спавна транспорта с ID %d", carid);

		return;
	}

	// TELEPORT
	if (cmdcmp("tp")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда телепортации бота, принимает 3 аргумента, которые являются X, Y и Z координатами.\n"
				"Для дробных чисел используется запятая!",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		float position[3];

		if (sscanf(cmd, "%*s%f%f%f", &position[0], &position[1], &position[2]) < 3) {
			RakBot::app()->log("[RAKBOT] Телепорт: введите координаты через пробел");
			return;
		}

		bot->teleport(position[0], position[1], position[2]);

		char buf[512];
		sprintf(buf, "[RAKBOT] Бот телепортирован на координаты (%0.2f; %0.2f; %0.2f)", position[0], position[1], position[2]);
		RakBot::app()->log(buf);
		return;
	}

	// SAVE COORDS
	if (cmdcmp("scoords")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда сохранения координат для телепорта после спавна,\n"
				"принимает 3 аргумента, которые являются X, Y и Z координатами.\n"
				"Для дробных чисел используется запятая!",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		float pos[3];

		if (sscanf(cmd, "%*s%f%f%f", &pos[0], &pos[1], &pos[2]) < 3) {
			RakBot::app()->log("[RAKBOT] Сохранение позиции: введите координаты через пробел");
			return;
		}

		vect3_copy(pos, vars.savedCoords);
		vars.savedTeleportEnabled ^= true;

		if (vars.savedTeleportEnabled) {
			char szBuf[512];
			sprintf(szBuf, "[RAKBOT] Координаты (%0.2f; %0.2f; %0.2f) сохранены",
				vars.savedCoords[0], vars.savedCoords[1], vars.savedCoords[2]);
			RakBot::app()->log(szBuf);
			RakBot::app()->log("[RAKBOT] После переподключения бот автоматически вернется на данные координаты");
		} else {
			RakBot::app()->log("[RAKBOT] Телепорт на сохраненные координаты отключен");
		}
		return;
	}

	// ROUTE

	if (cmdcmp("routedelay")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки задержки отправки пакетов при воспроизведении маршрута"
				"Принимает 1 аргумент: задержка обновления в миллисекундах",
				"Помощь",
				MB_ICONASTERISK);
			return;
		}

		int delay;
		if (sscanf(cmd, "%*s%d", &delay) < 1) {
			RakBot::app()->log("[RAKBOT] Задержка маршрута: введите задержку воспроизведения маршрута");
			return;
		}
		vars.routeUpdateDelay = delay;
		RakBot::app()->log("[RAKBOT] Задержка маршрута: установлена задержка %d", vars.routeUpdateDelay);
		if (vars.routeUpdateDelay < vars.mainDelay) {
			RakBot::app()->log("[WARNING] Задержка воспроизведения маршрута (%d) не может быть меньше основной задержки обновления (%d)!", vars.routeUpdateDelay, vars.mainDelay);
		}
		return;
	}

	if (cmdcmp("routecount")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки количества повторов отправки пакетов при воспроизведении маршрута"
				"Принимает 1 аргумент: количество повторов отправки пакетов",
				"Помощь",
				MB_ICONASTERISK);
			return;
		}

		int count;
		if (sscanf(cmd, "%*s%d", &count) < 1) {
			RakBot::app()->log("[RAKBOT] Повтор пакетов маршрута: введите количество повторов отправки пакетов");
			return;
		}
		vars.routeUpdateCount = count;
		RakBot::app()->log("[RAKBOT] Повтор пакетов маршрута: отправка пакетов будет выполняться %d раз", vars.routeUpdateCount);
		return;
	}

	if (cmdcmp("routeloop")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения повтора при воспроизведении маршрута.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.routeLoop ^= 1;
		if (vars.routeLoop) {
			RakBot::app()->log("[RAKBOT] Повтор маршрута включен");
		} else {
			RakBot::app()->log("[RAKBOT] Повтор маршрута отключен");
		}
		return;
	}

	if (cmdcmp("route")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда запуска маршрута, принимает 2 аргумента: имя файла маршрута (без расширения) и скорость.\n"
				"Скорость необходимо подстраивать под каждый ПК отдельно, универсального значения НЕТ!\n\n"
				"Пауза - \"!route +pause\"\nВозобновление - \"!route +resume\"",
				"Помощь",
				MB_ICONASTERISK);

			return;
		} else if (strstr(cmd, "+pause")) {
			if (!vars.routeEnabled) {
				RakBot::app()->log("[WARNING] Сохраненный маршрут уже остановлен");
				return;
			}

			vars.routeEnabled = false;
			bot->getKeys()->reset();
			bot->getAnimation()->reset();
			for (int i = 0; i < 3; i++)
				bot->setSpeed(i, 0.f);
			bot->sync();
			vars.syncAllowed = true;
			return;
		} else if (strstr(cmd, "+resume")) {
			if (vars.routeEnabled) {
				RakBot::app()->log("[WARNING] Сохраненный маршрут уже запущен");
				return;
			}

			if (vars.routeData.size() < 1) {
				RakBot::app()->log("[ERROR] Сначала загрузите маршрут!");
				return;
			}

			vars.routeEnabled = true;
			vars.syncAllowed = false;
			RakBot::app()->log("[RAKBOT] Сохраненный маршрут продолжил работу");
			return;
		}

		vars.routeEnabled = false;
		bot->getKeys()->reset();
		bot->getAnimation()->reset();
		for (int i = 0; i < 3; i++)
			bot->setSpeed(i, 0.f);
		bot->sync();
		vars.syncAllowed = true;

		char routeFile[64];
		if (sscanf(cmd, "%*s%s", routeFile) < 1) {
			RakBot::app()->log("[RAKBOT] Сохраненный маршрут: запуск командой !route <файл> <скорость>");
			RakBot::app()->log("[RAKBOT] Сохраненный маршрут: остановлен");
			return;
		}

		LoadRoute(routeFile);

		if (vars.routeData.size() > 0) {
			vars.routeEnabled = true;
			vars.syncAllowed = false;
			vars.routeIndex = 0;

			RakBot::app()->log("[RAKBOT] Сохраненный маршрут запущен");
		} else {
			RakBot::app()->log("[RAKBOT] Сохраненный маршрут: файл маршрутов пуст или недоступен");
		}
		return;
	}

	if (cmdcmp("buswork")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда начала работы водителем автобуса.\n"
				"Введите \"!route\" для подробной информации",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!SampRpFuncs::isSampRpServer()) {
			RakBot::app()->log("[ERROR] Данная функция предназначена только для серверов Samp-Rp.Ru");
			return;
		}

		vars.busWorkerRoute = std::strtoul(&cmd[8], nullptr, 10);

		switch (vars.busWorkerRoute) {
			case 0:
				RakBot::app()->log("[RAKBOT] ============[Автоматический бот автобуса]=============");
				RakBot::app()->log("[RAKBOT] Введите: !buswork [номер маршрута]. Номера маршрутов:");
				RakBot::app()->log("[RAKBOT] 1 - городской ЛС");
				RakBot::app()->log("[RAKBOT] 2 - городской СФ");
				RakBot::app()->log("[RAKBOT] 3 - городской ЛВ");
				RakBot::app()->log("[RAKBOT] 4 - междугородний ЛС-СФ");
				RakBot::app()->log("[RAKBOT] 5 - междугородний ЛС-ЛВ");
				RakBot::app()->log("[RAKBOT] 6 - междугородний СФ-ЛВ");
				RakBot::app()->log("[RAKBOT] 7 - пригородный ЛС-ФК");
				RakBot::app()->log("[RAKBOT] 8 - пригородный ЛС-ЗАВОДЫ");
				RakBot::app()->log("[RAKBOT] ============[Автоматический бот автобуса]=============");
				RakBot::app()->log("[RAKBOT] *Автоматический бот предназначен только для серверов Samp-Rp.Ru");
				return;

			case 1:
				DoCoordMaster(true, 1258.83f, 10.07f, 10.07f);
				vars.busWorkerBusModel = 437;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: городской ЛС");
				break;

			case 2:
				DoCoordMaster(true, 1985.03f, 96.93f, 23.82f);
				vars.busWorkerBusModel = 437;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: городской СФ");
				break;

			case 3:
				DoCoordMaster(true, 2778.17f, 1290.91f, 6.73f);
				vars.busWorkerBusModel = 437;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: городской ЛВ");
				break;

			case 4:
				vars.busWorkerRouteItem = 0;
				DoCoordMaster(true, 1654.91f, -1050.12f, 21.13f);
				vars.busWorkerBusModel = 431;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: междугородний ЛС-СФ");
				break;

			case 5:
				vars.busWorkerRouteItem = 1;
				DoCoordMaster(true, 1654.91f, -1050.12f, 21.13f);
				vars.busWorkerBusModel = 431;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: междугородний ЛС-ЛВ");
				break;

			case 6:
				vars.busWorkerRouteItem = 2;
				DoCoordMaster(true, 1654.91f, -1050.12f, 21.13f);
				vars.busWorkerBusModel = 431;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: междугородний СФ-ЛВ");
				break;

			case 7:
				vars.busWorkerRouteItem = 3;
				DoCoordMaster(true, 1654.91f, -1050.12f, 21.13f);
				vars.busWorkerBusModel = 431;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: пригородный ЛС-ФК");
				break;

			case 8:
				vars.busWorkerRouteItem = 4;
				DoCoordMaster(true, 1654.91f, -1050.12f, 21.13f);
				vars.busWorkerBusModel = 431;
				RakBot::app()->log("[RAKBOT] Выбран маршрут автобуса: пригородный ЛС-ЗАВОД");
				break;
		}
		return;
	}

	if (cmdcmp("setwork")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда устройства на работу.\n"
				"Введите \"!setwork\" для подробной информации",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.iSetWorkIndex = std::strtoul(&cmd[8], nullptr, 10);

		if (!vars.iSetWorkIndex) {
			RakBot::app()->log("[RAKBOT] !setwork 1 - водитель автобуса");
			RakBot::app()->log("[RAKBOT] !setwork 2 - таксист");
			RakBot::app()->log("[RAKBOT] !setwork 3 - продавец хот-догов");
			RakBot::app()->log("[RAKBOT] !setwork 4 - развозчик продуктов");
			RakBot::app()->log("[RAKBOT] !setwork 5 - механик");
			RakBot::app()->log("[RAKBOT] !setwork 6 - инкассатор");
			RakBot::app()->log("[RAKBOT] !setwork 7 - прораб");
			RakBot::app()->log("[RAKBOT] !setwork 8 - тренер");
			RakBot::app()->log("[RAKBOT] !setwork 9 - дальнобойщик");
			return;
		}

		RakBot::app()->log("[RAKBOT] Устройство на работу %d", vars.iSetWorkIndex);
		DoCoordMaster(true, 1480.00f, -1771.00f, 18.00f);
		return;
	}

	if (cmdcmp("flood")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения флудера.\n"
				"Введите \"!flood\" для подробной информации",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		std::string str = cmd;
		std::smatch matches;
		std::regex_search(str, matches, std::regex("\\S+\\s+(\\d+)\\s+(\\d+)\\s+(.+)"));

		if (matches.size() != 4) {
			if (!vars.floodEnabled) {
				RakBot::app()->log("[RAKBOT] !flood 1 <задержка> <текст> - флуд в чат с указанной задержкой");
				RakBot::app()->log("[RAKBOT] !flood 2 <задержка> <текст> - флуд в SMS с указанной задержкой");
				RakBot::app()->log("[RAKBOT] !flood - отключить флудер");
			} else {
				RakBot::app()->log("[RAKBOT] Флудер отключен");
				vars.floodEnabled = 0;
			}
			return;
		}

		vars.floodMode = std::stoul(matches[1]);
		vars.floodDelay = std::stoul(matches[2]);
		vars.floodText = matches[3];
		Trim(vars.floodText);

		switch (vars.floodMode) {
			case 0:
				RakBot::app()->log("[RAKBOT] Флудер отключен");
				vars.floodEnabled = 0;
				break;

			case 1:
				RakBot::app()->log("[RAKBOT] Включен флудер в чат");
				vars.floodEnabled = 1;
				break;

			case 2:
				RakBot::app()->log("[RAKBOT] Включен флудер в SMS");
				vars.floodEnabled = 1;
				break;
		}
		return;
	}

	if (cmdcmp("atm")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда получения баланса в банкомате.\n"
				"Введите \"!atm\" для подробной информации",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!SampRpFuncs::isSampRpServer()) {
			RakBot::app()->log("[ERROR] Данная функция предназначена только для серверов Samp-Rp.Ru");
			return;
		}

		int atmCity;

		if (sscanf(cmd, "%*s%d", &atmCity) < 1) {
			RakBot::app()->log("[RAKBOT] !atm 1 - получение баланса в банкомате ЛС");
			RakBot::app()->log("[RAKBOT] !atm 2 - получение баланса в банкомате СФ");
			RakBot::app()->log("[RAKBOT] !atm 3 - получение баланса в банкомате ЛВ");
			vars.getBalanceEnabled = false;
			return;
		}

		int sel = atmCity - 1;

		if (sel == -1) {
			vars.getBalanceEnabled = false;
			return;
		}

		float atm[3][3] = {
			{ 1919.98f, -1765.62f, 13.55f },
			{ -2032.73f, 159.74f, 29.04f },
			{ 2853.26f, 1286.76f, 11.39f }
		};

		DoCoordMaster(true, atm[sel][0], atm[sel][1], atm[sel][2]);
		vars.getBalanceEnabled = true;
		RakBot::app()->log("[RAKBOT] Телепорт к банкомату...");
		return;
	}

	if (cmdcmp("coord")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда телепортации бота коордмастером, принимает 3 аргумента, которые являются X, Y и Z координатами.\n"
				"Для дробных чисел используется запятая!",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		float pos[3];
		if (sscanf(cmd, "%*s%f%f%f", &pos[0], &pos[1], &pos[2]) < 3) {
			RakBot::app()->log("[RAKBOT] CoordMaster: введите координаты через пробел");
			return;
		}

		bool coordMasterToggle = (vars.coordMasterEnabled != true);
		DoCoordMaster(coordMasterToggle, pos[0], pos[1], pos[2]);
		return;
	}

	// ПЕРЕПОДКЛЮЧИТЬСЯ
	if (cmdcmp("rejoin")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда переподключения к серверу, не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		bot->disconnect(false);
		bot->reconnect(vars.reconnectDelay);
		return;
	}

	// УСТАНОВИТЬ ВРЕМЯ РЕКОННЕКТА
	if (cmdcmp("setrjtime")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки времени ожидания перед переподключением к серверу.\n"
				"В качестве аругмента принимает время ожидания в секундах",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int reconnectTime;

		if (sscanf(cmd, "%*s%d", &reconnectTime) < 1) {
			RakBot::app()->log("[RAKBOT] Время переподключения: укажите время переподключения");
			return;
		}

		if (reconnectTime < 0) {
			return;
		}

		vars.reconnectDelay = reconnectTime * 1000;
		RakBot::app()->log("[RAKBOT] Время переподключения: установлена задержка %d секунд", reconnectTime);
		return;
	}

	// УСТАНОВКА ЗДОРОВЬЯ
	if (cmdcmp("sethp")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки количества здоровья боту.\n"
				"В качестве аргумента принимает целое число, равное требуемому количеству здоровья",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int health;
		if (sscanf(cmd, "%*s%d", &health) < 1) {
			RakBot::app()->log("[RAKBOT] Установка здоровья: укажите уровень здоровья");
			return;
		}

		if (health < 0 || health > 100) {
			RakBot::app()->log("[RAKBOT] Уровень здоровья должен быть в диапазоне от 0 до 100");
			return;
		}

		if (!bot->isSpawned())
			return;

		bot->setHealth(static_cast<uint8_t>(health));
		bot->sync();
		return;
	}

	// СПИСОК ИГРОКОВ
	if (cmdcmp("players")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода списка игроков, не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isConnected()) {
			RakBot::app()->log("[RAKBOT] Список игроков: бот не подключен к серверу!");
			return;
		}

		RakBot::app()->log("[RAKBOT] === СПИСОК ИГРОКОВ ===");
		RakBot::app()->log("[RAKBOT] ID * НИК * ПИНГ * ЛВЛ");

		if (bot->isConnected())
			RakBot::app()->log("[RAKBOT] %d * %s * %d * %d", bot->getPlayerId(), bot->getName().c_str(), bot->getInfo()->getPing(), bot->getInfo()->getScore());

		for (int i = 0; i < MAX_PLAYERS; i++) {
			Player *player = RakBot::app()->getPlayer(i);
			if (player == nullptr)
				continue;

			RakBot::app()->log("[RAKBOT] %d * %s * %d * %d", i, player->getName().c_str(), player->getInfo()->getPing(), player->getInfo()->getScore());
		}

		RakBot::app()->log("[RAKBOT] === [ВСЕГО: %d] ===", RakBot::app()->getPlayersCount());

		return;
	}

	if (cmdcmp("quest")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения прохождения квеста, не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.bQuestEnabled ^= 1;
		if (vars.bQuestEnabled)
			RakBot::app()->log("[RAKBOT] Прохождение квеста включено. Для начала нажмите спавн");
		else
			RakBot::app()->log("[RAKBOT] Прохождение квеста отключено");
		return;
	}

	if (cmdcmp("loadcars")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения загрузки машин ботом грузчика, не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.botLoaderCheckVans ^= 1;
		if (vars.botLoaderCheckVans) {
			RakBot::app()->log("[RAKBOT] Включена загрузка машин ботом грузчика");
		} else {
			RakBot::app()->log("[RAKBOT] Отключена загрузка машин ботом грузчика");
		}
		return;
	}

	if (cmdcmp("loadcount")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки лимита мешков боту грузчику (после достижения забирает ЗП и работает дальше).\n"
				"В качестве аргумента принимает целое число: количество мешков.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int limit = std::strtoul(&cmd[10], nullptr, 10);
		vars.botLoaderLimit = limit;
		RakBot::app()->log("[RAKBOT] Установлен лимит мешков: %d", limit);
		return;
	}

	if (cmdcmp("picks")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода списка пикапов, не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int count = 0;
		RakBot::app()->log("[RAKBOT] === СПИСОК ПИКАПОВ ===");
		RakBot::app()->log("[RAKBOT] ID * МОДЕЛЬ * ТИП * РАССТОЯНИЕ * ПОЗИЦИЯ");
		for (int i = 0; i < MAX_PICKUPS; i++) {
			Pickup *pickup = RakBot::app()->getPickup(i);
			if (pickup == nullptr)
				continue;

			RakBot::app()->log("[RAKBOT] %d * %d * %d * %.2f * (%.2f; %.2f; %.2f)",
				i, pickup->getModel(), pickup->getType(), bot->distanceTo(pickup),
				pickup->getPosition(0), pickup->getPosition(1), pickup->getPosition(2));
			count++;
		}
		RakBot::app()->log("[RAKBOT] === [ВСЕГО: %d] ===", count);

		return;
	}

	if (cmdcmp("press")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда отправки нажатия игровой кнопки. Варианты ввода:\n\n"
				"!press <ID клавиши> - нажатие кнопки по ID\n(посмотреть на http://wiki.sa-mp.com/wiki/Keys)\n\n"
				"!press Y - нажатие клавиши Y\n"
				"!press N - нажатие клавиши N\n"
				"!press H - нажатие клавиши сигнала\n"
				"!press S - нажатие клавиши пробел\n"

				"!press U - нажатие клавиши вверх\n"
				"!press R - нажатие клавиши вправо\n"
				"!press D - нажатие клавиши вниз\n"
				"!press L - нажатие клавиши влево\n",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isConnected()) {
			RakBot::app()->log("[ERROR] Нажатие клавиши: бот должен быть подключен к серверу!");
			return;
		}

		uint8_t weapon = 0;
		uint16_t keys = 0;
		uint16_t upDownKey = 0;
		uint16_t leftRightKey = 0;

		switch (cmd[6]) {
			case 'Y':
				weapon = 64;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки Y...");
				break;

			case 'N':
				weapon = 128;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки N...");
				break;

			case 'H':
				weapon = 192;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки сигнала...");
				break;

			case 'S':
				keys = 8;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки пробел...");
				break;

			case 'U':
				upDownKey = -128;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки вверх...");
				break;

			case 'R':
				leftRightKey = 128;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки вправо...");
				break;

			case 'D':
				upDownKey = 128;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки вниз...");
				break;

			case 'L':
				leftRightKey = -128;
				RakBot::app()->log("[RAKBOT] Нажатие кнопки влево...");
				break;

			default:
			{
				keys = static_cast<uint16_t>(std::strtoul(&cmd[6], nullptr, 10));

				if (keys == 0) {
					RakBot::app()->log("[RAKBOT] Введите ID клавиши!");
					return;
				}

				RakBot::app()->log("[RAKBOT] Нажатие кнопки с ID: %d...", keys);
				break;
			}
		}

		bot->getKeys()->setKeyId(keys);
		bot->getKeys()->setLeftRightKey(leftRightKey);
		bot->getKeys()->setUpDownKey(upDownKey);

		uint8_t currentWeapon = bot->getWeapon();
		bot->setWeapon(weapon);
		bot->sync();

		RakBot::app()->getEvents()->defCallAdd(500, false, [bot, currentWeapon](DefCall *) {
			if (!bot->isConnected())
				return;

			bot->getKeys()->reset();
			bot->setWeapon(currentWeapon);
		});

		return;
	}

	if (cmdcmp("reqid")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда указания требуемого ID, проверяется при входе (если не подходит - переподключение, пока не будет подхдящий).\n"
				"Принимает 2 аргумента: минимальный ID и максимальный ID соответственно.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (sscanf(cmd, "%*s%d%d", &vars.minId, &vars.maxId) < 2) {
			RakBot::app()->log("[RAKBOT] Проверка ID отключена");
			vars.checkIdEnabled = false;
		} else {
			RakBot::app()->log("[RAKBOT] Проверка ID включена: %d-%d", vars.minId, vars.maxId);
			vars.checkIdEnabled = true;
		}

		return;
	}

	if (cmdcmp("reqonline")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда указания требуемого онлайна, проверяется при входе (если не подходит - переподключение, пока не будет подхдящий).\n"
				"Принимает 2 аргумента: минимальный онлайн и максимальный онлайн соответственно.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (sscanf(cmd, "%*s%d%d", &vars.minOnline, &vars.maxOnline) < 2) {
			RakBot::app()->log("[RAKBOT] Проверка онлайна отключена");
			vars.checkOnlineEnabled = false;
		} else {
			RakBot::app()->log("[RAKBOT] Проверка онлайна включена: %d-%d", vars.minOnline, vars.maxOnline);
			vars.checkOnlineEnabled = true;
		}
		return;
	}

	if (cmdcmp("instream")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода игроков поблизости, не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int playerCount = 0;

		RakBot::app()->log("[RAKBOT] ===================[ИГРОКИ РЯДОМ]===================");

		RakBot::app()->log("[RAKBOT] %-3s * %-24s * %-3s * %-16s * %s", "ID", "НИК", "ЛВЛ", "СТАТУС", "ПОЗИЦИЯ");

		for (int i = 0; i < MAX_PLAYERS; i++) {
			Player *player = RakBot::app()->getPlayer(i);
			if (player == nullptr)
				continue;

			if (!player->isInStream())
				continue;

			std::stringstream ss;
			ss << player->getPlayerStateName();

			if (player->getPlayerState() == PLAYER_STATE_DRIVER || player->getPlayerState() == PLAYER_STATE_PASSENGER)
				ss << "[" << player->getVehicle()->getVehicleId() << "]";

			char positionBuffer[64];
			snprintf(positionBuffer, sizeof(positionBuffer), "(%.2f; %.2f; %.2f)", player->getPosition(0), player->getPosition(1), player->getPosition(2));

			RakBot::app()->log("[RAKBOT] %-3d * %-24s * %-3d * %-16s * %s", i, player->getName().c_str(), player->getInfo()->getScore(), ss.str().c_str(), positionBuffer);
			playerCount++;
		}
		if (playerCount == 0) {
			RakBot::app()->log("[RAKBOT] Рядом нет игроков :(");
			RakBot::app()->log("[RAKBOT] ===================[ИГРОКИ РЯДОМ]===================");
		} else {
			RakBot::app()->log("[RAKBOT] ====================[ВСЕГО: %3d]====================", playerCount);
		}
		return;
	}

	if (cmdcmp("autopick")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения автоподнятия пикапов, когда бот оказался на нем. Не принимает аргументы.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.autoPickEnabled ^= true;

		if (vars.autoPickEnabled) {
			RakBot::app()->log("[RAKBOT] Автоподнятие пикапов: включено");
		} else {
			RakBot::app()->log("[RAKBOT] Автоподнятие пикапов: отключено");
		}

		return;
	}

	if (cmdcmp("timestamp")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения вывода времени в чат. Не принимает аргументы.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.timeStamp ^= 1;
		if (vars.timeStamp) {
			RakBot::app()->log("[RAKBOT] Время в чате включено");
		} else {
			RakBot::app()->log("[RAKBOT] Время в чате отключено");
		}
	}

	// INFO
	if (cmdcmp("info")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода информации об игроке. В качестве аргумента принимает ID игрока",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int playerId;

		if (sscanf(cmd, "%*s%d", &playerId) < 1) {
			RakBot::app()->log("[RAKBOT] Информация об игроке: введите ID");
			return;
		}

		if (playerId < 0 || playerId >= MAX_PLAYERS) {
			RakBot::app()->log("[RAKBOT] Информация об игроке: неверный ID");
			return;
		}

		Player *player = RakBot::app()->getPlayer(playerId);
		if (player == nullptr) {
			RakBot::app()->log("[RAKBOT] Информация об игроке: игрок не найден!");
			return;
		}

		RakBot::app()->log("[RAKBOT] =====[Информация о игроке]=====");
		RakBot::app()->log("[RAKBOT]  Ник: %s    ID: %d", player->getName().c_str(), playerId);

		char szBuf[256];
		snprintf(szBuf, sizeof(szBuf), "[RAKBOT]  Координаты: %f, %f, %f",
			player->getPosition(0), player->getPosition(1), player->getPosition(2));
		RakBot::app()->log(szBuf);

		RakBot::app()->log("[RAKBOT]  Здоровье: %d", player->getHealth());
		RakBot::app()->log("[RAKBOT]  Броня: %d", player->getArmour());
		RakBot::app()->log("[RAKBOT]  Анимация: %d", player->getAnimation()->getAnimId());
		RakBot::app()->log("[RAKBOT] =====[Информация о игроке]=====");

		return;
	}

	if (cmdcmp("admins")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода списка админов, не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		RakBot::app()->log("[RAKBOT] =====[СПИСОК АДМИНОВ]=====");

		vars.adminsMutex.lock();
		size_t adminsCount = vars.admins.size();
		vars.adminsMutex.unlock();

		if (adminsCount == 0) {
			RakBot::app()->log("[RAKBOT] Нет админов в списке");
			RakBot::app()->log("[RAKBOT] =====[СПИСОК АДМИНОВ]=====");
		} else {
			RakBot::app()->log("[RAKBOT] # * НИК");
			for (int i = 0; i < static_cast<int>(adminsCount); i++) {
				vars.adminsMutex.lock();
				RakBot::app()->log("[RAKBOT] %d * %s", (i + 1), vars.admins[i].c_str());
				vars.adminsMutex.unlock();
			}
			RakBot::app()->log("[RAKBOT] ===========[ВСЕГО: %d]===========", adminsCount);
		}
		return;
	}

	if (cmdcmp("admonline")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда переключения действия при нахождении админа в сети. Не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		switch (vars.adminOnlineAction) {
			case 0:
				RakBot::app()->log("[RAKBOT] Переподключение, если админ в сети");
				vars.adminOnlineAction = 1;
				break;

			case 1:
				RakBot::app()->log("[RAKBOT] Выход, если админ в сети");
				vars.adminOnlineAction = 2;
				break;

			case 2:
				RakBot::app()->log("[RAKBOT] Бездействие, если админ в сети");
				vars.adminOnlineAction = 0;
				break;
		}

		return;
	}

	if (cmdcmp("admnear")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда переключения действия при нахождении админа рядом. Не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		switch (vars.adminNearAction) {
			case 0:
				RakBot::app()->log("[RAKBOT] Переподключение, если админ рядом");
				vars.adminNearAction = 1;
				break;

			case 1:
				RakBot::app()->log("[RAKBOT] Выход, если админ рядом");
				vars.adminNearAction = 2;
				break;

			case 2:
				RakBot::app()->log("[RAKBOT] Бездействие, если админ рядом");
				vars.adminNearAction = 0;
				break;
		}

		return;
	}

	// GOTO
	if (cmdcmp("goto")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда телепорта к игроку. В качестве аргумента принимает ID игрока.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		int playerId;

		if (sscanf(cmd, "%*s%d", &playerId) < 1) {
			RakBot::app()->log("[RAKBOT] Телепорт к игроку: введите ID");
			return;
		}

		if (playerId < 0 || playerId > MAX_PLAYERS) {
			RakBot::app()->log("[RAKBOT] Телепорт к игроку: неверный ID");
			return;
		}

		Player *player = RakBot::app()->getPlayer(playerId);
		if (player == nullptr) {
			RakBot::app()->log("[RAKBOT] Телепорт к игроку: игрок не найден!");
			return;
		}

		if (player->getPosition(0) == 0.f
			&& player->getPosition(1) == 0.f
			&& player->getPosition(2) == 0.f) {
			RakBot::app()->log("[RAKBOT] Телепорт к игроку: местоположение игрока неизвестно", playerId);
			return;
		}

		bot->teleport(player->getPosition(0), player->getPosition(1), player->getPosition(2));

		RakBot::app()->log("[RAKBOT] Телепорт к игроку: телепортирован к игроку %s[%d]", player->getName().c_str(), playerId);
		return;
	}

	// СПИСОК АВТОМОБИЛЕЙ
	if (cmdcmp("vlist")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода видимых транспортных средств. Не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int vehicleModel = 0;

		if (sscanf(cmd, "%*s%d", &vehicleModel) == 1) {
			if (vehicleModel < 400 || vehicleModel > 611) {
				RakBot::app()->log("[RAKBOT] Типом транспорта должно быть число от 400 до 611");
				return;
			}
		}

		int cmd_count = 0;

		if (vehicleModel)
			RakBot::app()->log("[RAKBOT] =====[ТРАНСПОРТ МОДЕЛИ %d]=====", vehicleModel);
		else
			RakBot::app()->log("[RAKBOT] =====[ТРАНСПОРТ]=====");

		RakBot::app()->log("[RAKBOT] ID * НАЗВАНИЕ * СТАТУС * ЦВЕТ * ДИСТАНЦИЯ * ПОЗИЦИЯ");
		for (uint16_t i = 0; i < MAX_VEHICLES; i++) {
			Vehicle *vehicle = RakBot::app()->getVehicle(i);
			if (vehicle == nullptr)
				continue;

			if (vehicleModel && vehicle->getModel() == vehicleModel || !vehicleModel) {
				RakBot::app()->log("[RAKBOT] %d * %s * %s * %d/%d * %.2f * (%.2f; %.2f; %.2f)",
					i, vehicle->getName().c_str(), vehicle->isDoorsOpened() ? "Открыта" : "Закрыта",
					vehicle->getFirstColor(), vehicle->getSecondColor(), bot->distanceTo(vehicle),
					vehicle->getPosition(0), vehicle->getPosition(1), vehicle->getPosition(2));
				cmd_count++;
			}
		}

		if (cmd_count)
			RakBot::app()->log("[RAKBOT] =====[ВСЕГО: %d]=====", cmd_count);
		else
			RakBot::app()->log("[RAKBOT] =====[ВСЕГО: 0]=====");

		return;
	}

	if (cmdcmp("toplace")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда телепорта к сохраненному в файле месту. В качестве аргумента принимает номер места.\n"
				"Места можно посмотреть с помощью команды \"!places\"",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		char szBuf[512];

		if (FILE *f = fopen(GetRakBotPath("places.txt").c_str(), "r")) {
			for (int i = 0; i < 300; i++) {
				if (fgets(szBuf, 128, f)) {
					strcpy(vars.teleportPlaces[i].szName, strtok(szBuf, "|"));

					for (int n = 0; n < 3; n++)
						vars.teleportPlaces[i].position[n] = std::strtof(strtok(NULL, "|"), nullptr);
				}
			}
			fclose(f);

			int iPlaceIndex = std::strtoul(&cmd[8], nullptr, 10);
			float *pos = vars.teleportPlaces[iPlaceIndex - 1].position;
			DoCoordMaster(true, pos[0], pos[1], pos[2]);

			sprintf(szBuf, "[RAKBOT] CoordMaster: телепорт на координаты (%0.2f; %0.2f; %0.2f)", vars.coordMasterTarget[0], vars.coordMasterTarget[1], vars.coordMasterTarget[2]);
			RakBot::app()->log(szBuf);
		}

		return;
	}

	if (cmdcmp("places")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда вывода мест, сохраненных в файле \"places.txt\". Не принимает аргументов.\n"
				"Формат записи мест:\n\n"
				"Название|X|Y|Z\n"
				"Ферма 1|10,0|-12,5|5,3",
				"Помощь",
				MB_ICONASTERISK);
			return;
		}

		char buf[128];
		if (FILE *f = fopen(GetRakBotPath("places.txt").c_str(), "r")) {
			for (int i = 0; i < 300; i++) {
				if (fgets(buf, 128, f)) {
					strcpy(vars.teleportPlaces[i].szName, strtok(buf, "|"));

					for (int n = 0; n < 3; n++)
						vars.teleportPlaces[i].position[n] = std::strtof(strtok(NULL, "|"), nullptr);
				}
			}
			fclose(f);

			for (int i = 0; i < 300; i++) {
				if (vars.teleportPlaces[i].szName[0] != NULL)
					RakBot::app()->log("[RAKBOT] !toplace %d - %s\n", i + 1, vars.teleportPlaces[i].szName);
			}
		}

		return;
	}

	// ПОСАДКА В АВТОМОБИЛЬ
	if (cmdcmp("seat")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда посадки бота в транспорт. В качестве аргумента принимает ID транспорта.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		int vehicleId;

		if (sscanf(cmd, "%*s%d", &vehicleId) < 1) {
			RakBot::app()->log("[RAKBOT] Посадка в машину: введите ID машины");
			return;
		}

		Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
		bot->enterVehicle(vehicle, 0);
		return;
	}

	if (cmdcmp("pseat")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда посадки бота в транспорт на пассажирское место. В качестве аргумента принимает ID транспорта.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		int vehicleId;

		if (sscanf(cmd, "%*s%d", &vehicleId) < 1) {
			RakBot::app()->log("[RAKBOT] Посадка в машину: введите ID машины");
			return;
		}

		Vehicle *vehicle = RakBot::app()->getVehicle(vehicleId);
		bot->enterVehicle(vehicle, 1);
		RakBot::app()->log("[RAKBOT] Посадка в машину с ID %d", vehicleId);
		return;
	}

	if (cmdcmp("antisat")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения антиголода. Не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.bAntiSat ^= 1;
		if (vars.bAntiSat)
			RakBot::app()->log("[RAKBOT] Антисытность включена");
		else
			RakBot::app()->log("[RAKBOT] Антисытность отключена");
	}

	if (cmdcmp("exit")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда выхода из транспорта. Не принимает аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		if (bot->getPlayerState() != PLAYER_STATE_DRIVER
			&& bot->getPlayerState() != PLAYER_STATE_PASSENGER) {
			RakBot::app()->log("[RAKBOT] Бот не находится в транспорте");
			return;
		}

		bot->exitVehicle();
		RakBot::app()->log("[RAKBOT] Бот вышел из транспорта");
		return;
	}

	if (cmdcmp("farm")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда начала работы на ферме. В качестве аргумента принмает ID фермы.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		FarmIndex = std::strtoul(&cmd[5], nullptr, 10);
		DoCoordMaster(true, FarmPos[FarmIndex][0], FarmPos[FarmIndex][1], FarmPos[FarmIndex][2]);

		vars.botFarmerEnabled = 1;
		vars.botFarmerAutomated = 1;
		FarmWork = 0;
		RakBot::app()->log("[RAKBOT] Телепорт на ферму %d", FarmIndex);

		return;
	}

	// ВЫБРАТЬ ПУНКТ В МЕНЮ
	if (cmdcmp("menu")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда выбора пункта меню. В качестве аргумента принимает номер пункта.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		RakNet::BitStream bsSend;
		bsSend.Write<int>(std::strtoul(&cmd[5], nullptr, 10));
		rakClient->RPC(&RPC_MenuSelect, &bsSend, HIGH_PRIORITY, RELIABLE, 0, FALSE, UNASSIGNED_NETWORK_ID, NULL);

		return;
	}

	if (cmdcmp("bank")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда пополнения баланса в банке. В качестве аргумента принимает сумму пополнения.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int moneyAmount;

		if (sscanf(cmd, "%*s%d", &moneyAmount) < 1) {
			RakBot::app()->log("[RAKBOT] Введите сумму для пополнения счета в банке");
			return;
		}

		DoCoordMaster(true, 1414.69f, -1700.48f, 13.54f);

		vars.iBankPutMoney = moneyAmount;
		RakBot::app()->log("[RAKBOT] Автоматическое пополнение баланса на %d вирт", vars.iBankPutMoney);
		return;
	}

	if (cmdcmp("parsenicks")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда парсинга игроков в файл. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int minLvl;

		if (cmd[11] == ' ' || cmd[11] == '\0') {
			minLvl = 0;
		} else {
			minLvl = atol(&cmd[11]);
		}

		FILE *fOut = fopen(GetRakBotPath("nicks.txt").c_str(), "w");

		int iCount = 0;
		for (int i = 0; i < MAX_PLAYERS; i++) {
			Player *player = RakBot::app()->getPlayer(i);
			if (player == nullptr)
				continue;

			if (player->getInfo()->getScore() < minLvl)
				continue;

			fprintf(fOut, "%s|%d\n", player->getName().c_str(), player->getInfo()->getScore());
			iCount++;
		}

		fclose(fOut);

		if (iCount == 0)
			RakBot::app()->log("[RAKBOT] Парсер ников: клиент не подключен к серверу или на сервере нет игроков");
		else
			RakBot::app()->log("[RAKBOT] Парсер ников: %d игроков записаны в файл \"nicks.txt\" в корневой папке бота", iCount);
		return;
	}

	if (cmdcmp("follow")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда повтора действий за игроком. В качестве аргумента принимает ID игрока",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (vars.stickEnabled) {
			RakBot::app()->log("[RAKBOT] Преследование: сначала отключите липучку");
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		int playerId;

		if (sscanf(cmd, "%*s%d", &playerId) < 1) {
			RakBot::app()->log("[RAKBOT] Преследование: введите ID игрока");
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		if (playerId < 0 || playerId >= MAX_PLAYERS) {
			RakBot::app()->log("[RAKBOT] Преследование: введите корректный ID игрока");
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		Player *player = RakBot::app()->getPlayer(playerId);
		if (player == nullptr) {
			RakBot::app()->log("[RAKBOT] Преследование: игрок %d не найден", vars.followPlayerID);
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		if (!player->isInStream()) {
			RakBot::app()->log("[RAKBOT] Преследование: игрок %d не виден", vars.followPlayerID);
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		vars.followPlayerID = playerId;
		vars.followEnabled ^= true;

		if (vars.followEnabled)
			RakBot::app()->log("[RAKBOT] Преследование: включено. Игрок: %s[%d]", player->getName().c_str(), vars.followPlayerID);
		else
			RakBot::app()->log("[RAKBOT] Преследование: остановлено");

		return;
	}

	if (cmdcmp("stick")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения липучки. В качестве аргумента принимает ID игрока",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (vars.followEnabled) {
			RakBot::app()->log("[RAKBOT] Липучка: сначала отключите преследование");
			RakBot::app()->log("[RAKBOT] Липучка: отключено");
			vars.stickEnabled = false;
			return;
		}

		int playerId;

		if (sscanf(cmd, "%*s%d", &playerId) < 1) {
			RakBot::app()->log("[RAKBOT] Липучка: введите ID игрока");
			RakBot::app()->log("[RAKBOT] Липучка: отключено");
			vars.stickEnabled = false;
			return;
		}

		if (playerId < 0 || playerId >= MAX_PLAYERS) {
			RakBot::app()->log("[RAKBOT] Липучка: введите корректный ID игрока");
			RakBot::app()->log("[RAKBOT] Липучка: отключено");
			vars.stickEnabled = false;
			return;
		}

		Player *player = RakBot::app()->getPlayer(playerId);
		if (player == nullptr) {
			RakBot::app()->log("[RAKBOT] Преследование: игрок %d не найден", vars.followPlayerID);
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		if (!player->isInStream()) {
			RakBot::app()->log("[RAKBOT] Преследование: игрок %d не виден", vars.followPlayerID);
			RakBot::app()->log("[RAKBOT] Преследование: отключено");
			vars.followEnabled = false;
			return;
		}

		vars.followPlayerID = playerId;
		vars.stickEnabled ^= true;

		if (vars.stickEnabled)
			RakBot::app()->log("[RAKBOT] Липучка: включена. Игрок: %s[%d]", player->getName().c_str(), vars.followPlayerID);
		else
			RakBot::app()->log("[RAKBOT] Липучка: остановлена");

		return;
	}

	if (cmdcmp("virtualworld")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения виртуального мира. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!SampRpFuncs::isSampRpServer()) {
			RakBot::app()->log("[ERROR] Данная функция предназначена только для серверов Samp-Rp.Ru");
			return;
		}

		vars.virtualWorld ^= 1;
		if (vars.virtualWorld) {
			bot->requestClass(rand() % 299);
			RakBot::app()->log("[RAKBOT] Виртуальный мир: включен");
		} else {
			RakBot::app()->log("[RAKBOT] Виртуальный мир: отключен");
		}
		return;
	}

	if (cmdcmp("botloader")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения бота грузчика. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!SampRpFuncs::isSampRpServer()) {
			RakBot::app()->log("[ERROR] Данная функция предназначена только для серверов Samp-Rp.Ru");
			return;
		}

		vars.botLoaderEnabled ^= true;
		if (vars.botLoaderEnabled) {
			DoCoordMaster(true, 2126.78f, -2281.03f, 24.88f);
			RakBot::app()->log("[RAKBOT] Бот грузчика: включен");
		} else {
			RakBot::app()->log("[RAKBOT] Бот грузчика: отключен");
			vars.sendBadSync = false;
		}
		return;
	}

	if (cmdcmp("skipdialog")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения пропуска диалогов. Подробнее: введите \"!skipdialog\"",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int skipDialogAction;

		if (sscanf(cmd, "%*s%d", &skipDialogAction) < 1) {
			RakBot::app()->log("[RAKBOT] Пропуск диалогов: ВВЕДИТЕ действие");
			RakBot::app()->log("[RAKBOT]   0 - нормальное отображение диалогов");
			RakBot::app()->log("[RAKBOT]   1 - отправка ENTER");
			RakBot::app()->log("[RAKBOT]   2 - отправка ESC");
			RakBot::app()->log("[RAKBOT]   3 - полное игнорирование");
			return;
		}

		if (skipDialogAction < 0 || skipDialogAction > 3) {
			RakBot::app()->log("[RAKBOT] Пропуск диалогов: введите ВЕРНОЕ действие");
			RakBot::app()->log("[RAKBOT]   0 - нормальное отображение диалогов");
			RakBot::app()->log("[RAKBOT]   1 - отправка ENTER");
			RakBot::app()->log("[RAKBOT]   2 - отправка ESC");
			RakBot::app()->log("[RAKBOT]   3 - полное игнорирование");
			return;
		}

		vars.skipDialog = skipDialogAction;

		switch (vars.skipDialog) {
			case 0:
				RakBot::app()->log("[RAKBOT] Пропуск диалогов: нормальное отображение диалогов");
				break;

			case 1:
				RakBot::app()->log("[RAKBOT] Пропуск диалогов: отправка ENTER");
				break;

			case 2:
				RakBot::app()->log("[RAKBOT] Пропуск диалогов: отправка ESC");
				break;

			case 3:
				RakBot::app()->log("[RAKBOT] Пропуск диалогов: игнорирование диалогов");
				break;
		}

		return;
	}

	if (cmdcmp("whereiscp")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда поиска чекпоинта. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (checkpoint.active || raceCheckpoint.active) {
			float *position = (checkpoint.active) ? (checkpoint.position) : (raceCheckpoint.position);
			RakBot::app()->log("[RAKBOT] Позиция чекпоинта: (%.2f; %.2f; %.2f)!", position[0], position[1], position[2]);
		} else {
			RakBot::app()->log("[RAKBOT] Поиск чекпоинта: чекпоинт неактивен!");
		}
		return;
	}

	if (cmdcmp("takecp")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда поднятия чекпоинта. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		bot->takeCheckpoint();
		return;
	}

	if (cmdcmp("cpm")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения чекпоинт мастера. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.checkPointMaster ^= 1;
		if (vars.checkPointMaster) {
			RakBot::app()->log("[RAKBOT] Чекпоинт мастер включен");
		} else {
			RakBot::app()->log("[RAKBOT] Чекпоинт мастер отключен");
		}
		return;
	}

	if (cmdcmp("antideath")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения антисмерти (бот не спавнится при 0 ХП). Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.antiDeath ^= 1;
		if (vars.antiDeath) {
			RakBot::app()->log("[RAKBOT] Антисмерть включена");
		} else {
			RakBot::app()->log("[RAKBOT] Антисмерть отключена");
		}
		return;
	}

	if (cmdcmp("botfarmer")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения бота фермера (включается уже на поле, для полной автоматизации используйте \"!farm\"). Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.botFarmerEnabled ^= 1;
		FarmWork = vars.botFarmerEnabled;

		if (vars.botFarmerEnabled) {
			RakBot::app()->log("[RAKBOT] Бот фермера включен");
		} else {
			RakBot::app()->log("[RAKBOT] Бот фермера отключен");
			vars.botFarmerAutomated = 0;
			vars.sendBadSync = false;
		}

		return;
	}

	if (cmdcmp("parsestat")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда сбора информации об аккаунте (только Samp-Rp). Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!SampRpFuncs::isSampRpServer()) {
			RakBot::app()->log("[ERROR] Данная функция предназначена только для серверов Samp-Rp.Ru");
			return;
		}

		vars.parseStatistic = true;
		bot->sendInput("/mm");
		return;
	}

	if (cmdcmp("map")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда открытия/закрытия карты. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!vars.mapWindowOpened) {
			ShowMapWindow();
		} else {
			CloseMapWindow();
		}
		return;
	}

	if (cmdcmp("farchat")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения дальнего чата (расширить дальность получения сообщений чата). Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.farChatEnabled ^= 1;
		if (vars.farChatEnabled) {
			RakBot::app()->log("[RAKBOT] Дальний чат отключен");
		} else {
			RakBot::app()->log("[RAKBOT] Дальний чат включен");
		}
		return;
	}

	if (cmdcmp("skipmsg")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения пропуска сообщений сервера в чате. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.ignoreServerMessages ^= 1;
		if (vars.ignoreServerMessages) {
			RakBot::app()->log("[RAKBOT] Пропуск сообщений сервера включен");
		} else {
			RakBot::app()->log("[RAKBOT] Пропуск сообщений сервера отключен");
		}
		return;
	}

	if (cmdcmp("badpos")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения искаженной синхронизации. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.sendBadSync ^= 1;
		if (vars.sendBadSync) {
			RakBot::app()->log("[RAKBOT] Искаженная позиция включена");
		} else {
			RakBot::app()->log("[RAKBOT] Искаженная позиция отключена");
		}
		return;
	}

	if (cmdcmp("smartinvis")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда включения/выключения невидимки. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		vars.smartInvis ^= 1;
		if (vars.smartInvis) {
			RakBot::app()->log("[RAKBOT] SmartInvis by 0x32789 (http://ugbase.eu) включен");
		} else {
			RakBot::app()->log("[RAKBOT] SmartInvis by 0x32789 (http://ugbase.eu) отключен");
		}
		return;
	}

	if (cmdcmp("autoschool")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда начала/завершения сдачи на права. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!SampRpFuncs::isSampRpServer()) {
			RakBot::app()->log("[ERROR] Данная функция предназначена только для серверов Samp-Rp.Ru");
			return;
		}

		vars.botAutoSchoolEnabled ^= true;
		if (vars.botAutoSchoolEnabled) {
			DoCoordMaster(true, -2026.00f, -101.00f, 35.00f);
			RakBot::app()->log("[RAKBOT] Начало сдачи экзамена на права. Телепорт к автошколе...");
		} else {
			RakBot::app()->log("[RAKBOT] Сдача экзамена на права принудительно завершена");
			vars.botAutoSchoolActive = 0;
		}
		return;
	}

	if (cmdcmp("botkill")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда убийства бота. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		if (!bot->isSpawned())
			return;

		bot->kill();
		return;
	}

	if (cmdcmp("debug")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда запуска окна отладки. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		AllocConsole();
		SetConsoleTitle("RakBot Debug");
		SetConsoleCP(1251);
		SetConsoleOutputCP(1251);

		freopen("CONOUT$", "w", stdout);
		freopen("CONIN$", "r", stdin);

		printf("* ===================================================== *\n");
		printf("  RakBot " RAKBOT_VERSION " debug console inited\n");
		printf("  RakBot.Ru\n");
		printf("* ===================================================== *\n");
		return;
	}


	if (cmdcmp("tdclick")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда клика по текстдраву. В качестве аргумента принимает ID текстдрава.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int textDrawId;

		if (sscanf(cmd, "%*s%d", &textDrawId) < 1) {
			RakBot::app()->log("[RAKBOT] Клик текстдрава: укажите ID");
			return;
		}

		bot->clickTextdraw(textDrawId);
		RakBot::app()->log("[RAKBOT] Клик текстдрава: кликнут текстдрав с ID %d", textDrawId);
		return;
	}

	if (cmdcmp("setnick")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки ника бота. В качестве аргумента принимает новый ник (до 20 символов).",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		char nickName[25];

		if (sscanf(cmd, "%*s%s", nickName) < 1) {
			RakBot::app()->log("[RAKBOT] Настройка ника: укажите новый ник");
			return;
		}

		RakBot::app()->getSettings()->setName(nickName);
		RakBot::app()->log("[RAKBOT] Настройка ника: установлен ник - %s", RakBot::app()->getSettings()->getName().c_str());
		return;
	}

	if (cmdcmp("setpass")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки пароля бота. В качестве аргумента принимает новый пароль (до 120 символов).",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		char loginPass[128];

		if (sscanf(cmd, "%*s%s", loginPass) < 1) {
			RakBot::app()->log("[RAKBOT] Настройка пароля: укажите новый пароль");
			return;
		}

		RakBot::app()->getSettings()->setLoginPassword(loginPass);
		RakBot::app()->log("[RAKBOT] Настройка пароля: установлен пароль - %s",
			RakBot::app()->getSettings()->getLoginPassword());
		return;
	}

	if (cmdcmp("setip")) {

		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установки IP сервера. В качестве аргумента принимает новый IP (формат адрес:порт).",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		char fullAddr[256];

		char addrName[256];
		int addrPort;

		if (sscanf(cmd, "%*s%s", fullAddr) < 1) {
			RakBot::app()->log("[RAKBOT] Настройка сервера: укажите новый адрес в формате IP:PORT");
			return;
		}

		char *pch = fullAddr;
		while (*pch) {
			if (*pch == ':') {
				*pch = 0;
				addrPort = std::strtoul(pch + 1, nullptr, 10);
			}
			pch++;
		}
		strcpy(addrName, fullAddr);

		if (strlen(addrName) < 1 || addrPort < 0 || addrPort > 65535) {
			RakBot::app()->log("[RAKBOT] Настройка сервера: неверный формат адреса");
			return;
		}

		RakBot::app()->getSettings()->getAddress()->setIp(addrName);
		RakBot::app()->getSettings()->getAddress()->setPort(static_cast<uint16_t>(addrPort));
		RakBot::app()->log("[RAKBOT] Настройка сервера: установлен сервер - %s:%d",
			RakBot::app()->getSettings()->getAddress()->getIp().c_str(),
			RakBot::app()->getSettings()->getAddress()->getPort());
		return;
	}

	if (cmdcmp("setweapon")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда установка оружия. В качестве аргумента принимает ID оружия.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		int weaponId;

		if (sscanf(cmd, "%*s%d", &weaponId) < 1) {
			RakBot::app()->log("[RAKBOT] Оружие: укажите ID оружия");
			return;
		}

		bot->setWeapon(weaponId);
		RakBot::app()->log("[RAKBOT] Оружие: установлено оружие с ID %d", weaponId);
		bot->sync();
		return;
	}

	if (cmdcmp("openlog")) {
		char dir[MAX_PATH];
		GetModuleFileName(NULL, dir, sizeof(dir));
		*strrchr(dir, '\\') = 0;

		std::stringstream ss;
		ss << "\"" << dir << "\\logs\\"
			<< RakBot::app()->getSettings()->getAddress()->getIp() << ";" << RakBot::app()->getSettings()->getAddress()->getPort() << "\\"
			<< RakBot::app()->getSettings()->getName() << ".log\"";
		std::string filePath = "/select," + ss.str();

		RakBot::app()->log("[RAKBOT] Файл лога: %s", ss.str().c_str());
		ShellExecute(g_hWndMain, "open", "explorer.exe", filePath.c_str(), dir, SW_SHOWMAXIMIZED);
		return;
	}

	if (cmdcmp("saveakk")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда сохранения аккаунта (аналогична кнопке в лаунчере). Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		HRESULT hResult;
		IShellLink *pShellLink = NULL;
		IPersistFile *pPersistFile = NULL;

		char szAddress[32];
		_snprintf_s(szAddress, sizeof(szAddress), "%s;%d",
			RakBot::app()->getSettings()->getAddress()->getIp().c_str(),
			RakBot::app()->getSettings()->getAddress()->getPort());

		CoInitialize(NULL);
		hResult = CoCreateInstance(CLSID_ShellLink, NULL, CLSCTX_INPROC_SERVER, IID_IShellLink, (void **)&pShellLink);
		CoUninitialize();

		if (FAILED(hResult)) {
			if (pShellLink)
				pShellLink->Release();

			RakBot::app()->log("[ERROR] Ошибка при сохранении аккаунта!");
			return;
		}

		hResult = pShellLink->QueryInterface(IID_IPersistFile, (LPVOID*)&pPersistFile);

		if (FAILED(hResult)) {
			if (pPersistFile)
				pPersistFile->Release();
			if (pShellLink)
				pShellLink->Release();

			RakBot::app()->log("[ERROR] Ошибка при сохранении аккаунта!");
			return;
		}

		char szLauncherPath[MAX_PATH];
		GetModuleFileName(NULL, szLauncherPath, sizeof(szLauncherPath));
		*strrchr(szLauncherPath, '\\') = 0;
		strcat(szLauncherPath, "\\RakLaunch.exe");
		hResult = pShellLink->SetPath(szLauncherPath);

		if (FAILED(hResult)) {
			if (pPersistFile)
				pPersistFile->Release();
			if (pShellLink)
				pShellLink->Release();

			RakBot::app()->log("[ERROR] Ошибка при сохранении аккаунта!");
			return;
		}

		char szAccountsPath[MAX_PATH];
		GetModuleFileName(NULL, (char *)&szAccountsPath, sizeof(szAccountsPath));
		strcpy(strrchr(szAccountsPath, '\\') + 1, "accounts");
		CreateDirectory(szAccountsPath, NULL);

		char szAccountsDataPath[MAX_PATH];
		strcpy(szAccountsDataPath, szAccountsPath);
		strcat(szAccountsDataPath, "\\data");
		CreateDirectory(szAccountsDataPath, NULL);
		SetFileAttributes(szAccountsDataPath, FILE_ATTRIBUTE_HIDDEN);

		char szAccountData[MAX_PATH];
		_snprintf(szAccountData, sizeof(szAccountData), "%s\\%s@%s.ini", szAccountsDataPath, RakBot::app()->getSettings()->getName().c_str(), szAddress);
		SaveConfig(szAccountData);

		hResult = pShellLink->SetArguments(szAccountData);

		if (FAILED(hResult)) {
			if (pPersistFile)
				pPersistFile->Release();
			if (pShellLink)
				pShellLink->Release();

			RakBot::app()->log("[ERROR] Ошибка при сохранении аккаунта!");
			return;
		}

		char szAccountLink[MAX_PATH];
		_snprintf(szAccountLink, sizeof(szAccountLink), "%s\\%s@%s.lnk", szAccountsPath, RakBot::app()->getSettings()->getName().c_str(), szAddress);

		wchar_t wszAccountLink[MAX_PATH];
		MultiByteToWideChar(CP_ACP, 0, szAccountLink, -1, wszAccountLink, MAX_PATH);

		hResult = pPersistFile->Save(wszAccountLink, TRUE);

		if (FAILED(hResult)) {
			if (pPersistFile)
				pPersistFile->Release();
			if (pShellLink)
				pShellLink->Release();

			RakBot::app()->log("[ERROR] Ошибка при сохранении аккаунта!");
			return;
		}

		RakBot::app()->log("[RAKBOT] Аккаунт успешно сохранен");
		return;
	}

	if (cmdcmp("delakk")) {
		if (strstr(cmd, "+help")) {
			MessageBox(
				g_hWndMain,
				"Команда удаления ярлыка текущего аккаунта. Не требует аргументов.",
				"Помощь",
				MB_ICONASTERISK);

			return;
		}

		char szAddress[32];
		_snprintf_s(szAddress, sizeof(szAddress), "%s;%d",
			RakBot::app()->getSettings()->getAddress()->getIp().c_str(),
			RakBot::app()->getSettings()->getAddress()->getPort());

		char szAccountsPath[MAX_PATH];
		GetModuleFileName(NULL, (char *)&szAccountsPath, sizeof(szAccountsPath));
		strcpy(strrchr(szAccountsPath, '\\') + 1, "accounts");
		CreateDirectory(szAccountsPath, NULL);

		char szAccountsDataPath[MAX_PATH];
		strcpy(szAccountsDataPath, szAccountsPath);
		strcat(szAccountsDataPath, "\\data");
		CreateDirectory(szAccountsDataPath, NULL);
		SetFileAttributes(szAccountsDataPath, FILE_ATTRIBUTE_HIDDEN);

		char szAccountData[MAX_PATH];
		_snprintf(szAccountData, sizeof(szAccountData), "%s\\%s@%s.ini", szAccountsDataPath, RakBot::app()->getSettings()->getName().c_str(), szAddress);

		char szAccountLink[MAX_PATH];
		_snprintf(szAccountLink, sizeof(szAccountLink), "%s\\%s@%s.lnk", szAccountsPath, RakBot::app()->getSettings()->getName().c_str(), szAddress);

		if (!DeleteFile(szAccountData)) {
			RakBot::app()->log("[ERROR] Ошибка удаления данных сохраненного аккаунта");
			return;
		}

		if (!DeleteFile(szAccountLink)) {
			RakBot::app()->log("[ERROR] Ошибка удаления ярлыка сохраненного аккаунта");
			return;
		}

		RakBot::app()->log("[RAKBOT] Ярлык успешно удален");
		return;
	}

	if (cmdcmp("adapters")) {
		IP_ADAPTER_INFO * AdapterInfo;
		ULONG    ulOutBufLen;
		DWORD    dwRetVal;
		IP_ADDR_STRING * pIPAddr;

		AdapterInfo = (IP_ADAPTER_INFO *)GlobalAlloc(GPTR, sizeof(IP_ADAPTER_INFO));
		ulOutBufLen = sizeof(IP_ADAPTER_INFO);

		if (ERROR_BUFFER_OVERFLOW == GetAdaptersInfo(AdapterInfo, &ulOutBufLen)) {
			GlobalFree(AdapterInfo);
			AdapterInfo = (IP_ADAPTER_INFO *)GlobalAlloc(GPTR, ulOutBufLen);
		}

		if (dwRetVal = GetAdaptersInfo(AdapterInfo, &ulOutBufLen)) {
			RakBot::app()->log("[ERROR] Ошибка получения информации адаптера.");
		} else {
			while (AdapterInfo != NULL) {
				RakBot::app()->log("[RAKBOT] Адаптер: %s", AdapterInfo->Description);

				printf("IP Address(s):\n");
				RakBot::app()->log("[RAKBOT]     IP: %s", AdapterInfo->IpAddressList.IpAddress.String);

				pIPAddr = AdapterInfo->IpAddressList.Next;
				while (pIPAddr) {
					RakBot::app()->log("[RAKBOT]     IP: %s", pIPAddr->IpAddress.String);
					pIPAddr = pIPAddr->Next;
				}
				AdapterInfo = AdapterInfo->Next;
			}
		}
		return;
	}

	if (cmdcmp("showdialog")) {
		RakBot::app()->getSampDialog()->showDialog();
		return;
	}

	if (cmdcmp("crash")) {
		int *test = 0;
		*test = 1337;
		return;
	}

	RakBot::app()->log("[ERROR] Команда \"!%s\" не была найдена", cmd);
}
