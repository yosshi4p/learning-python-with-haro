




N = int(input()) 
num_list = list(map(int, input().split()))
even_count = 0
found_flag = False

for i in range(N):
    if num_list[i] % 2 == 0:
        even_count += 1
        if even_count % 2 == 1:
               print(i+1)
               found_flag = True
               break

if not found_flag:
    print(-1)