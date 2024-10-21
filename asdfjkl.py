# Import required modules
import flet as ft
from gradio_client import Client
import pyrebase
import os
import speech_recognition as sr


# Firebase configuration
firebaseConfig = {
Cant show this part of the code sorry
}

# Initialize Firebase and client
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
client = Client("saikub/chat")
#audio_client = Client("mrfakename/MeloTTS")
speech_client = Client("saikub/chat")

# Global variables
submit_value = 0
question_1, answer_1 = None, None
question_2, answer_2 = None, None
question_3, answer_3 = None, None
question_4, answer_4 = None, None
question_5, answer_5 = None, None
summary_statement = None
tasks = None
tasks_split = ["No tasks yet..."] * 5
total_answers = None
page = ft.Page

def logic(page, display_question, input_field):
    global submit_value, question_1, answer_1, question_2, answer_2, question_3, answer_3, question_4, answer_4, question_5, answer_5, summary_statement, tasks, tasks_split, total_answers

    submit_value += 1
    page.update()

    if submit_value == 1:
        question_1 = display_question.value
        answer_1 = input_field.value
        question_2 = client.predict(
            message=question_1 and answer_1,
            system_message="this is the second question you are a mental health chat bot. Ask a follow-up question to understand the mental health.",
            max_tokens=100,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )
        display_question.value, input_field.value = question_2, ""
        page.update()

    elif submit_value == 2:
        answer_2 = input_field.value
        question_3 = client.predict(
            message=question_1 and answer_1 and question_2 and answer_2,
            system_message="this is the third question you are a mental health chat bot. Ask a follow-up question to understand the mental health.",
            max_tokens=100,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )
        display_question.value, input_field.value = question_3, ""
        page.update()

    elif submit_value == 3:
        answer_3 = input_field.value
        question_4 = client.predict(
            message=question_1 and answer_1 and question_2 and answer_2 and question_3 and answer_3,
            system_message="this is the fourth question you are a mental health chat bot. Ask a follow-up question to understand the mental health.",
            max_tokens=100,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )
        display_question.value, input_field.value = question_4, ""
        page.update()

    elif submit_value == 4:
        answer_4 = input_field.value
        question_5 = client.predict(
            message=question_1 and answer_1 and question_2 and answer_2 and question_3 and answer_3 and question_4 and answer_4,
            system_message="this is the fifth question you are a mental health chat bot. Ask a follow-up question to understand the mental health.",
            max_tokens=100,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )
        display_question.value, input_field.value = question_5, ""
        page.update()

    elif submit_value == 5:
        answer_5 = input_field.value
        total_answers = f"{question_1}: {answer_1}, {question_2}: {answer_2}, {question_3}: {answer_3}, {question_4}: {answer_4}, {question_5}: {answer_5}"
        summary_statement = client.predict(
            message=total_answers,
            system_message="Summarize the answers concisely, addressing the user directly.",
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )

        tasks = client.predict(
            message=f"Provide 5 tasks to help a person feeling down based on this summary statement: {summary_statement}",
            system_message="Provide supportive tasks under 50 characters.",
            max_tokens=256,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )

        # Clean and split tasks into exactly 5 lines
        tasks_split = [task for task in tasks.strip().splitlines() if task][:5]
        switch_page(page, "summary_page")

# Function to show a loading spinner
def show_loading_spinner(page):
    loading_spinner = ft.ProgressRing(color="green")
    page.controls.clear()
    page.controls.append(loading_spinner)
    page.update()

def summary_page(page):
    global summary_statement
    page.controls.clear()
    
    # Show the summary statement
    page.controls.append(ft.Text(f"Summary: {summary_statement}", size=15, color="white"))
    
    # Continue button to go back to the main page
    continue_button = ft.ElevatedButton(
        text="Continue",
        on_click=lambda e: switch_page(page, "main_page"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            color=ft.colors.GREEN
        )
    )
    
    # Add continue button to the page
    page.controls.append(continue_button)
    page.update()

