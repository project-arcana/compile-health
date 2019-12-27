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

The first step is parsing the commands necessary to build the complete project.

    parse-build.py /folder/with/build.ninja/

This creates a `build.json` file expected by further processing steps.
