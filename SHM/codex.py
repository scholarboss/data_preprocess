import os
import shutil
import sys

# 对下采样的 YUV 数据 编码-->存储-->解码

def progress_bar(num, total, width=40):
    rate = num / total
    rate_num = int(rate * width)
    r = '\r[%s%s] %d%%%s%d' % ("=" * rate_num, " " * (width - rate_num), int(rate * 100), ' done of ', total)
    sys.stdout.write(r)
    sys.stdout.flush()


# QP = 35
# 对 QP 值为26--30进行操作
for QP in range(20,26):
	source_dir = 'downsampled_yuv'
	stream_dir = 'bit_stream' + '\\QP' + str(QP)
	target_dir = 'recs' + '\\QP' + str(QP)
	log_dir = 'logs'

	if not os.path.exists(log_dir):
	    os.makedirs(log_dir)
	else:
	    if os.path.exists(log_dir + '/encode_log.txt'):
	        os.remove(log_dir + '/encode_log.txt')
	    if os.path.exists(log_dir + '/decode_log.txt'):
	        os.remove(log_dir + '/decode_log.txt')

	dir_list = ['test', 'train']
	if not dir_list:
	    dir_list = os.listdir(source_dir)
	for name in dir_list:
	    if os.path.isdir(os.path.join(source_dir, name)):
	        if (QP is not None) and (not os.path.exists(os.path.join(stream_dir, name))):
	            os.makedirs(os.path.join(stream_dir, name))
	        if not os.path.exists(os.path.join(target_dir, name)):
	            os.makedirs(os.path.join(target_dir, name))
	    else:
	        dir_list.remove(name)

	for name in dir_list:
	    in_dir = os.path.join(source_dir, name)
	    bin_dir = os.path.join(stream_dir, name)
	    out_dir = os.path.join(target_dir, name)

	    if QP is None:
	        print('****************************')
	        print('QP is None. Skip codex.')
	        print('From [' + in_dir + '] to [' + out_dir + ']:')
	        count = 0
	        file_list = os.listdir(in_dir)
	        for file in file_list:
	            file_name, ext = os.path.splitext(file)
	            if not ext == '.yuv':
	                continue
	            count += 1
	            input = os.path.join(in_dir, file)
	            output = os.path.join(out_dir, file_name + '_' + str(QP) + '_rec.yuv')
	            shutil.copyfile(input, output)
	            progress_bar(count, len(file_list))
	        print('\n' + str(count) + ' files copied.')
	        continue

	    print('****************************')
	    print('Encoding... (QP=' + str(QP) + ')')
	    print('From [' + in_dir + '] to [' + bin_dir + ']:')
	    count = 0
	    file_list = os.listdir(in_dir)
	    for file in file_list:
	        file_name, ext = os.path.splitext(file)
	        if not ext == '.yuv':
	            continue
	        count += 1
	        lwdt, lhgt, swdt, shgt, fac = file_name.split('_')[-5:]
	        input = os.path.join(in_dir, file)
	        output = os.path.join(bin_dir, file_name + '_' + str(QP) + '.bin')
	        command = 'x265.exe --input-res ' + swdt + 'x' + shgt + ' --fps 30 ' + input + ' -o ' + output + ' --qp ' + str(
	            QP + 3) + ' 1>>' + log_dir + '/encode_log.txt 2>&1'  # 'QP-3' in x265 for first frame
	        # print('Encode ' + str(num) + ': ' + file + '...')
	        os.system(command)
	        progress_bar(count, len(file_list))
	    print('\n' + str(count) + ' files encoded.')
	    print('Log path: ' + log_dir + r'\encode_log.txt')

	    print('****************************')
	    print('Decoding...')
	    print('From [' + bin_dir + '] to [' + out_dir + ']:')
	    count = 0
	    file_list = os.listdir(bin_dir)
	    for file in file_list:
	        file_name, ext = os.path.splitext(file)
	        if not ext == '.bin':
	            continue
	        wdt, hgt, fac, bQP = file_name.split('_')[-4:]
	        if bQP != str(QP):
	            continue
	        count += 1
	        input = os.path.join(bin_dir, file)
	        output = os.path.join(out_dir, file_name + '_rec.yuv')
	        command = 'TAppDecoder.exe -b ' + input + ' -o ' + output + ' 1>>' + log_dir + '/decode_log.txt 2>&1'
	        # print('Decode ' + str(num) + ': ' + file + '...')
	        os.system(command)
	        progress_bar(count, len(file_list))
	    print('\n' + str(count) + ' files decoded.')
	    print('Log path: ' + log_dir + r'\decode_log.txt')
