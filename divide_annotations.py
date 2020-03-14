def divide_annotations(annotations_path, train_list, test_list):

    a = open(annotations_path, 'r')  # Annotations file
    tr = open(train_list, 'r')  # Original train/test file list
    ts = open(test_list, 'r')  # Original train/test file list
    d_tr = open('annotation' + '_train.txt', 'w')  # Train output file
    d_ts = open('annotation' + '_test.txt', 'w')  # Test output file

    for line_tr in tr:
        a = open(annotations_path, 'r')

        for line_a in a:
            if line_a.split(',')[0].replace('.png', '') == line_tr.replace('.inkml', '').strip('\n'):
                d_tr.write(line_a)
            else:
                pass

        a.close()

    for line_ts in ts:
        a = open(annotations_path, 'r')

        for line_a in a:
            if line_a.split(',')[0].replace('.png', '') == line_ts.replace('.inkml', '').strip('\n'):
                d_ts.write(line_a)
            else:
                pass

        a.close()

    tr.close()
    ts.close()
    d_tr.close()
    d_ts.close()
