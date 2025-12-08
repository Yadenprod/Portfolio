#pragma once

class Server {
private:
	bool _gameInited;
	std::string _serverName;

	std::mutex _serverMutex;

public:
	Server();
	~Server();

	void reset();

	void setGameInited(bool gameInited);
	bool isGameInited();

	void setServerName(std::string serverName);
	std::string getServerName();
};
