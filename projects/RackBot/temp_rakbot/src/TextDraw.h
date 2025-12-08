#pragma once

#include <cstdint>
#include <string>
#include <mutex>

class TextDraw {
private:
	bool _active;
	bool _hasShadow;
	bool _hasOutline;
	bool _selectable;

	uint8_t _flags;
	uint8_t _style;

	uint16_t _textDrawId;
	uint16_t _modelId;

	uint32_t _letterColor;
	uint32_t _boxColor;
	uint32_t _backgroundColor;
	uint32_t _color;

	float _zoom;

	float _letterSize[2];
	float _lineSize[2];
	float _position[2];
	float _rotation[3];

	std::string _string;

	std::mutex _textDrawMutex;

public:
	TextDraw();
	~TextDraw();

	void reset();

	void setActive(bool active);
	bool isActive();

	void setHasShadow(bool hasShadow);
	bool isHasShadow();

	void setHasOutline(bool hasOutline);
	bool isHasOutline();

	void setSelectable(bool selectable);
	bool isSelectable();

	void setFlags(uint8_t flags);
	uint8_t getFlags();

	void setStyle(uint8_t style);
	uint8_t getStyle();

	void setTextDrawId(uint16_t textDrawId);
	uint16_t getTextDrawId();

	void setModelId(uint16_t modelId);
	uint16_t getModelId();

	void setLetterColor(uint32_t letterColor);
	uint32_t getLetterColor();

	void setBoxColor(uint32_t boxColor);
	uint32_t getBoxColor();

	void setBackgroundColor(uint32_t backgroundColor);
	uint32_t getBackgroundColor();

	void setColor(uint32_t color);
	uint32_t getColor();

	void setZoom(float zoom);
	float getZoom();

	void setLetterSize(int n, float letterSize);
	float getLetterSize(int n);

	void setLineSize(int n, float lineSize);
	float getLineSize(int n);

	void setPosition(int n, float position);
	float getPosition(int n);

	void setRotation(int n, float rotation);
	float getRotation(int n);

	void setString(std::string string);
	std::string getString();
};