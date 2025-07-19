# origo3d.package.package_manifest

import json

def load_manifest(path):
    with open(path, 'r') as f:
        return json.load(f)
