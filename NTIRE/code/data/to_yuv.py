import os
for i in range(160, 240):
    num = "%03d"%i
    command = r"ffmpeg -i " + str(num) + r"/%8d.png -pix_fmt yuv420p -vsync 0 " + str(num) + ".yuv -y"
    os.system(command)

