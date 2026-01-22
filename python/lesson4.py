




N = int(input()) 
name_points_dict = {}
result_dict = {}

for _ in range(N):
    name, points = input().split()
    points = int(points)
    name_points_dict[name] = name_points_dict.get(name, 0) + points
    for name, total in name_points_dict.items():
        if total >= 10:
            result_dict[name] = total

sorted_names = sorted(result_dict.items(), key=lambda kv: (-kv[1], kv[0]))
for name, total in sorted_names:
    print(f"{name} {total}")