import tensorflow as tf
from yuv_io import *
import PIL.Image as Image
import os
import sys


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


def generate(im_input, im_label, im_size, patch_size, step, writer):
    [hgt, wdt] = im_size
    count_h = int((hgt - patch_size) / step + 1)
    count_w = int((wdt - patch_size) / step + 1)

    start_h = 0
    for h in range(count_h):
        start_w = 0
        for w in range(count_w):
            patch_input = im_input[start_h:start_h + patch_size, start_w:start_w + patch_size]
            patch_label = im_label[start_h:start_h + patch_size, start_w:start_w + patch_size]
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.rot90(patch_input)
            patch_label = np.rot90(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.rot90(patch_input)
            patch_label = np.rot90(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.rot90(patch_input)
            patch_label = np.rot90(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.fliplr(patch_input)
            patch_label = np.fliplr(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.rot90(patch_input)
            patch_label = np.rot90(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.rot90(patch_input)
            patch_label = np.rot90(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            patch_input = np.rot90(patch_input)
            patch_label = np.rot90(patch_label)
            example = tf.train.Example(features=tf.train.Features(feature={
                'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_input.tostring()])),
                'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[patch_label.tostring()]))
            }))
            writer.write(example.SerializeToString())

            start_w += step
        start_h += step
    return count_h * count_w * 8


QP = 32

input_source_dir = 'upsampled_yuv' + '\\QP' + str(QP)
label_source_dir = 'im_cropped_yuv'
target_dir = 'TFRdata' + '\\QP' + str(QP)

patch_size = 41
step = 36

dir_list = ['test', 'train']
if not dir_list:
    dir_list = os.listdir(label_source_dir)
for name in dir_list:
    if os.path.isdir(os.path.join(label_source_dir, name)):
        if not os.path.exists(os.path.join(target_dir, name)):
            os.makedirs(os.path.join(target_dir, name))
    else:
        dir_list.remove(name)

print('****************************')
print('Cutting patches...')

for name in dir_list:
    input_in_dir = os.path.join(input_source_dir, name)
    label_in_dir = os.path.join(label_source_dir, name)
    out_path = os.path.join(target_dir, name, name + '_' + str(QP) + '.tfrecords')
    print('Generate [' + out_path + ']:')

    writer = tf.python_io.TFRecordWriter(out_path)
    file_list = os.listdir(label_in_dir)

    count = 0
    count_patch = 0
    for file in file_list:
        file_name, ext = os.path.splitext(file)
        if not ext == '.yuv':
            continue
        count += 1
        width, height = file_name.split('_')[1:3]
        width = int(width)
        height = int(height)
        im_input = Yread(os.path.join(input_in_dir, file_name + '_' + str(QP) + '_rec_SHMUP.yuv'), [height, width], 1)
        im_label = Yread(os.path.join(label_in_dir, file), [height, width], 1)
        im_input = np.reshape(im_input, [height, width])
        im_label = np.reshape(im_label, [height, width])
        count_patch += generate(im_input, im_label, [height, width], patch_size, step, writer)
        progress_bar(count, len(file_list))
    print('\nNumber of patches:', count_patch)
    writer.close()
