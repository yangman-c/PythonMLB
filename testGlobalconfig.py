import common.globalConfig
import time
import sys

heads = common.globalConfig.heads

t1 = time.time()

for head in heads:
    for i in range(0, 1000):
        code = "{}{}".format(head, str(i).zfill(3))
        print(code)

print(t1, time.time())

sys.exit()