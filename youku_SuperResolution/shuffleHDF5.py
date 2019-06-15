import os
import time
import h5py
import numpy as np




def shuffle_time(h5f):
    input_key, label_key = list(h5f.keys())
    t1 = time.time()
    state = np.random.get_state()
    np.random.shuffle(h5f[input_key])
    print('complate input data')
    print('label data begin......')
    np.random.set_state(state)
    np.random.shuffle(h5f[label_key])
    t2 = time.time()
    print('Time to shuffle: {:.3f} seconds'.format(t2 - t1))




if __name__ == '__main__':
    root_dir = r'E:\competition\youku\dataset\train'
    yuv_path = r'yuv'
    hdf5dir = r'HDF5data'
    train_or_test = 'train'
    file_size = os.path.getsize(os.path.join(root_dir, hdf5dir, '{}_youku_multi.hdf5'.format(train_or_test)))
    print('Size of HDF5: {:.3f} GB'.format(file_size/2.0**30))
    f = h5py.File(os.path.join(root_dir, hdf5dir, '{}_youku_multi.hdf5'.format(train_or_test)), 'r+')
    print('shuffle begin.....')
    shuffle_time(f)
    f.close()

