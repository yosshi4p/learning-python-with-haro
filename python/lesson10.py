


s_list = list(map(str, input().split()))

counta = 0

for s in s_list:
    if s in ['a', 'e', 'i', 'o', 'u']:
        counta += 1

print(counta)