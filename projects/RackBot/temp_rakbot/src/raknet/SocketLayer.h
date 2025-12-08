#ifndef SOCKET_LAYER_H
#define SOCKET_LAYER_H

#include <winsock2.h>
#include <ws2tcpip.h>

class RakPeer;

class SocketLayer {
public:
	SocketLayer();
	~SocketLayer();

	static inline SocketLayer *Instance() {
		return &socketInstance;
	}

	int Connect(SOCKET s, unsigned int binaryAddress, unsigned short binaryPort);
	SOCKET CreateBoundSocket(unsigned short port, bool blockingSocket, const char *forceHostAddress);
	const char *DomainNameToIP(const char *domainName);
	bool AssociateSocketWithCompletionPortAndRead(SOCKET s, unsigned int binaryAddress, unsigned short port, RakPeer *rakPeer);
	int Write(const SOCKET s, const char *data, const int length);
	int Read(const SOCKET s, char *buf, const int length);
	int RecvFrom(const SOCKET s, RakPeer *rakPeer, int *errorCode);
	void GetMyIP(char ipList[10][16]);
	int SendTo(SOCKET s, const char *data, int length, char ip[16], unsigned short port);
	int SendTo(SOCKET s, const char *data, int length, unsigned int binaryAddress, unsigned short port);
	unsigned short GetLocalPort(SOCKET s);

private:
	static bool socketLayerStarted;
	static WSADATA socketInfo;
	static SocketLayer socketInstance;

	static SOCKET socks5Socket;
	static unsigned int socks5BinaryAddress;
	static unsigned short socks5BinaryPort;
	static unsigned short socks5UdpPort;
};

#endif