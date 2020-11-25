def googleJSONtoCharConf(file_path):

    import json

    characters = []
    google_confidences = []

    with open(file_path) as file:
        data = json.load(file)
        if('fullTextAnnotation' in data):
            for page in data['fullTextAnnotation']['pages']:
                for block in page['blocks']:
                    for paragraph in block['paragraphs']:
                        for word in paragraph['words']:
                            for char in word['symbols']:
                                characters.append(char['text'])
                                if('confidence' in char):
                                    google_confidences.append(char['confidence'])
                                else: 
                                    google_confidences.append(1)
                                if('property' in char):
                                    if('detectedBreak' in char['property']):
                                        if(char['property']['detectedBreak']['type'] == 'SPACE'):
                                            characters.append(' ')
                                            if('confidence' in char):
                                                google_confidences.append(char['confidence'])
                                            else: 
                                                google_confidences.append(1)
    
    google_characters = ''.join(characters)

    return google_characters, google_confidences


def tesseractHOCRtoCharConf(file_path, ocr):
    
    import xml.etree.ElementTree as ET

    characters = []
    tess_confidences = []
    tess_characters = []

    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for root_tag in root:
        if(root_tag.tag.split('}')[1] == 'body'):
            body = root_tag
            for page in body:
                for area in page:
                    for paragraph in area:
                        for line in paragraph:
                            for word in line:
                                for char in word:
                                    characters.append(char.text)
                                    confidence = float(char.attrib['title'].split(';')[1].split('conf')[1].strip()) / 100
                                    tess_confidences.append(confidence)
                                characters.append(' ')
                                confidence = float(word.attrib['title'].split(';')[1].split('conf')[1].strip()) / 100
                                tess_confidences.append(confidence)

    tess_characters = ''.join(characters)

    return ocr, tess_characters, tess_confidences


def tesseractLegacyHOCRtoCharConf(file_path, ocr):
    
    import xml.etree.ElementTree as ET

    characters = []
    tess_confidences = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    for root_tag in root:
        if(root_tag.tag.split('}')[1] == 'body'):
            body = root_tag
            for page in body:
                for area in page:
                    for paragraph in area:
                        for line in paragraph:
                            for word in line:
                                for strong in word:
                                    if(strong.text is None):
                                        for oem in strong:
                                            if(oem.text.strip() == ''):
                                                for char in oem:
                                                    characters.append(char.text)
                                                    char_confidence = float(char.attrib['title'].split(';')[1].split('conf')[1].strip()) / 100
                                                    tess_confidences.append(char_confidence)
                                    else:
                                        if(strong.text.strip() == ''):
                                            for char in strong:
                                                characters.append(char.text)
                                                char_confidence = float(char.attrib['title'].split(';')[1].split('conf')[1].strip()) / 100
                                                tess_confidences.append(char_confidence)
                                        else:
                                            char = strong
                                            characters.append(char.text)
                                            char_confidence = float(char.attrib['title'].split(';')[1].split('conf')[1].strip()) / 100
                                            tess_confidences.append(char_confidence)

                                characters.append(' ')

    tess_characters = ''.join(characters)

    return ocr, tess_characters, tess_confidences


def krakenHOCRtoCharConf(file_path):

    import xml.etree.ElementTree as ET

    characters = []
    kraken_confidences = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    for root_tag in root:
        if(root_tag.tag == 'body'):
            body = root_tag
            for page in body:
                for line in page:
                    for word in line:
                        confidences_str = word.attrib['title'].split(';')[1].split('confs ')[1].split(' ')
                        for i in range(0, len(confidences_str)):
                            characters.append(word.text[i])
                            kraken_confidences.append(float(confidences_str[i]))
    
    kraken_characters = ''.join(characters)

    return 'kraken', kraken_characters, kraken_confidences


def ocropusPROBtoCharConf(file_path):

    probability_file = file_path

    characters = []
    ocropus_confidences = []

    data = open(probability_file, 'r')
    for row in data:
        characters.append(row.split('\t')[0])
        ocropus_confidences.append(float(row.split('\t')[1].rstrip()))

    ocropus_characters = ''.join(characters)

    return 'ocropus', ocropus_characters, ocropus_confidences


def calamariJSONtoCharConf(file_path):

    import json

    characters = []
    calamari_confidences = []

    with open(file_path) as file:
        data = json.load(file)
        if('predictions' in data):
            for prediction in data['predictions']:
                if(prediction['id'] == 'fold_0'):
                    for position in prediction['positions']:
                        characters.append(position['chars'][0]['char'])
                        calamari_confidences.append(position['chars'][0]['probability'])

    calamari_characters = ''.join(characters)

    return 'calamari', calamari_characters, calamari_confidences

