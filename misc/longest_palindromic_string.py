class Solution:
    def longestPalindrome(self, s: str) -> list:
        palins = list(s)

        two_list = []
        for i in range(len(s)-1):
            if s[i] == s[i+1]:
                two_list.append(s[i:i+2])
        if len(two_list) > 0:
            palins = list(set(two_list))
        palin_len = 2

        for half_len in range(2, len(s)//2+2):
            for i in range(0, len(s)-half_len):
                # for half_len = 2, it can have total 3 or 4 chars, e.g., 'bab', 'baab'
                half_sub = s[i:i+half_len]

                # for odd length
                is_palin = True
                exp_len = half_len * 2 - 1
                if exp_len > palin_len:
                    for k in range(half_len - 1):
                        sym_pos = i + (exp_len-1)-k
                        if sym_pos >= len(s) or s[sym_pos] != half_sub[k]:
                            is_palin = False
                            break

                    if is_palin:
                        if exp_len > palin_len:
                            palins.clear()
                            palin_len = exp_len
                        palins.append(s[i:i + palin_len])

                # for even length
                is_palin = True
                exp_len = half_len * 2
                for k in range(half_len):
                    sym_pos = i + exp_len - 1 - k
                    if sym_pos >= len(s) or s[sym_pos] != half_sub[k]:
                        is_palin = False
                        break

                if is_palin:
                    if exp_len > palin_len:
                        palins.clear()
                        palin_len = exp_len
                    palins.append(s[i:i + palin_len])

        return palins


sol = Solution()
s = 'abcd'
s = sol.longestPalindrome('aassaa')
print(s)
