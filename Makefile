ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DATA_PATH       ?= 'data'
MAKE_ENV        += TOKEN SERVER_ID CATAGORY_ID COMMAND_CHANNEL_ID MEMBER_ROLE_ID DATA_PATH
SHELL_EXPORT    := $(foreach v,$(MAKE_ENV),$(v)='$($(v))' )

PACKAGE       ?= bot
DEFAULT_IMAGE ?= hackthemidlands/text-chat-bot
VERSION       ?= $(shell git describe --tags --always --dirty --match="v*" 2> /dev/null || cat $(CURDIR)/.version 2> /dev/null || echo v0)
DOCKER_REGISTRY_DOMAIN ?= docker.pkg.github.com
DOCKER_REGISTRY_PATH   ?= hackthemidlands/text-chat-bot
DOCKER_IMAGE           ?= $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(VERSION)
DOCKER_IMAGE_DOMAIN    ?= $(DOCKER_REGISTRY_DOMAIN)/$(DOCKER_IMAGE)
DOCKER_BUILD_ARGS      := $(foreach v,$(MAKE_ENV), --build-arg $(v)='$($(v))' )


.PHONY: run
run: config
	poetry run python -m chat-manager

.PHONY: build-config
build-config:

.PHONY: config
config:
	$(SHELL_EXPORT) envsubst <config_template.json >config.json ;\

.PHONY: watch
watch:
	reflex -r '\.py$\' -s -- sh -c 'make run'

.PHONY: docker-build
docker-build: config
	docker build $(ROOT_DIR) --tag $(DOCKER_IMAGE_DOMAIN) --file $(ROOT_DIR)/Dockerfile $(DOCKER_BUILD_ARGS)

.PHONY: docker-run
docker-run:
	docker run --rm $(DOCKER_IMAGE_DOMAIN)