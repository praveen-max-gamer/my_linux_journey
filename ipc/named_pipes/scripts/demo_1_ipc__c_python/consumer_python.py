
if __name__ =="__main__":

    try:
        fifo_path = "demo_pipe_1"

        print(f"Python - Consumer reading from named pipe : {fifo_path}\n\n")
        with open(fifo_path, "r") as f:
            while True:
                data = f.readline()   # read one line at a time
                if data:
                    print(f"Received from C code: \t { data }", end="")
    except KeyboardInterrupt:
        print("\nQuitting...")