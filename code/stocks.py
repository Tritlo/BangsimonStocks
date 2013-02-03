from stockInfo import stockInfo


def Bhelp():
    helpstring = "The following commands are available:\n\
            help: prints this message\n\
            plot: plots information about the stocks\
            "
    print helpstring


def Bplot():


def Bquit():
    print "Goodbye!"
    quit()





print "Welcome to the Bangsimon stock program!"
print "Please enter the ticker of the company/index you wish to check."
ticker = raw_input("Ticker: ")
obj = stockInfo(ticker)

c = 'help'
commands = {'plot': Bplot, 'help':Bhelp, 'quit':Bquit}
Bhelp()
while c != "quit":
    c = raw_input(">> ")
    if c not in commands:
        print "invalid command"
        continue
    commands[c]()