# Define the main page with tasks and a button to start questions
def main_page(page):
    page.controls.clear()
    page.window_width = 400
    page.window_height = 700
    # Center the content of the page
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Create settings icon
    brudda = ft.PopupMenuButton(
                icon_color=ft.colors.GREEN,
                items=[
                    ft.PopupMenuItem(
                        text="Log out",  on_click= lambda j: login_page(page)
                    ),
                ]
            )
    
    # Add controls to page
    left_aligned_row = ft.Row(
        controls=[brudda],
        alignment=ft.MainAxisAlignment.START  # Align to left
    )

    # Add the row to the page
    page.controls.append(left_aligned_row)

    start_questions_button = ft.ElevatedButton(
        text="Start",
        on_click=lambda e: switch_page(page, "page_1"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            color=ft.colors.GREEN
        )
    )

    # Add greeting text and tasks
    page.controls.append(
        ft.Container(
            content=ft.Text("Hello, There", size=25),
            alignment=ft.alignment.top_left,
            padding=10,
        )
    )

    page.controls.append(
        ft.Container(
            content=ft.Column(
                controls=[ft.Text("Explore today's feelings", size=20), start_questions_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor="#2E2E2E",
            width=page.window_width,
            height=150,
            border_radius=10,
        )
    )

    page.controls.append(ft.Container(content=ft.Text("Tasks:", size=20), alignment=ft.alignment.top_left, padding=10))
    task_counter = 0
    for task in tasks_split:
        task_counter += 1
        if task_counter == 6:\
            break
        if task == None:
            tasks_split.pop(task)
        else:
            page.controls.append(ft.Checkbox(label=task))
    

    page.update()
    
    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.GREEN,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        on_change=lambda e: navbar_logic(e,page),
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.icons.SMART_TOY_OUTLINED, label="Speak"),
            
        ]
    )
    page.add(ft.SafeArea(ft.Text("")))
def speech_speaker(page):
    # Initialize the audio client for TTS
    audio_client = Client("mrfakename/MeloTTS")
    speaker_text = "Hello, how are you doing today?"

    def audio_predict(e):
        global recognised_text
        page.overlay.clear()
        # Speech Recognition: Capture the user's voice and convert it to text
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            
            audio = r.listen(source)
        try:
            recognised_text = r.recognize_google(audio)
            print(f"Recognized Text: {recognised_text}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return
        
        # Generate a response based on the recognized text
        speech = speech_client.predict(
            message=f"{recognised_text}",
            system_message=f" you are mental health bot named 'green', generate a short response",
            max_tokens=256,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )
        print(f"Generated Speech: {speech}")
        
        # Update the speaker text with the new generated speech
        nonlocal speaker_text
        speaker_text = speech
        
        # Text-to-Speech: Generate audio from the generated speech
        audio_data = audio_client.predict(
            text=speaker_text,
            speaker="EN-Default",
            speed=0.9,
            language="EN",
            api_name="/synthesize"
        )

        # Save the generated audio file
        audio_file_name = f"{audio_data}.wav"
        os.rename(audio_data, audio_file_name)  # Ensure to replace with the correct logic if needed
        
        # Play the generated audio file
        audio_player = ft.Audio(
            src=audio_file_name,
            autoplay=True
        )
        
        # Optional: Add Rive animation
        
        
        # Add the audio player to the page and update the UI
        page.overlay.clear()  # Clear previous audio players
        page.overlay.append(audio_player)
        
        page.update()

    # Add a button to trigger the process and append it to the page
    
    circle_button = ft.Container(
        width=100,  # Width of the circle
        height=100,  # Height of the circle (same as width for a perfect circle)
        bgcolor=ft.colors.GREEN,  # Background color set to green
        border_radius=50,  # Rounded corners (half of width/height makes a circle)
        alignment=ft.alignment.center,  # Align content in the center
        content=ft.Text("Speak", color=ft.colors.WHITE),  # Text inside the button
        on_click=audio_predict,  # Action when clicked
        ink=True
        
    )
    page.controls.append(circle_button)
    page.update()
def navbar_logic(e,page):
    if e.control.selected_index == 1:
        page.controls.clear()
        page.update()
        speech_speaker(page)
        page.update()
    elif e.control.selected_index == 0:
        page.controls.clear()
        page.overlay.clear()
        page.update()
        switch_page(page, "main_page")
        page.update()
    print(e.control.selected_index)
        

def login_page(page):
    page.controls.clear()
    email_field = ft.TextField(label="Email", border_color="green", color="white", border_radius=30, label_style=ft.TextStyle(color="white"), cursor_color="green")
    password_field = ft.TextField(label="Password", password=True, border_color="green", color="white", border_radius=30, label_style=ft.TextStyle(color="white"), cursor_color="green")
    error_message = ft.Text("", color=ft.colors.RED)
    
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda e: login_logic_d(page, email_field, password_field, error_message),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30), color=ft.colors.GREEN)
    )
    
    signup_button = ft.ElevatedButton(
        text="Sign Up",
        on_click=lambda e: signup_logic(page, email_field, password_field, error_message),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30), color=ft.colors.GREEN)
    )
    
    # Place buttons side by side
    buttons_row = ft.Row(controls=[login_button, signup_button], alignment=ft.MainAxisAlignment.CENTER)
    
    # Add controls to page
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.append(ft.Text("5Question's", size=40, color="white"))
    page.controls.append(ft.Container(margin=10, padding=10, alignment=ft.alignment.center, height=20))
    page.controls.append(email_field)
    page.controls.append(password_field)
    page.controls.append(ft.Container(margin=10, padding=10, alignment=ft.alignment.center, height=5))
    page.controls.append(buttons_row)
    page.controls.append(error_message)
    page.update()

