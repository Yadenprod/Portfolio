class Pickup *FindNearestPickup(int model);
class Vehicle *FindNearestVehicle(int opened = -1, int model = -1, int color1 = -1, int color2 = -1);
class Player *FindNearestPlayer(int skin = -1);
class Player *FindPlayerByName(std::string name);
void DoCoordMaster(bool state, float x = 0.f, float y = 0.f, float z = 0.f);

bool IsDirExists(const std::string &dirPath);
bool IsFileExists(const std::string &filePath);

const char *GenRandomString(char *s, const int len, bool numbers = true);
std::string GetRakBotPath();
std::string GetRakBotPath(const std::string &append);

std::string UrlEncode(const std::string &s);

void LTrim(std::string &s);
void RTrim(std::string &s);
void Trim(std::string &s);
std::vector<std::string> Split(const std::string &s, char delim);

int vasprintf(char **strp, const char *fmt, va_list ap);
int asprintf(char **strp, const char *fmt, ...);