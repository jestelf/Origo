# tools.generate_docs

import os

def scan_and_generate(src='origo3d', out='docs/api'):
    os.makedirs(out, exist_ok=True)
    for root, _, files in os.walk(src):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                rel_path = os.path.relpath(os.path.join(root, file), src)
                module_name = rel_path.replace(os.sep, '.').replace('.py', '')
                with open(os.path.join(out, module_name + '.md'), 'w') as f:
                    f.write(f"# API: {module_name}\n\nTODO: Autodoc here\n")

if __name__ == '__main__':
    scan_and_generate()
