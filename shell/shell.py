import os, sys

# prompts forever
while (True):
    path = os.getcwd()
    inp = input(f'{path} $').split()

    # reprompt if user doesnt type anything
    if len(inp) == 0:
        continue
    #exits the shell
    if inp[0] == "exit":
        if len(inp) > 1:
            print("Program terminated with exit code", inp[1])
            sys.exit(int(inp[1]))
        print("Exiting")
        sys.exit(0)
    #changing directory
    if inp[0] == "cd":
        if len(inp) > 1:
            try:
                os.chdir(inp[1])
            except FileNotFoundError:
                print(f'{inp[0]} : no such file or directory: {inp[1]}')
        else:
            continue
