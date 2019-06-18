def braces(values):
    rs = []

    # match left/right braces with dictionary
    pairs = {'}' : '{', ']' : '[', ')' : '('}
    for value in values:
        seq = []
        last_c = None
        early_break = False
        for c in value:
            if c in ('{', '[', '('):
                seq.append(c)  # keep track of left braces
                last_c = c  # hold the last left brace
            elif c in ('}', ']', ')'):
                if last_c is None:
                    # have not found any left brace yet. Bad value. Abort
                    early_break = True
                    break
                else:
                    pair = pairs[c]
                    if pair == last_c:
                        # right brace matches the last left brace. Shrink
                        # the left brace sequence. Also update last left brace
                        seq = seq[:-1]
                        if len(seq) > 0:
                            last_c = seq[len(seq)-1]
                        else:
                            last_c = None
                    else:
                        # right brace does not match left brace. Bad value. Abort
                        early_break = True
                        break

        # if all left braces are matched and the matching loop was not stopped early
        # it is a good sequence in value
        if last_c is None and not early_break:
            rs.append('YES')
        else:
            rs.append('NO')

    return rs


if __name__ == '__main__':
    vs = ['{}asda[d]w(ed)', '{as[]qwe}[qw]', '{[12]32}(43{123})12[2]', 'as{1}123[]5(6)90']
    print(braces(vs))
