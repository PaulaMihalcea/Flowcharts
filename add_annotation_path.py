def add_annotation_path(file, path):

    with open(file, 'r') as file_in:
        new_file = file.replace('_pathless', '') + '_with_path.txt'
        with open(new_file, 'w') as file_out:
            for line in file_in:
                filename = line.split(',')[0]
                if path[0] == '/':
                    new_path = path + '/' + filename
                else:
                    new_path = '/' + path + '/' + filename
                file_out.write(line.replace(filename, new_path))
