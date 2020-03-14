import os
import shutil


def divide_dataset(dataset_path, train_list, test_list):

    tr = open(train_list, 'r')  # Original train file list
    ts = open(test_list, 'r')  # Original test file list
    tr_folder = dataset_path + '_train/'
    ts_folder = dataset_path + '_test/'

    if not os.path.exists(tr_folder):  # Create folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(tr_folder)
    if not os.path.exists(ts_folder):  # Create folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(ts_folder)

    for line_tr in tr:
        shutil.copy(dataset_path + '/' + line_tr.strip('\n').replace('.inkml', '.png'), tr_folder)

    for line_ts in ts:
        shutil.copy(dataset_path + '/' + line_ts.strip('\n').replace('.inkml', '.png'), ts_folder)

    tr.close()
    ts.close()
