import ollama
import colorama
import re

chat_history = []

def extract_think_sections(text: str):
    match = re.split(r"</think>\s*", text, maxsplit=1, flags=re.DOTALL)

    if len(match) == 2:
        think_content = match[0].split("<think>", 1)[-1].strip()
        after_think = match[1].strip()
        return think_content, after_think
    else:
        return None, text.strip()  # If no <think> tags are found, return the full text as "after_think"


def chat_prompt(message):
    global chat_history

    # Add the new prompt to the history
    chat_history.append({
        'role': 'user',
        'content': message
    })

    response = ollama.chat(
        model="deepseek-r1:14b",
        messages=chat_history,
    )

    chat_history.append({
        'role': response['message']['role'],
        'content': response['message']['content']
    })

    return response['message']['content']

while True:
    user_input = input('You: ')
    ia_response = chat_prompt(user_input)
    thinking, text_response = extract_think_sections(ia_response)
    print(colorama.Fore.CYAN + "IA: ")
    print(colorama.Style.DIM + thinking)
    print(colorama.Style.NORMAL + text_response + colorama.Style.RESET_ALL)