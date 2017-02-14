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

cont = 0
sumando = []
try:
    while True:
        print ('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print ('Request received:')
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")
        print (peticion)
        print ('Answering back...')

        recurso = peticion.split()[1][1:]
        if recurso == "favicon.ico":
            recvSocket.send(bytes("HTTP/1.1 404 Not found\r\n\r\n<html>" +
                                  "<body><h1>Not Found</h1></body>" +
                                  "</html>",
                                  "utf-8"))
            recvSocket.close()
            continue

        try:
            recurso = int(recurso)
            sumando.insert(cont, recurso)
            print("Sumando " + str(cont) + ": " + str(sumando[cont]))
            cont += 1
        except ValueError:
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                                  "<html><body><h1>Calculadora</h1>" +
                                  "<p>Me has dado un " + recurso + ". Vete" +
                                  "</p>" +
                                  "</body></html>" +
                                  "\r\n", "utf-8"))
            recvSocket.close()
            continue

        if cont == 1:
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                                  "<html><body><h1>Calculadora</h1>" +
                                  "<p>Me has dado un " + str(sumando[cont-1]) +
                                  ". Dame otro</p>" +
                                  "</body></html>" +
                                  "\r\n", "utf-8"))
            recvSocket.close()
        elif cont == 2:
            suma = sumando[0]+sumando[1]
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                                  "<html><body><h1>Calculadora</h1>" +
                                  "<p>Me habias dado un " +
                                  str(sumando[cont-2]) +
                                  ". Ahora me has dado un " +
                                  str(sumando[cont-1]) +
                                  ". La suma es " + str(suma) + "</p>" +
                                  "</body></html>" +
                                  "\r\n", "utf-8"))
            recvSocket.close()
            cont = 0

except KeyboardInterrupt:
    print ("Closing binded socket")
    mySocket.close()
