# Using OpenAI's library
import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print('Vocab Size :\t', encoder.n_vocab) # 2,00,019 ~ 200k

text = "The cat sat on the mat"

# Tokenization
tokens = encoder.encode(text)

print("Text :\t\t", text)
print("Encoded :\t", tokens) # Tokens [976, 9059, 10139, 402, 290, 2450]

my_tokens = [976, 9059, 10139, 402, 290, 2450]

decoded = encoder.decode([976, 9059, 10139, 402, 290, 2450])
print("Decoded :\t", decoded)
