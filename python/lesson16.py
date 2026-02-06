

s_list = input().strip()

counta = {}

for s in s_list:
    counta[s] = counta.get(s, 0) + 1

mx = max(counta.values())

for s in s_list:
    if counta[s] == mx:
        print(s)
        break


