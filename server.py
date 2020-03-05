#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from datetime import datetime


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("{}:{} has connected.".format(*client_address))
        client.send(bytes("Greetings from the cave! Now type your name and press enter!\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8").rstrip("\n\r")
    welcome = "Welcome {}! If you ever want to quit, type \\q to exit.\n".format(name)
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
            print(msg)
            if msg.decode("utf8").rstrip("\n\r") != '\q':
                broadcast(msg.decode("utf8").rstrip("\n\r") + "\n", name + ": ")
            else:
                client.send(bytes("Good bye :)", "utf8"))
                client.close()
                del clients[client]
                broadcast("{} has left the chat.".format(name))
                break
        except IOError as e:
            if client in clients:
                client.close()
                del clients[client]
            print("client {} is nor responding, removing!".format(name))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + bytes(msg.rstrip("\n\r") + "\n", "utf8"))


def ping():
    while True:
        now = datetime.now()
        broadcast("Current time: {}".format(now.strftime("%H:%M:%S")), ">>>>Server:")
        time.sleep(60)


clients = {}
addresses = {}

HOST = ''
PORT = 9999
BUFSIZ = 2048
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection... on IP: {} port: {}".format(HOST, PORT))
    PING_THREAD = Thread(target=ping)
    PING_THREAD.start()
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    PING_THREAD.join()
    SERVER.close()
