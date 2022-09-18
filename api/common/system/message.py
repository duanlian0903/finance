import api.parameter.project as app
import gtts
import playsound


def show_fundamental_operation_exception_message(exception_message, whether_speak_message=False):
    if app.whether_show_fundamental_operation_exception_message():
        print(exception_message)
        if whether_speak_message:
            speak_message(exception_message)


def show_normal_operation_exception_message(exception_message, whether_speak_message=False):
    if app.whether_show_normal_operation_exception_message():
        print(exception_message)
        if whether_speak_message:
            speak_message(exception_message)


def general_mp3_for_text(text_content, file_name):
    tts = gtts.gTTS(text_content)
    tts.save(file_name)


def speak_message(text_content):
    file_name = '.mp3'
    general_mp3_for_text(text_content, file_name)
    playsound.playsound(file_name)




''' not working anymore
def send_email(subject, content):  # tested
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('lian.program.email@gmail.com', 'test0002')
        server.sendmail('lian.program.email@gmail.com', 'duanlian.cn@gmail.com',
                        'Subject: ' + str(subject) + '\n\n' + str(content))
    except:
        show_fundamental_operation_exception_message('Having error for sending email')
'''