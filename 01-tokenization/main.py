import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I am Anirudh"
tokens = encoder.encode(text)

print("Token: ", tokens)

tokens = [13225, 11, 357, 939, 1689, 380, 115904]
decoded = encoder.decode(tokens)

print("Decoded Text: ", decoded)
