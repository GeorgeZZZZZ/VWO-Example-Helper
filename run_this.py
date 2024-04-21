import random

from pathlib import Path
from nicegui import app, ui
from configparser import ConfigParser
from write_config import write_conf, read_conf

current_subject = 0
current_include = []
subject_array_path = ['mathA','bio','chemi','phy']
selection_array_path = ['textbook','midterm','examples']
solution_list_path = ['textbook_solution','midterm_solution','examples_solution']
question_list = []
answer_list = []
working_question_number = []
at_previous_view = False
curr_ques_num = -1

def glob_folder(path):
    r_list = []
    folder = Path(__file__).parent / path
    files = sorted(f.name for f in folder.glob('*.jpg'))
    for f in files:
        r_list.append(path +'/'+ f)
    return r_list

def sort_path(subject, include):
    global subject_array_path
    global selection_array_path
    global question_list
    global answer_list
    question_list.clear()
    answer_list.clear()

    if include[0]:
        f_p = subject_array_path[subject] +'/'+ selection_array_path[0]
        question_list.extend(glob_folder(f_p))
        f_p = subject_array_path[subject] +'/'+ solution_list_path[0]
        answer_list.extend(glob_folder(f_p))
    if include[1]:
        f_p = subject_array_path[subject] +'/'+ selection_array_path[1]
        question_list.extend(glob_folder(f_p))
        f_p = subject_array_path[subject] +'/'+ solution_list_path[1]
        answer_list.extend(glob_folder(f_p))
    if include[2]:
        f_p = subject_array_path[subject] +'/'+ selection_array_path[2]
        question_list.extend(glob_folder(f_p))
        f_p = subject_array_path[subject] +'/'+ solution_list_path[2]
        answer_list.extend(glob_folder(f_p))

def true_next(next):
    global current_subject
    global current_include
    global working_question_number
    global question_list
    global curr_ques_num

    include_array = [0,0,0]
    include_array[0] = textbook.value
    include_array[1] = midterm.value
    include_array[2] = examples.value

    # if setting has been changed
    if next != current_subject or current_include != include_array:
        current_subject = next
        current_include = include_array
        sort_path(next, include_array)

    if len(question_list)<=0:
        return
    

    if random_pick.value == True:
        curr_ques_num = random.randrange(0,len(question_list))
    else:
        curr_ques_num = curr_ques_num + 1
        if curr_ques_num >= len(question_list): curr_ques_num = 0
        
    working_question_number.insert(0,curr_ques_num)
    if len(working_question_number) > 2:
        working_question_number.pop()

def click_previous(next):
    global working_question_number
    global at_previous_view
    global answer_list
    global curr_ques_num
    if len(working_question_number)>1:
        questimg.set_source(question_list[working_question_number[1]])    #render answer image
        at_previous_view = True

    if len(answer_list)>0:
        key_img.set_source(answer_list[working_question_number[1]])    #render answer image

def click_next(next):
    global working_question_number
    global at_previous_view
    if at_previous_view == False:
        true_next(next)
    else:
        at_previous_view = False

    questimg.set_source('')    #clean images first
    key_img.set_source('') 

    if len(working_question_number)>0:
        questimg.set_source(question_list[working_question_number[0]])    #render question image

def click_answer():
    global answer_list
    global curr_ques_num
    if len(answer_list)>0 and at_previous_view == False:
        key_img.set_source(answer_list[working_question_number[0]])    #render answer image


#read or create config
setting_list = read_conf()

if setting_list == -1: #there is no config file
    write_conf(0,True,True,True,True)
    setting_list = read_conf()

with ui.row():
    select = ui.select({0: 'MathA', 1: 'Bio', 2: 'Chemi', 3:'Physic'})
    random_pick = ui.checkbox('random pick questions', value=True)
    textbook = ui.checkbox('text_book_questions', value=True)
    midterm = ui.checkbox('midterm_questions', value=True)
    examples = ui.checkbox('example_questions', value=True)
    ui.button('save setting', on_click=lambda: write_conf(select.value, random_pick.value, textbook.value, midterm.value, examples.value))

    select.value = int(setting_list[0])
    random_pick.value = bool(setting_list[1])
    textbook.value = bool(setting_list[2])
    midterm.value = bool(setting_list[3])
    examples.value = bool(setting_list[4])

with ui.button_group():
    ui.button('Previous Question', on_click=lambda: click_previous(select.value))
    ui.button('Next Question', on_click=lambda: click_next(select.value))
    ui.button('show answer', on_click=lambda: click_answer())
    

questimg = ui.image('').props('fit=scale-down').props('position=left')

ui.add_head_html('''
    <style type="text/tailwindcss">
        h2 {
            font-size: 160%;
        }
    </style>
''')
ui.html('<h2>Solution shows below-------------------------------------------------</h2>')


key_img = ui.image('').props('fit=scale-down').props('position=left')


ui.run()