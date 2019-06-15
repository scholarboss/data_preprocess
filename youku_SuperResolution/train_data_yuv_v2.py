# 每个文件 20580 组数据
# 最后一个文件 13720 组数据
# 总计 20580*9 + 13720 = 198940 组数据


# from yuv_io import *
import os
import h5py
# import PIL.Image as Image
import numpy as np
import sys
# import numpy as np
import time

Root_dir = r'E:\competition\youku\dataset\train'
Yuv_path = r'yuv'
Hdf5dir = r'HDF5data'
train_or_test = 'train'


Height, Width = 1080, 1920
Total_frame = 100
Lr_size = 64
Sr_size = Lr_size * 4
Lr_step = 60
Sr_step = 60 * 4
Nto1 = 4 # 输入四张 lr 图，处理之后得到一张 sr 图



Excepted_file = ['Youku_00044_h_GT.yuv', 'Youku_00101_h_GT.yuv', 'Youku_00121_h_GT.yuv',
    'Youku_00140_h_GT.yuv', 'Youku_00142_h_GT.yuv']
sr_dir = ['youku_00000_00049_h_GT_yuv', 'youku_00050_00099_h_GT_yuv', 'youku_00100_00149_h_GT_yuv']
# Lr_dir = ['youku_00000_00049_I_yuv', 'youku_00050_00099_I_yuv', 'youku_00100_00149_I_yuv']



def generate(y, u, v, im_size, patch_size, step, name, f):
    [hgt, wdt] = im_size
    count_h = int((hgt - patch_size) / step + 1)
    count_w = int((wdt - patch_size) / step + 1)
    # uv 以 0 填补
    # V = np.zeros(patch_size * patch_size >> 2, dtype=np.uint8)
    # U = np.zeros(patch_size * patch_size >> 2, dtype=np.uint8)

    start_h = 0
    for h in range(count_h):
        start_w = 0
        for w in range(count_w):
            # print('y shape:', y.shape)
            # print('start_h:{}, start_w:{}, patch_size:{}'.format(start_h, start_w,patch_size))
            patch_y = y[:, start_h:start_h + patch_size, start_w:start_w + patch_size]
            # print('patch_y shape:', patch_y.shape)
            # print(patch_y)
            patch_y = np.reshape(patch_y, [Nto1, patch_size, patch_size])

            patch_u = u[:, int(start_h/2):int(start_h/2) + int(patch_size/2), int(start_w/2):int(start_w/2) + int(patch_size/2)]
            # print(patch_u)
            patch_u = np.reshape(patch_u, [int(Nto1/4), patch_size, patch_size])
            
            patch_v = v[:, int(start_h/2):int(start_h/2) + int(patch_size/2), int(start_w/2):int(start_w/2) + int(patch_size/2)]
            patch_v = np.reshape(patch_v, [int(Nto1/4), patch_size, patch_size])

            patch_all = np.concatenate([patch_y, patch_u, patch_v])
            patch_all = np.reshape(patch_all, [1, 6, patch_size, patch_size])

            save_h5(f, patch_all, name)

            start_w += step
        start_h += step
    return 0


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



def save_h5(h5f, data, target):
    shape_list = list(data.shape)
    if not h5f.__contains__(target):
        shape_list[0] = None  # 设置数组的第一个维度是0
        dataset = h5f.create_dataset(target, data=data, maxshape=tuple(shape_list), chunks=True)
        return
    else:
        dataset = h5f[target]
    len_old = dataset.shape[0]
    len_new = len_old + data.shape[0]
    shape_list[0] = len_new
    dataset.resize(tuple(shape_list))  # 修改数组的第一个维度
    dataset[len_old:len_new] = data  # 存入新的文件


def shuffle_time(h5f):
    input_key, label_key = list(h5f.keys())
    print('\n shuffle begining.....')
    t1 = time.time()
    state = np.random.get_state()
    np.random.shuffle(h5f[input_key])
    t3 = time.time()
    print('complate input data')
    print('Time to shuffle input data: {:.3f} seconds'.format(t3 - t1))
    print('label data begin......')
    np.random.set_state(state)
    np.random.shuffle(h5f[label_key])
    t2 = time.time()
    print('Time to shuffle: {:.3f} seconds'.format(t2 - t1))


