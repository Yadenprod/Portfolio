#pragma once

class Pickup {
private:
	bool _active;
	int _pickupId;
	int _model;
	int _type;
	float _position[3];

	std::mutex _pickupMutex;

public:
	Pickup();
	~Pickup();

	void reset();

	void setActive(bool active);
	bool isActive();

	void setPickupId(int pickupId);
	int getPickupId();

	void setModel(int model);
	int getModel();

	void setType(int type);
	int getType();

	void setPosition(int n, float position);
	float getPosition(int n);
};

/*
_pickups[pickupId]->setModel(model);
_pickups[pickupId]->setType(type);
_pickups[pickupId]->setPosition(0, positionX);
_pickups[pickupId]->setPosition(1, positionY);
_pickups[pickupId]->setPosition(2, positionZ);
*/