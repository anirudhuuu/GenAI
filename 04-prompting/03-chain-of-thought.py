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
    Output: {{ "step": "analyse", "content": "Alright! The user is interested in maths query and user is asking a basic arithmetic operation."  }}
    Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands."  }}
    Output: {{ "step": "output", "content": "4"  }}
    Output: {{ "step": "validate", "content": "Seems like 4 is correct answer for 2 + 2"  }}
    Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}
"""

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is 5 / 2 * 3 to the power of 4?"},

        # Chain of Thought Starts Here
        {"role": "assistant", "content": json.dumps(
            {
                "step": "analyse",
                "content": "Okay, the user wants me to evaluate an expression. The expression involves division, multiplication and exponentiation. I need to remember the order of operations (PEMDAS/BODMAS) to get this right. Exponentiation first, then division and multiplication from left to right."
            }
        )},
        {"role": "assistant", "content": json.dumps(
            {
                "step": "think",
                "content": "Alright, Let me evaluate this expression step by step.\n1. Evaluate the exponent: 3 to the power of 4 which is 3 * 3 * 3 * 3 = 81.\n2. Now the expression looks like this: 5 / 2 * 81.\n3. Perform division: 5 / 2 = 2.5.\n4. Now the expression looks like this: 2.5 * 81.\n5. Perform multiplication: 2.5 * 81 = 202.5."
            }
        )},
        {"role": "assistant", "content": json.dumps(
            {
                "step": "output",
                "content": "202.5"
            }
        )},
        {"role": "assistant", "content": json.dumps(
            {
                "step": "validate",
                "content": "The order of operations was correctly applied. Exponentiation, then division and multiplication from left to right. The calculations at each step are also correct. The final answer seems accurate."
            }
        )},
        # Chain of Thought Ends Here
    ]
)

"""
{
 "step": "result",
 "content": "5 / 2 * 3 to the power of 4 is equal to 202.5. This is calculated by applying the order of operations: exponentiation, division, and multiplication."
}
"""

print("\n\n🤖:", response.choices[0].message.content, "\n\n")
