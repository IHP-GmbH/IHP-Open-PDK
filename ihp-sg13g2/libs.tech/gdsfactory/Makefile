install:
	uv sync --extra docs --extra dev

dev: install

update-pre:
	pre-commit autoupdate

tech:
	python install_tech.py

test:
	uv run pytest -s

test-force:
	uv run pytest -s --force-regen

git-rm-merged:
	git branch -D `git branch --merged | grep -v \* | xargs`

release:
	git push
	git push origin --tags

build:
	rm -rf dist
	pip install build
	python -m build

docs:
	uv run python .github/write_cells.py
	uv run jb build docs

mask:
	python ubcpdk/samples/test_masks.py

.PHONY: drc doc docs install build
