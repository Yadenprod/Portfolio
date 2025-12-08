// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "Pickup.h"

Pickup::Pickup() {}

Pickup::~Pickup() {}

void Pickup::reset() {
	std::lock_guard<std::mutex> lock(_pickupMutex);

	_active = false;
	_pickupId = 0;
	_model = 0;
	_type = 0;

	for (int i = 0; i < 3; i++)
		_position[i] = 0.f;
}

void Pickup::setActive(bool active) {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	_active = active;
}

bool Pickup::isActive() {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	return _active;
}

void Pickup::setPickupId(int pickupId) {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	_pickupId = pickupId;
}

int Pickup::getPickupId() {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	return _pickupId;
}

void Pickup::setModel(int model) {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	_model = model;
}

int Pickup::getModel() {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	return _model;
}

void Pickup::setType(int type) {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	_type = type;
}

int Pickup::getType() {
	std::lock_guard<std::mutex> lock(_pickupMutex);
	return _type;
}

void Pickup::setPosition(int n, float val) {
	if (n < 0 || n > 2)
		return;

	std::lock_guard<std::mutex> lock(_pickupMutex);
	_position[n] = val;
}

float Pickup::getPosition(int n) {
	if (n < 0 || n > 2)
		return 0.f;

	std::lock_guard<std::mutex> lock(_pickupMutex);
	return _position[n];
}