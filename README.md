# compile-health

A collection of python scripts for creating compile health reports for C++ projects on linux


## Quick Start

TODO!


## (Planned) Features

* per-source compile times
* per-header compile times
* link times
* warnings for possible ODR-violations due to diverging headers
* warnings for multiply compiled sources
* binary sizes
* warnings for symbol explosions
* dependency analysis
* black- and whitelists for includes
* CI-compatible limits and warnings for compile times
* reports (tex, markdown, html, json)


## Requirements

Currently only supports C++ builds on linux with ninja using either gcc, clang, or zapcc.


## Usage


### Parse Build Setup

    parse-build.py /folder/with/build.ninja/

The first step is parsing the commands necessary to build the complete project.
This creates a `build.json` file expected by further processing steps.


### Compile and Link Times

    time-commands.py

Executes and times all commands (compile, link, pack).
This creates a `command-timing.json` file.

* Requires: `build.json`


### Build Dependencies

    build-deps.py

Creates `build-deps.json` containing per-source dependencies (all included headers).

* Requires: `build.json`

### Header Parse Times

    time-headers.py

Times parsing overhead of all headers.
This creates a `header-timing.json` file.

* Requires: `build.json`


### CSV Reports

    report-csv.py

Creates `.csv` files for various generated files (if they are present).
Supports:

* `command-timing.json`
* `header-timing.json`

* Requires: `build.json`
