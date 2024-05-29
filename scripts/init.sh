#!/usr/bin/env bash

# Install the required packages
conda update env -f environment.yml

# Install pre-commit hooks
pre-commit install