from utils.chatbot import get_answer

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    print("Bot:", get_answer(question))