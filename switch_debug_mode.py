import os, sys

def replace_func(fname, replace_set):
    target, replace = replace_set

    with open(fname, 'r') as f_read:
        tmp_list =[]
        for row in f_read:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f_write:
        for i in range(len(tmp_list)):
            f_write.write(tmp_list[i])

if __name__ == '__main__':
    # コマンドライン引数
    args = sys.argv

    # param set
    fname = os.path.join('.', 'config', 'settings.py')

    # (検索する文字列, 置換後の文字列)
    replace_debug_on  = ('DEBUG = False', 'DEBUG = True\n')
    replace_debug_off = ('DEBUG = True', 'DEBUG = False\n')

    if len(args) == 1:
        replace_set = replace_debug_off
    else:
        if args[1] == 'on':
            replace_set = replace_debug_on
        elif args[1] == 'off':
            replace_set = replace_debug_off
        else:
            replace_set = replace_debug_off

    # ファイル書き換え
    replace_func(fname, replace_set)
    print(replace_set[1])
