import os
import pandas as pd
from tqdm import tqdm
from textwrap3 import wrap
from reportlab.lib.pagesizes import A2
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image as PILImage
from pypdf import PdfMerger


name_to_visual_filename = {
    "Christian Steinmetz": "Screen Shot 2023-03-02 at 09.00.01 - Christian Steinmetz.png",
    "Corey Ford": "Screenshot 2023-06-02 at 10.00.09 - Corey Ford.png",
    "Jack Loth": "Screenshot 2023-06-02 at 10.52.31 - Jack Loth.png",
    "Ben Hayes": "main-diag - Ben Hayes.png",
    "Carey Bunks": "AIM_Summer_School_Carey_Bunks - Carey Bunks.png",
    "Chin-Yun Yu": "summer school poster concept - Chin-Yun Yu (Joey).png",
    "Xavier Riley": "Summer school poster - Xavier Riley.jpg",
    "Saurjya Sarkar": "BBCSO.drawio - Saurjya Sarkar.png",
    "Pedro Pereira Sarmento": "final_gfreq_guitar - Pedro Pereira Sarmento.png",
    "Yinghao Ma": "mert_architecture_v3 - Yinghao Ma.png",
    "David Südholt": "diagram - David Südholt.png",
    "Huan Zhang": "download (25) - Huan Zhang.jpeg",
    "Soumya Sai Vanka": "Music Mixing Technical and creative considerations Highly context-dependent - Soumya Sai Vanka.png",
    "Ruby Crocker": "Screenshot 2023-06-05 at 15.29.10 - ruby crocker.png",
    "Luca Marinelli": "Experimental pipeline ISMIR 2023 - Luca Marinelli.png",
    "Jordie Shier": "PhD Overview - Jordie Shier.png",
    "Andrew Edwards": "Screen Shot 2023-06-07 at 5.39.10 PM - Andrew Edwards.png",
    "Lele Liu": "Fig_24_1 - Lele Liu.png",
    "Andrea Martelloni": "Summer School.drawio - Andrea Martelloni.png",
    "Chris Winnard": "CW Visual - Chris Winnard.jpg",
    "Aditya Bhattacharjee": "SummerSchoolPoster - Aditya Bhattacharjee.jpg",
    "Ilaria Manco": "Research Overview copy - Ilaria Manco.jpg",
    "Kasia Adamska": "poster_visual - Kasia Adamska.jpg",
    "Franco Caspe": "image - Franco Caspe.jpg",
    "Tyler Howard McIntosh": "A-three-dimensional-timbre-space-found-from-a-CLASCAL-analysis-on-dissimilarity-data-from - Tyler Howard McIntosh.png",
    "Max Graf": "NetzMRScreenshot - Max Graf.png",
    "Xiaowan Yi": "framework-phase2 - Xiaowan Yi.png",
    "Yazhou Li": "ACC-1000Hz_0_0_headx_2 - Yazhou Li.png",
    "Jingjing Tang": "summer school - Jingjing Tang.png",
    "Jiawen Huang": "align_exp - Jiawen Huang.png",
    "Yin-Jyun Luo": "dsae-graph - Yin-Jyun Luo.png",
    "Oluremi Falowo ": "Oluremi Falowo.png",
    "Yannis Vasilakis": "Screenshot from 2023-06-09 15-48-17 - Yannis Vasilakis.png",
    "Alexander Williams": "traktor-dj-2 - Alex Williams.jpeg",
    "Elona Shatri": "Screenshot 2023-06-10 at 21.59.00 - Elona R. Shatri.png",
    "Eleanor Row": "pipeline - Eleanor Row.png",
    "Teresa Pelinski": "Screenshot 2023-06-11 at 10.49.40 - Teresa Pelinski.png",
    "Berker Banar": "Visual - Berker Banar.png"
}


def visual_find_person(
    student_name, visuals_path
):  # TO DO, not suitable for every case, double check, name surname etc., once match student names to file names, here bulky
    file_names = os.listdir(visuals_path)
    matched_index = [
        index
        for index, file_name in enumerate(file_names)
        if student_name in file_name and file_name[-4:] != ".pdf"
    ]  # more than 1?, TO DO automatic pdf to png converter
    return file_names[matched_index[0]]


def text_wrapper(
    canvas,
    text,
    wrapper_width=40,
    text_origin=(200, 1200),
    font_type="Helvetica",
    font_size=30,
    centered=False,
    page_width=None,
):
    text_lines = wrap(text, wrapper_width)
    max_line_width = max(
        [stringWidth(line, font_type, font_size) for line in text_lines]
    )
    wraped_text = "\n".join(text_lines)

    if centered:
        assert page_width is not None  # must supply page width if centered
        x = (page_width - max_line_width) / 2.0
        y = text_origin[1]
    else:
        x = text_origin[0]
        y = text_origin[1]

    text_object = canvas.beginText()
    text_object.setTextOrigin(x, y)
    text_object.setFont(font_type, font_size)
    text_object.textLines(wraped_text)
    canvas.drawText(text_object)


def new_text_wrapper(
    canvas,
    text,
    wrapper_width=40,
    text_origin=(200, 1200),
    font_type="Helvetica",
    font_size=30,
    centered=False,
):
    canvas.setFont(font_type, font_size)
    wraped_text = "\n".join(wrap(text, wrapper_width))
    print(wraped_text)
    canvas.drawCentredString(text_origin[0], text_origin[1], wraped_text)


