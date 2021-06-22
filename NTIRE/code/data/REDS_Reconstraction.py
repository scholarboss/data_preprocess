import os
import sys
import argparse



# only
def main(QP_start=36, Train_or_test='train'):
    Train_or_test = Train_or_test
    Train_ori_path = os.path.join('..', '..', 'ori_data', 'train_sharp_part1')
    Eval_ori_path = os.path.join('..', '..', 'ori_data', 'val_sharp')
    Ori_path = Train_ori_path if Train_or_test=='train' else Eval_ori_path
    Rec_path = os.path.join('..', '..', 'rec_data')
    Width, Heigh = 1280, 720
    QP_start = QP_start # 20, 26, 30, 36

    for qp in range(QP_start, QP_start+5):
        data_list = os.listdir(Ori_path)
        count = 1  # display count
        print('\n QP={} in Reconstracting... \n'.format(qp))
        for name_ in data_list:

            # display
            progress_bar(count, len(data_list))
            count += 1

            name, ext = os.path.splitext(name_)
            if ext != '.yuv':
                continue

            # input and output
            input_name = os.path.join(Ori_path, name_)
            bin_name = os.path.join(Rec_path, 'bin', Train_or_test, str(qp), name+'.bin')
            log_code_name = os.path.join(Rec_path, 'log', Train_or_test, 'code_{}_qp{}.txt'.format(name, qp))
            log_decode_name = os.path.join(Rec_path, 'log', Train_or_test, 'decode_{}_qp{}.txt'.format(name, qp))
            rec_name = os.path.join(Rec_path, 'rec_yuv', Train_or_test, str(qp), name_)
            if not os.path.exists(os.path.split(bin_name)[0]):
                os.makedirs(os.path.split(bin_name)[0])
            if not os.path.exists(os.path.split(log_code_name)[0]):
                os.makedirs(os.path.split(log_code_name)[0])
            if not os.path.exists(os.path.split(rec_name)[0]):
                os.makedirs(os.path.split(rec_name)[0])
            
            command_code = 'x265.exe --input-res {}x{} --fps 30 {} -o {} --qp {} 1>>{} 2>&1'\
                .format(Width, Heigh, input_name, bin_name, qp, log_code_name)
            os.system(command_code)
            command_decode = 'TAppDecoder.exe -b {} -o {} 1>>{} 2>&1'\
                .format(bin_name, rec_name, log_decode_name)
            os.system(command_decode)

        print('\n QP={} in coding... \n'.format(qp))


def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


if __name__ == '__main__':
    # two arguments
    #   -- QP_start: 
    #               20, 26, 30, 36
    #   -- Train_or_test:
    #               'train' , 'eval' 
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='train', help='train or eval ')
    parser.add_argument('--qp_begin', type=int, default=36, help='21 | 26 | 31 | 36 ')
    args = parser.parse_args()
    mode, qp_begin = args.mode, args.qp_begin

    main(QP_start=qp_begin, Train_or_test=mode)