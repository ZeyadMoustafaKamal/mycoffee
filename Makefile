# TODO: change this to fit windows, max, linux


lock:
	@echo compiling requirements.in file
	@uv pip compile requirements.in -o requirements.txt
	
	@echo compiling requirements-dev.in file
	@uv pip compile requirements-dev.in -o requirements-dev.txt
	
	@echo finished successfuly

