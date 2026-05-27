"""Main"""""
from grader import Grader 

grading = Grader()
pdf_path = "examples/ee"
print(grading.grade_pdf(pdf_path))
