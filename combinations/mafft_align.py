def align_text(strings_list):

    import subprocess

    input_file = create_temp_fasta(strings_list)
    output_file = 'temp_out.fa'

    command = 'mafft --text ' + input_file + ' > ' + output_file 
    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE).stderr

    if(b'err' in out):
        print(out)

    output_list = fasta_out_to_list(output_file)

    delete_temp_fasta(input_file, output_file)

    return output_list


def create_temp_fasta(stringslist):

    import codecs

    filename = 'temp_in.fa'
    file = codecs.open(filename, 'w', encoding='latin-1')

    for i in range(0, len(stringslist)):
        file.write('>STR' + str(i))
        file.write('\n')
        string = stringslist[i]
        string = string.replace('-', '¼')
        string = string.replace(' ', '½')
        string = string.replace('=', '¾')
        string = string.replace('<', '«')
        string = string.replace('>', '»')
        string = string.encode('latin-1', 'ignore')
        file.write(string.decode('latin-1'))
        file.write('\n')
    
    file.close()
    return filename


def delete_temp_fasta(input_file, output_file):
    import os
    os.remove(input_file)
    os.remove(output_file)


def fasta_out_to_list(output_file):
    
    import codecs

    output_list = []
    
    num_lines = 0
    with codecs.open(output_file, encoding='latin-1') as file:
        for line in file:
            num_lines += 1

    line_count = 0
    with codecs.open(output_file, encoding='latin-1') as file:
        for line in file:
            if(line[0] != '>'):
                line = line.rstrip()
                string = line.replace('½', ' ')
                string = string.replace('¾', '=')
                string = string.replace('«', '<')
                string = string.replace('»', '>')
                str_list = []
                for char in string:
                    if(char == '-'):
                        str_list.append(None)
                    elif(char == '¼'):
                        str_list.append('-')
                    else:
                        str_list.append(char)
                line_text.extend(str_list)
            else:
                if(line_count == 0):
                    line_text = []
                else:
                    output_list.append(line_text)
                    line_text = []
            if(line_count == num_lines - 1):
                output_list.append(line_text)
            line_count += 1

    return output_list
