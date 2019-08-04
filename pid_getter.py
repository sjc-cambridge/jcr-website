pids = []
file1 = open("ps.txt", "r")
processes = file1.readlines()
file1.close()

if len(processes) > 1:
    for process in processes:    
        process = process.split()
        if "grep" not in process:    
            pids.append(process[1])

    pids = " ".join(pids)
    file2 = open("pids.txt", "w")
    file2.write(pids)
    file2.close()

    
