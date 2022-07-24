from __future__ import division
import quiz_api
import os
import time
import random
from colorama import Fore, Style
from pyfiglet import figlet_format

class Quiz():
    def __init__(self):
        self.url = 'https://cae-bootstore.herokuapp.com'
        self.correct = 0.0
        self.score = 0.0

    def register(self):
        print('Registration')
        email = input("Email:\n ")
        first_name = input("First Name:\n")
        last_name = input("Last Name:\n")
        password = input("Password:\n")       

        user_dict={
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "password":password
        }
        return quiz_api.register_user(user_dict)

    def login(self):
        email = input('Please enter your email address:\n')
        password = input('Please enter your password:\n')
        self.user = quiz_api.login_user(email, password) 
        return self.user

    def guest(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Guest Display')
        print(f"Welcome, {self.user['first_name']}!")
        while True:
            prompt = input('''
1. Take quiz
2. Quit
            \n''')
            if prompt == '1':
                self.take_quiz()
            elif prompt == '2':
                quit()

    def admin(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Administartion Display')
        print('')
        print(f"Welcome, {self.user['first_name']}!")
        while True:
            prompt = input('''
Please select from the following options:
1. Show all questions
2. Show my questions
3. Edit my questions
4. Delete a question
5. Create a question
6. Take quiz
7. Quit
            \n''')
            if prompt == '1':
                self.show_all_questions()
            elif prompt == '2':
                self.show_my_questions()
            elif prompt == '3':
                self.edit_my_questions()
            elif prompt == '4':
                self.delete_a_question()
            elif prompt == '5':
                self.create_question()
            elif prompt == '6':
                self.take_quiz()
            elif prompt == '7':
                quit()
            else:
                print('Invalid command, please try again.')

    def show_all_questions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('All Quiz Questions')
        self.all_questions = quiz_api.get_all_questions(self.user['token'])
        for question in self.all_questions:
            print(question['question'])

    def show_my_questions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('My Quiz Questions:')
        self.my_questions = quiz_api.get_my_questions(self.user['token'])
        self.author = self.user['first_name'] + ' ' + self.user['last_name'] + '_' + str(0) + str(self.user['user_id'])
        self.my_list_questions = []
        for question in self.my_questions:
            if question['author'] == self.author:
                self.my_list_questions.append(question['question'])
                print(question['question'])

    def edit_my_questions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.my_questions = quiz_api.get_my_questions(self.user['token'])
        self.author = self.user['first_name'] + ' ' + self.user['last_name'] + '_' + str(0) + str(self.user['user_id'])
        for question in self.my_questions:
            if question['author'] == self.author:
                print(f"Question: {question['question']}")
                print(f"Answer: {question['answer']}")
                print(f"ID: {question['id']}")
        
        print(self.my_questions[0]['id'])

        prompt = input('Which question would you like to edit? Please enter the question id.\n')
        revised_question = input('Entre your revised question\n')
        revised_answer = input('Entre your revised answer\n')

        question_dict={
            'question': revised_question,
            'answer': revised_answer
        }
        return(quiz_api.edit_my_question(self.user['token'], prompt, question_dict))

    def delete_a_question(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.my_questions = quiz_api.get_my_questions(self.user['token'])
        self.author = self.user['first_name'] + ' ' + self.user['last_name'] + '_' + str(0) + str(self.user['user_id'])
        for question in self.my_questions:
            if question['author'] == self.author:
                print(f"Question: {question['question']}")
                print(f"Answer: {question['answer']}")
                print(f"ID: {question['id']}")

        prompt = input('Which question would you like to delete? Enter the question id to delete.\n')
        quiz_api.delete_question(self.user['token'], prompt)



    def create_question(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        question = input('Enter your question:\n')
        answer = input('Enter your answer:\n')

        question_dict={
            'question': question,
            'answer': answer
        }
        return quiz_api.create_question(self.user['token'], question_dict)

    def take_quiz(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.all_questions = quiz_api.get_all_questions(self.user['token'])
        length_of_quiz = 10
        for x in range(10):
            random_integer = random.randint(0, len(self.all_questions)-1)
            random_question = (self.all_questions[random_integer]['question'])
            correct_answer = (self.all_questions[random_integer]['answer'])

            response = input(random_question)
            if response.lower() == correct_answer.lower():
                print(Fore.GREEN, Style.BRIGHT,'Correct!', Style.RESET_ALL)
                self.correct += 1
                time.sleep(2)
            else:
                print(Fore.RED, Style.BRIGHT, f'Wrong! The correct answer is {correct_answer}', Style.RESET_ALL)
                time.sleep(2)
        score = round(self.correct / float(length_of_quiz), 2) * 100
        print('****************************************************************')
        if score == 100:
            print(Fore.GREEN, Style.BRIGHT,'You are a genius!', Style.RESET_ALL)
        elif score >= 90:
            print(Fore.GREEN, Style.BRIGHT,'Wow, you are pretty smart!', Style.RESET_ALL)
        elif score >= 80:
            print(Fore.YELLOW, Style.BRIGHT, 'Not too bad...', Style.RESET_ALL)
        elif score >= 70:
            print(Fore.YELLOW, Style.BRIGHT, "C's get degrees, am I right?", Style.RESET_ALL)
        elif score >= 60:
            print(Fore.RED, Style.BRIGHT, 'Those were dumb questions anyways.', Style.RESET_ALL)
        else:
            print(Fore.RED, Style.BRIGHT, 'Maybe pick up a book or visit your local library sometime.', Style.RESET_ALL)

        print(f"You scored {self.correct} out of 10.0!")
        print(f"You scored {score}%")
        time.sleep(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        
class User_prompt():
    quiz = Quiz()

    @classmethod
    def main(cls):
        while True:
            print(figlet_format('QUIZ BOWL!'))
            welcome = input("Welcome to the quiz generator! Would you like to login, register, or quit?\n")
            if welcome =='login':
                if cls.quiz.login():
                    if cls.quiz.user['admin'] ==  True:
                        cls.quiz.admin()
                    else:
                        cls.quiz.guest()

            elif welcome == 'register'.lower():
                if cls.quiz.register():
                    print('Registration succuessful.')
                    continue
                else:
                    print('Registration unsuccessful')
                    break

            elif welcome == 'quit':
                break 

            else:
                print("Shoot, that's an invalid command. Please try again. Type 'guest', 'admin', 'register', or 'quit'to continue")

if __name__ == "__main__":
    User_prompt.main()