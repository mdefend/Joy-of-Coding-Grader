from dotenv import load_dotenv
import anthropic
load_dotenv() 
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY") which is what I'm currently doing

)

# Replace placeholders like {{question}} with real values,
# because the SDK does not support variables.
question = " "
content = " "
message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=20000,
    system="""You are a tutor for an introductory Python coding course for middle and high schoolers. Your task is to grade the student's response to the question below. 
    Your grade should be formatted in JSON with 3 categories: whether the response passes or fails, the percentage score it earned, and the feedback you’ve provided. 
    The percentage score should be based on whether the student fully answers the question, how much detail they provide, and if the response makes sense both structurally and with the question and context below. 
    A response should be considered “passing” if the percentage is over 50%. Your feedback needs to always be positive, warm, friendly,  and formative. 
    If a response seems to lack detail, isn’t passing, or is blank, encourage the student to write more.\nQuestion: """ + question + """ \nContext:""" +  context + """\n""",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Syntactical rules (e.g., colons, indentation)\nGraphing parametric curves\nControl flow \n"
                }
            ]
        }
    ],
    thinking={
        "type": "adaptive"
    }
)
print(message.content)