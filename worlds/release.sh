#!/bin/bash

VERSION="1.6.0"

# Ensure the versioned release directory exists
mkdir -p "releases/${VERSION}"

# Define exclude patterns
EXCLUDES=(
  "*/.DS_Store"
  "*/__pycache__/*"
  "*/__MACOSX/*"
  "s4ap_0.1.11b_Messages.txt"
  "items-testing-please-ignore-me.json"
)

# Create the zip file in the versioned release folder
zip -r releases/${VERSION}/sims4.apworld sims4 -x "${EXCLUDES[@]}"