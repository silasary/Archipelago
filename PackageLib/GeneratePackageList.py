import os
import zipfile
import json
import hashlib

BASE_URL =  "https://raw.githubusercontent.com/zig-for/Archipelago/zig/apworld_manager/PackageLib/worlds/"

out = {
    "worlds": [
    ]
}
this_dir = os.path.dirname(os.path.realpath(__file__))
walk_dir = this_dir + '/worlds'
for file in os.listdir(walk_dir):
    path = os.path.join(walk_dir, file)
    with open(path, 'rb') as f:
        hash_sha256 = hashlib.sha256(f.read()).hexdigest()
    metadata_str = zipfile.ZipFile(path).read('metadata.json')
    metadata = json.loads(metadata_str)
    metadata = {
        'metadata': metadata,
        'world': BASE_URL + file,
        'hash_sha256': hashlib.sha256(metadata_str).hexdigest(),
        'size': os.path.getsize(path)
    }
    out['worlds'].append(metadata)

with open(this_dir + '/index.json', 'w') as f:
    f.write(json.dumps(out, indent=4))
    f.close()

