import lightshow
import unicornhathd as unicorn
import numpy as np
from PIL import Image
import time
import subprocess
from random import shuffle

def icon_show(run, running):
    running(True)
    list = []
    try:
        cmd = "echo ~/lamp2/icons/*"
        cmd2 = "pwd"
        process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
        output, error = process.communicate()
        output = str(output)[2:-3]
        print(output)
        list = output.split()
        print(list)
    except:
        print("except 1")
    shuffle(list)
    print(list)
    for path in list:
        img = Image.open(path)
        img.load()
        #img = img.convert("RGB")
        try:
            background = Image.new("RGB", img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        except:
            background = img
        A=np.asarray(background)
        for x in range(16):
            for y in range(16):
                #print(A[x][y], end = "\t")
                temp = A[x][y]
                try:
                    unicorn.set_pixel(x,y, temp[0], temp[1], temp[2])
                except:
                    unicorn.set_pixel(x,y, temp, 0, temp)
                #print()
        unicorn.show()
        now = time.monotonic()
        while time.monotonic() - now < 10:

            if not run():
                unicorn.off()
                running(False)
                return
            time.sleep(0.1)
    unicorn.off()
    running(False)

def test_continue():
    return True

def main():
    icon_show(test_continue)

if __name__ == '__main__':
    main()
