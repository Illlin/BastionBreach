# Made by Illin
#
# This is the main server code for the python game
# Bastion Breach
# The server has little to no security
# so no important data should ever be posted

# ---- Importing Modals
import atexit
import socket
import threading
import datetime
import random
import time

version = "2.0"
log_file = "Server_Log.txt"
# ---- Defining functions ----
def log(text):
    try:
        text = str(text)
    except ValueError:
        text = "TYPE ERROR OCCURRED IN LOG"
    text = str(datetime.datetime.now()) + " >>> " + text
    print(text)  # Prints text with a time stamp
    with open(log_file, "a") as file:
        file.write(text + "\n")


def get_hand(shuffle=True, cards=("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"), show=True):
    hand = []
    for i in cards:
        hand.append([i, show])
    if shuffle:
        random.shuffle(hand)
    return hand


def send_server_list(soc):
    server_list = []
    for i in users:
        if users[i]["Host"]:
            server_list.append([i, users[i]["Name"]])
    string = ""
    for i in server_list:
        string += str("," + str((i[0])) + "," + i[1])
    string = (string[1:]) + "."
    soc.send(string.encode("utf8"))


def echo(your_id, there_id, client_socket):
    while True:
        choice = client_socket.recv(1024).decode("utf8")
        if choice == "Game Over":
            return()
        else:
            users[there_id]["Que"].append(choice)
            while len(users[your_id]["Que"]) == 0:
                client_socket.send("".encode("utf8"))
                time.sleep(0.1)
            move = users[your_id]["Que"][0]
            del users[your_id]["Que"][0]
            client_socket.send(move.encode("utf8"))


def client_thread(address, client_socket):
    your_id = 0
    name = "NULL CLIENT"
    try:
        name = client_socket.recv(1024).decode("utf8")
        if "," in name or "." in name:
            raise ValueError
        valid = False
        while not valid:
            your_id = random.randint(100000, 1000000)
            if your_id not in users:
                valid = True

        users[your_id] = {"Host": False, "Name": name, "Que": []}
        client_socket.send("Ping".encode("utf8"))
        connected = True
        log(str(address) + "Now known as " + name)

        data = str(your_id) + ": " + name

        while connected:

            to_do = client_socket.recv(1024).decode("utf8")
            if to_do == "Send Server List":
                send_server_list(client_socket)
                log("Sent server list to " + data)

            elif to_do == "Host a Server":
                users[your_id]["Host"] = True
                log(data + " Hosting a server")

                while users[your_id]["Host"]:
                    while len(users[your_id]["Que"]) == 0:
                        client_socket.send("".encode("utf8"))
                        time.sleep(0.1)
                    there_id = users[your_id]["Que"][0]
                    del users[your_id]["Que"][0]
                    there_name = users[there_id]["Name"]
                    client_socket.send(there_name.encode("utf8"))
                    accept = client_socket.recv(1024).decode("utf8")
                    if accept == "Connection Refused":
                        users[there_id]["Que"].append("Rejected")
                        log(data + " Rejected game from " + str(there_id) + ": " + there_name)
                    if accept == "Connection Accepted":
                        log(data + " Accepted game from " + str(there_id) + ": " + there_name)
                        users[your_id]["Host"] = False
                        users[there_id]["Que"].append("Accepted")
                        string = ""
                        board = get_hand(shuffle=True)
                        for i in board:
                            string += i[0] + ","
                        string = string[:-1]
                        users[there_id]["Que"].append(string)
                        client_socket.send(string.encode("utf8"))
                        users[your_id]["Que"] = []
                        echo(your_id, there_id, client_socket)
                        log(data + " Out of game with " + str(there_id) + ": " + there_name)

            elif to_do == "Update Check":
                log(data + " Checking for update")
                user_version = client_socket.recv(1024).decode("utf8")
                if user_version == version:
                    client_socket.send("Up To Date".encode("utf8"))
                    log(data + " Up to date")
                else:
                    log(data + " Updating code")
                    client_socket.send("Update Now".encode("utf8"))

            else:
                try:
                    there_id = int(to_do)
                    if there_id not in users:
                        raise ValueError
                    if users[there_id]["Host"]:
                        log(data + " Requested to join " + str(there_id) + ": " + users[there_id]["Name"])
                        users[there_id]["Que"].append(your_id)
                        while len(users[your_id]["Que"]) == 0:
                            time.sleep(0.1)
                            client_socket.send("".encode("utf8"))
                        response = users[your_id]["Que"][0]
                        del users[your_id]["Que"][0]
                        if response == "Rejected":
                            client_socket.send("Rejected".encode("utf8"))
                        elif response == "Accepted":
                            client_socket.send("Accepted".encode("utf8"))
                            while len(users[your_id]["Que"]) == 0:
                                time.sleep(0.1)
                                client_socket.send("".encode("utf8"))
                            client_socket.send(users[your_id]["Que"][0].encode("utf8"))
                            users[your_id]["Que"] = []
                            echo(your_id, there_id, client_socket)

                    else:
                        client_socket.send("Rejected".encode("utf8"))
                except ValueError:
                    client_socket.send("Rejected".encode("utf8"))

    except (ConnectionRefusedError, ConnectionError, ConnectionResetError, ConnectionAbortedError):
        pass
    except ValueError:
        log(address + " Had a comma in the name sent to server")
    except Exception as e:
        log("Unknown Error happened " + str(e) + " " + name + " Disconnected")
    log(str(address) + "," + str(name) + ", Disconnected from the server")

    try:
        del users[your_id]
    except Exception as e:
        pass
    del client_socket

atexit.register(log, "Server Closed\n")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "0.0.0.0"#socket.gethostname()
print(server)
users = {}
port = 7064
server_socket.bind((server, port))

server_socket.listen(5)
log("Server Started")
try:
    while True:
        # accept connections from outside
        (client_sock, addr) = server_socket.accept()
        log("Connection from: " + str(addr))
        # Send connection socket to thread for parallel handling
        ct = threading.Thread(target=client_thread, args=(addr, client_sock,)).start()

except Exception as e:
    log("Critical Error: " + str(e))
