from main import greet_user, next_question, evaluate_ans, analyze_code
from tts import speak
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from tts import speak
from tststs import main

def generate_interview_report(filename: str, name: str, role: str, qa_data: list):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        alignment=1,
        fontSize=22,
        spaceAfter=20
    )
    story.append(Paragraph("AI INTERVIEWER REPORT", title_style))
    story.append(Spacer(1, 20))

    # Candidate Info
    story.append(Paragraph(f"<b>Candidate Name:</b> {name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Role:</b> {role}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Loop through all Q&A
    for i, qa in enumerate(qa_data, start=1):
        story.append(Paragraph(f"<b>Q{i}:</b> {qa['question']}", styles["Heading4"]))
        story.append(Spacer(1, 6))

        # Show candidate answer
        if qa["question_type"] == "technical":
            story.append(Paragraph("<b>Code Submitted:</b>", styles["Normal"]))
            story.append(Paragraph(f"<pre>{qa.get('answer','Not Provided')}</pre>", styles["Normal"]))
            evaluation = analyze_code(role, qa["question"], qa.get("answer", ""))
        else:
            story.append(Paragraph(f"<b>Answer:</b> {qa.get('answer','Not Provided')}", styles["Normal"]))
            evaluation = evaluate_ans(role, qa["question"], qa.get("answer", ""))

        story.append(Spacer(1, 6))

        # Show evaluation in table or paragraphs
        if qa["question_type"] == "technical":
            story.append(Paragraph("<b>Bugs & Mistakes:</b> " + evaluation.get("bugs", "N/A"), styles["Normal"]))
            story.append(Paragraph("<b>Optimizations:</b> " + evaluation.get("optimizations", "N/A"), styles["Normal"]))
            story.append(Paragraph("<b>Best Practices:</b> " + evaluation.get("best_practices", "N/A"), styles["Normal"]))
            story.append(Paragraph("<b>Improved Code:</b>", styles["Normal"]))
            story.append(Paragraph(f"<pre>{evaluation.get('improved_code','N/A')}</pre>", styles["Normal"]))
            story.append(Paragraph(f"<b>Score:</b> {evaluation.get('score','N/A')}/10", styles["Normal"]))
            story.append(Paragraph(f"<b>Feedback:</b> {evaluation.get('feedback','N/A')}", styles["Normal"]))
        else:
            data = [
                ["Score", "Feedback"],
                [evaluation.get("score", "N/A"), evaluation.get("feedback", "N/A")]
            ]
            table = Table(data, colWidths=[80, 400])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(table)

        story.append(Spacer(1, 15))
        
    doc.build(story)




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
            report_filename = f"{name.replace(' ', '_').lower()}_interview_report.pdf"
            generate_interview_report(report_filename, name, role, history)
            print(f"\n✅ Interview completed! Report generated as: '{report_filename}'")
            print(f"📄 You can download/view it from your file system.")
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
