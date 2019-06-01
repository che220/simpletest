class LeftBrace:
    def __init__(self, c):
        self.brace = c
        self.left = None
        self.right = None

def braces(values):
    rs = []
    pairs = {'}' : '{', ']' : '[', ')' : '('}
    for value in values:
        brace = None
        early_break = False
        for c in value:
            if c in ('{', '[', '('):
                if brace is None:
                    brace = LeftBrace(c)
                else:
                    brace.right = LeftBrace(c)
                    last_brace = brace
                    brace = brace.right
                    brace.left = last_brace

            if c in ('}', ']', ')'):
                if brace is None:
                    early_break = True
                    break
                else:
                    pair = pairs[c]
                    if brace.brace == pair:
                        brace = brace.left
                        if brace is not None:
                            brace.right = None
                            print('up:', brace.brace)
                    else:
                        early_break = True
                        break

        if brace is None and not early_break:
            rs.append('YES')
        else:
            rs.append('NO')

    return rs

if __name__ == '__main__':
    vs = ['{}[]()', '{[}]']
    print(braces(vs))
