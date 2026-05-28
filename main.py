"""Main"""""
from grader import Grader 

grading = Grader()
pdf_path = "examples/example_4.pdf"
graderoutput = grading.grade_pdf(pdf_path)
output_path = "results/"
student_id = "4"
grading.print_to_json(graderoutput,output_path,student_id)
