import socket

def getData():
    # crea un objeto socket
    s = socket.socket()
    s.settimeout(5)
    # especifica la dirección IP y el puerto en los que el servidor va a escuchar
    host = 'localhost'
    port = 12345
    # enlaza el socket al servidor
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
    s.close()


# llama a la función getData para recibir los datos
while True:
    getData()
    # respuesta = input("¿Desea continuar recibiendo datos? (S/N): ")
    # if respuesta.lower() == "n":
    #     break
