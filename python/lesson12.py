
###最初に2回出た数字
# 長さ N の整数列 A が与えられる。
# 左から順に見ていって、同じ値が2回目に出現した瞬間の値を出力せよ。
# もし最後まで見ても2回目が一度も起きなければ -1 を出力せよ。###

N = int(input())
A = list(map(int, input().split()))

seen = set()
for a in A:
    if a in seen:
        print(a)
        break
    seen.add(a)
else:
    print(-1)
    
