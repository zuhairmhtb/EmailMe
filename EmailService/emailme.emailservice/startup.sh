#!/bin/bash
echo "sleeping..."
sleep 10
echo "Publishing package to private Pypi..."
poetry build
poetry publish -r ppypi
echo "Running application"
poetry run python emailme_emailservice/startup.py