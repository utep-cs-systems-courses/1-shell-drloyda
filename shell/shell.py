
import os, sys, re
# prompts forever

while (True):
    path = os.getcwd() + ">$"
    rc = os.fork()
    
    #fork failure
    if rc < 0:
        sys.exit(1)

    #child process
    elif rc == 0:
        #get user input
        os.write(1, path.encode())
        inp = os.read(0, 10000).decode().split()

        #exit 
        if inp[0] == "exit":
            sys.exit(1)
            
        #change directory    
        if inp[0] == "cd":
            if len(inp) > 1:
                try:
                    os.chdir(inp[1])
                    continue
                    
                except FileNotFoundError:
                    print(f'{inp[0]} : no such file or directory: {inp[1]}')
            else:
                continue

            
        args = inp

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program

            except FileNotFoundError:
                pass
        # ...fail quietly
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)
    else:  # parent
        childPidCode = os.wait()
