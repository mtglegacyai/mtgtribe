# Phones never scroll sideways (MTG, 6 November 2026).
# Every table gets its column names copied onto each cell (data-label) and a class with its column count,
# so the stylesheet can stack each row on small screens instead of letting the table run off the edge:
#   2 columns, short values:  label on the left, value on the right, wrapping if needed   (class pt pt-c2)
#   2 columns, long text:     the first cell as a small title, the text underneath         (class pt pt-c2 pt-stack)
#   3 or more columns:        one block per row, a labelled line for each cell             (class pt pt-cN)
# Desktop and tablet layouts are unchanged. Pure text processing, no dependencies.
import re
from html import escape, unescape

LONG = 24   # a value longer than this (in characters) gets its own line on a phone

def _text(cell_html):
    return unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', cell_html)).strip())

def _add_class(tag, cls):
    m = re.search(r'\sclass="([^"]*)"', tag)
    if m:
        have = m.group(1).split()
        new = ' '.join(have + [c for c in cls.split() if c not in have])
        return tag[:m.start()] + f' class="{new}"' + tag[m.end():]
    return tag[:-1] + f' class="{cls}">'

def _label_table(t):
    head = re.search(r'<thead\b.*?</thead>', t, re.S)
    if not head: return t
    labels = [_text(x) for x in re.findall(r'<th\b[^>]*>(.*?)</th>', head.group(0), re.S)]
    n = len(labels)
    if n < 2: return t
    stack = False
    def row(m):
        nonlocal stack
        cells = list(re.finditer(r'<(td|th)\b[^>]*>(.*?)</\1>', m.group(0), re.S))
        out, pos = [], 0
        for i, c in enumerate(cells):
            out.append(m.group(0)[pos:c.start()])
            tag_end = c.group(0).index('>') + 1; tag = c.group(0)[:tag_end]
            if i < n and 'data-label=' not in tag:
                tag = tag[:-1] + f' data-label="{escape(labels[i], quote=True)}">'
            if i > 0 and len(_text(c.group(2))) > LONG:          # long text: label above, text underneath on phones
                tag = _add_class(tag, 'tl')
                if n == 2: stack = True
            out.append(tag + c.group(0)[tag_end:]); pos = c.end()
        out.append(m.group(0)[pos:])
        return ''.join(out)
    body = re.search(r'<tbody\b.*?</tbody>', t, re.S)
    if not body: return t
    new_body = re.sub(r'<tr\b.*?</tr>', row, body.group(0), flags=re.S)
    t = t[:body.start()] + new_body + t[body.end():]
    open_tag = re.match(r'<table\b[^>]*>', t).group(0)
    cls = f'pt pt-c{n}' + (' pt-stack' if stack else '')
    return _add_class(open_tag, cls) + t[len(open_tag):]

def label_tables(html):
    return re.sub(r'<table\b.*?</table>', lambda m: _label_table(m.group(0)), html, flags=re.S)

if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); n = label_tables(s)
        if n != s: open(f, 'w', encoding='utf-8').write(n); print('labelled tables in', f)