def YUVread(path, size, frame_num=None, start_frame=0, mode='420'):
    """
    Only for 4:2:0 and 4:4:4 for now.
    :param path: yuv file path
    :param size: [height, width]
    :param frame_num: The number of frames you want to read, and it shouldn't smaller than the frame number of original
    yuv file. Defult is None, means read from start_frame to the end of file.
    :param start_frame: which frame begin from. Defult is 0.
    :param mode: yuv file mode, '420' or '444'
    :return: byte_type y, u, v with a shape of [frame_num, height, width] of each
    """
    [height, width] = size
    if mode == '420':
        frame_size = int(height * width / 2 * 3)
    else:
        frame_size = int(height * width * 3)
    all_y = np.uint8([])
    all_u = np.uint8([])
    all_v = np.uint8([])
    with open(path, 'rb') as file:
        file.seek(frame_size * start_frame)
        if frame_num is None:
            frame_num = 0
            while True:
                if mode == '420':
                    y = np.uint8(list(file.read(height * width)))
                    u = np.uint8(list(file.read(height * width >> 2)))
                    v = np.uint8(list(file.read(height * width >> 2)))
                else:
                    y = np.uint8(list(file.read(height * width)))
                    u = np.uint8(list(file.read(height * width)))
                    v = np.uint8(list(file.read(height * width)))
                if y.shape == (0,):
                    break
                all_y = np.concatenate([all_y, y])
                all_u = np.concatenate([all_u, u])
                all_v = np.concatenate([all_v, v])
                frame_num += 1
        else:
            for fn in range(frame_num):
                if mode == '420':
                    y = np.uint8(list(file.read(height * width)))
                    u = np.uint8(list(file.read(height * width >> 2)))
                    v = np.uint8(list(file.read(height * width >> 2)))
                else:
                    y = np.uint8(list(file.read(height * width)))
                    u = np.uint8(list(file.read(height * width)))
                    v = np.uint8(list(file.read(height * width)))
                if y.shape == (0,):
                    break
                all_y = np.concatenate([all_y, y])
                all_u = np.concatenate([all_u, u])
                all_v = np.concatenate([all_v, v])

    all_y = np.reshape(all_y, [frame_num, height, width])
    if mode == '420':
        all_u = np.reshape(all_u, [frame_num, height >> 1, width >> 1])
        all_v = np.reshape(all_v, [frame_num, height >> 1, width >> 1])
    else:
        all_u = np.reshape(all_u, [frame_num, height, width])
        all_v = np.reshape(all_v, [frame_num, height, width])

    return all_y, all_u, all_v


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


if __name__ == '__main__':
    dir_count = 1
    h5_count = 0
    for path in sr_dir:
        print('\n processing {}... No.{} of {} '.format(path, dir_count, len(sr_dir)))
        dir_count += 1
        sr_fall_path = os.path.join(Root_dir, Yuv_path, path)
        lr_fall_path = os.path.join(Root_dir, Yuv_path, path.split('h')[0]+'l_yuv')
        sr_name_list = os.listdir(sr_fall_path)
        count = 1
        for name in sr_name_list:
            progress_bar(count, len(sr_name_list))
            count += 1
            if name in Excepted_file:
                continue
            
            if h5_count % 15 == 0:
                if h5_count != 0:
                    shuffle_time(f_hdf5)
                    f_hdf5.close()
                f_hdf5 = h5py.File(os.path.join(Root_dir, Hdf5dir, 'train_youku_multi_{}.hdf5'.format(h5_count//15)), 'w')
            h5_count += 1
            sr_fall_name = os.path.join(sr_fall_path, name)
            lr_fall_name = os.path.join(lr_fall_path, name.split('h')[0]+'l.yuv')
            for i in range(0, Total_frame-3, 2):
                y_sr, u_sr, v_sr = YUVread(sr_fall_name, [Height, Width], frame_num=4, start_frame=i)
                y_lr, u_lr, v_lr = YUVread(lr_fall_name, [Height>>2, Width>>2], frame_num=4, start_frame=i)
                # print(y_sr.shape)
                # print('='*20)
                # print(u_sr.shape)
                # print('='*20)
                # print(v_sr.shape)
                generate(y_lr, u_lr, v_lr, [Height>>2,Width>>2], patch_size=Lr_size, step=Lr_step, name='lr_{}_{}'.format(Lr_size, Lr_size), f=f_hdf5)
                generate(y_sr, u_sr, v_sr, [Height,Width], patch_size=Sr_size, step=Sr_step, name='sr_{}_{}'.format(Sr_size, Sr_size), f=f_hdf5)
    shuffle_time(f_hdf5)
    f_hdf5.close()
    






