import tkinter as tk
from tkinter import messagebox,font
import socket
import threading

# Create the main window
root = tk.Tk()
custom_font = font.Font(family="Arial", size=24, weight="bold")
root.title("TIC TAC TOE")
w = 390 # width for the Tk root
h = 600 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.configure(background="darkcyan")

# Intro label

def computer():
    global newWindow,current_player,machine,player
    newWindow = tk.Toplevel(root)
    newWindow.title("TIC TAC TOE")
    
    
   
    machine=0
    player=0
    newWindow.configure(background="darkcyan")
        
    
    current_player="X"
        
    game_over = False
        
    
    # Function to handle button clicks
    def button_click(row ,col ):
        global current_player,machine,player

        # Check if the button is already clicked
        if buttons[row][col]['text'] == "" and not game_over:
            
            buttons[row][col].configure(text=f"{current_player}",bg="lightblue" if current_player == "X" else "lightgreen")  # Change color based on player
            if check_winner():
                messagebox.showinfo("Game Over", f"Player {current_player} wins!")
                if current_player=="X":
                    player+=1
                    client_score.config(text=f"player = {player}")
                else:
                    machine+=1
                    computer_score.configure(text=f"computer = {machine}")
                reset_game()
            elif check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                reset_game()
            else:
                current_player = "O" if current_player == "X" else "X"  # Switch player
                if current_player == "O":
                    computer_move()  # Let the computer make a move
    # Function for computer to make a move
    def computer_move():
        global current_player,machine
        for i in range(3):
                for j in range(3):
                    if buttons[i][j]['text'] == "":
                        buttons[i][j]['text'] = "O"  # Computer's move
                        if check_winner():
                            return  # Win condition met
                        buttons[i][j]['text'] = ""  # Undo move

            # Check if the player can win and block them
        for i in range(3):
            for j in range(3):
                if buttons[i][j]['text'] == "":
                    buttons[i][j]['text'] = "X"  # Simulate player's move
                    if check_winner():
                        buttons[i][j]['text'] = "O"  # Block the player
                        buttons[i][j].config(bg="lightgreen")  # Change color for computer
                        current_player = "X"  # Switch back to player
                        return  # Blocked
                    buttons[i][j]['text'] = ""  # Undo move

            # If no immediate win or block, make a random move
        empty_buttons = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]['text'] == ""]
        if empty_buttons:
                import random
                row, col = random.choice(empty_buttons)  # Choose a random empty spot
                buttons[row][col].config(text="O", bg="lightgreen")  # Change color for computer
                
                if check_winner():
                    messagebox.showinfo("Game Over", "Computer wins!")
                    computer_score.config(text=f"computer = {machine}")
                    reset_game()
                else:
                    current_player = "X"  # Switch back to player


        # Check if the player can win and block them
    computer_score=tk.Label(newWindow,text=f"computer = {machine}",font=custom_font)
    computer_score.grid(column=10)
    client_score=tk.Label(newWindow,text=f"player = {player}",font=custom_font)
    client_score.grid(column=10)
      
    def check_winner():
        for row in range(3):
            if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
                return True
        for col in range(3):
            if buttons[0][col]['text'] == buttons[1][col]['text'] == buttons[2][col]['text'] != "":
                return True
        if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
            return True
        if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
            return True
        return False

    # Function to check for a draw
    def check_draw():
        for row in buttons:
            for button in row:
                if button['text'] == "":
                    return False
        return True

    # Function to reset the game
    def reset_game():
        global current_player, game_over
        current_player = "X"
        game_over = False
        for row in buttons:
            for button in row:
                button['text'] = ""
                button.configure(bg="white")  # Reset button color
    buttons=[]
    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(newWindow, text="", font=("Arial", 40), width=5, height=2,
                            bg="white", activebackground="lightgray", 
                            relief="raised", bd=1,
                            command=lambda row=i, col=j: button_click(row,col))
            button.grid(row=i, column=j, padx=3, pady=3)
            row.append(button)
        buttons.append(row)
        
    # Function to switch to play with computer
   
    newWindow.mainloop()
    # Create the main window
