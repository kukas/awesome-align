import sys

src = open(sys.argv[1], encoding='utf-8')
tgt = open(sys.argv[2], encoding='utf-8')

out = open(sys.argv[3], 'w')

for s, t in zip(src, tgt):
    s, t = s.strip(), t.strip()
    l = (' ||| ').join([s, t]) + '\n'
    out.write(l)

if next(src, None) is not None or next(tgt, None) is not None:
    raise ValueError('mismatch in number of lines')

src.close()
tgt.close()
