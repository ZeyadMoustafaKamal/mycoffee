
lock:
  @echo "Compiling requirements.in file"
  @uv pip compile -o requirements/requirements.txt requirements/requirements.in
  @echo "Compiling requirements-dev.in file"
  @uv pip compile -o requirements/requirements-dev.txt requirements/requirements-dev.in
	
  @echo finished successfuly

