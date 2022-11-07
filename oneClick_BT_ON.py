import subprocess


def run_win_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:

        line = line.rstrip()
        result.append(line.decode())    # converting from bytes to a string

    errcode = process.returncode

    for line in result:
        
        # bthserv service
        if(line == "SERVICE_NAME: bthserv"):  
            # print("HEYxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            
            if(result[3] == "        STATE              : 3  STOP_PENDING"):     # if success in stopping then start it 

                print("Stopped bthserv now starting it ")
                run_win_cmd("sc start bthserv")
                break
            elif(result[3] == '        STATE              : 2  START_PENDING'):  # if success in starting then stop sc stop BluetoothUserService_628e1 

                print("Started bthserv now starting BluetoothUserService")
                run_win_cmd("sc stop BluetoothUserService_628e1")       # CHECK: the ending 5 digits changes almost every time so dont know what to do to fix this 
                break
        # BluetoothUserService  service
        elif(line == "SERVICE_NAME: BluetoothUserService_628e1"):  
            if(result[3] == "        STATE              : 3  STOP_PENDING"):     # if success in stopping then start it 

                print("Stopped BluetoothUserService_628e1 now starting it ")
                run_win_cmd("sc start BluetoothUserService_628e1")          # CHECK: change the last 5 number if changed 
                break
            elif(result[3] == '        STATE              : 2  START_PENDING'):  # if success in starting then do nothing
                break
        
        elif(line == "[SC] ControlService FAILED 1062:"):   # service not started yet so start it

            print(f"{cmd} was not started yet so starting it")
            if(cmd == 'sc stop bthserv'):
                run_win_cmd("sc start bthserv")
                break
            elif(cmd == 'sc stop BluetoothUserService_628e1'):       # CHECK: change the last 5 number if changed 
                run_win_cmd("sc start BluetoothUserService_628e1")
                break

        elif(line == "[SC] StartService FAILED 1056:"):   # service is already running
            
            print(f"{cmd} was already running so stopping it")
            if(cmd == 'sc start bthserv'):
                run_win_cmd("sc stop bthserv")
                break
            elif(cmd == 'sc start BluetoothUserService_628e1'):       # CHECK: change the last 5 number if changed 
                run_win_cmd("sc stop BluetoothUserService_628e1")
                break
        elif(line == "[SC] ControlService FAILED 1051:"):
            print(f"{cmd} was dependent on another command")
            if(cmd == 'sc stop bthserv'):
                run_win_cmd("sc stop BluetoothUserService_628e1")
                break
            elif(cmd == 'sc stop BluetoothUserService_628e1'):       # CHECK: change the last 5 number if changed 
                run_win_cmd("sc stop bthserv")
                break

            
        # print(line)
    if errcode is not None:
        raise Exception('command %s failed, see above for details', cmd)


run_win_cmd('sc stop bthserv')