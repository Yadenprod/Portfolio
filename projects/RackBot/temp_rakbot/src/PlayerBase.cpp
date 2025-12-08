// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "MathStuff.h"
#include "Pickup.h"
#include "Vehicle.h"

#include "PlayerBase.h"

PlayerBase::PlayerBase() {
}

PlayerBase::~PlayerBase() {
}

float PlayerBase::distanceTo(float position[3]) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return vect3_dist(_position, position);
}

float PlayerBase::distanceTo(PlayerBase * player) {
	if (player == nullptr)
		return 0.f;

	float position[3];
	for (int i = 0; i < 3; i++)
		position[i] = player->getPosition(i);

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return vect3_dist(_position, position);
}

float PlayerBase::distanceTo(Pickup * pickup) {
	if (pickup == nullptr)
		return 0.f;

	float position[3];
	for (int i = 0; i < 3; i++)
		position[i] = pickup->getPosition(i);

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return vect3_dist(_position, position);
}

float PlayerBase::distanceTo(Vehicle * vehicle) {
	if (vehicle == nullptr)
		return 0.f;

	float position[3];
	for (int i = 0; i < 3; i++)
		position[i] = vehicle->getPosition(i);

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return vect3_dist(_position, position);
}

std::string PlayerBase::getPlayerStateName() {
	std::string playerStateName;

	_playerBaseMutex.lock();
	uint8_t playerState = _playerState;
	_playerBaseMutex.unlock();

	switch (playerState) {
		case PLAYER_STATE_SPECTATE:
			playerStateName = "наблюдатель";
			break;

		case PLAYER_STATE_DRIVER:
			playerStateName = "водитель";
			break;

		case PLAYER_STATE_ONFOOT:
			playerStateName = "пешеход";
			break;

		case PLAYER_STATE_PASSENGER:
			playerStateName = "пассажир";
			break;

		case PLAYER_STATE_ENTERING_VEHICLE:
			playerStateName = "садится в машину";
			break;

		default:
			playerStateName = "n/a";
			break;
	}

	return playerStateName;
}

void PlayerBase::reset() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);

	_playerState = PLAYER_STATE_NONE;
	_playerId = PLAYER_ID_NONE;
	_health = 0;
	_armour = 0;
	_weapon = 0;
	_specialAction = 0;
	_skin = 0;

	for (int i = 0; i < 3; i++)
		_position[i] = 0.f;

	for (int i = 0; i < 4; i++)
		_quaternion[i] = 0.f;

	for (int i = 0; i < 3; i++)
		_speed[i] = 0.f;

	_vehicleSeat = 0;
	_vehicle = nullptr;

	getInfo()->reset();
	getAnimation()->reset();
	getKeys()->reset();
	getSurfing()->reset();
}


// PLAYER STATE
void PlayerBase::setPlayerState(uint8_t playerState) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_playerState = playerState;
}

uint8_t PlayerBase::getPlayerState() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _playerState;
}

// HEALTH
void PlayerBase::setHealth(uint8_t playerState) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_health = playerState;
}

uint8_t PlayerBase::getHealth() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _health;
}

// ARMOUR
void PlayerBase::setArmour(uint8_t armour) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_armour = armour;
}

uint8_t PlayerBase::getArmour() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _armour;
}

// WEAPON
void PlayerBase::setWeapon(uint8_t weapon) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_weapon = weapon;
}

uint8_t PlayerBase::getWeapon() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _weapon;
}

// SPECIAL ACTION
void PlayerBase::setSpecialAction(uint8_t specialAction) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_specialAction = specialAction;
}

uint8_t PlayerBase::getSpecialAction() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _specialAction;
}

// PLAYER ID
void PlayerBase::setPlayerId(uint16_t playerId) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_playerId = playerId;
}

uint16_t PlayerBase::getPlayerId() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _playerId;
}

// SKIN
void PlayerBase::setSkin(int skin) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_skin = skin;
}

int PlayerBase::getSkin() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _skin;
}

// POSITION
void PlayerBase::setPosition(int n, float val) {
	if (n < 0 || n > 2)
		return;

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_position[n] = val;
}

float PlayerBase::getPosition(int n) {
	if (n < 0 || n > 2)
		return 0.f;

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _position[n];
}

// QUATERNION
void PlayerBase::setQuaternion(int n, float val) {
	if (n < 0 || n > 3)
		return;

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_quaternion[n] = val;
}

float PlayerBase::getQuaternion(int n) {
	if (n < 0 || n > 3)
		return 0.f;

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _quaternion[n];
}

// SPEED
void PlayerBase::setSpeed(int n, float val) {
	if (n < 0 || n > 2)
		return;

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_speed[n] = val;
}

float PlayerBase::getSpeed(int n) {
	if (n < 0 || n > 2)
		return 0.f;

	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _speed[n];
}

// NAME
void PlayerBase::setName(std::string name) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_name = name;
}

std::string PlayerBase::getName() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _name;
}

// VEHICLE SEAT
void PlayerBase::setVehicleSeat(uint8_t vehicleSeat) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_vehicleSeat = vehicleSeat;
}

uint8_t PlayerBase::getVehicleSeat() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _vehicleSeat;
}

// VEHICLE
void PlayerBase::setVehicle(Vehicle *vehicle) {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	_vehicle = vehicle;
}

Vehicle *PlayerBase::getVehicle() {
	std::lock_guard<std::mutex> lock(_playerBaseMutex);
	return _vehicle;
}