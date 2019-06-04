# 裁剪图片，输入YUV数据，对YUV数据裁剪，保存为png图片
# 裁剪的尺寸由 77，78 行确定

from yuv_io import *
import PIL.Image as Image
import os
import numpy as np


def generate(img, im_size, patch_size, step, target_dir, file_name):
    [hgt, wdt] = im_size
    count_h = int((hgt - patch_size) / step + 1)
    count_w = int((wdt - patch_size) / step + 1)
    # uv 以 0 填补
    V = np.zeros(patch_size * patch_size >> 2, dtype=np.uint8)
    U = np.zeros(patch_size * patch_size >> 2, dtype=np.uint8)

    start_h = 0
    for h in range(count_h):
        start_w = 0
        for w in range(count_w):
            patch = img[start_h:start_h + patch_size, start_w:start_w + patch_size]
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '0' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
            #                      file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '0' + '.png'))
            patch = np.rot90(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '1' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
            #                      file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '1' + '.png'))
            patch = np.rot90(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '2' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
                                #  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '2' + '.png'))
            patch = np.rot90(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '3' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
                                #  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '3' + '.png'))
            patch = np.fliplr(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '4' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
                                #  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '4' + '.png'))
            patch = np.rot90(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '5' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
                                #  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '5' + '.png'))
            patch = np.rot90(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '6' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
                                #  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '6' + '.png'))
            patch = np.rot90(patch)
            YUVwrite(patch, U, V, os.path.join(target_dir,
                                  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '7' + '.yuv'))
            # im = Image.fromarray(patch)
            # im.save(os.path.join(target_dir,
                                #  file_name + '_' + str(start_h) + '_' + str(start_w) + '_' + '7' + '.png'))

            start_w += step
        start_h += step


def cut(patch_size, step, source_dir, target_dir):
    dir_list = os.listdir(source_dir)
    for name in dir_list:
        if os.path.isdir(os.path.join(source_dir, name)):
            if not os.path.exists(os.path.join(target_dir, name)):
                os.makedirs(os.path.join(target_dir, name))
        else:
            dir_list.remove(name)

    print('****************************')
    print('Cutting patches...')

    for name in dir_list:
        in_dir = os.path.join(source_dir, name)
        out_dir = os.path.join(target_dir, name)
        print('From ' + in_dir + ':')

        for file in os.listdir(in_dir):
            file_name, ext = os.path.splitext(file)
            if not ext == '.yuv':
                continue
            width, height = file_name.split('_')[1:3]       # upsampled image
            # width, height = file_name.split('_')[3:5]       # downsampled image
            width = int(width)
            height = int(height)
            im = Yread(os.path.join(in_dir, file), [height, width], 1)
            im = np.reshape(im, [height, width])
            generate(im, [height, width], patch_size, step, out_dir, file_name)



if __name__ == '__main__':
    input_source_dir = 'im_cropped_yuv'       # ori network dataset
    # input_source_dir_test = 'im_cropped_yuv'+ '\\test'       # ori network dataset
    # input_source_dir = 'recs'+ '\\QP' + str(QP)
    # label_source_dir = 'im_cropped_yuv'                        # ori network dataset
    # label_source_dir = 'downsampled_yuv'
    target_source_dir = 'label_yuv_oriSR_192x192'
    # target_dir_test = 'label_yuv_oriSR' + 'test'

# 裁剪大小 大图时 加倍 小图42-36 大图84-72 
    patch_size = 192
    step = 100

    cut(patch_size, step, input_source_dir, target_source_dir)
    # cut(patch_size, step, input_source_dir_test, target_dir_test)


#     for i in range(20,31):

#         QP = i
#         # input_source_dir = 'upsampled_yuv'+ '\\QP' + str(QP)       # ori network dataset
#         input_source_dir = 'recs'+ '\\QP' + str(QP)
#         # label_source_dir = 'im_cropped_yuv'                        # ori network dataset
#         label_source_dir = 'downsampled_yuv'
#         input_target_dir = 'input_png'+ '\\QP' + str(QP)
#         label_target_dir = 'label_png_downsampled'

# # 裁剪大小 大图时 加倍
#         patch_size = 41
#         step = 36

#         cut(patch_size, step, input_source_dir, input_target_dir)
#         # cut(patch_size, step, label_source_dir, label_target_dir)
