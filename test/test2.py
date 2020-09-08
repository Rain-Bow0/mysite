
ans = []
n = int(input())
for i in range(n):
    t = int(input())
    if t in ans:
        ans.remove(t)
        ans.insert(0,t)
    else:
        ans.insert(0,t)
for i in ans:
    print(i)