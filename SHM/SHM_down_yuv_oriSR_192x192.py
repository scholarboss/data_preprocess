import os
import sys


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


source_dir = 'label_yuv_oriSR_192x192'
target_dir = 'label_yuv_downsampled_192x192'
log_dir = 'logs'

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
elif os.path.exists(log_dir + '/downsam_log.txt'):
    os.remove(log_dir + '/downsam_log.txt')

dir_list = ['test', 'train']
# if not dir_list:
#     dir_list = os.listdir(source_dir)
# for name in dir_list:
#     if os.path.isdir(os.path.join(source_dir, name)):
#         if not os.path.exists(os.path.join(target_dir, name)):
#             os.makedirs(os.path.join(target_dir, name))
#     else:
#         dir_list.remove(name)

print('****************************')
print('Down-sampling...')

for name in dir_list:
    in_dir = os.path.join(source_dir, name)
    out_dir = os.path.join(target_dir, name)
    print('From [' + in_dir + '] to [' + out_dir + ']:')

    count = 0
    file_list = os.listdir(in_dir)
    for file in file_list:
        file_name, ext = os.path.splitext(file)
        if not ext == '.yuv':
            continue
        count += 1
        # lwdt, lhgt, swdt, shgt, fac = file_name.split('_')[-5:]
        lwdt, lhgt, swdt, shgt = str(192), str(192), str(96), str(96)
        input_path = os.path.join(in_dir, file)
        output_path = os.path.join(out_dir, file)
        command = 'TAppDownConvert.exe ' + lwdt + ' ' + lhgt + ' ' + input_path + ' ' + swdt + ' ' + shgt + ' ' + output_path + ' 1>>' + log_dir + '/downsam_log.txt 2>&1'
        # print('Resample ' + str(num) + ': ' + file + '...')
        os.system(command)
        progress_bar(count, len(file_list))
    print('\n' + str(count) + ' files resampled.')
