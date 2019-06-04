import os
import sys


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()



dir_list = os.listdir('./')
for i in range(len(dir_list)-1, -1, -1):
	if not os.path.isdir(dir_list[i]):
		dir_list.pop(i)

for name in dir_list:
	bmp = os.path.join(name+'_bmp')
	yuv = os.path.join(name+'_yuv')
	if not os.path.exists(bmp):
		os.makedirs(bmp)
	if not os.path.exists(yuv):
		os.makedirs(yuv)
	file_list = os.listdir(name)
	print('process {} .....'.format(name))
	for i in range(len(file_list)):
		progress_bar(i+1, len(file_list))
		file_name = file_list[i]
		input_name = os.path.join(name, file_name)
		yuv_name = os.path.join(yuv, file_name.split('.')[0]+r'.yuv')
		bmp_name = os.path.join(bmp, file_name.split('.')[0]+r'%3d.bmp')
		command_yuv = "ffmpeg.exe -i {} -vsync 0 {}  -y".format(input_name, yuv_name)
		command_bmp = "ffmpeg.exe -i {} -vsync 0 {} -y".format(input_name, bmp_name)
		os.system(command_yuv)
		os.system(command_bmp)


