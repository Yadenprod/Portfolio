// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#define DEFAULT_MTU_SIZE 1500
#define MAXIMUM_MTU_SIZE 576

#include "StdAfx.h"

#include "RakBot.h"
#include "SocketLayer.h"
#include "RakNet.h"
#include "Settings.h"

typedef int socklen_t;

#ifdef _MSC_VER
#pragma warning( push )
#endif

bool SocketLayer::socketLayerStarted = FALSE;
struct WSAData SocketLayer::socketInfo;
class SocketLayer SocketLayer::socketInstance;

SOCKET SocketLayer::socks5Socket;
unsigned int SocketLayer::socks5BinaryAddress;
unsigned short SocketLayer::socks5BinaryPort;
unsigned short SocketLayer::socks5UdpPort = NULL;

extern void __stdcall ProcessNetworkPacket(const unsigned int binaryAddress, const unsigned short port, const char *data, const int length, RakPeer *rakPeer);
extern void __stdcall ProcessPortUnreachable(const unsigned int binaryAddress, const unsigned short port, RakPeer *rakPeer);

SocketLayer::SocketLayer() {
	if (socketLayerStarted == false) {
		WSAStartup(MAKEWORD(2, 2), &socketInfo);
		socketLayerStarted = true;
	}
}

SocketLayer::~SocketLayer() {
	if (socketLayerStarted == true) {
		WSACleanup();
		socketLayerStarted = false;
	}
}

int SocketLayer::Connect(SOCKET s, unsigned int binaryAddress, unsigned short binaryPort) {
	sockaddr_in connectSocketAddress;

	connectSocketAddress.sin_family = AF_INET;
	connectSocketAddress.sin_port = binaryPort;
	connectSocketAddress.sin_addr.s_addr = binaryAddress;

	return connect(s, (struct sockaddr *) & connectSocketAddress, sizeof(struct sockaddr));
}

#ifdef _MSC_VER
#pragma warning( disable : 4100 )
#endif
SOCKET SocketLayer::CreateBoundSocket(unsigned short port, bool blockingSocket, const char *forceHostAddress) {
	SOCKET listenSocket;
	sockaddr_in listenerSocketAddress;
	int ret;

	listenSocket = socket(AF_INET, SOCK_DGRAM, 0);

	if (listenSocket == INVALID_SOCKET)
		return INVALID_SOCKET;

	int sock_opt = 1;
	setsockopt(listenSocket, SOL_SOCKET, SO_REUSEADDR, (char *)& sock_opt, sizeof(sock_opt));

	sock_opt = 1024 * 256;
	setsockopt(listenSocket, SOL_SOCKET, SO_RCVBUF, (char *)& sock_opt, sizeof(sock_opt));

	sock_opt = 1024 * 16;
	setsockopt(listenSocket, SOL_SOCKET, SO_SNDBUF, (char *)& sock_opt, sizeof(sock_opt));

	unsigned long nonblocking = 1;
	if (ioctlsocket(listenSocket, FIONBIO, &nonblocking) != 0)
		return INVALID_SOCKET;

	setsockopt(listenSocket, SOL_SOCKET, SO_BROADCAST, (char *)& sock_opt, sizeof(sock_opt));

	listenerSocketAddress.sin_port = htons(port);
	listenerSocketAddress.sin_family = AF_INET;

	if (forceHostAddress && forceHostAddress[0]) {
		listenerSocketAddress.sin_addr.s_addr = inet_addr(forceHostAddress);
		RakBot::app()->log("[RAKBOT] Выбран адаптер с адресом: %s (Bot)", vars.adapterAddress.c_str());
	} else
		listenerSocketAddress.sin_addr.s_addr = INADDR_ANY;

	ret = ::bind(listenSocket, (struct sockaddr *) & listenerSocketAddress, sizeof(struct sockaddr));

	if (ret == SOCKET_ERROR)
		return INVALID_SOCKET;

	return listenSocket;
}