def login_logic(page):
    if os.path.exists("login_info.txt"):
        with open("login_info.txt", "r") as file:
            saved_email, saved_password = file.read().splitlines()
            try:
                auth.sign_in_with_email_and_password(saved_email, saved_password)
                page.snack_bar = ft.SnackBar(ft.Text(f"Welcome back! {saved_email}"), open=True)
                page.update()
                switch_page(page, "main_page")
            except:
                login_page(page)
    else:
        login_page(page)

# Function to handle user login
def login_logic_d(page, email_field, password_field, error_message):
    email = email_field.value
    password = password_field.value
    try:
        # Attempt Firebase authentication
        auth.sign_in_with_email_and_password(email, password)
        # Save credentials for auto-login
        with open("login_info.txt", "w") as file:
            file.write(f"{email}\n{password}")
        
        switch_page(page, "main_page")
        
        
    except:
        error_message.value = "Invalid email or password. Please try again."
        page.update()

# Function to handle new user signup
def signup_logic(page, email_field, password_field, error_message):
    email = email_field.value
    password = password_field.value
    try:
        # Create new user in Firebase
        auth.create_user_with_email_and_password(email, password)
        page.snack_bar = ft.SnackBar(ft.Text(f"New acount created successfully {email}"), open=True)
        page.update()
        # Automatically log in the user after signup
        with open("login_info.txt", "w") as file:
            file.write(f"{email}\n{password}")
        
        switch_page(page, "main_page")
        
    except Exception as e:
        error_message.value = f"The email aldready exists or invalid email."
        page.update()

# Function to switch between pages
def switch_page(page, page_name):
    if page_name == "login_page":
        page.controls.clear()
        page.controls.append(ft.Column(
            controls=[
                ft.Text("Login", size=30),
                ft.TextField(label="Email", on_change=lambda e: e),
                ft.TextField(label="Password", password=True),
                ft.ElevatedButton(text="Login", on_click=lambda e: login_logic_d(page, e.control.parent.controls[1], e.control.parent.controls[2], e.control.parent.controls[0])),
                ft.Text("", color="red"),
                ft.TextButton(text="Sign Up", on_click=lambda e: switch_page(page, "signup_page")),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ))
        page.update()

    elif page_name == "signup_page":
        page.controls.clear()
        page.controls.append(ft.Column(
            controls=[
                ft.Text("Sign Up", size=30),
                ft.TextField(label="Email", on_change=lambda e: e),
                ft.TextField(label="Password", password=True),
                ft.ElevatedButton(text="Sign Up", on_click=lambda e: signup_logic(page, e.control.parent.controls[1], e.control.parent.controls[2], e.control.parent.controls[0])),
                ft.Text("", color="red")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ))
        page.update()

    elif page_name == "page_1":
        page.controls.clear()
        page.controls.append(ft.Text("5Question's", color="White", size=30))
        page.controls.append(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("Non clickable"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    
                    width= page.window_width,
                    height=5,
                    border_radius=10,
                )]))
        display_question = ft.Text("Question", size=20)
        input_field = ft.TextField(label="Your Answer", multiline=True, max_lines=4, border_color="Green", color="white", border_radius=30, label_style=ft.TextStyle(color="white"), cursor_color="white")
        
        submit_button = ft.ElevatedButton(text="Submit", color="green", on_click=lambda e: logic(page, display_question, input_field))
        
        page.controls.append(ft.Column(
            controls=[display_question, input_field, submit_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ))
        display_question.value = "How are you doing today?"
        page.update()

    elif page_name == "summary_page":
        show_loading_spinner(page)
        summary_page(page)

    elif page_name == "main_page":
        main_page(page)
        
    elif page_name == "speech_speaker":
        speech_speaker(page)

# Function to initialize the app
def main(page):
    # Set window dimensions
    page.window_width = 400
    page.window_height = 700
    # Center the content of the page
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Start with the login page
    login_logic(page)
    

# Run the app
if __name__ == "__main__":
    ft.app(target=main)
