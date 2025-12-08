// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
#include <cstdlib>

struct pre_main {
	pre_main() {
#ifdef SOL2_CI
#ifdef _MSC_VER
	_set_abort_behavior(0, _WRITE_ABORT_MSG);
#endif
#endif
	}
} pm;
