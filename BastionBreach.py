# Code by Illin
#
# This is a complete re-write from my previous version.
# This should work better and now supports multilayer
#

# Main import
import os
import random
import time
import urllib.request
import socket
from msvcrt import getch
from msvcrt import kbhit

# Defining variables
github_url = "https://raw.githubusercontent.com/Illlin/BastionBreach/master/BastionBreach.py"
suit = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]  # Cards in a suit
progress = [b"\r", b" "]  # Keys to trigger text moving
punctuation = [".", "!", ",", "?"]

file_name = "BastionBreach.py"
version = "2.0"

try:
    print("\u2660\u2665\u2666\u2663")  # Test terminal support
    symbols = [" ", "\u2660", "\u2665", "\u2666", "\u2663"]
except (UnicodeEncodeError, UnicodeDecodeError, UnicodeError, UnicodeTranslateError, UnicodeWarning, ):
    symbols = [" "]*5

settings = {
               "Simple View": False,
               "Fast Text":  False,
               "Your Symbol": symbols[1],
               "There Symbol": symbols[2],
               "Server Port": 7064,
               "Server URL": "illin.ddns.net"
}

title = """
  ____            _   _               ____                      _
 |  _ \          | | (_)             |  _ \                    | |
 | |_) | __ _ ___| |_ _  ___  _ __   | |_) |_ __ ___  __ _  ___| |__
 |  _ < / _` / __| __| |/ _ \| '_ \  |  _ <| '__/ _ \/ _` |/ __| '_ \ 
 | |_) | (_| \__ \ |_| | (_) | | | | | |_) | | |  __/ (_| | (__| | | |
 |____/ \__,_|___/\__|_|\___/|_| |_| |____/|_|  \___|\__,_|\___|_| |_| V""" + version + "\n ----Python Edition----\n\n"


# Defining Functions


def clear():  # Clear screen
    os.system("cls")


def download_code(url, file):
    with open(file, "w") as code:
        code.write(urllib.request.urlopen(url).read().decode("utf8"))



def text(words, char_time=0.04, break_time=0.2, pause=True, end="\n", fast="0"):  # Scrolling text
    if fast == "0":
        fast = settings["Fast Text"]
    for char in words:
        print(char, end="", flush=True)
        if kbhit():
            if getch() in progress:
                fast = True
        if char != " ":
            if not fast:
                if char in punctuation:
                    time.sleep(break_time)
                else:
                    time.sleep(char_time)
    if pause:
        wait()
    print("", end=end)


def wait(press=progress):
    while True:
        if getch() in press:
            return


def get_hand(shuffle=False, cards=("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K",), show=True):
    hand = []
    for i in cards:
        hand.append([i, show])
    if shuffle:
        random.shuffle(hand)
    return hand


def compare(card_input):  # 3 cards in [table, player 1, player 2]
    def return_winner(card):  # Finds the max card and test to see test draw
        largest = card.index(max(card))
        if card.count(card[largest]) == 1:
            return largest  # Largest wins
        else:
            return 0  # Draw

    value = {"A": 14, "K": 13, "Q": 12, "J": 11}
    cards = []
    for i in card_input:
        if i in value:
            cards.append(value[i])
        else:
            cards.append(int(i))
    bord = cards[:]
    if 14 in cards:  # If ace played
        cards[:] = [x for x in cards if x != 14]  # Removes Ace
        low = False
        high = False
        for i in range(2, 11):  # 2 to 10 (Inclusive)
            if i in cards:
                low = True  # If number card played

        for i in range(11, 14):  # 11 to 14 (Inclusive)
            if i in cards:
                high = True  # If face card played

        if low and not high:  # In this situation only number cards and ace played, Highest number wins
            for n, i in enumerate(bord):
                if i == 14:
                    bord[n] = 1  # Set Ace low
            return return_winner(bord)

        elif high and not low:
            return return_winner(bord)

        elif high and low:
            return 0  # If Ace High and Low played result in draw

        else:  # This only makes sense wil Low False high False so all cards would be Ace
            return return_winner(bord)

    else:
        return return_winner(bord)


