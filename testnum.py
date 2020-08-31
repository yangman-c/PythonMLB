numOfCode = dict({"a":1,"b":2})

for (k, v) in numOfCode.items():
    print("k:{} v:{}".format(k, v))

items = list(numOfCode.items())
print(items)
items.sort(key=lambda x:x[1], reverse=True)
print(items)
for item in items:
    print("k:{} v:{}".format(item[0], item[1]))