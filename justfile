
lock:
	@echo compiling requirements.in file
	@uv pip compile --upgrade -o requirements.txt requirements.in
	
	@echo compiling requirements-dev.in file
	@uv pip compile --upgrade -o requirements-dev.txt requirements-dev.in
	
	@echo finished successfuly

