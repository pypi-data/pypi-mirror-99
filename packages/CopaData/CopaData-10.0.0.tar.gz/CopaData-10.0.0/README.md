## Package description
This package contains data connectivity modules developed by COPA-DATA.

## Included modules
- pyZAN

## pyZAN module description
pyZAN is a module to connect with a Report Engine metadata database. It provides:
- read access to metadata tables
- access to connector functions for reading historic variable values, alarms, events, lots, shifts and context lists
- option to execute SQL Stored Procedures and SQL Userdefined Functions

Data is returned as pandas DataFrames and can be used in all common data science libraries.

## Prerequisite modules
- pyodbc (requires Microsoft Visual C++ Build Tools)
- pandas

## Prerequisites to retrieve data
- Report Engine 10 or higher
- zenon Analyzer 3.30 or higher
- Report Engine metadada database including at least one project
- valid connection to the Report Engine metadata database
- valid configuration to receive data from at least one of the following connectors:
  - SCADA Service Engine Connector
  - SCADA SQL Connector
  - 3rd Party Database Connector

## Tutorials
https://github.com/COPA-DATA/pyZAN

