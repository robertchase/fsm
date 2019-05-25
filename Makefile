.PHONY: bash connect build test

IMAGE := fsm-dev
NAME := fsm
NET := --net test
GIT := $(HOME)/git
WORKING := -w /opt/git/fsm

VOLUMES := -v=$(GIT):/opt/git

DOCKER := docker run $(OPT) -it --rm  $(VOLUMES) $(WORKING) $(NET) -e PYTHONPATH=. --name $(NAME) $(IMAGE)

bash:
	$(DOCKER) /bin/bash

connect:
	docker exec -it $(NAME) bash

build:
	docker build -t $(IMAGE) -f Dockerfile .

test:
	$(DOCKER) pytest $(ARGS)
