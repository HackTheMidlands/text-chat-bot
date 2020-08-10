ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
TOKEN           ?= "<your Discord bot's token>"
SERVER_ID       ?= "<the Discord server's ID as a string>"
CATAGORY_ID     ?= "<the ID (as a string) of the catagory channels should be placed in>"
MAKE_ENV        += TOKEN SERVER_ID CATAGORY_ID
SHELL_EXPORT    := $(foreach v,$(MAKE_ENV),$(v)='$($(v))' )

PACKAGE       ?= bot
DEFAULT_IMAGE ?= hackthemidlands/text-chat-bot
VERSION       ?= $(shell git describe --tags --always --dirty --match="v*" 2> /dev/null || cat $(CURDIR)/.version 2> /dev/null || echo v0)
DOCKER_REGISTRY_DOMAIN ?= docker.pkg.github.com
DOCKER_REGISTRY_PATH   ?= hackthemidlands/text-chat-bot
DOCKER_IMAGE           ?= $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(VERSION)
DOCKER_IMAGE_DOMAIN    ?= $(DOCKER_REGISTRY_DOMAIN)/$(DOCKER_IMAGE)

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

.PHONY: docker-build
docker-build:
	docker build $(ROOT_DIR) --tag $(DOCKER_IMAGE_DOMAIN) --file $(ROOT_DIR)/Dockerfile \
	    --build-arg TOKEN=$(TOKEN) \
	    --build-arg SERVER_ID=$(SERVER_ID) \
	    --build-arg CATAGORY_ID=$(CATAGORY_ID)

.PHONY: docker-prod-build
docker-prod-build:
	docker build $(ROOT_DIR) --tag $(DOCKER_IMAGE_DOMAIN) --file $(ROOT_DIR)/prod.Dockerfile \
	    --build-arg TOKEN=$(TOKEN) \
	    --build-arg SERVER_ID=$(SERVER_ID) \
	    --build-arg CATAGORY_ID=$(CATAGORY_ID)

.PHONY: docker-run
docker-run:
	docker run --rm $(DOCKER_IMAGE_DOMAIN)