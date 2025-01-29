import os

import ollama
import colorama
import re

chat_history = []

def extract_code_blocks(markdown: str):
    pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
    matches = pattern.findall(markdown)
    return [code for _, code in matches]

def extract_think_sections(text: str):
    match = re.split(r"</think>\s*", text, maxsplit=1, flags=re.DOTALL)

    if len(match) == 2:
        think_content = match[0].split("<think>", 1)[-1].strip()
        after_think = match[1].strip()
        return think_content, after_think
    else:
        return None, text.strip()  # If no <think> tags are found, return the full text as "after_think"


def extract_between_markers(text):
    start_marker = "<<<"
    end_marker = ">>>"

    try:
        start_index = text.index(start_marker) + len(start_marker)
        end_index = text.index(end_marker, start_index)
        return text[start_index:end_index]
    except ValueError:
        return None

def generate_filename(code_block):

    task_description = ("Give me a filename including extension, that best represents the following code snippet, "
                        "take into account the language used for the filename extension:\n")
    formatting = "Respond only with the filename and extension, and nothing more, use the following format: <<<filename.ext>>>\n"
    xtra_info = "I will use your response as a filename variable for crating a file, so it should be only the filename and extension string."

    final_prompt = task_description + "\n" + code_block + formatting + xtra_info

    response = ollama.chat(
        model="deepseek-r1:14b",
        messages=[{
            'role': 'user',
            'content': final_prompt,
        }]
    )
    return response['message']['content']


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

# MAIN LOOP
while True:
    user_input = input('You: ')
    ia_response = chat_prompt(user_input)
    thinking, text_response = extract_think_sections(ia_response)
    code_blocks = extract_code_blocks(text_response)

    # For each code block in the IA response, save that code into a file
    for code_block in code_blocks:
        # Generate the code_block filename using the IA
        ia_filename_res = generate_filename(code_block)
        thinking_filename, fn_response = extract_think_sections(ia_filename_res)
        filename = extract_between_markers(fn_response)

        # Save the code files in the results folder
        results_folder="results"
        os.makedirs(results_folder, exist_ok=True)
        file_path = os.path.join(results_folder, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code_block)

    # IA response
    print(colorama.Fore.CYAN + "IA: ")
    print(colorama.Style.DIM + thinking)
    print(colorama.Style.NORMAL + text_response + colorama.Style.RESET_ALL)