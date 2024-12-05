from InquirerPy import prompt

questions = [
    {"type": "input", "message": "What's your name:", "name": "name"},
    {
        "type": "list",
        "message": "What's your favourite programming language:",
        "choices": ["Go", "Python", "Rust", "JavaScript"],
        "name": "fav_lang",
    },
    {"type": "confirm", "message": "Confirm?"},
]
result = prompt(questions)
name = result["name"]
fav_lang = result["fav_lang"]
confirm = result[2]

print(name)
print(fav_lang)
print(confirm)