
lock:
  @echo "Compiling requirements.in file"
  @uv pip compile -o requirements.txt requirements.in
  @echo "Compiling requirements-dev.in file"
  @uv pip compile -o requirements-dev.txt requirements-dev.in
	
  @echo finished successfuly

