import webbrowser
import time
import wikipediaapi
import pyttsx3
import pyautogui
import speech_recognition as sr

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)
wiki = wikipediaapi.Wikipedia('en')


class Chatbot:
    def __init__(self):
        self.commands = {
            'open youtube': self.open_youtube,
            'open google': self.open_google,
            'what is the time': self.get_time,
            'exit': self.get_exit,
            'previous tab': self.previous_tab,
            'next tab': self.next_tab,
        }

    def process_command(self, command):
        response = ''
        command = command.lower()
        if command in self.commands:
            response = self.commands[command]()
            return response
        elif 'look for' in command:
            topic = command.replace('look for', '')
            page = wiki.page(topic)
            if page.exists():
                summary = page.summary[0:500]
                return (f"According to Wikipedia: {summary}")
                print(f"text: {summary}\n")
            else:
                return "Sorry, I could not find any matching results in Wikipedia."
        elif 'look up' in command:
            command1 = command.replace('look up', '')
            lookup_flag = False
            for j in search(command1):
                webbrowser.open(j)
                lookup_flag = True
                break
            if lookup_flag:
                return f'Results for {command1} opened in the browser.'
            else:
                return f'Sorry, I could not find any results for {command1}.'

    def open_website(url):
        webbrowser.open(url)

    def open_youtube(self):
        webbrowser.open('https://www.youtube.com')
        return "opening youtube"

    def open_amazon(self):
        webbrowser.open('https://www.amazon.com')
        return "opening amazon"

    def open_google(self):
        webbrowser.open('https://www.google.com')
        return "opening google"

    def get_time(self):
        current_time = time.strftime('%I:%M %p')
        print(f'The time is {current_time}')
        return (f'The time is {current_time}')

    def next_tab(self):
        # Send a single hotkey to switch to the previous tab
        pyautogui.hotkey('ctrl', 'tab')
        return ("switching to next tab")

    def previous_tab(self):
        # Send a single hotkey to switch to the next tab

        pyautogui.hotkey('ctrl', 'shift', 'tab')
        return ("switching to previous tab")

    def get_exit(self):
        engine.say("Goodbye master")
        engine.runAndWait()
        exit()