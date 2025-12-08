#pragma once

#include "PlayerBase.h"

class Bot : public PlayerBase {
private:
	bool _connected;
	bool _spawned;
	bool _connectRequested;
	int _money;

	std::mutex _botMutex;

	void aimSync();
	void onfootSync();
	void passengerSync();
	void driverSync();
	void spectateSync();

public:
	Bot();
	~Bot();

	void reset(bool disconnect);
	void reconnect(int reconnectDelay);

	void setConnected(bool connected);
	bool isConnected();

	void setSpawned(bool spawned);
	bool isSpawned();

	void setConnectRequested(bool connectRequested);
	bool isConnectRequested();

	void setMoney(int money);
	int getMoney();

	void enterVehicle(Vehicle *vehicle, uint8_t seatId);
	void exitVehicle();

	void sync(int count = 1);
	void teleport(float fPosX, float fPosY, float fPosZ);
	void follow(uint16_t playerId);

	void connect(std::string address, uint16_t port);
	void disconnect(bool timeOut);

	void sendInput(std::string input);
	void requestClass(int classId);
	void requestSpawn();
	bool pickUpPickup(Pickup *pickup, bool checkDist = true);
	bool takeCheckpoint();
	void dialogResponse(uint16_t dialogId, uint8_t button = 1, uint16_t item = -1, std::string input = "", bool isOffline = false);
	void spawn();
	void kill();
	void clickTextdraw(uint16_t textDrawId);
};