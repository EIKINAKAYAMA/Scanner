import socket
import threading

max_port = 2000
min_port= 1

threads = []
ports =[]
isopen = []

target_host = input("Input target host name or address: ")

# ポートチェック関数
def Scan(port, i):
    # TCP socket の作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #正常時"0"を返却
    return_code = sock.connect_ex((target_host, port)) 
    sock.close()

    if return_code == 0:
        isopen[i] = "Open"


count = 0
for port in range(min_port, max_port):
    ports.append(port)
    isopen.append("unOpen")

    # 並列処理
    thread = threading.Thread(target = Scan, args=(port, count))
    thread.start()
    threads.append(thread)


for i in range(len(threads)):
    # 該当スレッドが終了するまで待機
    threads[i].join()
    if isopen[i] == "Open":
        print ("Port %d open!" %(ports[i]))

print ("Complete")

 # SYNスキャン