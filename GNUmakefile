#
#
# GNUmakefile
#
# Author: Valentin Ionita <valentin.ionita@ssh.com>
#
# Copyright (c) 2023 SSH Communications Security, Finland
#                    All rights reserved
#

help = \
make targets: _N\
	help: Show this help message. _N\
	build-local-environment: Create a local python virtual venv environment and activate it. _N\
	build-local-requirements: Compile complete Python requirements, including development. _N\
	build-server-requirements: Compile server Python requirements. _N\
	build-client-requirements: Compile Typer client Python requirements. _N\
	build-server: Build Docker image for server application. _N\
	serve: Run server application. _N\
	build-client: Build Docker image for Typer client application. _N\
	run-client: Run Typer client Docker image interactively.

.PHONY: help build-local-environment build-local-requirements build-server-requirements \
	build-client-requirements build-server serve build-client run-client

help:
	@echo $($@) | sed -e 's/ *_N/\n/g' | sed -e 's/^  */  /g'

build-local-environment:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r ./requirements.txt

build-local-requirements:
	@pip-compile --quiet --all-extras --resolver=backtracking --allow-unsafe --strip-extras

build-server-requirements:
	@pip-compile --quiet --extra=server --resolver=backtracking --allow-unsafe --strip-extras \
		--output-file=./server/requirements.txt

build-client-requirements:
	@pip-compile --quiet --extra=client --resolver=backtracking --allow-unsafe --strip-extras \
		--output-file=./client/requirements.txt

build-server:
	@cd server && docker build -t demo-server .

serve:
	@docker run -t --init --rm --network=host -v ./server/:/app demo-server

build-client:
	@cd client && docker build -t demo-client .

run-client:
	@docker run -it --init --rm --network=host -v ./client/:/app demo-client /bin/bash
