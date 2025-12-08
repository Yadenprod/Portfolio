// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "VehicleStuff.h"

#include "Vehicle.h"

void Vehicle::loadModelData() {
	for (int i = 0; i < VEHICLE_LIST_SIZE; i++) {
		if (VehicleList[i].id != _model)
			continue;

		_vehicleClass = VehicleList[i].classId;
		_seatsAmount = VehicleList[i].passengers + 1;
		_name = VehicleList[i].name;
		_passenger = new Player *[_seatsAmount];
		for (int i = 0; i < _seatsAmount; i++)
			_passenger[i] = nullptr;
	}
}

Vehicle::Vehicle() {}

Vehicle::~Vehicle() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);

	if (_passenger != nullptr)
		delete[] _passenger;
}

void Vehicle::reset() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);

	_active = false;
	_doorsOpened = false;
	_engineEnabled = false;
	_lightsEnabled = false;
	_sirenEnabled = false;
	_firstColor = 0;
	_secondColor = 0;
	_seatsAmount = 0;
	_vehicleId = 0;
	_model = 0;
	_vehicleClass = VEHICLE_CLASS_NONE;
	for (int i = 0; i < 3; i++)
		_position[i] = 0.f;
	for (int i = 0; i < 3; i++)
		_speed[i] = 0.f;
	for (int i = 0; i < 4; i++)
		_quaternion[i] = 0.f;
	_carHealth = 0.f;
	_driver = nullptr;
	_passenger = nullptr;
}

void Vehicle::setActive(bool active) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_active = active;
}

bool Vehicle::isActive() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _active;
}

void Vehicle::setDoorsOpened(bool doorsOpened) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_doorsOpened = doorsOpened;
}

bool Vehicle::isDoorsOpened() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _doorsOpened;
}

void Vehicle::setEngineEnabled(bool engineEnabled) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_engineEnabled = engineEnabled;
}

bool Vehicle::isEngineEnabled() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _engineEnabled;
}

void Vehicle::setLightsEnabled(bool lightsEnabled) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_lightsEnabled = lightsEnabled;
}

bool Vehicle::isLightsEnabled() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _lightsEnabled;
}

void Vehicle::setSirenEnabled(bool sirenEnabled) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_sirenEnabled = sirenEnabled;
}

bool Vehicle::isSirenEnabled() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _sirenEnabled;
}

void Vehicle::setFirstColor(uint8_t firstColor) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_firstColor = firstColor;
}

uint8_t Vehicle::getFirstColor() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _firstColor;
}

void Vehicle::setSecondColor(uint8_t secondColor) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_secondColor = secondColor;
}

uint8_t Vehicle::getSecondColor() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _secondColor;
}

uint8_t Vehicle::getSeatsAmount() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _seatsAmount;
}

void Vehicle::setVehicleId(uint16_t vehicleId) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_vehicleId = vehicleId;
}

uint16_t Vehicle::getVehicleId() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _vehicleId;
}

void Vehicle::setModel(int model) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_model = model;
	loadModelData();
}

int Vehicle::getModel() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _model;
}

int Vehicle::getVehicleClass() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _vehicleClass;
}

int Vehicle::getPassengerAmount() {
	int passengerCount = 0;

	_vehicleMutex.lock();
	for (int i = 0; i < _seatsAmount; i++) {
		if (_passenger[i] != nullptr)
			passengerCount++;
	}
	_vehicleMutex.unlock();

	return passengerCount;
}

void Vehicle::setPosition(int n, float position) {
	if (n < 0 || n >= 3)
		return;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_position[n] = position;
}

float Vehicle::getPosition(int n) {
	if (n < 0 || n >= 3)
		return 0.f;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _position[n];
}

void Vehicle::setSpeed(int n, float speed) {
	if (n < 0 || n >= 3)
		return;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_speed[n] = speed;
}

float Vehicle::getSpeed(int n) {
	if (n < 0 || n >= 3)
		return 0.f;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _speed[n];
}

void Vehicle::setQuaternion(int n, float quaternion) {
	if (n < 0 || n >= 4)
		return;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_quaternion[n] = quaternion;
}

float Vehicle::getQuaternion(int n) {
	if (n < 0 || n >= 4)
		return 0.f;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _quaternion[n];
}

void Vehicle::setCarHealth(float carHealth) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_carHealth = carHealth;
}

float Vehicle::getCarHealth() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _carHealth;
}

std::string Vehicle::getName() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _name;
}

void Vehicle::setDriver(Player *driver) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_driver = driver;
}

Player *Vehicle::getDriver() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _driver;
}

void Vehicle::setPassenger(int n, Player *passenger) {
	if (n < 0 || n > 5)
		return;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_passenger[n] = passenger;
}

Player *Vehicle::getPassenger(int n) {
	if (n < 0 || n >= _seatsAmount)
		return nullptr;

	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _passenger[n];
}

// GEAR STATE
void Vehicle::setGearState(uint8_t gearState) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_gearState = gearState;
}

uint8_t Vehicle::getGearState() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _gearState;
}

// TRAILER ID
void Vehicle::setTrailerId(uint16_t trailerId) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_trailerId = trailerId;
}

uint16_t Vehicle::getTrailerId() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _trailerId;
}

// TRAIN SPEED
void Vehicle::setTrainSpeed(float trainSpeed) {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	_trainSpeed = trainSpeed;
}

float Vehicle::getTrainSpeed() {
	std::lock_guard<std::mutex> lock(_vehicleMutex);
	return _trainSpeed;
}