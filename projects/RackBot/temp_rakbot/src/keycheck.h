uint32_t GetDeviceID();
bool IsWrongKey();
void CheckKey();
CURLcode OpenURL(const std::string &url);

extern char CurlBuffer[4096];