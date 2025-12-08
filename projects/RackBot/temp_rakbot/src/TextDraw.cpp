#include "TextDraw.h"

TextDraw::TextDraw() {}

TextDraw::~TextDraw() {}

void TextDraw::reset() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	_active = false;
	_hasShadow = false;
	_hasOutline = false;
	_selectable = false;

	_flags = 0;
	_style = 0;

	_textDrawId = 0;
	_modelId = 0;

	_letterColor = 0;
	_boxColor = 0;
	_backgroundColor = 0;
	_color = 0;

	_zoom = 0.f;

	for (int i = 0; i < 2; i++)
		_letterSize[i] = 0.f;

	for (int i = 0; i < 2; i++)
		_lineSize[i] = 0.f;

	for (int i = 0; i < 2; i++)
		_position[i] = 0.f;

	for (int i = 0; i < 3; i++)
		_rotation[i] = 0.f;

	_string = "";
}

// ACITVE
void TextDraw::setActive(bool active) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_active = active;
}

bool TextDraw::isActive() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _active;
}

// HASSHADOW
void TextDraw::setHasShadow(bool hasShadow) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_hasShadow = hasShadow;
}

bool TextDraw::isHasShadow() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _hasShadow;
}

// HASOUTLINE
void TextDraw::setHasOutline(bool hasOutline) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_hasOutline = hasOutline;
}

bool TextDraw::isHasOutline() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _hasOutline;
}

// SELECTABLE
void TextDraw::setSelectable(bool selectable) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_selectable = selectable;
}

bool TextDraw::isSelectable() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _selectable;
}

// FLAGS
void TextDraw::setFlags(uint8_t flags) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_flags = flags;
}

uint8_t TextDraw::getFlags() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _flags;
}

// STYLE
void TextDraw::setStyle(uint8_t style) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_style = style;
}

uint8_t TextDraw::getStyle() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _style;
}

// TEXTDRAWID
void TextDraw::setTextDrawId(uint16_t textDrawId) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_textDrawId = textDrawId;
}

uint16_t TextDraw::getTextDrawId() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _textDrawId;
}

// MODELID
void TextDraw::setModelId(uint16_t modelId) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_modelId = modelId;
}

uint16_t TextDraw::getModelId() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _modelId;
}

// LETTERCOLOR
void TextDraw::setLetterColor(uint32_t letterColor) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_letterColor = letterColor;
}

uint32_t TextDraw::getLetterColor() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _letterColor;
}

// BOXCOLOR
void TextDraw::setBoxColor(uint32_t boxColor) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_boxColor = boxColor;
}

uint32_t TextDraw::getBoxColor() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _boxColor;
}

// BACKGROUNDCOLOR
void TextDraw::setBackgroundColor(uint32_t backgroundColor) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_backgroundColor = backgroundColor;
}

uint32_t TextDraw::getBackgroundColor() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _backgroundColor;
}

// COLOR
void TextDraw::setColor(uint32_t color) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_color = color;
}

uint32_t TextDraw::getColor() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _color;
}

// ZOOM
void TextDraw::setZoom(float zoom) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_zoom = zoom;
}

float TextDraw::getZoom() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _zoom;
}

// LETTERSIZE
void TextDraw::setLetterSize(int n, float letterSize) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 2)
		return;

	_letterSize[n] = letterSize;
}

float TextDraw::getLetterSize(int n) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 2)
		return 0;

	return _letterSize[n];
}

// LINESIZE
void TextDraw::setLineSize(int n, float lineSize) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 2)
		return;

	_lineSize[n] = lineSize;
}

float TextDraw::getLineSize(int n) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 2)
		return 0;

	return _lineSize[n];
}

// POSITION
void TextDraw::setPosition(int n, float position) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 2)
		return;

	_position[n] = position;
}

float TextDraw::getPosition(int n) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 2)
		return 0;

	return _position[n];
}

// ROTATION
void TextDraw::setRotation(int n, float rotation) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 3)
		return;

	_rotation[n] = rotation;
}

float TextDraw::getRotation(int n) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);

	if (n < 0 || n >= 3)
		return 0;

	return _rotation[n];
}

// STRING
void TextDraw::setString(std::string string) {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	_string = string;
}

std::string TextDraw::getString() {
	std::lock_guard<std::mutex> lock(_textDrawMutex);
	return _string;
}