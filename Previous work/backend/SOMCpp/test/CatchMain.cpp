// Let Catch provide main():
#define CATCH_CONFIG_MAIN

#include "catch.hpp"

// Compile implementation of Catch for use with files that do contain tests:
// - g++ -std=c++11 -Wall -I$(CATCH_SINGLE_INCLUDE) -c CatchMain.cpp
// - cl -EHsc -I%CATCH_SINGLE_INCLUDE% -c CatchMain.cpp