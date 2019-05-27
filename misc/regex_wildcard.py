def isMatch(text, pattern):
    print('==:', text, pattern)
    if not pattern:
        return not text
    if not text:
        return not pattern

    c0 = pattern[0]
    first_match = c0 in [text[0], '.']
    if not first_match:
        return False

    if len(pattern) == 1:
        return first_match

    # text and pattern are not empty and len(pattern) >= 2
    if pattern[1] == '*':
        st_idx = 0
        for tc in text:
            if tc != c0:
                break
            st_idx += 1
        text = text[st_idx:]
        pattern = pattern[2:]
    else:
        text = text[1:]
        pattern = pattern[1:]
    return isMatch(text, pattern)

if __name__ == '__main__':
    t = 'gabcd'
    p = 'g.bc*d*'
    print(isMatch(t, p))

