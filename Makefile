.PHONY: sh connect build test lint

IMAGE := fsm-dev
IMAGE := alpine-python
NAME := fsm
NET := --net test
GIT := $(HOME)/git
WORKING := -w /opt/git/fsm

VOLUMES := -v=$(GIT):/opt/git

DOCKER := docker run $(OPT) -it --rm  $(VOLUMES) $(WORKING) $(NET) -e PYTHONPATH=. --name $(NAME) $(IMAGE)

sh:
	$(DOCKER) /bin/sh

connect:
	docker exec -it $(NAME) bash

build:
	docker build -t $(IMAGE) -f Dockerfile .

test:
	$(DOCKER) pytest $(ARGS)

lint:
	$(DOCKER) flake8 --exclude=.git,.ropeproject fsm tests
