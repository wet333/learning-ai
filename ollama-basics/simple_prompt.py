import ollama

response = ollama.chat(
    model="deepseek-r1:14b",
    messages=[{
        'role': 'user',
        'content': 'What is the capital of Argentina?'
    }]
)

print(response['message']['content'])