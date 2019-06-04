# pkg images to hdf5
from yuv_io import *
import h5py
import cv2
import os
import sys
import numpy as np

# import torch.utils.data as data
# from torchvision import transforms
# import numpy as np

# root_dir = os.path.join('input_yuv')

width = 96
height = 96
ext_dir = 'test'  # 'train' or 'test'

save_dir = os.path.join('HDF5data_v3')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
label_lr_path = os.path.join(r'label_yuv_downsampled_192x192', ext_dir)
label_sr_path = os.path.join(r'label_yuv_oriSR_192x192', ext_dir)
input_path = os.path.join('input_yuv_192x192')

# 获取所有测试图片名
def get_img_dict(QP=21, path=input_path, train_or_test=ext_dir):
    path = {'QP' + str(qp): [] for qp in range(QP, QP + 5)}
    for qp in range(QP, QP + 5):
        input_lr_path = os.path.join(path, 'QP' + str(qp), train_or_test)
        img_list = os.listdir(input_lr_path)
        path['QP' + str(qp)].append(img_list)
    return path


# 获取标签图片名
# label_folder: 'label_png_downsampled' or 'label_png_oriSR'
def get_name_list(label_folder):
    label_path = os.path.join(label_folder, ext_dir)
    return os.listdir(label_path)


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


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d %s %d' % ("=" * rate_num, " " * (width - rate_num), num, ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


# print('=========================> convert =====> ')
# img_dict = get_img_dict(QP=QP_begin, train_or_test=ext_dir)
# 按图片遍历，存储形式为 QP21,QP22....QP25,QP21,QP22.....每个QP一张，依次存储
input_path_name = os.path.join('input_yuv_192x192', 'QP21')
img_list = get_name_list(input_path_name)
total = len(img_list)
# img_num_per_QP = len(img_dict['QP' + str(QP_begin)][0])
# for j in [21, 26, 31, 36]:
for j in [21]:
    print('\n============== convert train dataset QP_begin={}'.format(j))
    QP_begin = j
    QP_end = QP_begin + 4
    f = h5py.File(os.path.join(save_dir, '{}_QP'.format(ext_dir) + str(QP_begin) + '_QP' + str(QP_end) + '.hdf5'), 'w')
    for i in range(total):
        progress_bar(i + 1, total)
        for qp in range(QP_begin, QP_begin + 5):
            img_name = img_list[i].split('_')
            img_name = img_name[0] + '_' + img_name[1] + '_' + img_name[2] + '_' + img_name[3] + '_' + img_name[4] + '_' + \
                       img_name[5] + '_' + img_name[6] + '_' + img_name[7] + '_' + img_name[8] + '_' + str(qp) + '_' + \
                       img_name[10]
            img_name = os.path.join(input_path, 'QP' + str(qp), ext_dir, img_name)
            # img = cv2.imread(img_name)
            img ,_ ,_ = YUVread(img_name, [width, height], frame_num=None, start_frame=0)
            #img = img[:, :, 0]
            img = np.reshape(img, [1, 1, width, height])
            save_h5(f, img, 'img_input_96_96')
        img_name = img_list[i].split('_')
        label1_name = img_name[0] + '_' + img_name[1] + '_' + img_name[2] + '_' + img_name[3] + '_' + img_name[4] + '_' + \
                     img_name[5] + '_' + img_name[6] + '_' + img_name[7] + '_' + img_name[8] + '.yuv'
        label2_name = label1_name
        label_lr_name = os.path.join(label_lr_path, label1_name)
        label_sr_name = os.path.join(label_sr_path, label2_name)
        # img = cv2.imread(label_lr_name)
        # img = img[:, :, 0]
        img ,_ ,_ = YUVread(label_lr_name, [width, height], frame_num=None, start_frame=0)
        img = np.reshape(img, [1, 1, width, height])
        save_h5(f, img, 'img_label_96_96')

        img ,_ ,_ = YUVread(label_sr_name, [2*width, 2*height], frame_num=None, start_frame=0)
        img = np.reshape(img, [1, 1, 2*width, 2*height])
        save_h5(f, img, 'img_label_192_192')


f.close()




