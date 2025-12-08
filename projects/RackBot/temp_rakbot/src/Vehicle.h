#pragma once

class Player;

class Vehicle {
private:
	bool _active;
	bool _doorsOpened;
	bool _engineEnabled;
	bool _lightsEnabled;
	bool _sirenEnabled;

	uint8_t _firstColor;
	uint8_t _secondColor;
	uint8_t _seatsAmount;
	uint8_t _gearState;

	uint16_t _vehicleId;
	uint16_t _trailerId;

	int _model;
	int _vehicleClass;

	float _position[3];
	float _speed[3];
	float _quaternion[4];
	float _carHealth;
	float _trainSpeed;

	std::string _name;

	Player *_driver;
	Player **_passenger;

	std::mutex _vehicleMutex;

	void loadModelData();

public:
	Vehicle();
	~Vehicle();

	void reset();

	void setActive(bool active);
	bool isActive();

	void setDoorsOpened(bool doorsOpened);
	bool isDoorsOpened();

	void setEngineEnabled(bool engineEnabled);
	bool isEngineEnabled();

	void setLightsEnabled(bool lightsEnabled);
	bool isLightsEnabled();

	void setSirenEnabled(bool sirenEnabled);
	bool isSirenEnabled();

	void setFirstColor(uint8_t firstColor);
	uint8_t getFirstColor();

	void setSecondColor(uint8_t secondColor);
	uint8_t getSecondColor();

	uint8_t getSeatsAmount();

	void setVehicleId(uint16_t vehicleId);
	uint16_t getVehicleId();

	void setModel(int model);
	int getModel();

	int getVehicleClass();

	int getPassengerAmount();

	void setPosition(int n, float position);
	float getPosition(int n);

	void setSpeed(int n, float speed);
	float getSpeed(int n);

	void setQuaternion(int n, float quaternoin);
	float getQuaternion(int n);

	void setCarHealth(float carHealth);
	float getCarHealth();

	std::string getName();

	void setDriver(Player *driver);
	Player *getDriver();

	void setPassenger(int n, Player *passenger);
	Player *getPassenger(int n);

	void setGearState(uint8_t gearState);
	uint8_t getGearState();

	void setTrailerId(uint16_t trailerId);
	uint16_t getTrailerId();

	void setTrainSpeed(float trainSpeed);
	float getTrainSpeed();
};