def generate_poster(
    output_dir: str,
    student_name: str,
    cohort: str,
    supervisor_name: str,
    project_title: str,
    answered_question: str,
    unanswered_question: str,
    visual_path: str,
):
    filepath = output_dir + student_name + "_Poster.pdf"
    canvas = Canvas(filepath, pagesize=A2)
    page_width = A2[0]
    page_height = A2[1]

    # AIM Logo
    image_filepath = "Logos/AIM_logo.png"
    img = PILImage.open(image_filepath)
    width, height = img.size
    logo_height = 40
    factor = logo_height / height
    width *= factor
    height *= factor

    x = 125
    y = 1580

    canvas.drawImage(
        image_filepath,
        x,
        y,
        width=width,
        height=height,
        preserveAspectRatio=False,
    )

    # AIM title
    text_wrapper(
        canvas,
        "AIM Summer School 2023",
        40,
        (125 + 15 + width, 1590),
        "Helvetica",
        24,
        centered=False,
        page_width=page_width,
    )

    # precompute number of lines in title
    title_wrap_width = 40
    num_text_lines = len(wrap(project_title, title_wrap_width))

    # title
    text_wrapper(
        canvas,
        project_title,
        40,
        (100, 1500),
        "Helvetica-Bold",
        48,
        centered=True,
        page_width=page_width,
    )
    title_end = 1500 - (num_text_lines * 48)

    # student name
    text_wrapper(
        canvas,
        student_name,
        40,
        (100, title_end - 35),
        "Helvetica",
        32,
        centered=True,
        page_width=page_width,
    )

    # student cohort
    text_wrapper(
        canvas,
        cohort,
        40,
        (100, title_end - 70),
        "Helvetica",
        24,
        centered=True,
        page_width=page_width,
    )

    canvas.setFont("Helvetica", 30)

    # canvas.drawString(200, 1100, supervisor_name)

    image_filepath = os.path.join(visual_path, name_to_visual_filename[student_name])
    img = PILImage.open(image_filepath)
    width, height = img.size

    max_img_width = 750
    factor = max_img_width / width
    width1 = width * factor
    height1 = height * factor

    max_img_height = 500
    factor = max_img_height / height
    width2 = width * factor
    height2 = height * factor

    if height1 > max_img_height:  # use width2
        width = width2
        height = height2
    elif width2 > max_img_width:
        width = width1
        height = height1

    x = (page_width - width) / 2
    y = 1260 - height

    canvas.drawImage(
        image_filepath,
        x,
        y,
        width=width,
        height=height,
        preserveAspectRatio=False,
    )

    # precompute number of lines in answered question
    answered_question_wrap_width = 60
    num_text_lines = len(wrap(answered_question, answered_question_wrap_width))

    wrap_width = 65

    text_wrapper(
        canvas,
        "Finding",
        60,
        (175, y - 100),
        "Helvetica-Bold",
        36,
    )

    # answered question
    text_wrapper(
        canvas,
        answered_question,
        wrap_width,
        (175, y - 140),
        "Helvetica",
        28,
    )
    answered_question_end = y - 130 - (num_text_lines * 30)

    text_wrapper(
        canvas,
        "Question",
        60,
        (175, answered_question_end - 100),
        "Helvetica-Bold",
        36,
    )

    # unanswered question
    text_wrapper(
        canvas,
        unanswered_question,
        wrap_width,
        (175, answered_question_end - 140),
        "Helvetica",
        28,
    )

    text_wrapper(
        canvas,
        f"Supervisor(s): {supervisor_name}",
        300,
        (175, 65),
        "Helvetica",
        22,
    )

    canvas.save()


if __name__ == "__main__":
    # ********************** Parameters to check *************************

    expected_number_of_posters = 38
    csv_file = "AIM Summer School - Posters Session Information3.csv"  # csv file name, assuming that it's in the same folder
    visuals_folder = "./Visuals/"
    output_dir = "./Posters/"
    merge_pdfs = True

    # *******************************************************************

    df = pd.read_csv(csv_file)

    # Has the questions as the labels, the following indices hard coded

    student_names = df.iloc[:, 1]
    supervisor_names = df.iloc[:, 2]
    cohorts = df.iloc[:, 3]
    project_titles = df.iloc[:, 4]
    answered_questions = df.iloc[:, 6]
    unanswered_questions = df.iloc[:, 7]
    papers = df.iloc[:, 8]

    assert (
        len(student_names) == expected_number_of_posters
    ), "Expected number of students doesn't match the csv file."

    for student_index in tqdm(range(expected_number_of_posters)):
        generate_poster(
            output_dir,
            student_names[student_index],
            str(cohorts[student_index]),
            supervisor_names[student_index],
            project_titles[student_index],
            answered_questions[student_index],
            unanswered_questions[student_index],
            visuals_folder,
        )

    if merge_pdfs:
        pdf_merger = PdfMerger()
        for filename in os.listdir(output_dir):
            if filename.endswith(".pdf") and "All" not in filename:
                pdf_merger.append(os.path.join(output_dir, filename))
        pdf_merger.write(os.path.join("All_Posters.pdf"))
        pdf_merger.close()
