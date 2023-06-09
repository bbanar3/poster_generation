from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A2
import pandas as pd
from textwrap3 import wrap
import os
from tqdm import tqdm

# ********************** Parameters to check *************************

expected_number_of_posters = 32

csv_file = 'AIM Summer School - Posters Session Information.csv' # csv file name, assuming that it's in the same folder

visuals_folder = './Visuals/'

generated_posters_folder = './Posters/'

test_mode_student_index = 15

# *******************************************************************

df = pd.read_csv(csv_file)

csv_column_names = df.columns # Has the questions as the labels, the following indices hard coded

student_names = df[csv_column_names[1]]
supervisor_names = df[csv_column_names[2]]
cohorts = df[csv_column_names[3]]
project_titles = df[csv_column_names[4]]
answered_questions = df[csv_column_names[6]]
unanswered_questions = df[csv_column_names[7]]
papers = df[csv_column_names[8]]

def visual_find_person(student_name, visuals_path): # TO DO, not suitable for every case, double check, name surname etc., once match student names to file names, here bulky

    file_names = os.listdir(visuals_path)
    print(student_name)
    matched_index = [index for index, file_name in enumerate(file_names) if student_name in file_name and file_name[-4:] != '.pdf'] # more than 1?, TO DO automatic pdf to png converter
    return file_names[matched_index[0]]

def text_wrapper(canvas, text, wrapper_width = 80, text_origin = (200, 1200), font_type = 'Helvetica', font_size = 30):
    text_object = canvas.beginText()
    text_object.setTextOrigin(text_origin[0], text_origin[1])
    text_object.setFont(font_type, font_size)
    wraped_text = "\n".join(wrap(text, wrapper_width))
    text_object.textLines(wraped_text)
    canvas.drawText(text_object)

assert len(student_names) == expected_number_of_posters, "Expected number of students doesn't match the csv file."

for student_index in tqdm(range(expected_number_of_posters)):

    canvas = Canvas(generated_posters_folder + student_names[student_index] + "_Poster.pdf", pagesize=A2)

    canvas.setFont("Helvetica", 30)
    canvas.drawString(500, 1500, student_names[student_index])
    canvas.drawString(200, 1400, supervisor_names[student_index])

    image_file_name = visual_find_person(student_names[student_index], visuals_folder)

    canvas.drawInlineImage(visuals_folder + image_file_name, 300, -700, width=500, preserveAspectRatio=True)

    text_wrapper(canvas, project_titles[student_index], 60, (200, 1200), 'Helvetica', 30)
    text_wrapper(canvas, answered_questions[student_index], 60, (200, 1000), 'Helvetica', 30)
    text_wrapper(canvas, unanswered_questions[student_index], 60, (200, 700), 'Helvetica', 30)

    canvas.save()


