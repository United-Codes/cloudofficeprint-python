#!/usr/bin/env bash
set -e


# Clean old build folders
echo "[1] Cleaning previous build artifacts (build/, dist/, *.egg-info)..."
rm -rf build/ dist/ *.egg-info

# Remove any previously generated docs for this package
echo "[2] Removing old auto-generated docs (docs/cloudofficeprint/)..."
rm -rf docs/cloudofficeprint

# Generate documentation via pdoc
echo "[3] Generating documentation with pdoc into docs/cloudofficeprint/..."
# Make sure pdoc is installed: pip install pdoc3
pdoc --html --force --output-dir docs/ cloudofficeprint

# Build source (+sdist) and wheel (+bdist_wheel)
echo "[4] Building source and wheel distributions (python setup.py sdist bdist_wheel)..."
python setup.py sdist bdist_wheel

# Verify the newly built distributions with twine
echo "[5] Verifying distributions with twine check dist/*..."
twine check dist/*

echo
echo " wow ,completed all steps."
