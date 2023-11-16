# TODO: change this to fit windows, max, linux

PIP_COMPILE = pip-compile

compile_libs:
	@echo compiling requirements.in file
	${PIP_COMPILE}
	@echo compiling requirements-dev.in file
	${PIP_COMPILE} requirements-dev.in -o requirements-dev.txt
	@echo finished successfuly

