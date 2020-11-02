from multiprocessing.shared_memory import SharedMemory
import numpy as np
import common.globalConfig
def readData(name):
    try:
        shapeSm = SharedMemory(name + "_shape", False)
    except Exception as err:
        return err, None
    shapeArr = np.ndarray((1,2), dtype=np.int,buffer=shapeSm.buf)

    try:
        sm = SharedMemory(name, False)
    except Exception as err:
        return err, None
    arr = np.ndarray(shapeArr[0], dtype=np.float,buffer=sm.buf)
    return None, arr

allData = list([])
heads = common.globalConfig.heads
for head in heads:
    for i in range(1000):
        code = "{}{}".format(head, str(i).zfill(3))
        err, data = readData("s_{}".format(code))
        if err != None:
            print("err:{} code:{}".format(err, code))
        # if err == None:
            # allData.append(data)

# err, z_000001 = readData("z_000001")
# err, z_399001 = readData("z_399001")
# err, z_399006 = readData("z_399006")

# print(len(allData))
# print("z_000001")
# print(z_000001)
# print("z_399001")
# print(z_399001)
# print("z_399006")
# print(z_399006)
