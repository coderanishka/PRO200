import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000 
server.bind((ip_address, port))
server.listen()
print('server has started')
clients = []
list_of_clients = []
nicknames = []
questions = [
    "1. What type of animal is a seahorse?\n A)Crustacean\n B) Arachnid\n C) Fish\n D) Shell\n\n",
    "2. Which of the following dog breeds is the smallest?\n A) Dachshund\n B) Poodle\n C) Pomeranian\n D) Chihuahua"
    "3. What color are zebras?\n A) White with black stripes\n B) Black with white stripes\n C) Both of the above\n D) None of the above"
    "4. What existing bird has the largest wingspan?\n A) Stork\n B) Swan\n C) Condor\n D) Albatross"
    "5. What is the biggest animal that has ever lived?\n A) Blue whale\n B) African elephant\n C) Apatosaurus (aka Brontosaurus)\n D) Spinosaurus"
]
answers = ['C', "D", "B", "D", "A"]

def getRandomQuestionAnswer(conn):
    random_index = random.randint(0, len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def removeQuestion(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection): 
    if connection in questions: 
        questions.remove(connection)

def clientthread(conn):
    score = 0
    conn.send("Welcome to this Animal Quiz Game!".encode('utf-8'))
    conn.send("You will recieve a Question. You have to choose any of the options from A, B, C or D.".encode('utf-8'))
    conn.send("Best Of Luck!\n\n")
    index, answer = getRandomQuestionAnswer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.upper() == answer:
                    score +=1
                    conn.send(f"Nice! Your Score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Woops! That's incorrect.. Better Luck Next Time!\n\n".encode('utf-8'))
                removeQuestion(index)
                index, answer = getRandomQuestionAnswer(conn)
            else:
                remove(conn)
        except:
            continue
while True: 
    conn, addr = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + ' Connected!')
    new_thread = Thread(target = clientthread, args = conn(nickname))
    new_thread.start

