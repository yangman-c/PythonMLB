a = [[1,4,7],2,3,34,5]

print(a[:-1])

b = [n for n in a[0]] + a[1:]

print(b[-len(a):-1])
