#pragma once

#pragma warning(disable:4091)
#pragma warning(disable:4005)
#pragma warning(disable:4996)
#pragma warning(disable:4800)

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <map>
#include <forward_list>
#include <cstdlib>
#include <cstddef>
#include <cstdint>
#include <cstdarg>
#include <algorithm> 
#include <cctype>
#include <locale>
#include <string>
#include <iomanip>
#include <sstream>
#include <list>
#include <regex>
#include <functional>
#include <thread>
#include <mutex>

#include <shlobj.h>
#include <shellapi.h>
#include <shobjidl.h>
#include <shlguid.h>
#include <objbase.h>
#include <intrin.h>
#include <direct.h>
#include <wbemcli.h>
#include <comutil.h>
#include <atlconv.h>
#include <io.h>
#include <fcntl.h>
#include <iconv.h>
#include <DbgHelp.h>
#include <iphlpapi.h>
#include <Psapi.h>
#include <winsock2.h>
#include <WinInet.h>
#include <commctrl.h>
#include <process.h>

#include "curl\curl.h"

#pragma intrinsic(_ReturnAddress)

#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "Psapi.lib")
#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "DbgHelp.lib")
#pragma comment(lib, "libiconv.lib")
#pragma comment(lib, "wbemuuid.lib")
#pragma comment(lib, "comsuppw.lib")
#pragma comment(lib, "libcurl.lib")
#pragma comment(lib, "wldap32.lib")
#pragma comment(lib, "comctl32.lib")
#pragma comment(lib, "urlmon.lib")

#pragma comment(linker, "/manifestdependency:\"type='win32' \
                        name='Microsoft.Windows.Common-Controls' \
                        version='6.0.0.0' processorArchitecture='*'\
                        publicKeyToken='6595b64144ccf1df' language='*'\"")

#include <VMProtectSDK.h>
#pragma comment(lib, "VMProtectSDK32.lib")