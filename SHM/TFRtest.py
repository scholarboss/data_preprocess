from yuv_io import *
import tensorflow as tf
import os
import PIL.Image as Image
import matplotlib.pyplot as plt


#
# source_dir = r'D:\documents\WORKS_ML_SHVC\DnCNN\data\input_png\test'
# target_path = r'D:\documents\WORKS_ML_SHVC\DnCNN\data\input_png\test1.tfrecords'
#
# # writer = tf.python_io.TFRecordWriter(target_path)
# #
# # for file in os.listdir(source_dir):
# #     file_name, ext = os.path.splitext(file)
# #     if not ext == '.png':
# #         break
# #     width, height = (41, 41)
# #
# #     im = Image.open(os.path.join(source_dir, file))
# #     im = np.array(im)
# #     ims = im.tobytes()
# #     # ims = im.tostring()
# #     example = tf.train.Example(features=tf.train.Features(feature={
# #         'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[ims]))
# #     }))
# #     writer.write(example.SerializeToString())
# # writer.close()
#
#
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

def make_dataset(TFR_path, batch_size):
    dataset = tf.contrib.data.TFRecordDataset(TFR_path)

    def example_process(exa):
        ims = tf.parse_single_example(exa, features={
            'input': tf.FixedLenFeature([], tf.string),
            'label': tf.FixedLenFeature([], tf.string)
        })
        im_input = ims['input']
        im_label = ims['label']
        im_input = tf.decode_raw(im_input, tf.uint8)
        im_label = tf.decode_raw(im_label, tf.uint8)
        im_input = tf.reshape(im_input, [41, 41, 1])
        im_label = tf.reshape(im_label, [41, 41, 1])
        return im_input, im_label

    dataset = dataset.map(example_process)
    dataset = dataset.repeat()
    dataset = dataset.batch(batch_size)
    iterator = dataset.make_one_shot_iterator()
    batch = iterator.get_next()

    return batch


batch = make_dataset(r'D:\documents\WORKS_ML_SHVC\DnCNN\data\TFRdata\QP32\train\train_only2_32.tfrecords', 1)
sess = tf.InteractiveSession()

for i in range(100):
    img = sess.run(batch)

plt.figure()
plt.imshow(np.reshape(img[0], [41, 41]))
plt.figure()
plt.imshow(np.reshape(img[1], [41, 41]))
