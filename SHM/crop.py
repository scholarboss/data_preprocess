from PIL import Image
from yuv_io import *
import os
import sys


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


def crop_base(factor):
    factor = round(factor * 100)  # Improve accuracy
    base = factor * 2
    if (base % 200) != 0:
        base *= 2
    return base // 100


def crop_by(image, factor):
    base = crop_base(factor)
    out_width = image.width - (image.width % base)
    out_height = image.height - (image.height % base)
    return image.crop((0, 0, out_width, out_height))


if __name__ == '__main__':

    source_dir = 'im_ori'
    target_dir = 'im_cropped_yuv'

    extension = {'.jpg', '.bmp'}
    # factors = {1.5, 2, 3}
    factors = {2}

    dir_list = []
    if not dir_list:
        dir_list = os.listdir(source_dir)
    for name in dir_list:
        if os.path.isdir(os.path.join(source_dir, name)):
            if not os.path.exists(os.path.join(target_dir, name)):
                os.makedirs(os.path.join(target_dir, name))
        else:
            dir_list.remove(name)

    print('****************************')
    print('Cropping...')

    for name in dir_list:
        in_dir = os.path.join(source_dir, name)
        out_dir = os.path.join(target_dir, name)
        print('From [' + in_dir + '] to [' + out_dir + ']:')

        for factor in factors:
            print('Cropping by factor of ' + str(factor))
            file_list = os.listdir(in_dir)
            count = 0
            for file in file_list:
                file_name, ext = os.path.splitext(file)
                if ext in extension:
                    im = Image.open(os.path.join(in_dir, file))  # type: Image.Image
                    im_cropped = crop_by(im, factor)
                    out_file = file_name + '_' + str(im_cropped.width) + '_' + str(im_cropped.height) + '_' + str(
                        round(im_cropped.width / factor)) + '_' + str(round(im_cropped.height / factor)) + '_' + str(
                        factor) + '.yuv'
                    out_path = os.path.join(out_dir, out_file)

                    y, u, v = im_cropped.convert('YCbCr').split()  # type: Image.Image
                    u = u.resize([(im_cropped.width // 2), (im_cropped.height // 2)])
                    v = v.resize([(im_cropped.width // 2), (im_cropped.height // 2)])

                    yy = np.array(y)
                    uu = np.array(u)
                    vv = np.array(v)

                    YUVwrite(yy, uu, vv, out_path)
                    count += 1
                    progress_bar(count, len(file_list))
            print()
