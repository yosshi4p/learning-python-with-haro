




N = int(input())
name_score_list = []

for _ in range(N):
    name, a, b = input().split()
    a = int(a)
    b = int(b)
    score = a - b
    name_score_list.append((name, a, b, score))

sorted_list = sorted(name_score_list, key=lambda x: (-x[3], -x[1], x[0] ))

for name, a, b, score in sorted_list:
    print(name, score)

