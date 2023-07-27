import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import speech_recognition as sr
from chat import Chatbot
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)


class CommandListener(QThread):
    recognized_command = pyqtSignal(str)
    response_received = pyqtSignal(str)

    def run(self):
        chatbot = Chatbot()
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        while True:
            with microphone as source:
                print('Listening...')
                '''recognizer.adjust_for_ambient_noise(source)
                recognizer.pause_threshold = 0.5'''
                audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                self.recognized_command.emit(command)
                response = chatbot.process_command(command)
                print("Response:", response)
                engine.say(response)
                engine.runAndWait()
                self.response_received.emit(response)
            except sr.UnknownValueError:
                print('Sorry, I did not understand that.')
                engine.say(response)
                engine.runAndWait()
            except sr.RequestError:
                print('Sorry, my speech service is down.')
                engine.say(response)
                engine.runAndWait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Assistant")

        self.dialog_box = QTextEdit(self)
        self.dialog_box.setReadOnly(True)
        self.dialog_box.setGeometry(20, 20, 360, 200)

        self.listen_button = QPushButton("Listen", self)
        self.listen_button.setGeometry(150, 230, 80, 30)
        self.listen_button.clicked.connect(self.start_listening)

        self.command_listener = CommandListener()
        self.command_listener.recognized_command.connect(self.handle_command)
        self.command_listener.response_received.connect(self.display_response)

        self.introduce_chatbot()

    def introduce_chatbot(self):
        intro_message = "Hello, I am chatbot, your personal assistant. How can I assist you today?"
        engine.say(intro_message)
        engine.runAndWait()

    def start_listening(self):
        self.command_listener.start()

    def handle_command(self, command):
        # Process the recognized command
        self.dialog_box.append("You: " + command)

    def display_response(self, response):
        # Display the response in the dialog box
        self.dialog_box.append("Chatbot: " + response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 280)
    window.show()
    sys.exit(app.exec_())