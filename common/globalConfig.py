heads = ("000", "002", "300", "600", "601", "603", "688", "689", "787")
blackList = ("000003", "000024", "000562", "000787", "600296", "600553", "000549", "000542", "601299", "600632", "600832", "600840", "600205", "600002")
allCodes = ()

def foreachAllCodes(callback):
    for head in heads:
        for i in range(1, 1000):
            code = f"{head}{str(i).zfill(3)}"
            if code not in blackList:
                if callback(code):
                    return
