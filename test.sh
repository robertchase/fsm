# use docker to run tests
#
# to override default tests, supply cmdline arguments, which will be passed to pytest
#
# to override default directories and names, set env variables:
#     TEST_GIT - location of git directory where fsm and ergaleia are cloned ($HOME/git)
#     TEST_IMAGE - name of python3.6 docker image (bob/python3.6)
#
# assumes: 1. docker is running
#          2. a python3.6+ image is available ($TEST_IMAGE below)
#             with pytest installed
#
TEST_GIT=${TEST_GIT:-$HOME/git}
TEST_IMAGE=${TEST_IMAGE:-bob/python3.6}

CMD=${*:-tests}
GIT=/opt/git

docker run --rm -v=$TEST_GIT:$GIT -w $GIT/fsm -e PYTHONPATH=$GIT/fsm:$GIT/ergaleia $TEST_IMAGE pytest $CMD
