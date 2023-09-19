
from startup import *
from route import *
from blogdb import * 
from chat import *

def banner():
    print("**************\n")
    print("Welcome to vinoth blog\n")
    print("*****************\n")
    print("Started")

banner()
print("initialized complete.....")


if __name__ == "__main__":
    #app.run(debug=True)
    banner()
    socketio.run(app)


