#pragma once

#define ENCODE_BITS 4 // by z0rek
#define RAKBOT_VERSION "0.8.3.2"
#define NETCODE_OPENCONNLULZ 26985
#define NETGAME_VERSION 4057

#define TRNSLT_AUTHOR "Ruskadance"
#define ADAPT_AUTHOR "MishaN, CentuiS"
#define SPECIAL_THANKS "Jamely, Logotipo, Wa3Rix, CentiuS, urShadow, DexT3R"

#define MAX_PLAYERS 1000
#define MAX_VEHICLES 2001
#define MAX_PICKUPS 4097
#define MAX_TEXTDRAWS 2048 + 256
#define MAX_OBJECTS 1001
#define MAX_ADMINS 300
#define MAX_LOGLINES 1000
// #define MAX_LOGLEN 512

#define VEHICLE_ID_NONE -1
#define PLAYER_ID_NONE -1
#define PICKUP_ID_NONE -1
#define DIALOG_ID_NONE 65535

#define KEY_UP                      -128
#define KEY_DOWN                    128
#define KEY_LEFT                    -128
#define KEY_RIGHT                   128
#define KEY_ACTION                  1
#define KEY_CROUCH                  2
#define KEY_FIRE                    4
#define KEY_SPRINT                  8
#define KEY_SECONDARY_ATTACK        16
#define KEY_JUMP                    32
#define KEY_LOOK_RIGHT              64
#define KEY_HANDBRAKE               128
#define KEY_LOOK_LEFT               256
#define KEY_SUBMISSION              512
#define KEY_LOOK_BEHIND             512
#define KEY_WALK                    1024
#define KEY_ANALOG_UP               2048
#define KEY_ANALOG_DOWN             4096 
#define KEY_ANALOG_LEFT             8192
#define KEY_ANALOG_RIGHT            16384

enum DisconnectReason {
	DISCONNECT_REASON_SELF = 0,
	DISCONNECT_REASON_CONNECTION_LOST,
	DISCONNECT_REASON_KICK,
	DISCONNECT_REASON_SERVER_FULL,
	DISCONNECT_REASON_PLAYER_ONLINE,
	DISCONNECT_REASON_WRONG_PASSWORD,
	DISCONNECT_REASON_SERVER_OFFLINE,
	DISCONNECT_REASON_BANNED
};