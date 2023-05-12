BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from tkinter import messagebox
import pandas
import random

# ---------------------------- New flash card
try:
    df = pandas.read_csv('words_to_learn')
    count = 101 - len(df)
    print(len(df))
    if len(df) == 0:
        count = 0
        df = pandas.read_csv('data/polish_words.csv')
        languages = df.to_dict(orient='records')
    else:
        languages = df.to_dict(orient='records')
except (FileNotFoundError, pandas.errors.EmptyDataError):
    df = pandas.read_csv('data/polish_words.csv')
    count = 101 - len(df)
    print(F"Length of french_words: {len(df)}")
    print(F"Count: {count}")
    languages = df.to_dict(orient='records')
# except pandas.errors.EmptyDataError:
#     df = pandas.read_csv('data/polish_words.csv')
#     count = 101 - len(df)
#     print(F"Length of french_words: {len(df)}")
#     print(F"Count: {count}")
#     languages = df.to_dict(orient='records')

# print(languages)
# data_frame = pandas.read_csv('data/french_words.csv')
# languages = data_frame.to_dict(orient='records')

current_card = random.choice(languages)


# -------------- Functionality --------

def switch_card():
    global current_card
    canvas.itemconfig(language_text, fill='white', text='Polski')
    canvas.itemconfig(word_text, fill='white', text=current_card['Polish'])
    canvas.itemconfig(flash_card, image=back_card_image)


def reset_card():
    global card_delay, current_card
    current_card = random.choice(languages)
    window.after_cancel(id=card_delay)
    canvas.itemconfig(language_text, fill='black', text='Angielski')
    canvas.itemconfig(word_text, fill='black', text=current_card['English'])
    canvas.itemconfig(flash_card, image=front_card_image)
    card_delay = window.after(3000, switch_card)


def remove_word():
    global count
    print(F"Length of languages list before removing {len(languages)}")
    languages.remove(current_card)
    print(F"Length of languages list after removing {len(languages)}")

    data_frame = pandas.DataFrame(languages)
    data_frame.to_csv('words_to_learn', index=False)
    print(F"Length of data frame: {len(data_frame)}")
    count += 1
    count_label.config(text=f"{count}/101")
    if len(languages) == 0:
        messagebox.showinfo(message='That\'s it. You learned everything')
        window.destroy()
        count_label.config(text="0/101")
    reset_card()


# ----------------- UI ------------------
window = Tk()
window.title('Flash cards')
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)

# Label
count_label = Label(text=F'{count}/101', font=('Ariel', 30, 'normal'))

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
back_card_image = PhotoImage(file='images/card_back.png')
front_card_image = PhotoImage(file='images/card_front.png')
flash_card = canvas.create_image(400, 263, image=front_card_image)
language_text = canvas.create_text(400, 150, text='Title', font=('Ariel', 40, 'italic'))
word_text = canvas.create_text(400, 253, text='Word', font=('Ariel', 60, 'bold'))

# Buttons
cross_image = PhotoImage(file='images/wrong.png')
check_image = PhotoImage(file='images/right.png')
cross_button = Button(image=cross_image, highlightthickness=0, borderwidth=0, command=reset_card)
check_button = Button(image=check_image, highlightthickness=0, borderwidth=0, command=remove_word)

# Grid
canvas.grid(row=0, column=0, columnspan=2)
cross_button.grid(row=1, column=0)
check_button.grid(row=1, column=1)
count_label.grid(row=0, column=2)
card_delay = window.after(3000, switch_card)

canvas.itemconfig(language_text, fill='black', text='Angielski')
canvas.itemconfig(word_text, fill='black', text=current_card['English'])

window.mainloop()
