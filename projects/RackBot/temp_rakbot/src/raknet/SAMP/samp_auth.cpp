// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include "StdAfx.h"

#include "RakBot.h"
#include "MiscFuncs.h"
#include "Settings.h"

#include "keycheck.h"
#include "raknet/SAMP/samp_netencr.h"

int charToInt(char input) {
	if (input >= '0' && input <= '9')
		return input - '0';
	if (input >= 'A' && input <= 'F')
		return input - 'A' + 10;
	if (input >= 'a' && input <= 'f')
		return input - 'a' + 10;
	return 0;
}

// This function assumes src to be a zero terminated sanitized string with
// an even number of [0-9a-f] characters, and target to be sufficiently large
void hexToBin(const std::string& input, uint8_t *out) {
	const char *src = input.c_str();

	while (*src && src[1]) {
		*(out++) = charToInt(*src) * 16 + charToInt(src[1]);
		src += 2;
	}
}

std::string binToHex(const uint8_t *input, int size) {
	std::string res;
	const char hex[] = "0123456789ABCDEF";
	for (int i = 0; i < size; i++) {
		uint8_t c = input[i];
		res += hex[c >> 4];
		res += hex[c & 0xf];
	}

	return res;
}

bool isHexString(const std::string &input) {
	const char hex[] = "0123456789ABCDEF";

	if ((input.length() % 2) != 0)
		return false;

	for (size_t i = 0; i < input.length(); i++) {
		bool result = false;

		for (size_t j = 0; j < sizeof(hex); j++) {
			if (input[i] == hex[j]) {
				result = true;
				break;
			}
		}

		if (!result)
			return false;
	}

	return true;
}

uint8_t mask1[] = {
	0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00,
	0x00, 0x0D, 0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x01, 0x00,
	0x00, 0x00, 0x00, 0x80, 0x08, 0x06, 0x00, 0x00, 0x00, 0xE4,
	0xB5, 0xB7, 0x0A, 0x00, 0x00, 0x00, 0x09, 0x70, 0x48, 0x59,
	0x73, 0x00, 0x00, 0x0B, 0x13, 0x00, 0x00, 0x0B, 0x13, 0x01,
	0x00, 0x9A, 0x9C, 0x18, 0x00, 0x00, 0x00, 0x04, 0x67, 0x41,
	0x4D, 0x41, 0x00, 0x00, 0xB1, 0x8E, 0x7C, 0xFB, 0x51, 0x93,
	0x00, 0x00, 0x00, 0x20, 0x63, 0x48, 0x52, 0x4D, 0x00, 0x00,
	0x7A, 0x25, 0x00, 0x00, 0x80, 0x83, 0x00, 0x00, 0xF9, 0xFF,
	0x00, 0x00, 0x80, 0xE9, 0x00, 0x00, 0x75, 0x30, 0x00, 0x00
};

uint8_t mask2[] = {
	0xFF, 0x25, 0x34, 0x39,
	0x4D, 0x00, 0x90, 0x90,
	0x90, 0x90, 0x56, 0x57,
	0x50, 0x8B, 0x44, 0x24,
	0x14, 0x8D, 0x0C, 0x80
};

uint8_t mask3[] = {
	0x45, 0xF7, 0x85, 0xFE, 0x83, 0xD1, 0xB6, 0xD8, 0x4A, 0xBA,
	0x65, 0x1B, 0x68, 0xFA, 0x01, 0x8A, 0x34, 0x4E, 0x44, 0xF5,
	0x38, 0x31, 0xA5, 0x24, 0x31, 0x34, 0xC9, 0xC6, 0x20, 0xCF,
	0xD1, 0xDA, 0x9A, 0x6C, 0x09, 0x11, 0xB5, 0x77, 0x25, 0xEB,
	0x69, 0x37, 0x2B, 0xD9, 0xD7, 0xE4, 0x2D, 0x7F, 0x64, 0x19,
	0xC9, 0x36, 0x80, 0x6C, 0x34, 0xBC, 0xBD, 0x19, 0x4C, 0x36,
	0xCD, 0x53, 0x0A, 0x4F, 0x9C, 0xA3, 0x9C, 0x83, 0x15, 0x58,
	0x56, 0x24, 0x3A, 0xC6, 0x19, 0x0F, 0x42, 0x7E, 0x8B, 0x19,
	0xEF, 0x12, 0xB8, 0x94, 0xA7, 0xDA, 0x83, 0x0D, 0x07, 0x2F,
	0x9A, 0x7E, 0x37, 0x24, 0x11, 0x0C, 0xB2, 0xEC, 0xB9, 0x69
};

