
lock additional_args='':
  @echo "Compiling requirements.in file"
  @uv pip compile -o requirements.txt {{additional_args}} requirements/requirements.in
  @echo "Compiling requirements-dev.in file"
  @uv pip compile -o requirements-dev.txt {{additional_args}} requirements/requirements-dev.in
	
  @echo finished successfuly

