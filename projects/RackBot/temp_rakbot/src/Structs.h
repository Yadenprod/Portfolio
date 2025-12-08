#pragma once

#pragma pack(push, 1)

struct OnfootData {
	uint16_t leftRightKey;
	uint16_t upDownKey; // 2
	uint16_t keys; // 4
	float position[3]; // 6
	float quaternion[4]; // 18
	uint8_t health; // 34
	uint8_t armour; // 35
	uint8_t weapon; // 36
	uint8_t specialAction; // 37
	float speed[3]; // 38
	float surfOffsets[3]; // 50
	uint16_t surfVehicleId; // 62
	uint16_t animId; // 64
	uint16_t animFlags; // 66
};

struct SpectatorData {
	uint16_t	sLeftRightKeys;
	uint16_t	sUpDownKeys;
	uint16_t	sKeys;
	float		fPosition[3];
};

struct IncarData {
	uint16_t sVehicleId;
	uint16_t lrAnalog;
	uint16_t udAnalog;
	uint16_t sKeys;
	float quaternion[4];
	float position[3];
	float vecMoveSpeed[3];
	float fCarHealth;
	uint8_t bytePlayerHealth;
	uint8_t bytePlayerArmour;
	uint8_t weapon;
	uint8_t byteSirenOn;
	uint8_t byteLandingGearState;
	uint16_t TrailerID_or_ThrustAngle;
	float fTrainSpeed;
};

struct PassengerData {
	uint16_t	sVehicleID;
	uint8_t		byteSeatID;
	uint8_t		byteCurrentWeapon;
	uint8_t		byteHealth;
	uint8_t		byteArmor;
	uint16_t	sLeftRightKeys;
	uint16_t	sUpDownKeys;
	uint16_t	sKeys;
	float		fPosition[3];
};

struct AimData {
	uint8_t camMode;
	float aimf1[3];
	float aimPos[3];
	float aimZ;
	uint8_t camZoom : 6;
	uint8_t weaponState : 2;
	uint8_t unknown;
};

struct UnoccupiedData {
	int16_t sVehicleID;
	uint8_t byteSeatID;
	float	fRoll[3];
	float	fDirection[3];
	float	fPosition[3];
	float	fMoveSpeed[3];
	float	fTurnSpeed[3];
	float	fHealth;
};

struct BulletData {
	uint8_t		byteType;
	uint16_t	sTargetID;
	float		fOrigin[3];
	float		fTarget[3];
	float		fCenter[3];
	uint8_t		byteWeaponID;
};

struct NewVehicle {
	uint16_t VehicleId;
	int		  iVehicleType;
	float	  position[3];
	float	  fRotation;
	char	  aColor1;
	char	  aColor2;
	float	  fHealth;
	uint8_t	  byteInterior;
	uint8_t	  doorsLock;
	uint32_t	  dwDoorDamageStatus;
	uint32_t	  dwPanelDamageStatus;
	uint8_t	  byteLightDamageStatus;
};

#define MAX_MENU_ITEMS 12
#define MAX_MENU_LINE 32
#define MAX_MENU_COLUMNS 2

struct GTAMenuInt {
	BOOL bMenu;
	BOOL bRow[MAX_MENU_ITEMS];
	BOOL bPadding[8 - ((MAX_MENU_ITEMS + 1) % 8)];
};

struct GTAMenu {
	char szTitle[MAX_MENU_LINE];
	char szSeparator[MAX_MENU_LINE];
	uint8_t byteColCount;
	char szColumnContent[MAX_MENU_COLUMNS][MAX_MENU_LINE];
};

#define IDB_BUTTON1				10
#define IDB_BUTTON2				11
#define IDE_INPUTEDIT			12
#define IDL_LISTBOX				13

#define DIALOG_STYLE_MSGBOX		0
#define DIALOG_STYLE_INPUT		1
#define DIALOG_STYLE_LIST		2
#define DIALOG_STYLE_PASSWORD	3
#define DIALOG_STYLE_TABLIST    4

struct Checkpoint {
	float position[3];
	float size;
	bool active;
};

struct RaceCheckpoint {
	uint8_t type;
	float position[3];
	float fNextPos[3];
	float size;
	bool active;
};

struct SpawnInfo {
	uint8_t team;
	int skin;
	uint8_t unk;
	float position[3];
	float rotation;
	int spawnWeapons[3];
	int spawnWeaponsAmmo[3];
};

struct GTAObject {
	uint16_t usObjectId;
	uint32_t ulModelId;
	float position[3];
	float fRotation[3];
	float fDrawDistance;
	bool active;
};

struct TeleportPlace {
	float position[3];
	char szName[64];
};

#pragma pack(pop)