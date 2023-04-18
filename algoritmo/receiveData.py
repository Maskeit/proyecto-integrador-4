import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

def getData():
    # crea un objeto socket
    s = socket.socket()
    # especifica la dirección IP y el puerto en los que el servidor va a escuchar
    host = 'localhost'
    port = 18748
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
    #try:
    getData()
    # except Exception as e:
    #     error_msg = f"Se produjo un error en el servidor: {e}"
    #     print(error_msg)
    #     send_email("error en el servidor", "Reparar urgentemente o reconectar servidor")
