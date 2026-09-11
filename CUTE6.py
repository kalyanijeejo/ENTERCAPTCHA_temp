import tkinter as tk
import random

attempts = 0
shapes = []
animation_running = True
current_captcha = ""
current_question = ""

def random_color(pastel=True):
    r = random.randint(150, 255) if pastel else random.randint(0, 255)
    g = random.randint(150, 255) if pastel else random.randint(0, 255)
    b = random.randint(150, 255) if pastel else random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# Short obvious yes/no questions
irritating_questions = [
    "Is the sky blue? (Yes/No)",
    "Do cats meow? (Yes/No)",
    "Is fire hot? (Yes/No)",
    "Do fish swim? (Yes/No)",
    "Is 2+2=4? (Yes/No)"
]

def fake_captcha():
    global current_captcha
    current_captcha = ''.join(random.choice("ABCDEFG123456") for _ in range(6))
    captcha_label.config(text="CAPTCHA: " + current_captcha, fg=random_color(), bg=random_color())

def check_input():
    global attempts
    attempts += 1
    if entry.get().strip().upper() == current_captcha:
        status_label.config(
            text="✅ Correct CAPTCHA!\nNow answer the silly yes/no question below:",
            fg="green",
            bg="white"
        )
        show_secret_option()
    else:
        status_label.config(
            text="❌ Wrong CAPTCHA.\n✨ Try again… You still have hope, keep trying!",
            fg=random_color(),
            bg=random_color(),
            wraplength=450,
            justify="center"
        )

def show_secret_option():
    global current_question
    current_question = random.choice(irritating_questions)
    question_label.config(text="Question: " + current_question, wraplength=450, justify="center")
    question_label.place(relx=0.5, rely=0.65, anchor="center")
    answer_entry.place(relx=0.5, rely=0.72, anchor="center")
    answer_button.place(relx=0.5, rely=0.79, anchor="center")

def check_answer():
    # Always wrong, but encourage retry
    status_label.config(
        text=f"❌ Wrong again. Even answering '{current_question}' with the obvious answer didn't help!\nBut don’t give up — try again, maybe next time you’ll succeed!",
        fg="red",
        bg="black",
        wraplength=450,
        justify="center"
    )

def reset():
    global attempts
    attempts = 0
    entry.delete(0, tk.END)
    answer_entry.delete(0, tk.END)
    question_label.place_forget()
    answer_entry.place_forget()
    answer_button.place_forget()
    fake_captcha()
    status_label.config(text="", bg=random_color())

# Animate bouncing shapes across full backdrop
def create_shapes():
    for _ in range(15):
        x, y = random.randint(20, 480), random.randint(20, 480)
        shape_type = random.choice(["oval", "flower"])
        color = random_color()
        if shape_type == "oval":
            s = canvas.create_oval(x, y, x+25, y+25, fill=color, outline="")
        else:  # flower (simple circle petals)
            s = canvas.create_oval(x, y, x+20, y+20, fill=color, outline="")
        dx, dy = random.choice([-2,2]), random.choice([-2,2])
        shapes.append((s, dx, dy))

def animate_shapes():
    global animation_running
    if not animation_running:
        return
    for i, (s, dx, dy) in enumerate(shapes):
        canvas.move(s, dx, dy)
        pos = canvas.coords(s)
        if pos[0] < 0 or pos[2] > 500:
            dx = -dx
        if pos[1] < 0 or pos[3] > 500:
            dy = -dy
        shapes[i] = (s, dx, dy)
    root.after(100, animate_shapes)

# Main window setup
root = tk.Tk()
root.title("Cute Glitchy CAPTCHA App")
root.geometry("500x500")

canvas = tk.Canvas(root, width=500, height=500, bg=random_color(pastel=True))
canvas.pack(fill="both", expand=True)

captcha_label = tk.Label(root, text="", font=("Comic Sans MS", 18), relief="ridge", bd=5)
captcha_label.place(relx=0.5, rely=0.15, anchor="center")

entry = tk.Entry(root, font=("Comic Sans MS", 14), relief="groove", bd=3)
entry.place(relx=0.5, rely=0.25, anchor="center")

check_button = tk.Button(root, text="Submit", command=check_input, font=("Comic Sans MS", 12), relief="raised", bd=4)
check_button.place(relx=0.5, rely=0.32, anchor="center")

status_label = tk.Label(root, text="", font=("Comic Sans MS", 12), width=50, height=6, relief="sunken", bd=3, wraplength=450, justify="center")
status_label.place(relx=0.5, rely=0.45, anchor="center")

reset_button = tk.Button(root, text="Try Again", command=reset, font=("Comic Sans MS", 12), relief="ridge", bd=4)
reset_button.place(relx=0.5, rely=0.55, anchor="center")

# Hidden question input
question_label = tk.Label(root, text="", font=("Comic Sans MS", 12), wraplength=450, justify="center")
answer_entry = tk.Entry(root, font=("Comic Sans MS", 14), relief="groove", bd=3)
answer_button = tk.Button(root, text="Answer", command=check_answer, font=("Comic Sans MS", 12), relief="ridge", bd=4)

fake_captcha()
create_shapes()
animate_shapes()
root.mainloop()
