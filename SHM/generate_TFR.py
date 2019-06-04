import tensorflow as tf
import PIL.Image as Image
from yuv_io import *
import os

QP = 32

input_source_dir = 'input_png' + '\\QP' + str(QP)
label_source_dir = 'label_png'
target_dir = 'TFRdata' + '\\QP' + str(QP)

patch_size = 41

dir_list = os.listdir(input_source_dir)
for name in dir_list:
    if os.path.isdir(os.path.join(input_source_dir, name)):
        if not os.path.exists(os.path.join(target_dir, name)):
            os.makedirs(os.path.join(target_dir, name))
    else:
        dir_list.remove(name)

for name in dir_list:
    input_in_dir = os.path.join(input_source_dir, name)
    label_in_dir = os.path.join(label_source_dir, name)
    out_path = os.path.join(target_dir, name, name + '_' + str(QP) + '.tfrecords')
    print('Generate ' + out_path + ':')

    input_writer = tf.python_io.TFRecordWriter(out_path)
    file_list = np.array(os.listdir(label_in_dir))

    np.random.shuffle(file_list)

    num = 0
    for file in file_list:
        file_name, ext = os.path.splitext(file)
        if not ext == '.png':
            continue
        num += 1
        name = file.split('_')
        im_input = np.array(Image.open(os.path.join(input_in_dir,
                                                    name[0] + '_' + name[1] + '_' + name[2] + '_' + name[3] + '_' +
                                                    name[4] + '_' + name[5] + '_' + str(QP) + '_rec_SHMUP_' + name[
                                                        6] + '_' + name[7] + '_' + name[8])))
        im_label = np.array(Image.open(os.path.join(label_in_dir, file)))
        ims_input = im_input.tostring()
        ims_label = im_label.tostring()
        example = tf.train.Example(features=tf.train.Features(feature={
            'input': tf.train.Feature(bytes_list=tf.train.BytesList(value=[ims_input])),
            'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[ims_label]))
        }))
        input_writer.write(example.SerializeToString())
        if num % 100 == 0:
            print(num)

    input_writer.close()
#
# input_writer = tf.python_io.TFRecordWriter(target_path)
#
# for file in os.listdir(source_dir):
#     file_name, ext = os.path.splitext(file)
#     if not ext == '.png':
#         continue
#     width, height = (41, 41)
#
#     im = Image.open(os.path.join(source_dir, file))
#     im = np.array(im)
#     ims = im.tobytes()
#     # ims = im.tostring()
#     example = tf.train.Example(features=tf.train.Features(feature={
#         'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[ims]))
#     }))
#     writer.write(example.SerializeToString())
# writer.close()

# ds = tf.contrib.data.TFRecordDataset(target_path)
#
# def decc(exa):
#     im = tf.parse_single_example(exa, features={'image': tf.FixedLenFeature([], tf.string)})
#     im = im['image']
#     im = tf.decode_raw(im, tf.uint8)
#     im = tf.reshape(im, [41,41])
#     return im
#
# ds = ds.map(decc)
# ds = ds.batch(2)
#
# iterator = ds.make_one_shot_iterator()
# batch = iterator.get_next()
#
# sess = tf.InteractiveSession()
# # tf.parse_single_example()
