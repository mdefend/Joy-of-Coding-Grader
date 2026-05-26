# Joy-of-Coding-Grader
## Setup Guide
### Files 
----
In order to run the grader (regardless of php or python, you will need the following)
1. a .env (or php equivalent)
    *  should only consist of this line: ```ANTHROPIC_API_KEY={Your Key Here}```
2. config folder with files 
    * **important!!** This is how the json is currently setup  ```json{
  "context": ["","",],
  "questions": [
    {
      "number": 1,
      "question": "insert question here",
      "examples": {
        "passing": {
          "user": "student answer",
          "response": {
            "pass": true,
            "percentage": 80,
            "feedback": "this is our claude response"
          }
        },
        "failing": {
          "user": "I didn't struggle with anything this week.",
          "response": {
            "pass": false,
            "percentage": 15,
            "feedback": "this is our failing claude response."
          }
        }
      }
    },],
    }```
    * Up to you how to sort them, but mine are setup with folders for camp name, followed by jsons named by their assignment number
        * ex: config/intro_coding/assignment_1.json

    
    
