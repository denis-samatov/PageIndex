import json
import sys
import glob

def analyze_notebook(path):
    print(f"--- Analyzing {path} ---")
    try:
        with open(path, 'r') as f:
            nb = json.load(f)
        
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                print(f"Cell {i}:\n{source}\n")
                print("-" * 20)
    except Exception as e:
        print(f"Error reading {path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            analyze_notebook(path)
    else:
        # Default to all notebooks in ../notebooks relative to src
        notebooks = glob.glob("../notebooks/*.ipynb")
        for nb in notebooks:
            analyze_notebook(nb)