'''
print('=========================> convert input data ')
img_dict = get_img_dict(QP=QP_begin, train_or_test=ext_dir)
# 按图片遍历，存储形式为 QP21,QP22....QP25,QP21,QP22.....每个QP一张，依次存储
img_path = os.path.join(root_dir, 'input_png')
img_num_per_QP = len(img_dict['QP' + str(QP_begin)][0])
for i in range(img_num_per_QP):
    progress_bar(i+1, img_num_per_QP)
    for key in img_dict:
        img_name = os.path.join(img_path, key, ext_dir, img_dict[key][0][i])
        img = cv2.imread(img_name)
        img = img[:, :, 0]
        img = img.reshape([1, 1, 41, 41])
        save_h5(f, img, 'img_input_41_41')
        

print('\n=========================> convert label_png_downsampled data ')
label_img_list = get_label_list('label_png_downsampled')
label_img_path = os.path.join(root_dir, 'label_png_downsampled', ext_dir)
total_label = len(label_img_list)
for i in range(total_label):
    progress_bar(i+1, total_label)
    label_img_full_name = os.path.join(label_img_path, label_img_list[i])
    img = cv2.imread(label_img_full_name)
    img = img[:, :, 0]
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    img = img.reshape([1, 1, 41, 41])
    save_h5(f, img, 'img_label_41_41')
print('\n=========================> convert label_png_oriSR data ')
label_img_list = get_label_list('label_png_oriSR')
label_img_path = os.path.join(root_dir, 'label_png_oriSR', ext_dir)
total_label = len(label_img_list)
for i in range(total_label):
    progress_bar(i+1, total_label)
    label_img_full_name = os.path.join(label_img_path, label_img_list[i])
    img = cv2.imread(label_img_full_name)
    img = img[:, :, 0]
    img = img.reshape([1, 1, 82, 82])
    save_h5(f, img, 'img_label_82_82')
'''

# cv2.imshow('test', img[:, :, 0])
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#
# def data_compress(train_or_test):
#     for QP in range(QP_begin, QP_end):
#         input_lr_path = os.path.join(root_dir, r'input_png', 'QP' + str(QP), train_or_test)
#         label_lr_path = os.path.join(root_dir, r'label_png_downsampled', train_or_test)
#         label_sr_path = os.path.join(root_dir, r'label_png_oriSR', train_or_test)
#
#
# class CData(data.Dataset):
#     def __init__(self, train=True, transform=None):
#         self.root_dir = r'../data'
#         self.ext_dir = 'train' if train else 'test'
#         self.QP_begin = 31
#         self.QP_end = self.QP_begin + 4
#         self.transform = transform
#
#     def _get_path(self, QP=31):
#         input_lr_path = os.path.join(self.root_dir, r'input_png', 'QP' + str(QP), self.ext_dir)
#         label_lr_path = os.path.join(self.root_dir, r'label_png_downsampled', self.ext_dir)
#         label_sr_path = os.path.join(self.root_dir, r'label_png_oriSR', self.ext_dir)
#         return input_lr_path, label_lr_path, label_sr_path
#
#     def __len__(self):
#         _, _, label_sr_path = self._get_path()
#         return len(os.listdir(label_sr_path)) * 5
#
#     def _get_tensor(self, idx, QP):
#         input_lr_path, label_lr_path, label_sr_path = self._get_path(QP)
#         input_lr_list = os.listdir(input_lr_path)
#         label_lr_list = os.listdir(label_lr_path)
#         label_sr_list = os.listdir(label_sr_path)
#         # can't use '\\' for path
#         input_lr = cv2.imread(os.path.join(input_lr_path, input_lr_list[idx]), 0)
#         label_lr = cv2.imread(os.path.join(label_lr_path, label_lr_list[idx]), 0)
#         label_sr = cv2.imread(os.path.join(label_sr_path, label_sr_list[idx]), 0)
#         # input_lr = cv2.imread(input_lr_path+'\\'+input_lr_list[idx], 0)
#         # label_lr = cv2.imread(label_lr_path+'\\'+label_lr_list[idx], 0)
#         # label_sr = cv2.imread(label_sr_path+'\\'+label_sr_list[idx], 0)
#         input_lr = transforms.ToTensor()(input_lr)
#         label_lr = transforms.ToTensor()(label_lr)
#         label_sr = transforms.ToTensor()(label_sr)
#         # H1, W1 = input_lr.shape
#         # H2, W2 = label_lr.shape
#         # H3, W3 = label_sr.shape
#         # input_lr = transforms.ToTensor()(input_lr.reshape(H1,W1,1))
#         # label_lr = transforms.ToTensor()(label_lr.reshape(H2,W2,1))
#         # label_sr = transforms.ToTensor()(label_sr.reshape(H3,W3,1))
#         return input_lr, label_lr, label_sr
#
#     def __getitem__(self, idx):
#         img_idx = idx // 5
#         QP = idx % 5 + self.QP_begin
#         input_lr, label_lr, label_sr = self._get_tensor(img_idx, QP)
#         if self.transform:
#             input_lr = self.transform(input_lr)
#             label_lr = self.transform(label_lr)
#             label_sr = self.transform(label_sr)
#         return input_lr, label_lr, label_sr
#
#
# if __name__ == "__main__":
#     dataset = CData(train=False)
#     print(len(dataset))
#
# #
# # class CDataLoader():
