def write_empty_hocr(filename):
    file = open(filename, 'w')
    file.write('<html>\n\t<head>\n\t</head>\n</html>')
    file.close()


def write_empty_prob(filename):
    file = open(filename + '.prob', 'w')
    file.write('\t0.0')
    file.close()
    

def write_empty_txt(filename):
    file = open(filename + '.txt', 'w')
    file.write('')
    file.close()


def write_empty_json(filename):
    file = open(filename + '.json', 'w')
    file.write('{}')
    file.close()


def tesseract_set_version(version, psm):
    
    import subprocess
    import pytesseract

    if(version == 'legacy'):

        out_string = '--oem 0 --psm ' + str(psm) + ' --tessdata-dir "/home/iago/tesseract_data/legacy" -c hocr_char_boxes=1'
        return out_string

    elif(version == '4.1'):

        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        out_string = '--psm ' + str(psm) + ' --tessdata-dir "/home/iago/tesseract_data/4.1" -c hocr_char_boxes=1'
        return out_string

    elif(version == '5.0'):

        pytesseract.pytesseract.tesseract_cmd = '/home/iago/tesseract5.0/tesseract' 
        out_string = '--psm ' + str(psm) + ' --tessdata-dir "/home/iago/tesseract_data/5.0" -c hocr_char_boxes=1'
        return out_string


def run_kraken(img, mode):

    import os
    import subprocess
    from convert_outputs import krakenHOCRtoCharConf

    output_path = 'outputs/kraken/'

    problematic_files = []

    img_nf = img.split('/')[-1]
    i = img_nf.split('.')[0]

    if mode != 'a':
        output_folder = output_path + i + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    else:
        output_folder = output_path + img.split('/')[-2] + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
                
    output = output_folder + i + '.hocr'
    model_path = '/home/iago/Downloads/en_best.mlmodel'
                        
    command = 'kraken -i ' + img + ' ' + output + \
        ' binarize segment ocr -m ' + model_path + ' -h --threads 20'
    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE).stderr

    if(b'script_detection' in out or b'err' in out):
        write_empty_hocr(output)

    return krakenHOCRtoCharConf(output)


def run_ocropus(img, mode):
    
    import os
    import subprocess
    import pathlib
    from convert_outputs import ocropusPROBtoCharConf

    output_path = 'outputs/ocropus/'

    create_empty = []
    img_nf = img.split('/')[-1]
    p = img.split('.')[0]
    i = img_nf.split('.')[0]
    if(p == i):
        p = str(pathlib.Path().absolute())
    else:
        p = '/'.join(p.split('/')[:-1]) + '/'

    if mode != 'a':
        output_folder = output_path + i + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    else:
        output_folder = output_path + img.split('/')[-2] + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    # Binarize
    command = 'ocropus-nlbin -n ' + img

    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE).stderr

    if(b'Err' in out):
        create_empty.append(i)
    else:

        for j in os.listdir(p):
            if(j[-8:] == '.bin.png' or j[-8:] ==  '.nrm.png'):
                os.rename(str(p) + '/' + j, output_folder + j)

        # Recognition
        command = 'ocropus-rpred -n -m en-default.pyrnn.gz ' + output_folder + '*.bin.png --parallel 10 --probabilities'
                            
        out = subprocess.run(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL).stderr

        if not (out):
            for j in os.listdir(output_folder):
                if(j[-8:] == '.bin.png' or j[-8:] ==  '.nrm.png'):
                    os.remove(output_folder + j)

        if(len(create_empty) > 0):
            for s in create_empty:
                write_empty_prob(output_folder + s[:-4])
                write_empty_txt(output_folder + s[:-4])

    return ocropusPROBtoCharConf(output_folder + i + '.prob')
        

def run_calamari(img, mode):
    
    import os
    import subprocess
    import pathlib
    from convert_outputs import calamariJSONtoCharConf

    output_path = 'outputs/calamari/'

    create_empty = []
    img_nf = img.split('/')[-1]
    p = img.split('.')[0]
    i = img_nf.split('.')[0]
    if(p == i):
        p = str(pathlib.Path().absolute())
    else:
        p = '/'.join(p.split('/')[:-1]) + '/'

    if mode != 'a':
        output_folder = output_path + i + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    else:
        output_folder = output_path + img.split('/')[-2] + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    # Binarize
    command = 'ocropus-nlbin -n ' + img

    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE).stderr

    if(b'Err' in out):
        create_empty.append(i)
    else:

        if mode != 'a':
            for j in os.listdir(p):
                if(j[-8:] == '.bin.png' or j[-8:] ==  '.nrm.png'):
                    os.rename(str(p) + '/' + j, output_folder + j)
        else:
            import shutil
            shutil.copyfile(str(p) + '/' + str(i) + '.bin.png', output_folder + str(i) + '.bin.png')
            shutil.copyfile(str(p) + '/' + str(i) + '.nrm.png', output_folder + str(i) + '.nrm.png')


        # Recognition
        command = 'calamari-predict --checkpoint antiqua_modern/4.ckpt.json --files ' + output_folder + '*.bin.png --batch_size=20 --extended_prediction_data'
                            
        out = subprocess.run(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL).stdout

        if(b'All files written' in out):
            for j in os.listdir(output_folder):
                if(j[-8:] == '.bin.png' or j[-8:] ==  '.nrm.png'):
                    os.remove(output_folder + j)            
                
        if(len(create_empty) > 0):
            for s in create_empty:
                write_empty_json(output_folder + s[:-4])
                write_empty_txt(output_folder + s[:-4])

    return calamariJSONtoCharConf(output_folder + i + '.json')


def run_tesseract(img, version, psm, mode):
    
    import os
    import pytesseract
    import pathlib
    from convert_outputs import tesseractHOCRtoCharConf, tesseractLegacyHOCRtoCharConf

    output_path = 'outputs/tesseract_' + version + '_psm' + str(psm) +'/'

    config_str = tesseract_set_version(version, psm)
    
    img_nf = img.split('/')[-1]
    p = img.split('.')[0]
    i = img_nf.split('.')[0]
    if(p == i):
        p = str(pathlib.Path().absolute())
    else:
        p = '/'.join(p.split('/')[:-1]) + '/'

    if mode != 'a':
        output_folder = output_path + i + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    else:
        output_folder = output_path + img.split('/')[-2] + '/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    hocr = pytesseract.image_to_pdf_or_hocr(img, extension = 'hocr', config = config_str)
    output_file_name = output_folder + i + '.hocr'
    output_file = open(output_file_name, 'wb')
    output_file.write(hocr)
    output_file.close()

    ocr_name = 'tesseract_' + version + '_psm' + str(psm)
    if(version == 'legacy'):
        return tesseractLegacyHOCRtoCharConf(output_file_name, ocr_name)
    else:
        return tesseractHOCRtoCharConf(output_file_name, ocr_name)