std::string genAuthKey(const std::string &authIn) {
	VMProtectBeginUltra(__FUNCTION__);

	const char *authKeyUrlFormat = VMProtectDecryptStringA("https://rakbot.ru/keys/action/auth-key?v=3&auth_in=%s&key=%s&hwid=%u&ver=%s");

	std::string regKeyEncoded = UrlEncode(vars.regKey);
	std::string versionEncoded = UrlEncode(RAKBOT_VERSION);

	int authInLength = authIn.length();
	std::string authInHex = binToHex(reinterpret_cast<const uint8_t *>(authIn.c_str()), authInLength);

	uint8_t *authInBytes = new uint8_t[authInLength + 2];
	hexToBin(authInHex, authInBytes);

	uint8_t tmp1 = 0;
	uint8_t tmp2 = 0;
	uint8_t tmp3 = 0;

	for (int i = 0; i < authInLength; i++) {
		tmp1 = authInBytes[i];
		for (int j = 0; j < 66; j++) {
			tmp2 = tmp1 ^ mask3[j] ^ 0x13;
			tmp1 = tmp2;
		}
		authInBytes[i] = tmp2;
	}

	for (int i = 0; i < 4; i++) {
		tmp1 = authInBytes[i];
		for (int j = 0; j < 17; j++) {
			tmp2 = tmp1 ^ mask2[j] ^ 0x37;
			tmp1 = tmp2;
		}
		authInBytes[i] = tmp2;
	}

	srand(time(nullptr));
	authInBytes[authInLength] = rand() % 100;
	authInBytes[authInLength + 1] = rand() % 100;

	for (int k = 0; k < authInBytes[authInLength + 1]; k++) {
		for (int i = 0; i < authInLength; i++) {
			tmp1 = authInBytes[i];
			tmp2 = authInBytes[i + 1];
			tmp3 = authInBytes[authInLength + 1];
			authInBytes[i] = tmp1 ^ tmp2 ^ tmp3 ^ mask3[k];
		}

		tmp1 = authInBytes[authInLength];
		tmp2 = authInBytes[authInLength + 1];
		authInBytes[authInLength] = tmp1 ^ tmp2 ^ mask3[k];
	}

	std::string authInEncrypted = binToHex(authInBytes, authInLength + 2);
	delete[] authInBytes;

	char url[256];
	snprintf(url, sizeof(url), authKeyUrlFormat,
		authInEncrypted.c_str(), regKeyEncoded.c_str(), GetDeviceID(), versionEncoded.c_str());

	CURLcode curlCode = OpenURL(url);

	VMProtectFreeString(authKeyUrlFormat);

	if (curlCode == CURLE_OK) {
		std::string authTempKey = CurlBuffer;

		if (!isHexString(authTempKey))
			return authIn;

		uint8_t *authOutBytes = new uint8_t[authTempKey.length() + 1];
		hexToBin(authTempKey, authOutBytes);

		for (int k = (authOutBytes[21] - 1); k >= 0; k--) {
			tmp1 = authOutBytes[20];
			tmp2 = authOutBytes[21];
			authOutBytes[20] = tmp1 ^ tmp2 ^ mask3[k];

			for (int i = 20; i > 0; i--) {
				tmp1 = authOutBytes[i - 1];
				tmp2 = authOutBytes[i];
				tmp3 = authOutBytes[21];
				authOutBytes[i - 1] = tmp1 ^ tmp2 ^ tmp3 ^ mask3[k];
			}
		}

		for (int i = 0; i < 20; i++) {
			tmp1 = authOutBytes[i];
			for (int j = 0; j < 100; j++) {
				tmp2 = tmp1 ^ mask3[j] ^ 0xAD;
				tmp1 = tmp2;
			}
			authOutBytes[i] = tmp2;
		}

		for (int i = 0; i < 15; i++) {
			tmp1 = authOutBytes[i];
			for (int j = 0; j < 100; j++) {
				tmp2 = tmp1 ^ mask1[j] ^ 0xDE;
				tmp1 = tmp2;
			}
			authOutBytes[i] = tmp2;
		}

		for (int i = 0; i < 10; i++) {
			tmp1 = authOutBytes[i];
			for (int j = 0; j < 100; j++) {
				tmp2 = tmp1 ^ mask3[j] ^ 0x88;
				tmp1 = tmp2;
			}
			authOutBytes[i] = tmp2;
		}

		for (int i = 0; i < 5; i++) {
			tmp1 = authOutBytes[i];
			for (int j = 0; j < 100; j++) {
				tmp2 = tmp1 ^ mask1[j] ^ 0x14;
				tmp1 = tmp2;
			}
			authOutBytes[i] = tmp2;
		}

		for (int i = 10; i < 15; i++) {
			tmp1 = authOutBytes[i];
			for (int j = 0; j < 100; j++) {
				tmp2 = tmp1 ^ mask1[j] ^ 0x6F;
				tmp1 = tmp2;
			}
			authOutBytes[i] = tmp2;
		}

		for (int i = 15; i < 20; i++) {
			tmp1 = authOutBytes[i];
			for (int j = 0; j < 100; j++) {
				tmp2 = tmp1 ^ mask1[j] ^ 0xDB;
				tmp1 = tmp2;
			}
			authOutBytes[i] = tmp2;
		}

		for (int i = 0; i < 20; i++) {
			authOutBytes[i] ^= mask2[i];
		}

		std::string authOut = binToHex(authOutBytes, 20);
		delete[] authOutBytes;

		VMProtectEnd();
		return authOut;
	} else {
		RakBot::app()->log("[RAKBOT] Ошибка #%d при получении AUTH_KEY");
		VMProtectEnd();
		return nullptr;
	}
}