def menu(options, advance=progress, header=title, footer="", selected=0):
    # Draw Menu
    while True:
        clear()
        print(header)
        for n, i in enumerate(options):
            if selected == n:
                print(" >  " + i)
            else:
                print("    " + i)
        print(footer)

        # Keyboard Input
        press = getch()
        if press in advance:
            return selected, options[selected]
        else:
            if press == b"\xe0":  # Arrow key pressed
                press = getch()
                if press == b"P":  # Down Key
                    if (selected + 1) >= len(options):
                        selected = 0
                    else:
                        selected += 1
                if press == b"H":
                    if selected == 0:
                        selected = len(options) - 1
                    else:
                        selected -= 1


def credit():  # Called from menu
    clear()
    text(title, pause=False, char_time=0.02, break_time=0.02, )
    text("This was originally a mini-game from the visual novel Angels with Scaly Wings by Radical Phi", pause=False)
    print("\n")
    text("All programming for this Python port was done by Illin")


def draw_cards(cards, icon=" "):
    if len(icon) != 1:
        raise TypeError
    if settings["Simple View"]:
        print("|", end="")
        for i in cards:
            if i[1]:
                if i[0] == "10":
                    print("10", end="")
                elif i[0] == 0:
                    print("  ", end="")
                else:
                    print(i[0], end=" ")
            else:
                print("##", end="")
            print("|", end="")
        print("")

    else:
        for i, show in cards:  # Top of Card
            if i != 0:
                print("+-------+", end=" ")
            else:
                print("         ", end=" ")
        print("")

        for i, show in cards:  # Number Row Top
            if i != 0:
                if show:
                    print("|" + i + icon, end="")
                    if i == "10":
                        print("    |", end=" ")
                    else:
                        print("     |", end=" ")
                else:
                    print("|///////|", end=" ")
            else:
                print("          ", end="")
        print("")

        for x in range(4):
            for i, show in cards:  # Card Center Row
                if i != 0:
                    if show:
                        print("|       |", end=" ")
                    else:
                        print("|///////|", end=" ")
                else:
                    print("          ", end="")
            print("")

        for i, show in cards:  # Lower Number Row
            if i != 0:
                if show:
                    if i == "10":
                        print("|     " + i + "| ", end="")
                    else:
                        print("|      " + i + "| ", end="")
                else:
                    print("|///////| ", end="")
            else:
                print("          ", end="")
        print("")

        for i, show in cards:  # Lower part Card
            if i != 0:
                print("+-------+", end=" ")
            else:
                print("         ", end=" ")
        print('\n\n')


def tutorial():  # Called from menu
    clear()
    text("So, lets go over the rules.")
    clear()
    text("I am going to set up an example board for you to see.")
    clear()

    ai = get_hand(show=False)
    board = get_hand()
    hand = get_hand(shuffle=False)

    if not settings["Simple View"]:
        draw_cards(ai)
        time.sleep(0.25)
        draw_cards(board, icon=symbols[1])
        time.sleep(0.25)
        draw_cards(hand, icon=symbols[3])
        text("If the screen looks like a mess, full screen the window.")
        text("If the screen still looks like a mess you can press 'S' to change to simple view, this will only work here.", pause=False)
        if getch() in [b"s", b"S"]:
            settings["Simple View"] = True
            clear()
            draw_cards(ai)
            time.sleep(0.25)
            draw_cards(board, symbols[1])
            time.sleep(0.25)
            draw_cards(hand, icon=symbols[3])
            text("This view is a lot simpler but should work on most screens. If you want to change back go in to settings")
            clear()
    clear()
    draw_cards(ai)
    time.sleep(0.25)
    draw_cards(board, symbols[1])
    time.sleep(0.25)
    draw_cards(hand, icon=symbols[3])

    text("As you can see, each of us starts with all cards of a given suit in their hands. You're diamonds and I'll be hearts.")
    text("What you see in the center is the middle row, which is a line of shuffled cards from another suit.")
    text("This way, each game is going to be unique since the middle row always changes between games.")

    clear()
    draw_cards(ai)
    draw_cards(board, symbols[1])
    draw_cards(hand, icon=symbols[3])

    print("")
    text("During each round, we both decide which card to play and put it there face down.")
    text("Once we have both played a card, we flip them over. The highest card wins the round, and whoever played it gets a point.")
    text("To clarify, 2 is the lowest card and the king is the highest. The ace is a special card - it beats every face card, but will lose against any number card.")
    text("Don't worry, you don't need to remember this, there will be a help card at the bottom of the screen.")

    clear()
    draw_cards(ai)
    draw_cards(board, symbols[1])
    draw_cards(hand, icon=symbols[3])

    print("")
    text("Now, the card from the middle row also counts, so it's possible that neither of us will get the point for a round.")
    text("If there is a tie, no clear winner between the three cards, or the middle row has the highest card, no player will get a point for that round.")
    text("However, the next round will give the winner an extra point to make up for it.")
    text("At the end, the player with the most number of points wins the game.")

    print("")
    text("That will be all.")
    clear()


