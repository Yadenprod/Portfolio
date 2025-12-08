#pragma once

class SAMPDialog {
private:
	bool _dialogActive;
	bool _dialogOffline;
	uint8_t _dialogStyle;
	uint16_t _dialogId;
	std::string _dialogTitle;
	std::string _okButtonText;
	std::string _cancelButtonText;
	std::string _dialogText;

	std::mutex _sampDialogMutex;

public:
	SAMPDialog();
	~SAMPDialog();

	void reset();

	void setDialogActive(bool dialogActive);
	bool isDialogActive();

	void setDialogOffline(bool offlineDialog);
	bool isDialogOffline();

	void setDialogStyle(uint8_t dialogStyle);
	uint8_t getDialogStyle();

	void setDialogId(uint16_t dialogId);
	uint16_t getDialogId();

	void setDialogTitle(std::string dialogTitle);
	std::string getDialogTitle();

	void setOkButtonText(std::string okButtonText);
	std::string getOkButtonText();

	void setCancelButtonText(std::string cancelButtonText);
	std::string getCancelButtonText();

	void setDialogText(std::string dialogText);
	std::string getDialogText();

	void showDialog();
	void hideDialog();
};