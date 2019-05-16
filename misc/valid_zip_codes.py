# 6-digit zipcode, no more than 2 alternative repeats

regex_integer_in_range = r"^[1-9]\d{5}$"	# Do not delete 'r'.
regex_alternating_repetitive_digit_pair = r"(\d)(?=\d\1)"	# Do not delete 'r'.


import re

#P = input()
P = '4542867'
print('int:', bool(re.match(regex_integer_in_range, P)))
print('pair:', re.findall(regex_alternating_repetitive_digit_pair, P))
print('pair len:', len(re.findall(regex_alternating_repetitive_digit_pair, P)))
exit(0)

print (bool(re.match(regex_integer_in_range, P))
and len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2)