def com_listen(que, com_socket):
    while True:
        try:
            data = com_socket.recv(1024)
            if data == b"":
                return
            else:
                que.append(data)
        except (ConnectionAbortedError, ConnectionError, ConnectionResetError):
            return


def multiplayer(soc, opponent, your_name, host=False):
    score = [0, 0, 0]

    def draw(oppon, sco, you_name):
        clear()
        print("You are in a game with: " + oppon)
        print("\n\n")
        draw_cards(there_hand, settings["There Symbol"])
        draw_cards(board)
        draw_cards(your_hand, settings["Your Symbol"])
        print(you_name + "'s Score: " + str(sco[1]))
        print(oppon + "'s Score: " + str(sco[2]))
        print("\n")

    try:
        your_hand = get_hand()
        there_hand = get_hand(show=False)
        clear()
        print("Setting up game...")
        if host:
            string = ""
            board = get_hand(shuffle=True)
            for i in board:
                string += i[0] + " "
            string = string[:-1]
            soc.send(string.encode("utf8"))
        else:
            board = []
            string = soc.recv(1024).decode("utf8")
            for i in string.split(" "):
                board.append([i, True])

        for num, hold in enumerate(board):
            table = hold[0]
            valid = False
            while not valid:
                draw(opponent, score, your_name)
                choice = input("Pick a card to play\n >").upper()
                for n, i in enumerate(your_hand):
                    if i[0] == choice:
                        valid = True
                        your_hand[n][0] = 0
                if not valid:
                    text("That is not a valid move")
            if choice == "10":
                soc.send("v".encode("utf8"))
            else:
                soc.send(choice.encode("utf8"))
            draw(opponent, score, your_name)
            print("Waiting for opponents move.")
            move = soc.recv(1).decode("utf8")
            if move == "v":
                move = "10"
            valid = False
            for n, i in enumerate(there_hand):
                if i[0] == move:
                    valid = True
                    there_hand[n][0] = 0
            if not valid:
                clear()
                text("The Opponent has sent an invalid move.\nThis is either a network error or your opponent is trying to cheat.")
                del soc
                return

            point = compare([table, choice, move])
            if point != 0:
                score[point] += (1 + score[0])
                score[0] = 0
            else:
                score[0] += 1

            board[num][1] = False

        clear()
        if score[1] > score[2]:
            text("Congratulations You win!")
        elif score[1] < score[2]:
            text("You lost. Better luck next time.")
        elif score[1] == 0 and score[2] == 0:
            text("ummm, what happened! No one got any points.")
        else:
            text("It looks like it was a draw")

    except (ConnectionAbortedError, ConnectionError, ConnectionResetError, ConnectionRefusedError):
        clear()
        text("The server connection was lost. Sorry.")

    del soc


def com(player, ai, table):
    for i in range(3):
        move = random.choice(ai)
        point = compare([table, table, move])
        if point == 2:
            return move
    return ai[0]
        

