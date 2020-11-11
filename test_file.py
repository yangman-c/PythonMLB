import sys
import io
import os

def main():
    file = None
    if os.path.exists("temp"):
        file = io.open("temp", "r")
        print(file.read(0))
    else:
        file = io.open("temp", "x")
    file.
    print(os.path.getsize("temp"), os.path.exists("temp"))
    file.close()

try:
    main()
except Exception as err:
    print(err)
    sys.exit(1)

sys.exit()