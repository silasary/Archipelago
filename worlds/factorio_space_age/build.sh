#!/usr/bin/env bash

set -e

files=(
    LICENSE
    CHANGELOG.md
    archipelago.json
    requirements.txt

    __init__.py
    Client.py
    Mod.py
    Options.py
    settings.py
    Logic.py
    FactorioData.py

    data/__init__.py
    data/ap_data.py
    data/generated_names.py
    data/generated_ids.py
    data/json_dumps_but_smaller.py
    data/ap-dump.json
    data/ap-dump-vulcanus.json
    data/ap-dump-gleba.json
    data/ap-dump-fulgora.json

    data/mod/LICENSE.md
    data/mod/thumbnail.png
    data/mod/settings.lua
    data/mod/settings-updates.lua
    data/mod/data-updates.lua
    data/mod/control.lua
    data/mod/lib.lua
    data/mod/graphics/icons/ap.png
    data/mod/graphics/icons/ap_unimportant.png
    data/mod/graphics/icons/trophy.png
    data/mod_template/template_parameters.lua
    data/mod_template/locale/en/locale.cfg

    docs/en_Factorio_Space_Age.md
    docs/setup_en.md
    docs/factorio-download.png
    docs/connect-to-ap-server.png
)

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

(cd "$(dirname "$here")" &&
    rm -f factorio_space_age/factorio_space_age.apworld &&
    zip -q factorio_space_age/factorio_space_age.apworld \
        $(for f in "${files[@]}"; do echo factorio_space_age/"$f"; done) &&

    echo "$(pwd)"/factorio_space_age/factorio_space_age.apworld
)