def play(multi=False, player1="", player2=""):
    def draw(go=1):
        clear()
        print("\n\n")
        if go == 1:
            draw_cards(there_hand, icon=settings["There Symbol"])
            draw_cards(board)
            draw_cards(your_hand, icon=settings["Your Symbol"])
        else:
            draw_cards(your_hand, icon=settings["Your Symbol"])
            draw_cards(board)
            draw_cards(there_hand, icon=settings["There Symbol"])
        print("\n\n")
        if not multi:
            print("Your Score: " + str(score[1]))
            print("Ai's Score: " + str(score[2]))
        else:
            print(player1 + "'s Score: " + str(score[1]))
            print(player2 + "'s Score: " + str(score[2]))
        print("\n")
    score = [0, 0, 0]
    your_hand = get_hand()
    board = get_hand(shuffle=True)
    there_hand = get_hand(show=multi)
    for num, hold in enumerate(board):
        table = hold[0]

        if not multi:
            valid = False
            choice = ""
            while not valid:
                draw()
                choice = input("Pick a card to play\n >").upper()
                for n, i in enumerate(your_hand):
                    if i[0] == choice:
                        your_hand[n][0] = 0
                        valid = True
                if not valid:
                    text("That is not a valid move")

            player_hand = []
            for n, i in enumerate(your_hand):
                if i[0] != 0:
                    player_hand.append(i[0])
            ai_hand = []
            for n, i in enumerate(there_hand):
                if i[0] != 0:
                    ai_hand.append(i[0])
    
            move = com(player_hand, ai_hand, table)
            valid = False
            for n, i in enumerate(there_hand):
                if i[0] == move:
                    there_hand[n][0] = 0
                    valid = True
            if not valid:
                clear()
                text("The ai made an invalid choice")
                return()
        else:
            valid = False
            choice = ""
            while not valid:
                draw(go=1)
                choice = input(player1 + ": Pick a card to play\n >").upper()
                for n, i in enumerate(your_hand):
                    if i[0] == choice:
                        your_hand[n][0] = 0
                        valid = True
                if not valid:
                    text("That is not a valid move")

            valid = False
            move = ""
            while not valid:
                draw(go=2)
                move = input(player2 + ": Pick a card to play\n >").upper()
                for n, i in enumerate(there_hand):
                    if i[0] == move:
                        there_hand[n][0] = 0
                        valid = True
                if not valid:
                    text("That is not a valid move")
        point = compare([table, choice, move])
        if point != 0:
            score[point] += (1 + score[0])
            score[0] = 0
        else:
            score[0] += 1

        board[num][1] = False

    clear()

    if not multi:
        if score[1] > score[2]:
            text("Congratulations You win!")
        elif score[1] < score[2]:
            text("You lost. Better luck next time.")
        elif score[1] == 0 and score[2] == 0:
            text("ummm, what happened! No one got any points.")
        else:
            text("It looks like it was a draw")
    else:
        if score[1] > score[2]:
            text(player1 + " Won")
        elif score[2] > score[1]:
            text(player2 + " Won")
        else:
            text("It looks like it was a draw")


def options_menu():
    menu_no = 0
    while True:
        options = []
        for i in settings:
            string = ""
            string += i
            string = "{:<15}".format(string)
            string += "|"
            string += str(settings[i])
            options.append(string)
        options.append("Back to menu")
        menu_no, menu_item = menu(options, selected=menu_no)
        if menu_no == 0:
            settings["Simple View"] = not settings["Simple View"]
        elif menu_no == 1:
            settings["Fast Text"] = not settings["Fast Text"]
        elif menu_no == 2:
            settings["Your Symbol"] = symbols[symbols.index(settings["Your Symbol"])-1]
        elif menu_no == 3:
            settings["There Symbol"] = symbols[symbols.index(settings["There Symbol"]) - 1]
        elif menu_no == 4:
            print("Enter a new port to use: should be between 1024 and 49151")
            test = input(" >")
            try:
                test = int(test)
                if test in range(1024,49152):
                    settings["Server Port"] = test
                else:
                    raise ValueError
            except ValueError:
                text("This is not a valid port")
        elif menu_no == 5:
            print("Enter a new server URL or IP to use:")
            settings["Server URL"] = input(" >")
        if menu_item == "Back to menu":
            return