def server():
    global button_click,game_over,X,O,current_player
    #Instance
    game_over = False
    X = 0
    O = 0
    current_player = "X"
    
    def serverconnection(position):
        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 3434
        serversocket.bind((host,port))
        serversocket.listen()
        print(position)
        while True:
            conn , addr = serversocket.accept()
            print('server is ready for connection!')
            print(f'someone with this address = {addr} connected!')
            conn.sendall(position.encode())
    client_handler = threading.Thread(target =serverconnection)
    client_handler.start()
    
    def server_gui():
        global server_window,button_click,current_player,position
        server_window = tk.Toplevel(root)
        server_window.title("MULTIPLAYER MOD3")
        server_window.configure(bg=("blue"))
        
        
        def button_click(button,message):
            global current_player,machine,player,buttons,O,X,server_window,position
            
            a = message[0]
            b = message[1]
            c = (a,b)
            server_thread = threading.Thread(target=serverconnection,args=(c))  
            server_thread.start()
            # server_connection(a,b)
            # conn.send(f"{message}")
            print(a,b)
            # Check if the button is already clicked
            button.configure(text=":)",bg="red")
            buttons[a][b]['text'] = 'X'
            if not game_over:
                if check_winner():
                    messagebox.showinfo("state","PLAYER X WON !")
                    X+=1
                    X_score.config(text=f"computer = {X}")
                    reset_game()
                elif check_draw():
                    messagebox.showinfo("state","DRAW")
                    reset_game()
        def check_winner():
            # Check rows
            for row in buttons:
                if row[0]['text'] == row[1]['text'] == row[2]['text'] != ' ':
                    
                    return True
                    
            # Check columns
            for col in range(3):
                if buttons[0][col]['text'] == buttons[1][col]['text'] == buttons[2][col]['text'] != ' ':
                    return True
            # Check diagonals
            if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != ' ':
                return True
            if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != ' ':
                return True
            return False
        def check_draw():
            for row in buttons:
                for button in row:
                    if button['text'] == " ":
                        return False
            return True
        def reset_game():
            global current_player, game_over
            current_player = "X"
            
            for row in buttons:
                for button in row:
                    button['text'] = ""
                    button.config(bg="white")
        
        global buttons 
        buttons = []

        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(server_window, text=" ", font=("Arial", 40), width=5, height=2,
                                   bg="white", activebackground="lightgray",
                                   relief="raised", bd=1)
                # Make sure row=i, col=j is within the lambda scope correctly
                button.config(command=lambda row=i, col=j,b=button :button_click(b,(row,col)))
                button.grid(row=i, column=j, padx=3, pady=3)
                row.append(button)
            buttons.append(row)
        # bott = tk.Button(server_window,text="  ",command=button_click)
        # bott.grid(row=4,column=4)
            
        X_score=tk.Label(server_window,text=f"you = {X}",font=custom_font,bg="white")
        X_score.grid(column=6,row=0)
        O_score=tk.Label(server_window,text=f"opponent = {O}",font=custom_font,bg="white")
        O_score.grid(column=6,row=2)
      
        
        server_window.mainloop()
        
    server_gui()
    
    # def server_connection(a,b):
    
    # def server_thread():
    #     threading.thread()
    
    # def ser_sock():    
    #     serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     host = "127.0.0.1"
    #     port = 5858

    #     serversocket.bind((host,port))
    #     serversocket.listen()
    #     conn,addr = serversocket.accept()
    #     while True:
    #         server_gui()
            





# def client():
#     global client_window
#     clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     client_window = tk.Toplevel(root)
#     client_window.title("MULTIPLAYER MOD3")
#     client_window.configure(bg=("red"))
#     host = "127.0.0.1"
#     port = 5858
#     clientsocket.connect((host,port))
    
#     while True:
#         sending_text = tk.Entry(client_window,text="what you want to say to server? ",bg="white")
#         sending_text.grid(row=0,column=1)
#         clientsocket.sendall(sending_text)
#         response = clientsocket.recv(1024)
        
        
    
    # buttons=[]
    # for i in range(3):
    #     row = []
    #     for j in range(3):
    #         button = tk.Button(client_window, text=" ", font=("Arial", 40), width=5, height=2,
    #                         bg="white", activebackground="lightgray", 
    #                         relief="raised", bd=1)
    #         button.grid(row=i, column=j, padx=3, pady=3)
    #         row.append(button)
    #     buttons.append(row)
    
    
    
    
    

    
        
#         client_window.mainloop()
# def run_client_thread():
#         threading.Thread(target=client, daemon=True).start()   
        



intro_label = tk.Label(root, text="WELCOME MATE", font=custom_font, bg="darkcyan", fg="white",width=20, height=2)
intro_label.grid(row=0, column=1,pady=10, sticky="nsew")

# Add a title label above the buttons

player_num_bt = tk.Button(root, text="Play with Computer", font=custom_font, bg="blue", fg="white", width=20, height=2, command=computer)
player_num_bt.grid(row=1, column=1,pady=10, sticky="nsew")


player_num2_bt = tk.Button(root, text="CREATE A SERVER", font=custom_font, bg="#007BFF", fg="white",command=server)
player_num2_bt.grid(row=2, column=1,pady=5, sticky="nsew")

player_num3_bt = tk.Button(root, text="JOIN THE SERVER", font=custom_font, bg="#007BFF", fg="white")
player_num3_bt.grid(row=3, column=1,pady=5, sticky="nsew")

# Exit button
def exit_app():
    root.quit()

exit_bt = tk.Button(root, text="Exit", font=custom_font, bg="red", fg="white", command=exit_app)
exit_bt.grid(row=4, column=1, pady=10, sticky="nsew")


# Start the main event loop
root.mainloop()
