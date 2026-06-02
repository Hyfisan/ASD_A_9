import time
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait(sec):
    time.sleep(sec)

def nato_pato():
    natopato = """
     __    _  _______  _______  _______  _______  _______  _______  _______ 
    |  |  | ||   _   ||       ||       ||       ||   _   ||       ||       |
    |   |_| ||  |_|  ||_     _||   _   ||    _  ||  |_|  ||_     _||   _   |
    |       ||       |  |   |  |  | |  ||   |_| ||       |  |   |  |  | |  |
    |  _    ||       |  |   |  |  |_|  ||    ___||       |  |   |  |  |_|  |
    | | |   ||   _   |  |   |  |       ||   |    |   _   |  |   |  |       |
    |_|  |__||__| |__|  |___|  |_______||___|    |__| |__|  |___|  |_______|
    """
    print(natopato)
    