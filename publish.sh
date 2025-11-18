#!/bin/bash

# SUTRA Publishing Script
# This script automates the process of publishing to PyPI

set -e  # Exit on error

echo "======================================"
echo "SUTRA Publishing Script"
echo "======================================"

# Check if build and twine are installed
echo ""
echo "Checking dependencies..."
pip show build > /dev/null 2>&1 || pip install build
pip show twine > /dev/null 2>&1 || pip install twine
echo "✓ Dependencies installed"

# Clean old builds
echo ""
echo "Cleaning old builds..."
rm -rf build/ dist/ *.egg-info
echo "✓ Old builds removed"

# Build the package
echo ""
echo "Building package..."
python -m build
echo "✓ Package built successfully"

# Check the distribution
echo ""
echo "Checking distribution..."
python -m twine check dist/*
echo "✓ Distribution check passed"

# Upload to TestPyPI
echo ""
echo "======================================"
echo "Uploading to TestPyPI..."
echo "======================================"
python -m twine upload --repository testpypi dist/*

echo ""
echo "✓ Uploaded to TestPyPI successfully!"
echo ""
echo "Test installation with:"
echo "pip install --index-url https://test.pypi.org/simple/ --no-deps sutra"
echo ""

# Ask for confirmation before uploading to PyPI
read -p "Do you want to upload to PyPI? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "======================================"
    echo "Uploading to PyPI..."
    echo "======================================"
    python -m twine upload dist/*
    
    echo ""
    echo "======================================"
    echo "✓ Successfully published to PyPI!"
    echo "======================================"
    echo ""
    echo "Install with: pip install sutra"
    echo ""
else
    echo ""
    echo "✓ Skipped PyPI upload"
    echo ""
fi

echo "Done!"
