.PHONY: test dist clean

.DEFAULT_TARGET = test

test:
	python3 -B -m unittest test.basic

dist:
	python3 -m build --no-isolation --wheel && rm -rf a4.egg-info

clean:
	rm -rf a4.egg-info build dist
