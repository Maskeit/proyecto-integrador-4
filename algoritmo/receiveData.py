import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

def send_email(subject, body):
    sender_email = "miguelagustin182@gmail.com"  # Replace with your email address
    receiver_email = "malejandre@ucol.mx"  # Replace with recipient email address
    password = "contrasena_ejem"  # Replace with your email password

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Create secure connection with server and send email
    context = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    context.login(sender_email, password)
    context.sendmail(sender_email, receiver_email, message.as_string())
    context.quit()

def getData():
    # crea un objeto socket
    s = socket.socket()
    # especifica la dirección IP y el puerto en los que el servidor va a escuchar
    host = 'localhost'
    port = 12345
    # enlazar el socket al servidor
    s.bind((host, port))
    # escucha conexiones entrantes
    s.listen(1)
    # acepta una conexión entrante
    conn, addr = s.accept()
    print('Conexión establecida con', addr)
    # recibe el mensaje enviado por el cliente
    data = conn.recv(1024).decode()
    print('Datos recibidos:', data)
    # cierra la conexión
    conn.close()


# llama a la función getData para recibir los datos
while True:
    try:
        getData()
    except Exception as e:
        error_msg = f"Se produjo un error en el servidor: {e}"
        print(error_msg)
        send_email("error en el servidor", "Reparar urgentemente o reconectar servidor")