def online_multiplayer(user_name):
    def get_server_list(soc):
        print("Getting server list")
        soc.send("Send Server List".encode("utf8"))
        string = " "
        while string[-1] != ".":
            string += soc.recv(1024).decode("utf8")
        string = string[1:-1]
        string = string.split(",")
        server_list = []
        for j in range(int(len(string) / 2)):
            j = j * 2
            server_list.append([string[j], string[j + 1]])
        return server_list

    def check_for_update(soc):
        print("Checking for update")
        soc.send("Update Check".encode("utf8"))
        soc.send(version.encode("utf8"))
        update = soc.recv(1024).decode("utf8")
        if update == "Up To Date":
            print("Your game version is up to date")
            return True
        else:
            i, n = menu(["Download", "Refuse"], header = title + "An Update is available")
            if not i:
                print("Downloading")
                download_code(github_url, file_name)
                text("Your game is now up to date, Please re-launch the application")
                return False
            else:
                return False

    def online_game(soc, there_name, your_name):
        def draw(oppon, scr, you_name):
            clear()
            print("You are in a game with: " + oppon)
            print("\n\n")
            draw_cards(there_hand, settings["There Symbol"])
            draw_cards(board)
            draw_cards(your_hand, settings["Your Symbol"])
            print(you_name + "'s Score: " + str(scr[1]))
            print(oppon + "'s Score: " + str(scr[2]))
            print("\n")

        score = [0, 0, 0]
        card_string = soc.recv(1024).decode("utf8")
        board = card_string.split(",")
        for n, j in enumerate(board):
            board[n] = [j, True]

        clear()
        your_hand = get_hand()
        there_hand = get_hand(show=False)

        for num, hold in enumerate(board):
            table = hold[0]
            valid = False
            while not valid:
                draw(there_name, score, your_name)
                choice = input("Pick a card to play\n >").upper()
                for n, k in enumerate(your_hand):
                    if k[0] == choice:
                        your_hand[n][0] = 0
                        valid = True
                if not valid:
                    text("That is not a valid move")
            print("Waiting for opponent to make a move")
            client_socket.send(choice.encode("utf8"))
            move = client_socket.recv(1024).decode("utf8")
            print(move)
            valid = False
            for n, l in enumerate(there_hand):
                if l[0] == move:
                    there_hand[n][0] = 0
                    valid = True
            if not valid:
                text("Your opponent made an invalid move")
                return()

            point = compare([table, choice, move])
            if point != 0:
                score[point] += (1 + score[0])
                score[0] = 0
            else:
                score[0] += 1

            board[num][1] = False
        client_socket.send("Game Over".encode("utf8"))
        clear()
        if score[1] > score[2]:
            text("Congratulations, you Won!")
        elif score[2] > score[1]:
            text(there_name + " Won")
        elif score[1] == 0 and score[2] == 0:
            text("Wait, what happened. No one got any points...")
        else:
            text("It looks like it was a draw")

    try:
        connect = False
        print("Connecting...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((settings["Server URL"], settings["Server Port"],))
        print("Connected")
        client_socket.send(user_name.encode("utf8"))
        ping = client_socket.recv(1024).decode("utf8")
        name_list = []
        if ping == "Ping":
            connect = True
            servers = get_server_list(client_socket)
        else:
            raise ConnectionError

        if connect:
            update = check_for_update(client_socket)
            if not update:
                text("Sorry, your game version does not match that of the server.")
                return()
            name_list = ["Host New Server\n\n    ####Games to Join####", "Refresh\n"]
            for i in servers:
                name_list.append(i[1])

        while connect:
            ingame = False
            to_join, i = menu(name_list, selected=1)
            if to_join == 0:
                client_socket.send("Host a Server".encode("utf8"))
                while not ingame:
                    clear()
                    print(title + "Hosting server on " + settings["Server URL"] + "\n    ----Waiting for an opponent----")
                    opponent = client_socket.recv(1024).decode("utf8")
                    accepted, i = menu(["Accept", "Refuse"],
                                       header=title + "Hosting server on " + settings["Server URL"] + "\n\n    " + opponent + " is trying to join\n")
                    if accepted:
                        client_socket.send("Connection Refused".encode("utf8"))
                    elif not accepted:
                        client_socket.send("Connection Accepted".encode("utf8"))
                        ingame = True

                        online_game(client_socket, opponent, user_name)

            elif to_join == 1:
                servers = get_server_list(client_socket)
                name_list = ["Host New Server\n\n    ####Games to Join####", "Refresh\n"]
                for i in servers:
                    name_list.append(i[1])
            else:
                user_id = servers[to_join-2][0]
                user_id = str(user_id)
                client_socket.send(user_id.encode("utf8"))
                clear()
                print(title + "\n    ----Waiting for response from " + i + " ----")
                response = client_socket.recv(1024).decode("utf8")
                if response == "Rejected":
                    text("\n" + i + " Rejected your game.")
                    servers = get_server_list(client_socket)
                    name_list = ["Host New Server\n\n    ####Games to Join####", "Refresh\n"]
                    for i in servers:
                        name_list.append(i[1])
                elif response == "Accepted":
                    online_game(client_socket, i, user_name)

    except (ConnectionRefusedError, ConnectionError, ConnectionResetError, ConnectionAbortedError, socket.gaierror):
        clear()
        text("A Connection Error Has Occurred")


while True:
    option_no, option = menu(["Singleplayer", "Multiplayer", "Tutorial", "Options", "Credits", "Quit"])
    if option == "Singleplayer":
        try:
            play()
        except Exception as e:
            clear()
            print(e)
            wait()

    elif option == "Multiplayer":
        name = ""
        number, join = menu(["Online: " + str(settings["Server URL"]), "Offline"])
        if number == 0:
            # ip, null = menu(["Join " + settings["Server URL"], "Join Via IP"], header=title + "---- Server Option ----\n")
            ip = 0
            while name == "":
                clear()
                print(title + " ----Multiplayer----\n")
                name = input("Enter Username to use\n >")
                if "," in name or "." in name or len(name) > 40:
                    text("Sorry you can't have a ',' or '.' and a maximum of 40 characters in your user name")
                    name = ""

            if not ip:
                try:
                    online_multiplayer(name)
                except Exception as e:
                    print(e)
                    wait()

            elif ip:
                number, join = menu(["Host Server", "Join Server", ""], header=title + " ----Multiplayer----\n")
                if join == "Host Server":
                    external_ip = urllib.request.urlopen("http://ident.me").read().decode("utf8")
                    local_ip = socket.gethostbyaddr(socket.gethostname())[0]
                    port = settings["Server Port"]
                    connected = False
                    accept = False
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.bind((socket.gethostname(), port))
                    server_socket.listen(1)
                    while not connected:
                        try:
                            clear()
                            print(title + " ----Hosting Game----\n")
                            print("----Server Info----")
                            print("Your External IP  : " + external_ip)
                            print("Your Local IP     : " + local_ip)
                            print("Server Port       : " + str(port))
                            print("\nServer Started, Waiting for connection.")
                            (client_socket, address) = server_socket.accept()
                            client_socket.send(name.encode("utf8"))
                            user = client_socket.recv(1024).decode("utf8")
                            del accept
                            accept = not menu(["Accept", "Refuse"], header=title + " ----Hosting Game----\n\nConnection From " + user)[0]
                            if accept:
                                connected = True
                                client_socket.send("Accept".encode("utf8"))
                                try:
                                    multiplayer(client_socket, user, name, host=True)
                                except Exception as e:
                                    clear()
                                    print(e)
                                    wait()
                            else:
                                client_socket.send("Refuse".encode("utf8"))
                                del client_socket
                        except (ConnectionRefusedError, ConnectionError):
                            clear()
                            print(title + " ----Hosting Game----\n")
                            if accept:
                                text("There was a network error. Sorry, please try again.")
                elif join == "Join Server":
                    connected = False
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    while not connected:
                        clear()
                        print(title + " ----Joining Game----\n")
                        ip = input("Enter Server IP:\n >")
                        port = ""
                        while type(port) == str:
                            clear()
                            print(title + " ----Joining Game----\n")
                            print("Enter Server IP:\n >" + ip)
                            port = input("enter Server Port: press enter for " + str(settings["Server Port"]) + "\n >")
                            if port == "":
                                port = settings["Server Port"]
                            else:
                                try:
                                    port = int(port)
                                    if port not in range(1024, 49152):
                                        raise ValueError
                                except ValueError:
                                    text("A port should be a number between 1024 and 49151")
                        try:
                            client_socket.connect((ip, port,))
                            client_socket.send(name.encode("utf8"))
                            user = client_socket.recv(1024).decode("utf8")
                            clear()
                            print(title + " ----Connecting----\n")
                            print("Connected to: " + user)
                            print("Awaiting response")
                            accept = client_socket.recv(1024).decode("utf8") == "Accept"
                            connected = True
                            if accept:
                                try:
                                    multiplayer(client_socket, user, name)
                                except Exception as e:
                                    clear()
                                    print(e)
                                    wait()
                            else:
                                text("Connection Refused")
                                del client_socket
                                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        except (ConnectionRefusedError, ConnectionError, ConnectionResetError, ConnectionAbortedError, socket.gaierror):
                            clear()
                            print(title + " ----Joining Game----\n")
                            text("Connection Error.\nPlease Try again.")
        elif join == "Offline":
            player1 = ""
            player2 = ""
            while player1 == "":
                clear()
                print(title + " ----Multiplayer----\n")
                player1 = input("Player 1, Enter Username\n >")
            while player2 == "":
                clear()
                print(title + " ----Multiplayer----\n")
                player2 = input("Player 2, Enter Username\n >")
            play(multi=True, player1=player1, player2=player2)

    elif option == "Tutorial":
        tutorial()
    elif option == "Options":
        options_menu()
    elif option == "Credits":
        credit()
    elif option == "Quit":
        quit()
