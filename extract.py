import json
nb = json.load(open('Sample_ML_Submission_Template (1).ipynb', encoding='utf-8'))
with open('mdowns.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(nb.get('cells', [])):
        if c['cell_type'] == 'markdown':
            content = ''.join(c['source'])
            f.write(f"--- Cell {i} ---\n{content}\n")
