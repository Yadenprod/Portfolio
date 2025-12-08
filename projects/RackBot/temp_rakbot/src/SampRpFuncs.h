#pragma once

class SampRpFuncs {
private:
	static bool _botSuspended;

public:
	SampRpFuncs();
	~SampRpFuncs();

	static void pickUpPickup(Pickup *pickupId, std::function<void()> afterAction = std::function<void()>());
	static void takeCheckpoint(std::function<void()> afterAction = std::function<void()>());
	static bool isBotSuspended() { return _botSuspended; }
	static bool isSampRpServer();
	static bool onServerMessage(std::string msg);
	static bool onAttachObjectToPlayer(uint16_t playerId, uint32_t slotId, bool attach);
	static bool onDialogShow(uint16_t dialogId, uint8_t dialogStyle, std::string dialogTitle, std::string okButtonText, std::string cancelButtonText, std::string dialogText);
	static bool onSpawned();
	static void onCreateObject(GTAObject *object);
	static void onDestroyObject(GTAObject *object);
	static void onDialogResponseSent(uint16_t dialogId, uint8_t dialogButton, uint16_t dialogItem, std::string dialogInput);
};

