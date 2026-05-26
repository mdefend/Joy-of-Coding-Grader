import json
import base64
import re
from dotenv import load_dotenv
import anthropic
load_dotenv() 
client = anthropic.Anthropic( # defaults to os.environ.get("ANTHROPIC_API_KEY") which is what we use  
)

""""Grader Class and functions"""
"""Prompts"""
PDF_PROMPT = """You are a scanner that converts PDF info to text for a teacher trying to grade student answers. 
            The PDF should be formatted with the question first, followed by the student's answer. 
            Please extract the question number and the student's answer for each question in a JSON. 
            The question numbers should have the key \"numbers\" and the student answers should have the key answer \"answers\". 
            If an answer is blank or not found, please put <BLANK> in the json. Do not grade the answers, just retrieve them. """
GRADER_PROMPT = """You are a tutor for an introductory Python coding course for middle and high schoolers. 
                    Your task is to grade the student's response to the question below. ]
                    Your grade should be formatted in JSON with 3 keys: a “pass” key that is true or false, 
                    whether the response passes or fails, a "percentage" key that is the percentage score it earned, and a “feedback” key that is feedback you’ve provided. 
                    The percentage score should be based on whether the student fully answers the question, 
                    how much detail they provide, and if the response makes sense both structurally and with the question and context below. 
                    A response should be considered “passing” if the percentage is over 55%. 
                    Your feedback needs to always be positive, warm, friendly, formative, and proportional to the percentage. 
                    In the feedback, encourage the student to write more through follow-up questions, or have them review the codex. 
                    Encourage a student to contact a coach through email or to schedule a call only if they are confused, still struggling, or if their response scored below 60%."""

class Grader:

    def __init__(self):
           """intialize grader"""
           self.context = None
           self.questions_examples = None
           self.config_path = "config"

    def api_call(self, prompt,typecon):
        """Handles Claude API call, Prompt = Prompt, Typecon, -> type of input and input"""
        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=20000,
            system = prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                   typecon
                    ]
                }
            ],
            thinking={
                "type": "adaptive"
            }
            )
        return message.content[0].text

    def grade_pdf(self, pdf_path: str):
        """Does all of the main grading work."""
        student_resp = self.extract_pdf_data(pdf_path)
        prompt = self.build_prompt(student_resp['answers'])
        claude_resp = self.api_call(GRADER_PROMPT, {"type": "text", "text": prompt})
        print(claude_resp)
    def extract_pdf_data(self,pdf_path):
        """extracts pdf info and loads config."""
        self.config_path = self.config_path + "/intro_coding/assignment_1.json"
        """temporary auto load"""
        pdf_base64 = None
        with open(self.config_path) as f:
            assignment = json.load(f)
            self.questions_examples = assignment['questions']
            self.context = assignment['context'] 
        with open(pdf_path,"rb") as pdf:
              pdf_data = pdf.read()
              pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
              content = {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_base64
                        }
                    }
              api_resp = self.api_call(PDF_PROMPT,content)
              return self.parse_grading_response(api_resp)
        
    def parse_grading_response(self, raw: str) -> dict:
        """Cleans up api response, in case claude has weird formatting."""
        try:
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError(f"Could not parse grading response: {raw}") #TO DO: Fix this! 

    def format_examples(self, question: dict) -> str:
        passing = question["examples"]["passing"]
        failing = question["examples"]["failing"]
    
        return f"""Passing Example:
        User: {passing["user"]}
        Response: {json.dumps(passing["response"])}

        Failing Example:
        User: {failing["user"]}
        Response: {json.dumps(failing["response"])}"""
    def build_prompt(self, answers: dict) -> str:
        context_str = ", ".join(self.context)
    
        questions_str = ""
        for q in self.questions_examples:
            questions_str += f"""
    ---
    Question {q["number"]}: {q["question"]}

    {self.format_examples(q)}

    Student Answer: {answers[int(q['number']) - 1]}
    """

        return f"""Context: {{{context_str}}}

    Grade each of the following student answers using the examples as a guide.

    {questions_str}

    ---
    Return a single JSON object with this structure:
    {{
    "question_1": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_2": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_3": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_4": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_5": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_6": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_7": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}},
    "question_8": {{"pass": true/false, "percentage": 0-100, "feedback": "..."}}
     }}"""
