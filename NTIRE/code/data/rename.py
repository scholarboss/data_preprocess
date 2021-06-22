import os

Path = os.path.join('..', '..')
Extension = {'.yuv'}

def rename_recursive(path_):
    path_list = os.listdir(path_)
    # print(path_list)
    for path in path_list:
        if os.path.isdir(os.path.join(path_, path)):
            # print(os.path.join(path_, path))
            rename_recursive(os.path.join(path_, path))
        else:
            name, ext = os.path.splitext(path)
            # print(ext)
            if ext in Extension:
                os.rename(os.path.join(path_, path), os.path.join(path_, name+'_1280x720.yuv'))
                print(os.path.join(path_, path), 'reame to ', os.path.join(path_, name+'_1280x720.yuv'))
                
if __name__ == '__main__':
    rename_recursive(Path)


    