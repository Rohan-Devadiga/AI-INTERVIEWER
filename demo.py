from main import greet_user, next_question, evaluate_ans, analyze_code
from tts import speak
from tststs import main




def run_interview():
    name = input("Enter your name: ")
    role = input("Enter the role you are applying for: ")
    fresher_input = input("Are you a fresher? (yes/no): ").strip().lower()
    is_fresher = fresher_input == "yes"

    greeting= greet_user(name)
    print("\n" + greeting + "\n")
    speak(greeting)

    history = []
    q_count = 0
    difficulty = "easy"
    last_eval = None   

    while True:
        question_data = next_question(
            name=name,
            role=role,
            history=history,
            q_count=q_count,
            lasteval=last_eval,
            difficulty=difficulty,
            is_fresher=is_fresher
        )

        if question_data["question_type"] == "end":
            print("\n" + question_data["question"])
            break
            

        question = question_data["question"]
        print(f"\nQ{q_count+1}: {question}")
        speak(question)

        
        if question_data["question_type"] == "technical":
            code = input("Please write your code:\n")
            history.append(
                {
                    "question":question,
                    "question_type":"technical",
                    "answer":code
                }
            )
        else:
            answer = main()
            history.append(
                {
                    "question":question,
                    "question_type":"general",
                    "answer":answer
                }
            )
       
        q_count += 1
        difficulty = question_data.get("difficulty", difficulty)


if __name__ == "__main__":
    run_interview()

