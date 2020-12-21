def remove_empty_values(val_list):

    output_list = []
    
    for val in val_list:
        if(val != None):
            output_list.append(val)
    
    return output_list


def adjust_weigths_list(strings_list, weights_lists, degree_certain):
    
    for string, weight in zip(strings_list, weights_lists):
        for i in range(0, len(string)):
            if(string[i] == None):
                weight.insert(i, degree_certain)

    return weights_lists


def adjust_string_len(strings_list):
    
    sizes = []

    for string in strings_list:
        sizes.append(len(string))

    max_size = max(sizes)

    for string in strings_list:
        while(len(string) < max_size):
            string.append(None)

    return strings_list


def aligned_ranking(strings_lists, weights_lists):

    from combinations.mafft_align import align_text
    from collections import Counter
    import numpy as np

    output_string = ''
    aligned_strings = align_text(strings_lists)
    adjusted_strings = adjust_string_len(aligned_strings)
    aligned_weights = adjust_weigths_list(adjusted_strings, weights_lists, 0.5)

    choices_list = list(map(list, zip(*adjusted_strings)))
    choices_weights_list = list(map(list, zip(*aligned_weights)))

    for choice, weights in zip(choices_list, choices_weights_list):

        unique_values = list(set(choice))
        acc_weights = [0] * len(unique_values)
        
        index = 0
        for unique_value in unique_values:
            for char, w in zip(choice, weights):
                if(char == unique_value):
                    acc_weights[index] += w
            index += 1

        biggest_frequency = max(acc_weights)
        most_voted = []

        for unique_value, acc_weight in zip(unique_values, acc_weights):
            if(acc_weight == biggest_frequency):
                most_voted.append(unique_value)

        if(len(most_voted) > 1):
            most_voted = remove_empty_values(most_voted)
            if most_voted[0]:
                output_string += most_voted[0]
        else:
            if most_voted[0]:
                output_string += most_voted[0]


    return output_string


def main():

    a = 'NO.E\''
    aw = [0.9, 0.8, 0.9, 0.5, 0.3]
    b = '55, 8'
    bw = [0.3, 0.3, 0.8, 0.3, 0.4]
    c = 'NO.5%'
    cw = [0.9, 0.9, 0.9, 0.5, 0.6]
    d = 'NO.5:'
    dw = [0.9, 0.8, 0.9, 0.5, 0.7]
    
    strs_list = [a, b, c, d]
    weights_list = [aw, bw, cw, dw]

    txt = aligned_ranking(strs_list, weights_list)
    print(txt)


if __name__ == "__main__":
    main()