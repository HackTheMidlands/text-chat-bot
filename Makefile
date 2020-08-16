ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DATA_PATH       ?= data
MAKE_ENV        += TOKEN SERVER_ID CATAGORY_ID COMMAND_CHANNEL_ID MEMBER_ROLE_ID DATA_PATH
SHELL_EXPORT    := $(foreach v,$(MAKE_ENV),$(v)='$($(v))' )
CONFIG          := $(shell $(SHELL_EXPORT) envsubst <config_template.json)

PACKAGE       ?= bot
DEFAULT_IMAGE ?= hackthemidlands/text-chat-bot
VERSION       ?= $(shell git describe --tags --always --dirty --match="v*" 2> /dev/null || cat $(CURDIR)/.version 2> /dev/null || echo v0)
DOCKER_REGISTRY_DOMAIN ?= docker.pkg.github.com
DOCKER_REGISTRY_PATH   ?= hackthemidlands/text-chat-bot
DOCKER_IMAGE           ?= $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(VERSION)
DOCKER_IMAGE_DOMAIN    ?= $(DOCKER_REGISTRY_DOMAIN)/$(DOCKER_IMAGE)


.PHONY: run
run:
	source ./bin/build-config.sh && poetry run python -m chat-manager

.PHONY: watch
watch:
	reflex -r '\.py$\' -s -- sh -c "$(MAKE) docker-logs"

.PHONY: docker-build
docker-build:
	docker build $(ROOT_DIR) --tag $(DOCKER_IMAGE_DOMAIN) --file $(ROOT_DIR)/Dockerfile

.PHONY: docker-run
docker-run: docker-build docker-rm
	source ./bin/build-config.sh && docker run -d --name chat-manager -e CONFIG -v $(DOCKER_MOUNT_PATH)/data:/data --restart=no $(DOCKER_IMAGE_DOMAIN)

.PHONY: docker-rm
docker-rm:
	docker rm -f chat-manager | true

.PHONY: docker-logs
docker-logs: docker-run
	docker logs -f chat-manager
