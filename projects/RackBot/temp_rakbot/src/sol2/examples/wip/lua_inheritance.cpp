// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#define SOL_CHECK_ARGUMENTS 1
#include <sol.hpp>

#include "../assert.hpp"
#include <iostream>

int main(int, char*[]) {
	std::cout << "=== lua inheritance example ===" << std::endl;

	sol::state lua;
	lua.open_libraries(sol::lib::base);

	/* This example is currently under construction.
	For inheritance and classes within Lua, 
	consider using kikito's middleclass
	-- https://github.com/kikito/middleclass */

	return 0;
}
