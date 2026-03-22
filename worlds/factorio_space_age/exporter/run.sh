#!/usr/bin/env bash

set -e

FACTORIO_PATH=~/software/factorio # Or whatever path

rm -rf mods/ && mkdir mods/
./build.sh
mv archipelago-extractor*.zip mods/
echo -n '/ap-get-info-dump' | gtkclip # copy this to clipboard
$FACTORIO_PATH/bin/x64/factorio --mod-directory "$(cd mods/ && pwd)" --start-server-load-latest
# Then paste the above.
# Then type /quit and hit Enter.
