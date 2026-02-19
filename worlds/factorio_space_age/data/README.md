# factorio/data

How to recreate all the data:

1. See https://github.com/thejoshwolfe/FactorioInformationExtractor . The result is a file `ap-dump.json`.
2. Run `./import-ap-dump.py .../path/to/ap-dump.json`. This creates all the `generated*.py` files. There is an additional `ap-dump.json` file (gitignored) that can be useful for debugging.
