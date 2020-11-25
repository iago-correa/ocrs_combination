def segment_ocropus(file, output_folder):

    import os
    import subprocess
    import pathlib

    img_name = file.split('/')[-1].split('.')[0]
    img_orig_folder = '/'.join(file.split('/')[:-1]) + '/'
    if(img_orig_folder == '/'):
        img_orig_folder = str(pathlib.Path().absolute()) + '/'

    # Binarize
    command = 'ocropus-nlbin -n ' + file

    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE).stderr

    for j in os.listdir(img_orig_folder):
        if(j[-8:] == '.bin.png' or j[-8:] ==  '.nrm.png'
         or j[-8:] ==  '.bin.jpg'  or j[-8:] ==  '.nrm.jpg'):
            os.rename(img_orig_folder + j, output_folder + j)

    if not(b'Err' in out):
                    
        # Segmentation
        command = 'ocropus-gpageseg -n ' + output_folder + img_name + '.bin.png --minscale 3.0 --maxlines 1000'
        out = subprocess.run(command,
                             shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.PIPE).stderr
                    
        for j in os.listdir(output_folder):
            if(j[-8:] == '.bin.png' or j[-8:] ==  '.nrm.png' or j[-9:] ==  '.pseg.png'
             or j[-8:] == '.bin.jpg' or j[-8:] ==  '.nrm.jpg' or j[-9:] ==  '.pseg.jpg'):
                os.remove(output_folder + j)

        ocropus_seg_path = output_folder + img_name + '/'
        for j in os.listdir(ocropus_seg_path):
            os.rename(ocropus_seg_path + j, output_folder + j)
        os.removedirs(ocropus_seg_path)


def segment_kraken(file, output_folder):
    
    import pytesseract
    import matplotlib.pyplot as plt
    from pytesseract import Output
    import subprocess
    import cv2
    import os
    import csv
    
    img = cv2.imread(file)
    img_name = file.split('/')[-1].split('.')[0]

    command = 'kraken -i ' + file + ' ' + output_folder + img_name + '.txt binarize segment'
                
    out = subprocess.run(command,
                          shell=True,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.PIPE).stderr

    if(b'Err' in out):
        if(file[-4:] == '.png'):
            converted_file = file[:-4] + '.jpg'

            command = 'convert ' + file + ' ' + converted_file
            out = subprocess.run(command,
                                 shell=True,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.PIPE).stderr

            command = 'kraken -i ' + converted_file + ' ' + output_folder + img_name + '.txt binarize segment'
            out = subprocess.run(command,
                                 shell=True,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.PIPE).stderr

            os.remove(converted_file)

            if(b'Err' in out):
                print('Error: ' + file)
                return 0

    segments_list_file = output_folder + img_name + '.txt'
    img = cv2.imread(file)
                    
    file = open(segments_list_file, 'r')
    content = file.read()
    m = content.split('boxes\": [')[1].split('], \"script')[0] + ','
    m = m.split('], ')[0:len(m.split('], '))]
    m[len(m) - 1] = m[len(m) - 1][:-2]

    count = 0
    for i in m:
        vals = i[1:].split(', ')
        crop_img = img[int(vals[1]):int(vals[3]), int(vals[0]):int(vals[2])]
        index = '%04d' % (count)
        cv2.imwrite(output_folder + str(index) + '.png', crop_img) 
        count += 1


def segment_tesseract(file, output_folder):

    import pytesseract
    import matplotlib.pyplot as plt
    from pytesseract import Output
    import cv2
    import os
    import csv

    img = cv2.imread(file)
    img_name = file.split('/')[-1].split('.')[0]

    data = pytesseract.image_to_data(file, output_type=Output.DICT)

    count = 0
    with open(output_folder + img_name + '.csv', 'w', newline='') as csvfile:
        for word, conf, x, y, w, h in zip(data['text'], data['conf'], data['left'], data['top'], data['width'], data['height']):
            if(float(conf) >= 0 and w > 0 and h > 0):
                crop_img = img[y:y+h, x:x+w]
                index = '%04d' % (count)
                cv2.imwrite(output_folder + str(index) + '.png', crop_img) 
                writer = csv.writer(csvfile)
                writer.writerow([x, y, w, h, str(index)])
                count += 1