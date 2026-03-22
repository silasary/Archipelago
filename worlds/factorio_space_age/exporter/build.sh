#!/usr/bin/env bash

set -e

version=$(jq -r .version archipelago-extractor/info.json)
rm -f archipelago-extractor_*.zip
zip -rq archipelago-extractor_"$version".zip archipelago-extractor/
echo archipelago-extractor_"$version".zip
