.PHONY: download_input
download_input:
	python tools/download_inputs.py

# usage: make run_day day=1
.PHONY: run_day
run_day:
	python days/day$(day)/main.py

