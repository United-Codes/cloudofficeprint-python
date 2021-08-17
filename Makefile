PYTHON = python3

.PHONY = help clean-build package clean-docs docs docs-live

help:
	@echo "*----------------------------------*"
	@echo "| cloudofficeprint-python make help |"
	@echo "*----------------------------------*"
	@echo
	@echo "package:             build the package"
	@echo "clean-build:         remove previously built package files, executed by the package rule"
	@echo "docs:                build the docs"
	@echo "clean-docs:          remove previously built docs, executed by the docs rule"
	@echo "docs-live:           host a live (auto-update) version of the docs at localhost:8080 for testing"

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

package: clean-build
	${PYTHON} setup.py sdist bdist_wheel

clean-docs:
	rm -rf docs/html/

docs: clean-docs
	pdoc --html -o ./docs/html --template-dir ./docs/templates cloudofficeprint/

docs-live:
	pdoc --html -f -o ./docs/html --template-dir ./docs/templates cloudofficeprint/ --http localhost:8080
