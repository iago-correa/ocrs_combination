def combine_ocrs(img, ocrs, comb, seg=0, metrics=False, text=None, mode='w'):
    
    """
    Parametros
    
        img: imagem de entrada que tera seu texto identificado
        pode ser um segmento ou uma imagem inteira, como uma 
        pagina, espera receber uma string com o endereco da imagem
        
        ocrs: lista dos ocrs que seram utilizados na combinacao,
        deve conter pelo menos 3 ocrs
            kraken
            calamari
            ocropus
            tesseract3-psm<n>
            tesseract4-psm<n>
            tesseract5-psm<n>
                <n> deve ser substituído pelo valor do parâmetro
                psm (page segmentation mode) do Tesseract
        
        comb: lista dos metodos de combinacao que seram realizados
            align_maj_vote: voto majoritário com alinhamento de strings
            align_rank: ranqueamento com alinhamento de strings
            median_string: mediana de strings
            wei_median_string: mediana de strings com ponderacao
        
        seg: segmentacao que sera utilizado
            0 (valor default) considera que a imagem de entrada 
                ja foi segmentada
            1 ocropus
            2 kraken
            3 tesseract4 
        
        metrics: se False(default) não calcula nenhuma metrica, 
        se True calcula:
            char_acc: acuracia de caracteres
            word_acc: acuracia de palavra
            inserts: numero de operacoes de insercao
            removes: numero de operacoes de remocao
            substitutes numero de operacoes de substituicao
        
        text: caso seja necessario calcular metricas, recebe o 
        texto que devia ser identificado na imagem, espera em
        forma de string

        mode: modo de abertura de arquivo, é para escrever as
        saídas todas num mesmo arquivo no caso de precisar segmentar
    """
    import os

    img_name = img.split('/')[-1].split('.')[0]
    output = []

    if len(ocrs) < 3:
        print('Favor informar pelo menos 3 ocrs')
        return None

    if seg > 0:
        
        segments_folder = segmenta_imagem(img, seg, img_name)
        segments = os.listdir(segments_folder)
        segments.sort()
        file_n = 1
        for segment in segments:
            print(str(file_n) + '/' + str(len(segments)) + ':' + segment)
            if(segment[-3:] == 'png' or segment[-3:] == 'jpg'):
                img_file = segments_folder + segment
                combine_ocrs(img=img_file, ocrs=ocrs, comb=comb, mode='a')
            file_n += 1

        output_subdir = segments_folder.split('/')[-2]
        combined_texts = []

        for c in comb:
            file_path = 'outputs/' + c + '/' + output_subdir + '.txt'
            file = open(file_path, 'r')
            combined_texts.append([c, file.read()])

        if(metrics):
            if(text is not None):
                results = []
                for method, combined_text in combined_texts:
                    result = calcula_metricas(combined_text, text, img_name, method, ocrs)
                    results.append(result)
                    output.append([method, combined_text, result[1], result[2], result[3], result[4], result[5]])
                return output
            else:
                print('Favor informar o texto correto para o cálculo de métricas')
                return None
        else:
            return combined_texts


    else:

        text_data = identifica_texto(img, ocrs, mode)
        if (mode == 'a'):
            combined_texts = combina_textos(text_data, comb, img.split('/')[-2], mode)
        else:
            combined_texts = combina_textos(text_data, comb, img_name, mode)

        if(metrics):
            if(text is not None):
                results = []
                for method, combined_text in combined_texts:
                    result = calcula_metricas(combined_text, text, img_name, method, ocrs)
                    results.append(result)
                    output.append([method, combined_text, result[1], result[2], result[3], result[4], result[5]])
                return output
            else:
                print('Favor informar o texto correto para o cálculo de métricas')
                return None
        else:
            return combined_texts


def clearEmpties(x,y):
    
    i = 0
    length = len(x)
    length_y =  len(y)
    while(i < length):
        if(x[i] == ''):
            x.remove(x[i])
            y.remove(y[i])
            length = length -1  
            continue
        i = i+1
    if(len(x) == 0 and len(y) == 1):
        y.remove(y[0])


def segmenta_imagem(img, seg, img_name):

    import os
    from segment_ocrs import segment_ocropus, segment_kraken, segment_tesseract

    if seg == 1:
        dir_path = 'segments/' + img_name + '_ocropus/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        segment_ocropus(img, dir_path)
    elif seg == 2:
        dir_path = 'segments/' + img_name + '_kraken/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        segment_kraken(img, dir_path)
    elif seg == 3:
        dir_path = 'segments/' + img_name + '_tesseract/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        segment_tesseract(img, dir_path)

    return dir_path


