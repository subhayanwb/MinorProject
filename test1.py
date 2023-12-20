# import libraries
import nltk
from nltk.chat.util import Chat, reflections
from tkinter import *

# Define the chat pairs
pairs = [
    (r'hi|hello|hey', ['Hi there!', 'Hello!', 'Hey!']),

    (r'who are you?|what is your name?|introduce yourself', ['My name is CareerBot', 'I\'m CareerBot.']),

    (r'best career options', [
        'There are many great career options available today. Some of the best career options in India include data science, artificial intelligence/machine learning, investment banking, product management, corporate/cyber law and medicine 1. These careers offer excellent salary packages and growth opportunities.']),

    (r'what can you do|what do you do', ['I can provide career guidance. What do you need help with?']),

    (r'i need career advice|career advice',
     ['Sure, what area are you interested in?', 'What kind of career do you have in mind?']),

    (r'i want to be a (.*)', ['Why do you want to be a %1?', 'What kind of skills do you think you need to be a %1?',
                              'What steps have you taken towards becoming a %1?']),

    (r'how do i become a (.*)',
     ['What qualifications and skills do you need to become a %1?', 'What is the job outlook for %1?',
      'What kind of experience is required for %1?']),

    (r'what jobs are in demand|in-demand jobs',
     ['There are many jobs in demand, such as software developers, data analysts, nurses, and financial analysts.']),

    (r'doctor', ['Doctors are responsible for diagnosing and treating illnesses and injuries.']),

    (r'engineer', ['Engineers design, build, and test systems, structures, and machines.']),

    (r'teacher', ['Teachers educate and inspire students of all ages and backgrounds.']),

    (r'lawyer', ['Lawyers represent individuals and organizations in legal matters.']),

    (r'business',
     ['Business is a broad field with many different career paths. What area of business are you interested in?']),

    (r'contact', ['MAIL: careerbot@gmail.com WEBSITE: www.careerbot.com']),

    (r'thank you|thanks', ['You\'re welcome!', 'No problem.']),

    (r'bye|goodbye', ['Goodbye!', 'Bye!', 'Take care.'])
]
# Create the chatbot
chatbot = Chat(pairs, reflections)


# Define the function to handle user input and generate response
def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot.respond(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


# Create the GUI using Tkinter
base = Tk()
base.title("Career Guidance Chatbot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

# Create the chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial")
ChatLog.config(state=DISABLED)

# Bind scrollbar to chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

# Create the button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="SEND", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")

# Place all components on the screen
scrollbar.place(x=476, y=6, height=486)
ChatLog.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()