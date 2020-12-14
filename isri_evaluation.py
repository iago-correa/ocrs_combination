import subprocess

def char_acc_evaluation(prediction_file, gt_file, db_name, ocr_name):

    import os

    img_name = prediction_file.split('/')[-1][:-4]
    dir_path = 'evaluations/' + db_name + '/' + ocr_name + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    evaluation_file = dir_path + img_name + '_characc.txt'

    command = 'accuracy ' + gt_file + ' ' + prediction_file + ' ' + evaluation_file
                            
    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL).stderr

    report_file = open(evaluation_file, 'r')
    out = report_file.read()

    char_acc = float(out.split('\n')[4].split('%')[0])

    return abs(char_acc)


def sum_char_acc(db_name, ocr_name):

    import os

    evaluation_file = 'evaluations/' + db_name + '/' + ocr_name + '_char_acc.txt'
    command = 'accsum '

    reports_path = 'evaluations/' + db_name + '/' + ocr_name + '/char_acc/'
    reports = os.listdir(reports_path)
    for report in reports:
        command += (reports_path + report + ' ')

    command += ('> ' + evaluation_file)

    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL).stderr

    report_file = open(evaluation_file, 'r')
    out = report_file.read()

    char_acc = float(out.split('\n')[4].split('%')[0])

    return abs(char_acc)
    

def word_acc_evaluation(prediction_file, gt_file, db_name, ocr_name):

    import os

    img_name = prediction_file.split('/')[-1][:-4]
    dir_path = 'evaluations/' + db_name + '/' + ocr_name + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    evaluation_file = dir_path + img_name + '_wordacc.txt'

    command = 'wordacc ' + gt_file + ' ' + prediction_file + ' ' + evaluation_file
                            
    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL).stdout

    report_file = open(evaluation_file, 'r')
    out = report_file.read()

    word_acc = float(out.split('\n')[4].split('%')[0])

    return abs(word_acc)


def sum_word_acc(db_name, ocr_name):
    
    import os

    evaluation_file = 'evaluations/' + db_name + '/' + ocr_name + '_word_acc.txt'
    command = 'wordaccsum '

    reports_path = 'evaluations/' + db_name + '/' + ocr_name + '/word_acc/'
    reports = os.listdir(reports_path)
    for report in reports:
        command += (reports_path + report + ' ')

    command += ('> ' + evaluation_file)

    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL).stderr

    report_file = open(evaluation_file, 'r')
    out = report_file.read()

    word_acc = float(out.split('\n')[4].split('%')[0])

    return abs(word_acc)


def editop_evaluation(prediction_file, gt_file, db_name, ocr_name):

    import os

    img_name = prediction_file.split('/')[-1][:-4]
    dir_path = 'evaluations/' + db_name + '/' + ocr_name + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    evaluation_file = dir_path + img_name + '_editop.txt'
    
    command = 'editop ' + gt_file + ' ' + prediction_file + ' ' + evaluation_file
                            
    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL).stdout

    report_file = open(evaluation_file, 'r')
    out = report_file.read()

    insertions = int(out.split('\n')[2].split('Insertions')[0])
    deletions = int(out.split('\n')[3].split('Deletions')[0])
    moves = int(out.split('\n')[4].split('Moves')[0])

    return [insertions, deletions, moves]


def sum_editop(db_name, ocr_name):
    
    import os

    evaluation_file = 'evaluations/' + db_name + '/' + ocr_name + '_editop.txt'
    command = 'editopsum '

    reports_path = 'evaluations/' + db_name + '/' + ocr_name + '/editop/'
    reports = os.listdir(reports_path)
    for report in reports:
        command += (reports_path + report + ' ')

    command += ('> ' + evaluation_file)

    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL).stderr

    report_file = open(evaluation_file, 'r')
    out = report_file.read()

    insertions = int(out.split('\n')[2].split('Insertions')[0])
    deletions = int(out.split('\n')[3].split('Deletions')[0])
    moves = int(out.split('\n')[4].split('Moves')[0])

    return [insertions, deletions, moves]


