min_n = -(2 ** 31)
max_n = 2 ** 31 - 1


class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x > -10 and x < 10:
            return x

        sign, x = (1, x) if x >= 0 else (-1, -x)
        r = 0
        while x >= 10:
            r = r*10 + (x % 10)
            x = x // 10
        r = r * 10 + x
        r *= sign
        return 0 if r < min_n or r > max_n else r


if __name__ == '__main__':
    s = Solution()
    print(s.reverse(1534236469))
    print(s.reverse(153423646))
    print(s.reverse(123))
    print(s.reverse(-123))
    print(s.reverse(120))
    print(s.reverse(-120))
