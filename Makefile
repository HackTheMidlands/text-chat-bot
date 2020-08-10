ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
TOKEN           ?= "<your Discord bot's token>"
SERVER_ID       ?= "<the Discord server's ID as a string>"
CATAGORY_ID     ?= "<the ID (as a string) of the catagory channels should be placed in>"
MAKE_ENV        += TOKEN SERVER_ID CATAGORY_ID
SHELL_EXPORT    := $(foreach v,$(MAKE_ENV),$(v)='$($(v))' )

.PHONY: run
run:
	poetry run python -m chat-manager

.PHONY: build-config
build-config:

.PHONY: config
config:
	$(SHELL_EXPORT) envsubst <config_template.json >config.json ;\


.PHONY: watch
watch:
	reflex -r '\.py$\' -s -- sh -c 'make run'
