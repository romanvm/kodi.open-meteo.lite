lint:
	. .venv/bin/activate && \
	pylint weather.open-meteo.lite/libs weather.open-meteo.lite/main.py

PHONY: lint
