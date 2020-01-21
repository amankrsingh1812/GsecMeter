import xlrd
import sys
import pickle
import os
import json

# To genarate all the dictionaries
def create_dic(sheet_index):
    workbook = xlrd.open_workbook(sys.argv[1])

    sheet = workbook.sheet_by_index(sheet_index)
    # intermediate_dict contains ->  { agenda: {category: ---, description: ---, status: ---, current_status: ---, representative_comment: ---, verifier_comment: ---}, ...}
    intermediate_dict = {}

    for row_num in range(1, sheet.nrows):
        row = sheet.row_values(row_num)
        temp = {}
        temp['category'] = row[2]
        temp['description'] = row[3]
        temp['status'] = row[4]
        temp['current_status'] = row[5]
        temp['representative_comment'] = row[6]
        temp['verifier_comment'] = row[7]

        intermediate_dict[row[1]] = temp

    # candidate_dict contains -> { status: { agenda: { category: ---, description: ---, current_status: ---,
    #                                           representative_comment: ---, verifier_comment: ---
    #                                          },
    #                             ...},
    #                     ...}
    candidate_dict = {}

    for key, value_dict in intermediate_dict.items():
        status = value_dict['status']

        # temp -> { category: ---, description: ---, current_status: ---, representative_comment: ---, verifier_comment: ---}
        temp = {}

        temp['category'] = value_dict['category']
        temp['description'] = value_dict['description']
        temp['current_status'] = value_dict['current_status']
        temp['representative_comment'] = value_dict['representative_comment']
        temp['verifier_comment'] = value_dict['verifier_comment']

        if status in candidate_dict.keys():
            candidate_dict[status][key] = temp
        else:
            candidate_dict[status] = {key: temp}

    return candidate_dict


def create_info_dict():
    workbook = xlrd.open_workbook(sys.argv[2])

    sheet = workbook.sheet_by_index(0)
    candidate_dict = {}

    for row_num in range(1, sheet.nrows):
        row = sheet.row_values(row_num)
        temp = {}
        temp['name'] = row[0]
        post = row[1]
        temp['description'] = row[2]
        temp['image'] = row[3]
        temp['youtube_url'] = row[4]
        temp['agenda_pdf'] = row[5]
        temp['extra_pdf'] = row[6]

        candidate_dict[post] = temp
    return candidate_dict



# To print all the dictionaries generated :
def print_dictionary(dict):
    print("___________________________________________________________________________________________________")
    for key, value_dict in dict.items():
        print(key)
        print(value_dict)
        print()
    print()
    print()


# To save the dictionary into file
def save_dic_pkl(dict_name, fname):
    dict_dir ='dict_dir'
    try:
        os.makedirs(dict_dir)
    except:
        pass
    fname_out = os.path.join(dict_dir,fname+'.pkl')
    fout = open(fname_out,'wb')
    pickle.dump(dict_name,fout)
    fout.close()

# To save the dictionary into file
def save_dic_json(dict_name, fname):
    dict_dir ='dict_dir'
    try:
        os.makedirs(dict_dir)
    except:
        pass
    fname_out = os.path.join(dict_dir,fname+'.json')
    fout = open(fname_out,'w')
    json.dump(dict_name,fout, indent=2)
    fout.close()





# Main function
def main():

    # To create dictionaries of all the candidates
    gensec_list = [ 'vp' , 'sports', 'hab', 'cultural', 'welfare', 'technical']

    for i,gs in enumerate(gensec_list):
        temp_init_dic = create_dic(i)
        print(temp_init_dic)
        save_dic_pkl(temp_init_dic,gs)
        save_dic_json(temp_init_dic,gs)
    candidate_dict = create_info_dict()
    fname = 'candidate_info'
    save_dic_pkl(candidate_dict,fname)
    save_dic_json(candidate_dict,fname)


if __name__ =='__main__':
    main()

