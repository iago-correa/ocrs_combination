def convert_string_list(string):

    output_list = []
    for char in string:
        output_list.append(char)

    return output_list


def remove_empty_values(val_list):

    output_list = []
    
    for val in val_list:
        if(val != None):
            output_list.append(val)
    
    return output_list


def adjust_string_len(strings_list):
    
    sizes = []

    for string in strings_list:
        sizes.append(len(string))

    try:
        max_size = max(sizes)
    except:
        return strings_list

    for string in strings_list:
        while(len(string) < max_size):
            string.append(None)

    return strings_list


def aligned_majority_voting(strings_lists):

    from combinations.mafft_align import align_text
    from collections import Counter

    output_string = ''
    aligned_strings = align_text(strings_lists)
    adjusted_strings = adjust_string_len(aligned_strings)

    choices_list = list(map(list, zip(*adjusted_strings)))

    for choice in choices_list:
        
        occurence_count = Counter(choice)
        
        bigger_occurence = occurence_count[occurence_count.most_common(1)[0][0]]
        most_commons = []
        for i in occurence_count:
            if(occurence_count[i] == bigger_occurence):
                most_commons.append(i)

        if(len(most_commons) > 1):
            most_commons = remove_empty_values(most_commons)
            if most_commons[0]:
                output_string += most_commons[0]
        else:
            if most_commons[0]:
                output_string += most_commons[0]

    return output_string


def main():

    a = 'IAA LACU'
    b = 'IAlAN ALU'
    c = 'WIAN S-ALU'
    d = 'JALAN SAG)'
    
    ss = [a,b,c,d]

    txt = aligned_majority_voting(ss)
    print(txt)

if __name__ == "__main__":
    main()