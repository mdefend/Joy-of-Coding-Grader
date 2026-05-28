"""Main"""""
from grader import Grader 

grading = Grader()
pdf_path = "examples/example_1.pdf"
graderoutput = grading.grade_pdf(pdf_path)
output_path = "results/results.json"
grading.handleoutput(graderoutput,output_path)