def calcula_metricas(combined_text, text, img, method, ocrs):

    import os
    from isri_evaluation import char_acc_evaluation, word_acc_evaluation, editop_evaluation

    temp_out_filename = 'temp_output.txt'
    temp_annotation_filename = 'temp_annotation.txt'

    file = open(temp_out_filename, 'w')
    file.write(combined_text)
    file.close()

    file = open(temp_annotation_filename, 'w')
    file.write(text)
    file.close()

    char_acc = char_acc_evaluation(temp_out_filename, temp_annotation_filename, img, method + '_' + '_'.join(ocrs))
    word_acc = word_acc_evaluation(temp_out_filename, temp_annotation_filename, img, method + '_' + '_'.join(ocrs))
    inserts, delets, subs = editop_evaluation(temp_out_filename, temp_annotation_filename, img, method + '_' + '_'.join(ocrs))

    metrics = [method, char_acc, word_acc, inserts, delets, subs]

    os.remove(temp_out_filename)
    os.remove(temp_annotation_filename)

    return metrics


def combina_textos(text_data, combs, img_name, mode):

    from combinations.aligned_majority import aligned_majority_voting
    from combinations.aligned_rank import aligned_ranking
    from statistics import mean
    from Levenshtein import median

    texts = [row[1] for row in text_data]
    confidences = [row[2] for row in text_data]
    clearEmpties(texts, confidences)

    combined_texts = []

    for comb in combs:
        if comb == 'align_maj_vote':

            maj_out = aligned_majority_voting(texts)
            combined_texts.append(['align_maj_vote', maj_out])
            escreve_saida_txt(maj_out, comb, img_name, mode)

        elif comb == 'align_rank':

            rank_out = aligned_ranking(texts, confidences)
            combined_texts.append(['align_rank', rank_out])
            escreve_saida_txt(rank_out, comb, img_name, mode)

        elif comb == 'median_string':

            median_out = median(texts)
            combined_texts.append(['median_string', median_out])
            escreve_saida_txt(median_out, comb, img_name, mode)

        elif comb == 'wei_median_string':

            word_confidences = []
            for i in confidences:
                word_confidences.append(mean(i))
            wei_median_out = median(texts, word_confidences)
            combined_texts.append(['wei_median_string', wei_median_out])
            escreve_saida_txt(wei_median_out, comb, img_name, mode)

    return combined_texts
        
        
def identifica_texto(img, ocrs, mode):

    from run_ocrs import run_kraken, run_ocropus, run_calamari, run_tesseract

    text_data = []

    for ocr in ocrs:
        if ocr == 'kraken':
            text_data.append(run_kraken(img, mode))
        elif ocr == 'calamari':
            text_data.append(run_calamari(img, mode))
        elif ocr == 'ocropus':
            text_data.append(run_ocropus(img, mode))
        elif ocr[:14] == 'tesseract3-psm':
            psm = ocr[14:]
            text_data.append(run_tesseract(img, 'legacy', psm, mode))
        elif ocr[:14] == 'tesseract4-psm':
            psm = ocr[14:]
            text_data.append(run_tesseract(img, '4.1', psm, mode))
        elif ocr[:14] == 'tesseract5-psm':
            psm = ocr[14:]            
            text_data.append(run_tesseract(img, '5.0', psm, mode))

    return text_data


def escreve_saida_txt(text, comb_name, img_name, mode = 'w'):

    import os

    dir_path = 'outputs/' + comb_name + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    output_file_name = dir_path + img_name + '.txt'
    output_file = open(output_file_name, mode)
    output_file.write(text + '\n')
    output_file.close()


def main():
    
    # seg_img = 'test_seg.png'
    # test_seg_annotation = 'Receipt No: 1670327566'
    
    # full_img = 'test.png'
    # test_annotation = 'This is a lot of 12 point text to test the\nocr code and see if it works on all types\nof file format.\nThe quick brown dog jumped over the\nlazy fox. The quick brown dog jumped\nover the lazy fox. The quick brown dog\njumped over the lazy fox. The quick\nbrown dog jumped over the lazy fox.\n'

    full_img = 'sample.jpg'
    annotations_file = 'annotations_sample.txt'
    with open(annotations_file) as f:
        lines = f.readlines()
    test_annotation = ''.join(lines)

    ocrs = ['tesseract4-psm10', 'tesseract5-psm10', 'calamari']
    comb = ['align_rank', 'median_string', 'wei_median_string']

    out = combine_ocrs(img=full_img, ocrs=ocrs, comb=comb, seg=1, text=test_annotation, metrics = True)

    for comb in out:
        print('Combinação:\t\t\t' + str(comb[0]))
        print('Acurácia de caractere:\t\t' + str(comb[2]))
        print('Acurácia de palavra:\t\t' + str(comb[3]))
        print('Número de inserções:\t\t' + str(comb[4]))
        print('Número de remoções:\t\t' + str(comb[5]))
        print('Número de substituições:\t' + str(comb[6]))


if __name__ == "__main__":
    main()
