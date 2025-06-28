import os
import json
from openai import OpenAI

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Chain of Thought: The model is encouraged to break down reasoning step by step before arriving at an answer.

SYSTEM_PROMPT = """
    You are an helpful AI assistant who is specialized in resolving user query.
    For the given input, analyse the input and break down the problem step by step.

    The steps are: you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation.

    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query.

    Output Format:
    {{ "step": "string", "content": "string" }}

    Example:
    Input: What is 2 + 2?
    Output: {{ "step": "analyse", "content": "Alright! The user is interested in maths query and user is asking a basic arithmetic operation." }}
    Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }}
    Output: {{ "step": "output", "content": "4" }}
    Output: {{ "step": "validate", "content": "Seems like 4 is correct answer for 2 + 2" }}
    Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}

    Example:
    Input: What is 2 + 2 * 5 / 3
    Output: {{ "step": "analyse", "content": "Alright! The user is interested in maths query and user is asking a basic arithmetic operations." }}
    Output: {{ "step": "think", "content": "To perform this addition, I must use BODMAS rule." }}
    Output: {{ "step": "validate", "content": "Correct! Using BODMAS is the right approach here." }}
    Output: {{ "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.6666666666666667" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS the divison must be performed" }}
    Output: {{ "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks like 2 + 2 * 1.6666666666666667" }}
    Output: {{ "step": "validate", "content": "Yes, The new equation is absolutely correct" }}
    Output: {{ "step": "think", "content": "The equation now is 3.3333333333" }}
    and so on...
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

query = input("> ")

messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        response_format={"type": "json_object"},
        messages=messages
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    parsed_response = json.loads(response.choices[0].message.content)

    if parsed_response.get("step") != "result":
        print("\t\t🧠:", parsed_response.get("content"), "\n")
        continue

    print("\n\n🤖:", parsed_response.get("content"), "\n\n")
    break

"""
> what is the average of sum of 2 and 3 multiplied by 5 divided by 2

🧠: The user wants to calculate the average of a series of arithmetic operations: adding 2 and 3, multiplying the sum by 5, and then dividing the result by 2. 

🧠: To solve this, I need to follow the order of operations (PEMDAS/BODMAS). First, I'll calculate the sum of 2 and 3. Then, I'll multiply the sum by 5. Finally, I'll divide the result by 2. Since the user asks for the average of the result, and only one number will be left, I will return the result itself. 

🧠: 12.5 

🧠: Let's verify the calculations: 2 + 3 = 5. 5 * 5 = 25. 25 / 2 = 12.5. The result seems correct. 

🤖: The average of the sum of 2 and 3 multiplied by 5, then divided by 2 is 12.5. This is calculated as follows: (2 + 3) * 5 / 2 = 12.5
"""

# Improved system prompt with chain of thought

"""
> 2 * 5 / 3 + 4
    🧠: The user wants me to evaluate the expression 2 * 5 / 3 + 4. This involves multiplication, division, and addition. I need to follow the order of operations (PEMDAS/BODMAS). 
    🧠: According to the order of operations, multiplication and division have the same precedence, so I'll perform them from left to right. Then I'll do the addition. 
    🧠: First, calculate 2 * 5 which equals 10. Then, calculate 10 / 3 which equals 3.3333333333333335. Finally, calculate 3.3333333333333335 + 4 which equals 7.333333333333333. 
    🧠: The steps are correct and the final result is accurate. Multiplication and division were performed from left to right before addition.

🤖: 2 * 5 / 3 + 4 = 7.333333333333333. This is calculated by first multiplying 2 by 5, then dividing the result by 3, and finally adding 4.
"""
