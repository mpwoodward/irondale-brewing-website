#!/usr/bin/env python3
"""
Scan main.css selectors and search repository files for usage.
Outputs JSON to stdout.
"""
import os, re, json, sys
root = r"c:\Users\mpwoo\projects\irondale-brewing-pelican"
css_path = os.path.join(root, 'themes','irondale-brewing','static','css','main.css')

if not os.path.exists(css_path):
    print(json.dumps({'error':'main.css not found', 'path': css_path}))
    sys.exit(1)

try:
    txt = open(css_path, encoding='utf-8').read()
except Exception as e:
    print(json.dumps({'error':'could not read main.css', 'exception':str(e)}))
    sys.exit(1)

# crude selector extraction: split on '{' and parse selector parts
parts = re.split(r"\{", txt)
selectors = []
for p in parts[:-1]:
    selector_text = p.strip()
    # remove possible trailing comments
    selector_text = re.sub(r'/\*.*?\*/', '', selector_text, flags=re.S)
    for s in selector_text.split(','):
        s = s.strip()
        for m in re.finditer(r'([.#][A-Za-z0-9_-]+)', s):
            selectors.append(m.group(1))
selectors = sorted(set(selectors))

# file extensions to search
exts = {'.html','.htm','.js','.py','.css','.md','.jinja','.txt','.json'}
files = []
for dirpath, dirnames, filenames in os.walk(root):
    # skip .git and node_modules and output/pagefind
    parts = dirpath.split(os.sep)
    if '.git' in parts or 'node_modules' in parts:
        continue
    for fn in filenames:
        _,e = os.path.splitext(fn)
        if e.lower() in exts:
            files.append(os.path.join(dirpath,fn))

file_contents = {}
for f in files:
    try:
        file_contents[f] = open(f,encoding='utf-8',errors='ignore').read()
    except Exception as e:
        file_contents[f] = ''

results = []
for token in selectors:
    kind = 'class' if token.startswith('.') else 'id'
    name = token[1:]
    re_html = re.compile(r'class=["\'][^"\']*\b' + re.escape(name) + r'\b[^"\']*["\']')
    re_css = re.compile(r'\.' + re.escape(name) + r'\b')
    re_id_html = re.compile(r'id=["\']' + re.escape(name) + r'["\']')
    total = 0
    matches = []
    for path, content in file_contents.items():
        # skip main.css itself
        if os.path.normpath(path) == os.path.normpath(css_path):
            continue
        found = False
        if kind == 'class':
            if re_html.search(content) or re_css.search(content):
                found = True
        else:
            if re_id_html.search(content) or re_css.search(content):
                found = True
        if found:
            total += 1
            matches.append(path)
    results.append({'token':token,'type':kind,'name':name,'count_files':total,'sample_files':matches[:6]})

unused = [r for r in results if r['count_files']==0]
out = {'summary':{'css_path':css_path,'total_selectors':len(selectors),'unused_count':len(unused)},'unused':unused,'results_sample':results[:20]}
print(json.dumps(out, indent=2))
