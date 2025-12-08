// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#define SOL_CHECK_ARGUMENTS 1
#include <sol.hpp>

#include <iostream>
#include "../../assert.hpp"

int main(int, char*[]) {
	std::cout << "=== opening a state example ===" << std::endl;

	sol::state lua;
	// open some common libraries
	lua.open_libraries(sol::lib::base, sol::lib::package);
	lua.script("print('bark bark bark!')");

	std::cout << std::endl;

	return 0;
}
