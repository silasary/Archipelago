# factorio/data

How to recreate all the data:

1. See https://github.com/thejoshwolfe/FactorioInformationExtractor . The result is a file `ap-dump.json`.
2. Run `./import-ap-dump.py .../path/to/ap-dump.json`. This creates `__init__.py`
