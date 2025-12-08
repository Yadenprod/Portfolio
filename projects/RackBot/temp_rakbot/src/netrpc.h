#define REJECT_REASON_BAD_VERSION 1
#define REJECT_REASON_BAD_NICKNAME 2
#define REJECT_REASON_BAD_MOD 3
#define REJECT_REASON_BAD_PLAYERID 4

extern bool spawnInfoExists;
extern SpawnInfo spawnInfo;
extern GTAMenu gtaMenu;
extern GTAObject Objects[MAX_OBJECTS];
extern RaceCheckpoint raceCheckpoint;
extern Checkpoint checkpoint;

void RegisterRPCs();
extern bool FarmGetPay;