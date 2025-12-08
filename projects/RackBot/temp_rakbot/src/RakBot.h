#pragma once

#include "Includes.h"
#include "Defines.h"
#include "Structs.h"

#include "Bot.h"
#include "Settings.h"
#include "Funcs.h"
#include "Server.h"
#include "Events.h"
#include "SAMPDialog.h"
#include "ServerInfo.h"
#include "Pickup.h"
#include "PlayerBase.h"
#include "Player.h"
#include "Vehicle.h"
#include "TextDraw.h"

class RakClientInterface;

class RakBot {
private:
	bool _botOff;

	RakClientInterface *_rakClient;

	Player _players[MAX_PLAYERS];
	Pickup _pickups[MAX_PICKUPS];
	Vehicle _vehicles[MAX_VEHICLES];
	TextDraw _textDraws[MAX_TEXTDRAWS];

	Bot _bot;
	Settings _settings;
	Server _server;
	Events _events;
	SAMPDialog _sampDialog;
	ServerInfo _serverInfo;

	std::mutex _botOffMutex;
	std::mutex _logToFileMutex;

	RakBot();
	~RakBot();

	RakBot(RakBot const&);
	RakBot& operator= (RakBot const&);

	void logToFile(std::string line);

public:
	static RakBot *app();

	bool isBotOff();
	void exit();

	Player *getPlayer(uint16_t playerId);
	Player *addPlayer(uint16_t playerId);
	void deletePlayer(uint16_t playerId);
	uint16_t getPlayersCount();

	Pickup *getPickup(int pickupId);
	Pickup *addPickup(int pickupId);
	void deletePickup(int pickupId);

	Vehicle *getVehicle(uint16_t vehicleId);
	Vehicle *addVehicle(uint16_t vehicleId);
	void deleteVehicle(uint16_t vehicleId);

	TextDraw *getTextDraw(int textDrawId);
	TextDraw *addTextDraw(int textDrawId);
	void deleteTextDraw(int textDrawId);

	Bot *getBot();
	Settings *getSettings();
	RakClientInterface *getRakClient();
	Server *getServer();
	Events *getEvents();
	SAMPDialog *getSampDialog();
	ServerInfo *getServerInfo();

	void log(const char *format, ...);
};