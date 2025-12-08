// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "Player.h"

Player::Player() : PlayerBase() {
	// reset();
}

Player::~Player() {

}

void Player::reset() {
	std::lock_guard<std::mutex> lock(_playerMutex);

	_active = false;
	_inStream = false;
	_admin = false;

	PlayerBase::reset();
}

void Player::setActive(bool active) {
	std::lock_guard<std::mutex> lock(_playerMutex);
	_active = active;
}

bool Player::isActive() {
	std::lock_guard<std::mutex> lock(_playerMutex);
	return _active;
}

// IN STREAM
void Player::setInStream(bool inStream) {
	std::lock_guard<std::mutex> lock(_playerMutex);
	_inStream = inStream;
}

bool Player::isInStream() {
	std::lock_guard<std::mutex> lock(_playerMutex);
	return _inStream;
}

// ADMIN
void Player::setAdmin(bool admin) {
	std::lock_guard<std::mutex> lock(_playerMutex);
	_admin = admin;
}

bool Player::isAdmin() {
	std::lock_guard<std::mutex> lock(_playerMutex);
	return _admin;
}
