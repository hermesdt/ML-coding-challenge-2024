#!/usr/bin/env bash

set -e

# Install the required packages
mamba env update -f conda.yaml

# Install pre-commit hooks
pre-commit install