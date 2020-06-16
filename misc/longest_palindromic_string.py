class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2:
            return s

        palin = s[0]
        palin_len = 1

        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                palin = s[i:i + 2]
                palin_len = 2
                break

        if len(s) > 2:
            for half_len in range(len(s) // 2 + 1, 1, -1):
                long_palin = None
                for i in range(0, len(s) - half_len):
                    # for half_len = 2, it can have total 3 or 4 chars, e.g., 'bab', 'baab'
                    half_sub = s[i:i + half_len]

                    # for even length
                    exp_len = half_len * 2
                    if i + exp_len - 1 < len(s):
                        is_palin = True
                        for k in range(half_len):
                            sym_pos = i + exp_len - 1 - k
                            if s[sym_pos] != half_sub[k]:
                                is_palin = False
                                break

                        if is_palin:
                            return s[i:i + exp_len]

                    # for odd length
                    exp_len = half_len * 2 - 1
                    if exp_len > palin_len and (i + exp_len - 1) < len(s):
                        is_palin = True
                        for k in range(half_len - 1):
                            sym_pos = i + (exp_len - 1) - k
                            if s[sym_pos] != half_sub[k]:
                                is_palin = False
                                break

                        if is_palin:
                            long_palin = s[i:i + exp_len]

                if long_palin != None:
                    return long_palin

        return palin


sol = Solution()
s = ['a', 'aa', 'ab', 'aaa', 'aca', 'abc', 'abcd', 'cbbd', 'adabd']
s = ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
for one in s:
    p = sol.longestPalindrome(one)
    print(one, p)
