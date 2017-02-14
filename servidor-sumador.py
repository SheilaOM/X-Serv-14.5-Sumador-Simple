#!/usr/bin/python3

"""
Sumador Simple

Seila Oliva Muñoz
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind((socket.gethostname(), 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
    while True:
        print ('Waiting for connections')
        (recvSocket, address) = mySocket.accept()       #Me quedo con el objeto socket y una lista de 2 elementos: IP y puerto
        print ('Request received:')
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")
        print (peticion)   #bytes -> utf-8
        print ('Answering back...')

        recurso = peticion.split()[1][1:] #por espacios y saltos de linea
        if recurso == "favicon.ico":
            recvSocket.send(bytes("HTTP/1.1 404 Not found\r\n\r\n<html><body><h1>Not Found</h1></body></html>", "utf-8"))
            recvSocket.close()
            continue

        try:
            recurso = int(recurso)
        except ValueError:
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                            "<html><body><h1>Calculadora</h1>" +
                            "<p>Me has dado un " + recurso + ". Vete" +
                            "</p>" +
                            "</body></html>" +
                            "\r\n", "utf-8"))
            recvSocket.close()
            continue

        recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                        "<html><body><h1>Calculadora</h1>" +
                        "<p>Me has dado un " + str(recurso) + ". Dame mas" +
                        "</p>" +
                        "</body></html>" +
                        "\r\n", "utf-8"))
        recvSocket.close()
except KeyboardInterrupt:       #^C
    print ("Closing binded socket")
    mySocket.close()


#5 -> me has dado un 5. Dame más
#a -> me has dado un a. Vete
#3 -> me habias dado un 5. Ahora me has dado un 3. La suma es 8
#4.5 -> me has dado un 4.5. Vete