def main():
    
    import os

    db_names = ['sroie']
    outputs_root = 'outputs/'
    # ocr_names = {'funsd':['calamari', 'kraken', 'ocropus', 'tesseract'],
    #             'sroie':['calamari', 'kraken', 'ocropus', 'tesseract','google']}
    # ocr_names = {'funsd':['combination_weighted'],
    #             'sroie':['combination_weighted', 'combination_majority']}
    # ocr_names = {'funsd':['tesseract_5.0', 'tesseract_legacy', 'tesseract_4.1'],
    #             'sroie':['tesseract_5.0', 'tesseract_legacy', 'tesseract_4.1']}

    ocrs_groups = {'all_tess': ['tesseract_5.0_psm1', 'tesseract_5.0_psm3', 'tesseract_5.0_psm4', 'tesseract_5.0_psm5', 'tesseract_5.0_psm6', 'tesseract_5.0_psm7', 'tesseract_5.0_psm8', 'tesseract_5.0_psm9', 'tesseract_5.0_psm10', 'tesseract_5.0_psm11', 'tesseract_5.0_psm12', 'tesseract_5.0_psm13', 'tesseract_4.1_psm1', 'tesseract_4.1_psm3', 'tesseract_4.1_psm4', 'tesseract_4.1_psm5', 'tesseract_4.1_psm6', 'tesseract_4.1_psm7', 'tesseract_4.1_psm8', 'tesseract_4.1_psm9', 'tesseract_4.1_psm10', 'tesseract_4.1_psm11', 'tesseract_4.1_psm12', 'tesseract_4.1_psm13'], 
                    'all_tess_4': ['tesseract_4.1_psm1', 'tesseract_4.1_psm3', 'tesseract_4.1_psm4', 'tesseract_4.1_psm5', 'tesseract_4.1_psm6', 'tesseract_4.1_psm7', 'tesseract_4.1_psm8', 'tesseract_4.1_psm9', 'tesseract_4.1_psm10', 'tesseract_4.1_psm11', 'tesseract_4.1_psm12', 'tesseract_4.1_psm13'], 
                    'all_tess_5': ['tesseract_5.0_psm1', 'tesseract_5.0_psm3', 'tesseract_5.0_psm4', 'tesseract_5.0_psm5', 'tesseract_5.0_psm6', 'tesseract_5.0_psm7', 'tesseract_5.0_psm8', 'tesseract_5.0_psm9', 'tesseract_5.0_psm10', 'tesseract_5.0_psm11', 'tesseract_5.0_psm12', 'tesseract_5.0_psm13'] , 
                    'tess_best3_funsd': ['tesseract_5.0_psm6', 'tesseract_5.0_psm12', 'tesseract_4.1_psm6'], 
                    'tess_best5_funsd': ['tesseract_5.0_psm6', 'tesseract_5.0_psm11', 'tesseract_5.0_psm12', 'tesseract_4.1_psm6', 'tesseract_4.1_psm11'], 
                    'tess_best_metrics_funsd': ['tesseract_5.0_psm1', 'tesseract_5.0_psm3', 'tesseract_5.0_psm4', 'tesseract_5.0_psm6', 'tesseract_4.1_psm6'], 
                    'tess_best3_sroie': ['tesseract_5.0_psm8', 'tesseract_5.0_psm10', 'tesseract_5.0_psm13'], 
                    'tess_best5_sroie': ['tesseract_5.0_psm7', 'tesseract_5.0_psm8', 'tesseract_5.0_psm10', 'tesseract_5.0_psm13', 'tesseract_4.1_psm10'], 
                    'tess_best_metrics_sroie': ['tesseract_5.0_psm4', 'tesseract_5.0_psm6', 'tesseract_5.0_psm7', 'tesseract_5.0_psm10', 'tesseract_5.0_psm13'], 
                    'ocrs_best3_funsd': ['kraken', 'tesseract_4.1_psm6', 'tesseract_5.0_psm6'], 
                    'ocrs_best3_sroie_no_google': ['calamari', 'tesseract_4.1_psm10', 'tesseract_5.0_psm10'], 
                    'ocrs_best3_sroie': ['google', 'tesseract_4.1_psm10', 'tesseract_5.0_psm10']}

    combination_names = ['comb_align_maj_', 'comb_median_', 'comb_wei_median_']
    
    folders_to_evaluate = []
    for combination in combination_names:
        for group in ocrs_groups:
            folders_to_evaluate.append(combination + group)
    
    for db in db_names:

        combs_path = outputs_root + db + '/'
        combinations = []

        for folder in os.listdir(combs_path):
            if(folder in folders_to_evaluate):
                combinations.append(folder)

        combinations.sort()
        print(db + '-----------')
        for ocr in combinations:
            editops = sum_editop(db, ocr)
            char_acc = sum_char_acc(db, ocr) 
            word_acc = sum_word_acc(db, ocr)
            print(str(char_acc) + '\t' + str(word_acc) + '\t' + str(editops[0]) + '\t' + str(editops[1]) + '\t' + str(editops[2]) + '\t' + ocr)


if __name__ == "__main__":
    main()