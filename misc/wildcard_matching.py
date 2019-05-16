def break_string(p, delimiter):
    seq = []
    while 1:
        if delimiter not in p:
            if len(p) > 0:
                seq.append(p)
            break

        pos = p.index(delimiter)
        s = p[0:pos]
        if len(s) > 0:
            seq.append(p[0:pos])
        seq.append(delimiter)
        if pos < len(p) - len(delimiter):
            p = p[pos + len(delimiter):]
        else:
            p = ''
    return seq

def match(a, p):
    if p == '*':
        return True

    if a == '':
        return p == ''

    if p == '':
        return a == ''

    seq1 = break_string(p, '*')
    seq = []
    for s in seq1:
        if '?' not in s:
            seq.append(s)
        else:
            seq += break_string(s, '?')
    print(seq)

    wild_len = len(a)
    gap = 0
    for s in seq:
        if s == '?':
            a = a[1:]
        elif s == '*':
            gap = wild_len
        else:
            if s not in a:
                return False

            pos = a.index(s)
            if pos > gap:
                return False

            a = a[pos+len(s):]
            gap = 0

    return len(a) <= gap

a = 'abcdefghijklmn'
p = '*cd??gh?*?'

print(match(a, p))
