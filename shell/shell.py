import os, sys, re

#executing commands
def execute(inp):
    for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
        program = "%s/%s" % (dir, inp[0])
        try:
            os.execve(program, inp, os.environ)  # try to exec program
        except FileNotFoundError:
            pass
        
#changing directories
def change_dir(inp):
    try:
        os.chdir(inp[1])
    except FileNotFoundError:
        os.write(1, f'{inp[0]} : no such file or directory: {inp[1]}')

def redirect(inp, direct):
    if direct == '>':
        os.close(1)                
        os.open(inp[inp.index(">")+1], os.O_CREAT | os.O_WRONLY);
        os.set_inheritable(1, True)

    else:
        os.close()
        os.open(inp[inp.index("<")+1], os.O_RONLY)
        os.set_inheritable(0, True)
    

def pipe(inp):
    pr, pw = os.pipe()
    fork1 = os.fork()
    
    if fork1 < 0:
       sys.exit(1)
        
    if fork1 == 0:  # writing
        os.close(1)
        os.dup(pw)
        os.set_inheritable(1, True)

        for f in (pr, pw):
            os.close(f)
            
        inp = inp[:inp.index("|")]
        execute(inp)
        sys.exit(0)

    elif fork1 > 0:  # reading
        fork2 = os.fork()

        if fork2 < 0:
            sys.exit(1)

        elif fork2 == 0:
            os.close(0)
            os.dup(pr)
            os.set_inheritable(0, True)

            for f in (pr, pw):
                os.close(f)

            inp = inp[inp.index("|") + 1:]
            execute(inp)
            sys.exit(0)
            
        else:
            for f in (pr, pw):
                os.close(f)
                os.wait()
            
                
# prompts forever
while (True):
    path = os.getcwd() + ">$ "

    
    #Get user inout
    os.write(1, path.encode())
    inp = os.read(0,1000).decode().split()

    if len(inp) == 0:
        continue
    #exit
    if inp[0] == "exit":
        sys.exit(1)

    #change directory
    elif inp[0] == "cd":
        change_dir(inp)
        continue
    
    #pipe
    elif "|" in inp:
        pipe(inp)
        continue
        
    else:
        rc = os.fork()
        #fork failure
        if rc < 0:
            sys.exit(1)

            #child process
        elif rc == 0:
            #redirect
            if ">" in inp:
                redirect(inp, ">")
                inp = inp[:inp.index(">")]

            elif "<" in inp:
                redirect(inp, "<")
                inp = inp[:inp.index("<")]
                
            execute(inp)
            sys.exit(1)
        
        #parent
        else:
            childPidCode = os.wait()
