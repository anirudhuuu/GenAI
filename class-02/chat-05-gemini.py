import json
import os
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "ooutput", "validate", and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next intput
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2
Output: {{ step: "analyse", content: "Alright! The user is interested in maths query and he is asking a basic arthematic oepration" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct answer for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

result = client.chat.completions.create(
    model='gemini-2.0-flash',
    response_format={"type": "json_object"},
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'what is 3 + 4 * 5'},

        # Manual addition of the assistant response
        { "role": "assistant", "content": json.dumps({ "step": "analyse", "content": "The user has provided an expression that requires order of operations to solve correctly. The expression contains both addition and multiplication." }) },
        { "role": "assistant", "content": json.dumps({ "step": "think", "content": "To solve this, I need to remember the order of operations (PEMDAS/BODMAS): Parentheses/Brackets, Exponents/Orders, Multiplication and Division (from left to right), and Addition and Subtraction (from left to right). In this case, multiplication should be performed before addition." }) },
        { "role": "assistant", "content": json.dumps({ "step": "output", "content": "23" }) },
        { "role": "assistant", "content": json.dumps({ "step": "validate", "content": "Let's check the calculation. 4 * 5 = 20, and then 3 + 20 = 23. So the answer is correct." }) }
    ]
)

print(result.choices[0].message.content)

# {
#   "step": "result",
#   "content": "Following the order of operations, 3 + 4 * 5 = 3 + (4 * 5) = 3 + 20 = 23"
# }
