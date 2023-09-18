#pragma once
#include "parser.h"
#include <vector>


void createTable(const Command& command, std::vector<Command>& collection);

void insertRecord(const Command& command, std::vector<Command>& collection, SelectionResult& result);

void deleteAllRecords();

void printSelectionResult(const SelectionResult& result);
