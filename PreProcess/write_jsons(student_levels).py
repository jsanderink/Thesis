import functions as fx

# Load the neccesary datasets
# student_x = fx.csv_to_df('student_2.csv')
students = fx.csv_to_df('export_students.csv')
users = fx.csv_to_df('export_users.csv')


text_to_number = {'LWOO': 1,  # Leerwegondersteunend onderwijs

                  'PO': 2,  # Primair onderwijs}
                  'VMBOB': 2,  # Basisberoepsgerichte leerweg
                  'VMBOK': 2,  # Kaderberoepsgerichte leerweg
                  'VMBOG': 2,  # Gemengde leerweg
                  'VMBO': 2,  # Koepel term
                  'VMBOT': 3,  # Theoretische leerweg
                  'VMBO_HAVO': 3,
                  'HAVO': 4,
                  'HAVO_VWO': 5,
                  'VWO': 6,
                  'ATHENEUM': 6,
                  'GYMNASIUM': 6}

spellings = {'LWOO': 'LWOO',
             'PO': 'PO',
             'VMBOB': 'VMBOB',
             'VMBO-B': 'VMBOB',
             'VMBOK': 'VMBOK',
             'VMBO-K': 'VMBOK',
             'VMBOG': 'VMBOG',
             'VMBO-GT': 'VMBOG',
             'VMBO-G': 'VMBOG',
             'VMBO': 'VMBO',
             'MAVO': 'VMBO',
             'VMBOT': 'VMBOT',
             'VMBO-T': 'VMBOT',
             'VMBO_HAVO': 'VMBO_HAVO',
             'HAVO': 'HAVO',
             'HAVO_VWO': 'HAVO_VWO',
             'HAVO / VWO': 'HAVO_VWO',
             'VWO': 'VWO',
             'ATHENEUM': 'ATHENEUM',
             'GYMNASIUM': 'GYMNASIUM',
             'Gymnasium': 'GYMNASIUM'}

#save those to that i can access them from other spots as well
fx.dict_to_json(text_to_number, 'text_to_number (levels)')
fx.dict_to_json(spellings, 'spellings of levels')

#initialize the dictionaries
id_to_text = {}
id_to_text_raw = {}
id_to_number = {}

#iteratively fill the dictionaries
for i in range(1800):

    # select student
    student_x = fx.csv_to_df('student_{}.csv'.format(i))

    if student_x.shape[0] > 0:

        # select student ID from this dataframe
        student_x_id = student_x['student_id'].iloc[0]

        # look in the user-dataset for the userable id (needed for the academic level)
        userable_id_student_x = users[users['id'] == student_x_id]['userable_id'].iloc[0]

        # define level in text and in number
        level_student_x_text_raw = students[students['id'] == userable_id_student_x]['academic_level'].iloc[0]

        level_student_x_text = spellings[level_student_x_text_raw]
        level_student_x_number = text_to_number[level_student_x_text]

        id_to_text[student_x_id] = level_student_x_text
        id_to_text_raw[student_x_id] = level_student_x_text_raw
        id_to_number[student_x_id] = level_student_x_number

        print('student {} level: {}     == {} ({})'.format(i, level_student_x_number, level_student_x_text,
                                                           level_student_x_text_raw))
    else:
        print('no data for this student')

#save the dictionaries
fx.dict_to_json(id_to_text, 'id_to_text')
fx.dict_to_json(id_to_text_raw, 'id_to_text_raw')
fx.dict_to_json(id_to_number, 'id_to_number')

print("Dictionaries are saved as jsons!")