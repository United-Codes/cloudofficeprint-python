#!/bin/bash
read -p "This may overwrite existing docs, continue? [yN] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi
pdoc --html --force --output-dir ./docs/html --template-dir ./docs/templates apexofficeprint/
