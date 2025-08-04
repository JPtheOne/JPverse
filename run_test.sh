#!/bin/bash
# Simple test runner without Docker (for GitHub Actions exercise)

python -m unittest discover -s tests -v
