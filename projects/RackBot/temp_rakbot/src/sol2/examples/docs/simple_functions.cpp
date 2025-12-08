// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#define SOL_CHECK_ARGUMENTS 1

#include <sol.hpp>
#include "../assert.hpp"

int main() {
	sol::state lua;
	int x = 0;
	lua.set_function("beep", [&x]{ ++x; });
	lua.script("beep()");
	c_assert(x == 1);

	sol::function beep = lua["beep"];
	beep();
	c_assert(x == 2);

	return 0;
}
