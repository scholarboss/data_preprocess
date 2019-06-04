from yuv_io import *
import os
import sys


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


def upsample(input_path, output_path, input_width, input_height, factor):
    # widths and heights
    w_ori = input_width
    h_ori = input_height
    w_pad = w_ori + 8
    h_pad = h_ori
    w_16_tmp = round(w_ori * factor)
    h_16_tmp = h_ori + 8
    w_out = round(w_ori * factor)
    h_out = round(h_ori * factor)

    filters = np.array([
        [0, 0, 0, 64, 0, 0, 0, 0],
        [0, 1, -3, 63, 4, -2, 1, 0],
        [-1, 2, -5, 62, 8, -3, 1, 0],
        [-1, 3, -8, 60, 13, -4, 1, 0],
        [-1, 4, -10, 58, 17, -5, 1, 0],
        [-1, 4, -11, 52, 26, -8, 3, -1],
        [-1, 3, -9, 47, 31, -10, 4, -1],
        [-1, 4, -11, 45, 34, -10, 4, -1],
        [-1, 4, -11, 40, 40, -11, 4, -1],
        [-1, 4, -10, 34, 45, -11, 4, -1],
        [-1, 4, -10, 31, 47, -9, 3, -1],
        [-1, 3, -8, 26, 52, -11, 4, -1],
        [0, 1, -5, 17, 58, -10, 4, -1],
        [0, 1, -4, 13, 60, -8, 3, -1],
        [0, 1, -3, 8, 62, -5, 2, -1],
        [0, 1, -2, 4, 63, -3, 1, 0]
    ])

    # filters = np.array([
    #     [  0,    0,    0,   64,    0,    0,    0,    0 ],
    #     [  0,    1,   -3,   63,    4,   -2,    1,    0 ],
    #     [ -1,    2,   -5,   62,    8,   -3,    1,    0 ],
    #     [ -1,    3,   -8,   60,   13,   -4,    1,    0 ],
    #     [ -1,    4,  -10,   58,   17,   -5,    1,    0 ],
    #     [ -1,    4,  -11,   52,   26,   -8,    3,   -1 ],
    #     [ -1,    3,   -9,   47,   31,  -10,    4,   -1 ],
    #     [ -1,    4,  -11,   45,   34,  -10,    4,   -1 ],
    #     [ -1,    4,  -11,   40,   40,  -11,    4,   -1 ],
    #     [ -1,    4,  -10,   34,   45,  -11,    4,   -1 ],
    #     [ -1,    4,  -10,   31,   47,   -9,    3,   -1 ],
    #     [ -1,    3,   -8,   26,   52,  -11,    4,   -1 ],
    #     [  0,    1,   -5,   17,   58,  -10,    4,   -1 ],
    #     [  0,    1,   -4,   13,   60,   -8,    3,   -1 ],
    #     [  0,    1,   -3,    8,   62,   -5,    2,   -1 ],
    #     [  0,    1,   -2,    4,   63,   -3,    1,    0 ]
    # ])

    # only Y
    y_ori, u_ori, v_ori = YUVread(input_path, [h_ori, w_ori], 1)
    y_ori = np.reshape(y_ori, [h_ori, w_ori])
    y_ori = np.int32(y_ori)

    y_pad = np.zeros([h_pad, w_pad], np.int32)
    y_pad[0:h_ori, 4:4 + w_ori] = y_ori[:, :]
    # pad left
    y_pad[0:h_ori, 0] = y_ori[:, 0]
    y_pad[0:h_ori, 1] = y_ori[:, 0]
    y_pad[0:h_ori, 2] = y_ori[:, 0]
    y_pad[0:h_ori, 3] = y_ori[:, 0]
    # pad right
    y_pad[0:h_ori, -4] = y_ori[:, -1]
    y_pad[0:h_ori, -3] = y_ori[:, -1]
    y_pad[0:h_ori, -2] = y_ori[:, -1]
    y_pad[0:h_ori, -1] = y_ori[:, -1]

    y_16_tmp = np.zeros([h_16_tmp, w_16_tmp], np.int32)
    y_out = np.zeros([h_out, w_out], np.int32)

    # horizontal
    for h in range(h_ori):
        for w in range(w_out):
            w_in_16 = round(w * 16 / factor)
            y_16_tmp[h + 4, w] = np.sum(y_pad[h, w_in_16 // 16 + 1:w_in_16 // 16 + 9] * filters[w_in_16 % 16])

    # pad top
    y_16_tmp[0, :] = y_16_tmp[4, :]
    y_16_tmp[1, :] = y_16_tmp[4, :]
    y_16_tmp[2, :] = y_16_tmp[4, :]
    y_16_tmp[3, :] = y_16_tmp[4, :]
    # pad bottom
    y_16_tmp[-4, :] = y_16_tmp[-5, :]
    y_16_tmp[-3, :] = y_16_tmp[-5, :]
    y_16_tmp[-2, :] = y_16_tmp[-5, :]
    y_16_tmp[-1, :] = y_16_tmp[-5, :]

    # y_16_tmpo = np.uint8(y_16_tmp/64)
    # Ywrite(y_16_tmpo, 'test00.yuv')

    # vertical
    for w in range(w_out):
        for h in range(h_out):
            h_in_16 = round(h * 16 / factor)
            value = np.sum(y_16_tmp[h_in_16 // 16 + 1:h_in_16 // 16 + 9, w] * filters[h_in_16 % 16])
            if value % (4096) >= 2048:
                y_out[h, w] = (value >> 12) + 1
            else:
                y_out[h, w] = (value >> 12)

    # clip & output
    y_out = np.clip(y_out, 0, 255)
    y_out = np.uint8(y_out)
    Ywrite(y_out, output_path)


if __name__ == '__main__':

    QP = 32
    source_dir = 'recs' + '\\QP' + str(QP)
    target_dir = 'upsampled_yuv' + '\\QP' + str(QP)
    extension = '.yuv'

    dir_list = ['test', 'train']
    if not dir_list:
        dir_list = os.listdir(source_dir)
    for name in dir_list:
        if os.path.isdir(os.path.join(source_dir, name)):
            if not os.path.exists(os.path.join(target_dir, name)):
                os.makedirs(os.path.join(target_dir, name))
        else:
            dir_list.remove(name)

    print('****************************')
    print('Up-sampling...')

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
            lwdt, lhgt, swdt, shgt, fac = file_name.split('_')[-7:-2]
            input_path = os.path.join(in_dir, file)
            output_path = os.path.join(out_dir, file_name + '_SHMUP.yuv')
            upsample(input_path, output_path, int(swdt), int(shgt), float(fac))
            progress_bar(count, len(file_list))
        print('\n' + str(count) + ' files resampled.')
