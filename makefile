train-with-pre-processed:
	python3 main.py --pre-processed
train:
	python3 main.py
test-model:
	python3 main.py --test-model
cache-clear:
	python3 scripts/cache_clear.py