import os, sys, re
# prompts forever

while (True):
    path = os.getcwd()
    pid = os.getpid()
    rc = os.fork()
    
    #fork failure
    if rc < 0:
        sys.exit(1)

    #child process
    elif rc == 0:
        #get user input
        inp = input(f'{path}> $').split()

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
            
        args = [inp[0], inp[1]]

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program

            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)
    else:  # parent (forked ok)

        #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()

        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())
        #break
