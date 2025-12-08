#pragma once

class Funcs {
public:
	Funcs();
	~Funcs();
};

extern int BotLoaderBagCount;
extern bool BotLoaderWithBag;
extern bool BotLoaderWaitDialog;
extern bool BotLoaderWaitAfterPay;
extern Timer BotLoaderTakenBagTimer;

extern bool FarmWork;
extern float FarmPos[5][3];
extern float FarmFieldPos[5][3];
extern int FarmIndex;
extern int FarmCount;
extern bool ChangeFarm;
extern bool FarmGetPay;

void AntiAFK();
void KeepOnline();
void NoAfk();
void RoutePlay();
void CheckChangePos();
void UpdateInfo();
void AdminChecker();
void BotLoader();
void FuncsLoop();
void FuncsOff();