const char *SocketLayer::DomainNameToIP(const char *domainName) {
	struct hostent * phe = gethostbyname(domainName);

	if (phe == 0 || phe->h_addr_list[0] == 0)
		return 0;

	struct in_addr addr;
	memcpy(&addr, phe->h_addr_list[0], sizeof(struct in_addr));

	return inet_ntoa(addr);
}

int SocketLayer::Write(const SOCKET s, const char *data, const int length) {
	return send(s, data, length, NULL);
}

int SocketLayer::Read(const SOCKET s, char *buffer, const int length) {
	memset(buffer, 0, length);
	return recv(s, buffer, length, NULL);
}

#ifdef _MSC_VER
#pragma warning( disable : 4100 )
#endif
bool SocketLayer::AssociateSocketWithCompletionPortAndRead(SOCKET s, unsigned int binaryAddress, unsigned short port, RakPeer *rakPeer) {
	return true;
}

int SocketLayer::RecvFrom(const SOCKET s, RakPeer *rakPeer, int *errorCode) {
	int len;
	char data[MAXIMUM_MTU_SIZE + 1];
	sockaddr_in sa;

	const socklen_t len2 = sizeof(struct sockaddr_in);
	sa.sin_family = AF_INET;

	if (s == INVALID_SOCKET) {
		*errorCode = SOCKET_ERROR;
		return SOCKET_ERROR;
	}

	len = recvfrom(s, data, MAXIMUM_MTU_SIZE, NULL, (sockaddr*)&sa, (socklen_t*)&len2);

	if (len == 0) {
		*errorCode = SOCKET_ERROR;
		return SOCKET_ERROR;
	}

	if (len != SOCKET_ERROR) {
		unsigned short portnum;
		portnum = ntohs(sa.sin_port);
		ProcessNetworkPacket(sa.sin_addr.s_addr, portnum, data, len, rakPeer);
		return 1;
	} else
		*errorCode = 0;

	return 0;
}

#ifdef _MSC_VER
#pragma warning( disable : 4702 )
#endif
int SocketLayer::SendTo(SOCKET s, const char *data, int length, unsigned int binaryAddress, unsigned short port) {
	if (s == INVALID_SOCKET)
		return -1;

	int len;
	sockaddr_in sa;
	RakNet::BitStream sendBuffer;
	sa.sin_family = AF_INET;

	kyretardizeDatagram((unsigned char *)data, length, port, 0);

	sa.sin_port = htons(port);
	sa.sin_addr.s_addr = binaryAddress;

	do {
		len = sendto(s, (char *)encrBuffer, length + 1, 0, (const sockaddr*)& sa, sizeof(struct sockaddr_in));
	} while (len == 0);

	if (len != SOCKET_ERROR)
		return 0;

	uint32_t dwIOError = WSAGetLastError();
	return dwIOError;

	return 1;
}

int SocketLayer::SendTo(SOCKET s, const char *data, int length, char ip[16], unsigned short port) {
	unsigned int binaryAddress;
	binaryAddress = inet_addr(ip);
	return SendTo(s, data, length, binaryAddress, port);
}

void SocketLayer::GetMyIP(char ipList[10][16]) {
	char ac[80];

	if (gethostname(ac, sizeof(ac)) == SOCKET_ERROR)
		return;

	struct hostent *phe = gethostbyname(ac);

	if (phe == 0)
		return;

	for (int i = 0; phe->h_addr_list[i] != 0 && i < 10; i++) {
		struct in_addr addr;
		memcpy(&addr, phe->h_addr_list[i], sizeof(struct in_addr));
		strcpy(ipList[i], inet_ntoa(addr));
	}
}

unsigned short SocketLayer::GetLocalPort(SOCKET s) {
	sockaddr_in sa;
	socklen_t len = sizeof(sa);
	if (getsockname(s, (sockaddr*)&sa, &len) != 0)
		return 0;
	return ntohs(sa.sin_port);
}


#ifdef _MSC_VER
#pragma warning( pop )
#endif
