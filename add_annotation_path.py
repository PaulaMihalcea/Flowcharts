def add_annotation_path(path):

    with open('annotation_pathless.txt', 'r') as file_in:
        with open('annotation.txt', 'w') as file_out:
            for line in file_in:
                filename = line.split(',')[0]
                if path[0] == '/':
                    new_path = path + '/' + filename
                else:
                    new_path = '/' + path + '/' + filename
                file_out.write(line.replace(filename, new_path))
