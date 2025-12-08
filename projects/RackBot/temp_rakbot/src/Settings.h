#pragma once

#include "Includes.h"
#include "Defines.h"
#include "Structs.h"

#include "Timer.h"

struct Vars {
	bool windowOpened;
	bool waitForRequestSpawnReply;

	std::vector<std::string> admins;
	std::string adminsUrl;
	static std::mutex adminsMutex;

	bool farChatEnabled;

	bool botAutoSchoolEnabled;
	bool botAutoSchoolActive;
	bool botAutoSchoolFinished;

	bool ignoreServerMessages;
	bool floodEnabled;
	int floodMode;
	int floodDelay;
	std::string floodText;

	int reconnectDelay;
	int adminReconnectDelay;

	int iBankPutMoney;
	bool bBuySkin;

	bool getBalanceEnabled;
	bool getBalanceFinished;

	int busWorkerRoute;
	int busWorkerRouteItem;
	int busWorkerBusModel;
	bool checkPointMaster;
	bool timeStamp;

	int iSetWorkIndex;

	bool parseStatistic;

	bool botFarmerEnabled;
	bool botFarmerAutomated;

	bool virtualWorld;
	int adminNearAction;
	int adminOnlineAction;
	int skipDialog;

	int dialogIdBan;
	int dialogIdPassword;

	float coordMasterHeight;
	float coordMasterDist;
	int coordMasterDelay;

	int maxId;
	int minId;
	bool checkIdEnabled;

	uint8_t interiorId;

	bool bQuestEnabled;
	int iQuestStep;
	bool bQuestSpawn;

	int maxOnline;
	int minOnline;
	bool checkOnlineEnabled;

	// Follow & Stick
	int followPlayerID;
	bool stickEnabled;
	bool followEnabled;

	// AutoReger
	bool autoRegEnabled;
	std::string autoRegMail;
	std::string autoRegReferer;
	int autoRegSex;

	bool autoPickEnabled;
	bool antiDeath;
	bool bAntiSat;

	// CoordMaster
	bool coordMasterEnabled;
	float coordMasterTarget[3];

	// Register
	std::string regKey;
	bool keyAccepted;

	float savedCoords[3];
	bool savedTeleportEnabled;

	// AntiAFK
	bool noAfk;
	bool syncAllowed;
	bool antiAfkEnabled;
	uint32_t antiAfkDelay;
	float antiAfkOffset;

	bool botLoaderEnabled;
	int botLoaderDelay;
	int botLoaderLimit;
	int botLoaderGetPay;
	bool botLoaderCheckVans;

	unsigned int uiChallenge;

	bool sleepEnabled;

	bool keepOnlineEnabled;
	bool keepOnlineWait;
	bool keepOnlineBeginAfterEnd;
	int keepOnlineBegin;
	int keepOnlineEnd;

	uint32_t dwLicenseCheckResult;

	std::string resourcePath;

	bool routeEnabled;
	bool routeLoop;
	int routeUpdateDelay;
	int routeUpdateCount;
	std::vector<OnfootData> routeData;
	uint32_t routeIndex;

	bool textDrawCreateLogging;
	bool textDrawHideLogging;
	bool textDrawSetStringLogging;

	bool textLabelCreateLogging;

	bool sendBadSync;
	bool smartInvis;

	float faceAngle;
	std::string adapterAddress;

	int mainDelay;
	int luaUpdateDelay;
	int networkUpdateDelay;
	int spawnDelay;
	int dialogResponseDelay;
	int noAfkDelay;
	int afterSpawnDelay;
	int enterVehicleDelay;

	FILE *logFile;
	std::string logFileMode;

	bool mapWindowOpened;
	HANDLE mapWindowThread;
	HANDLE dialogWindowThread;

	static TeleportPlace teleportPlaces[300];

	static Timer botConnectedTimer;
	static Timer botSpawnedTimer;
	static Timer gameInitedTimer;
	static Timer reconnectTimer;
	static Timer lastChangePos;

	static std::queue<std::string> commandQueue;
	static std::mutex commandQueueMutex;

	float syncSpeedOffset[3];
	float syncPositionOffset[3];

	uint16_t badSyncSurfId;
	bool badSyncNanOffset;
};

extern Vars vars;

class Address {
private:
	std::string _ip;
	uint16_t _port;

	std::mutex _addressMutex;

public:
	Address() { }

	void reset() {
		std::lock_guard<std::mutex> lock(_addressMutex);
		_ip = "127.0.0.1";
		_port = 7777;
	}

	void setIp(std::string ip) {
		std::lock_guard<std::mutex> lock(_addressMutex);
		_ip = ip;
	}

	std::string getIp() {
		std::lock_guard<std::mutex> lock(_addressMutex);
		return _ip;
	}

	void setPort(uint16_t port) {
		std::lock_guard<std::mutex> lock(_addressMutex);
		_port = port;
	}

	uint16_t getPort() {
		std::lock_guard<std::mutex> lock(_addressMutex);
		return _port;
	}
};

class Settings {
private:
	Address _address;
	std::string _name;
	std::string _serverPassword;
	std::string _loginPassword;

	std::mutex _settingsMutex;

public:
	Settings();
	~Settings();

	void reset();

	Address *getAddress();

	void setName(std::string name);
	std::string getName();

	void setLoginPassword(std::string loginPassword);
	std::string getLoginPassword();

	void setServerPassword(std::string serverPassword);
	std::string getServerPassword();
};