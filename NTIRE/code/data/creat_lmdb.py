from LileiLib.yuv_io import YUVread
from LileiLib import progress_bar
import lmdb
import os
import sys
import pickle
import argparse


def REDS2LMDB(mode='train', QP_begin = 36):
    ''' 
        creat lmdb for the REDS dataset, each image with fixed size, only sharp_part1
            GT: [100, 720, 1280]    key: GT_000_000  (GT_nVideo_nFrame)
            RecImg: [100, 720, 1280] key: Rec_000_000_00 (Rec_nVideo_nFrame_qp)
        
        Arguments:
            mode: 'train' | 'eval'     
            QP_begin: 20 | 26 | 30 | 36
            
        path: 
            Root_path: '../../'
            GT_path: 'ori_data/train_sharp_part1' | 'ori_data/val_sharp'  
            Rec_path: 'rec_data/rec_yuv/train/%d' %qp     | 'rec_data/rec_yuv/eval%d' %qp
    '''

    ### configurations
    Width, Heigh = 1280, 720
    
    Root_path = os.path.join('..', '..')
    if mode == 'train':
        GT_path = os.path.join(Root_path, 'ori_data', 'train_sharp_part1')
    if mode == 'eval':
        GT_path = os.path.join(Root_path, 'ori_data', 'val_sharp')
    Rec_path = os.path.join(Root_path, 'rec_data', 'rec_yuv', mode)
    Lmdb_path = os.path.join(Root_path, 'rec_data', 'lmdb')
    if not os.path.exists(Lmdb_path):
        os.makedirs(Lmdb_path)
    Lmbd_name = os.path.join(Lmdb_path, mode+'_QP{}_QP{}'.format(QP_begin, QP_begin+4))
    if os.path.exists(Lmbd_name):
        print('Folder [{:s}] already exists. Exit...'.format(Lmbd_name))
        sys.exit(1)

    ### 
    GT_list = os.listdir(GT_path)
    length = len(GT_list)
    env = lmdb.open(Lmbd_name, map_size=length*1073741824) #map_size=214748364800)
    txn = env.begin(write=True)

    GT_keys = []
    Rec_keys = []
    
    print('processing GT data... ')
    for GT_name in GT_list:
        if GT_name.split('.')[-1] != 'yuv':
            continue
        print('\n GT data / {} ... '.format(GT_name))
        name = os.path.join(GT_path, GT_name)
        y, _, _ = YUVread(name, [Heigh, Width])
        nVideo = GT_name.split('_')[0]
        count = 0
        for frame in y:
            key = 'GT_{}_{}'.format(nVideo, '%.3d'%count)
            GT_keys.append(key)
            key = key.encode('ascii')
            count += 1
            progress_bar(count, y.shape[0])  # display progress bar
            txn.put(key, frame)
        txn.commit()
        txn = env.begin(write=True)
    print('\n'+'*'*20)
    print('processing Rec data... \n')
    for qp in range(QP_begin, QP_begin+5):
        print('\nQP = %d'%qp)
        # Rec_path = os.path.join(Rec_path, str(qp))
        Rec_list = os.listdir(os.path.join(Rec_path, str(qp)))
        for Rec_name in Rec_list:
            print('\n Rec data / {} ... '.format(Rec_name))
            nVideo = Rec_name.split('_')[0]
            name = os.path.join(Rec_path, str(qp), Rec_name)
            y, _, _ = YUVread(name, [Heigh, Width])
            count = 0
            for frame in y:
                key = 'Rec_{}_{}_{}'.format(nVideo, '%.3d'%count, qp)
                Rec_keys.append(key)
                key = key.encode('ascii')
                count += 1
                progress_bar(count, y.shape[0])   # display progress
                txn.put(key, frame)
            txn.commit()
            txn = env.begin(write=True)
    txn.commit()
    env.close()
    print('\nFinish writing lmdb...')

    ### creat meta information
    meta_info = {}
    meta_info['name'] = Lmbd_name
    meta_info['GT_keys'] = GT_keys
    meta_info['Rec_keys'] = Rec_keys
    pickle.dump(meta_info, open(mode + '_QP{}_QP{}'.format(QP_begin, QP_begin+4) + '_meta_info.pkl', 'wb')) 
    print('Finish creating lmdb meta info...')






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='train', help='train or eval ')
    parser.add_argument('--qp_begin', type=int, default=36, help='20 | 26 | 30 | 36 ')
    args = parser.parse_args()
    mode, qp_begin = args.mode, args.qp_begin
    
    REDS2LMDB(mode=mode, QP_begin = qp_begin)

'''
run scripts:
    python creat_lmdb.py --mode eval --qp_begin 36

'''