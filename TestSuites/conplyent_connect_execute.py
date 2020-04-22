import os
import sys
import time
import threading
import conplyent



class RUN(object):
    """
    connect was needed
    """

    def __init__(self, ip, port, testName="Undefined tests", timeout=60):
        self._ip = ip
        self._port = port
        self._testName = testName
        self._timeout = timeout
        self._err = "SUCCESS"
        #self._outDir = os.path.join(os.getcwd(), "log")
        self._outDir = os.path.join("C:\\Temp\\")
        self.__conn = conplyent.client.add(self._ip, self._port)

    def reinit(self):
        self.__conn = conplyent.client.add(self._ip, self._port)

    def connect(self, timeout=60):
        try:
            self.reinit()
            self.__conn.connect(timeout=timeout)
        except Exception as e:
            print(e)
            return False
        return True

    def disconnect(self):
        try:
            self.__conn.disconnect()
        except conplyent.ClientTimeout:
            raise ConnectionError

    def close(self):
        self.__conn.close()

    def cd(self, dest):
        try:
            self.__conn.cd(dest)
        except conplyent.ClientTimeout:
            raise ConnectionError

    def reboot(self):
        try:
            self.__conn.reboot(complete=False)
        except conplyent.ClientTimeout:
            raise ConnectionError

    def shutdown(self):
        try:
            self.__conn.shutdown(complete=False)
        except conplyent.ClientTimeout:
            raise ConnectionError

    def sleep(self):
        try:
            self.__conn.sleep(complete=False)
        except conplyent.ClientTimeout:
            raise ConnectionError

    def heartbeat(self, timeout=5):
        return self.__conn.heartbeat(timeout=5)

    def checkdevice(self, retrys=10):
        for retry in range(0, int(retrys)):
            if self.connect(timeout=5):
                return True
            if self.heartbeat(timeout=5):
                return True
            self.reinit()
        return False

    def winReboot(self, num_runs=1, wait_time=10):
        """
        run test 
        """
        startTime = time.time()
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        rounds = int(num_runs) + 1
        retrys = 20
        logWritter = self.saveLog(self._testName)
        logWritter.write("*"*30 + "\n")
        logWritter.write("Start tests: {} at {} \n".format(self._testName, nowTime))
        self.__conn.connect(timeout=60)
        for round in range(0, int(rounds)):
            logWritter.write("-"*30 + "\n")
            logWritter.write("Run {} at round {} \n".format(self._testName, round))
            print("Run {} at round {} \n".format(self._testName, round))

            alive = self.checkdevice(retrys=20)
            if not alive:
                logWritter.write("Reboot run FAILED at attempt {}, Error:fail to connect with dut\n".format(round))
                self._err = "FAILED"
                break
            try:
                print("device alive?{}".format(alive))
                time.sleep(int(wait_time))
                self.connect(timeout=60)
                self.__conn.reboot(complete=True)
                #self.__conn.exec("shutdown /r /t 1")
                print("Reboot run SUCCESS\n")
                time.sleep(60)
                logWritter.write("Reboot run SUCCESS\n")
            except Exception as e:
                self._err = "FAILED"
                logWritter.write("Reboot run FAILED at attempt {}, Error: {}\n".format(round, e))
                break
        logWritter.write("*"*30 + "\n")
        logWritter.write("Result of reboot tests: {}, total rounds: {}\n".format(self._err, round))
        logWritter.write("Finish runing tests: {} at {} \n".format(self._testName, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        logWritter.close()

    def start_test(self, cmd, runTime=0, workDir=None):
        startTime = time.time()
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        runTime = float(runTime) * 60 # minitus to seconds
        logWritter = self.saveLog(self._testName)
        logWritter.write("*"*30 + "\n")
        logWritter.write("Start tests: {} at {} \n".format(self._testName, nowTime))

        alive = self.checkdevice()
        if not alive:
            logWritter.write("FAILED to connect with SUT.")
            return False

        if workDir:
            self.cd(workDir)
        try:
            if (runTime > 0):
                run = 0
                while((time.time() - startTime) < runTime): # run tests till the end of runTime
                    run += 1
                    logWritter.write("test rounds {} \n".format(run))
                    for response in self.run_cmd(cmd):
                        logWritter.write(response)
                        print(response)
                    if (self._err != "SUCCESS"):
                        break
            else: #only run 1 rounds
                logWritter.write("test rounds {} \n".format(1))
                for response in self.run_cmd(cmd):
                    logWritter.write(response)
                    print(response)
        except Exception as e:
            self._err = e
            logWritter.write("Error:{} occur when trying to run tests {}".format(e, self._testName))
        self.close()
        logWritter.write("\n" + "*"*30 + "\n")
        logWritter.write("Result of runing tests {} : {} \n".format(self._testName, self._err))
        logWritter.write("Finish runing tests: {} at {} \n".format(self._testName, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        logWritter.write("*"*30)
        logWritter.close()


    def run_cmd(self, cmd, time_between_messages=360, max_re_attempts=5):
        """
        run any cmd on remote device
        """
        listener = self.__conn.exec(cmd, complete=False, max_interval=2)
        #listener = self.__conn.exec(cmd)
        last_message = time.time()
        exit_flag = False
        attempts = max_re_attempts
        while(True):
            try:
                line = listener.next()  # 2 second grace
                attempts = max_re_attempts
            except conplyent.ClientTimeout:
                if(not(listener.done)):
                    try:
                        if(self.heartbeat()):
                            if((time.time() - last_message) > time_between_messages):
                                raise ConnectionError
                            continue
                        else:
                            yield "Executor died unexpectedly without informing client..."
                            if(exit_flag):
                                break  # Server completed but complete message not received
                            else:
                                exit_flag = True
                                continue
                    except ConnectionError:
                        self._err = "ConnectionError"
                        yield "ConnectionError"
                    except RuntimeError:
                        if(attempts > 0):
                            yield "Runtime error? Re-attempting {}/{}".format(
                                max_re_attempts - attempts, max_re_attempts)
                            attempts -= 1
                            continue
                        else:
                            yield "Num attempts exceeded! System is really not responding!"
                            self._err = "RuntimeError"
                else:
                    yield "Should never happen..."
                    break  # This should never happen..?

            if(line is None):
                break  # Listener exited
            else:
                if(type(line) is bytes or type(line) is str):
                    yield line[:-1]
                    last_message = time.time()
                    yield line
                else:
                    yield "Test exited with: {}".format(str(line))
                    self._err = "UNKNOWN_SETUP"
                    break
        if(listener.exit_code != 0):
            yield "Application exited with: {}".format(listener.exit_code)
            self._err = "APPLICATION_ERROR"


    def saveLog(self, testName):
        strTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        logFile = "_".join(testName.split()) + "_" + strTime + ".txt"
        if not os.path.isdir(self._outDir):
           os.mkdir(self._outDir)
        log     = os.path.join(self._outDir, logFile)
        fw      = open(log, 'w+')
        return fw



if __name__ == "__main__" :
    #define parameters
    if (len(sys.argv) > 1):
        DUT_IP = sys.argv[1]
    else:
        DUT_IP = "10.67.135.19"
    ports = [9922, 9933]
    workDir = "C:\\Program Files\\Futuremark\\3DMark 11\\bin\\x64"
    hostLog = os.path.join(os.getcwd(), "Temp")
    """
    #1, reboot test part
    rebooter = RUN(DUT_IP, 9922, "reboot test")
    rebooter.winReboot(num_runs=500)
    
    #2, memory test part
    memTest = RUN(DUT_IP, 9933, "memory test")
    test2 = threading.Thread(target=memTest.start_test, args=("winautotester memtestpro -p 5 -c 400 -t 600", ))
    test2.start()

    #3, 3d mark test part
    threeDMarkTest = RUN(DUT_IP, 9922, "3d mark tests")
    test3 = threading.Thread(target=threeDMarkTest.start_test, args=("3DMark11Cmd.exe --definition=extreme_definition_window.xml", 240, "C:\\Program Files\\Futuremark\\3DMark 11\\bin\\x64"))
    test3.start()

    test2.join()
    test3.join()
    print("all tests finished")
    """    
    test1 = RUN(DUT_IP, 9922)
    test2 = threading.Thread(target=test1.start_test, args=("ipconfig", 10,))
    test2.start()
    test2.join()
