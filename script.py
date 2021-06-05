import socket
from concurrent.futures import ThreadPoolExecutor

max_port = 81
min_port= 79

threads = []
ports =[]
isopen = []
isopenPorts = []

target_host = input("Input target host name or address: ")

# ポートチェック関数
def scan(port, i):
    # TCP socket の作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #正常時"0"を返却
    return_code = sock.connect_ex((target_host, port)) 

    if return_code == 0:
        isopen[i] = 1
    sock.close()

# ポートへの接続関数
def connect(target_port):
    if int(target_port) ==  80 or int(target_port) == 8080 :
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host,int(target_port)))
        request_str = 'GET / HTTP/1.1\r\nHost: %s\r\n\r\n' % (target_host + ':' + target_port)
        client.send(request_str.encode('utf-8'))
        result = client.recv(4096).decode()
        print(result)
        client.close()
    else:
        print("It doesn't support the port protocol sorry, only support HTTP protocol")
    print('Finish')

count = 0
# 並列数を決定する
pool = ThreadPoolExecutor(max_workers=10)

for port in range(min_port, max_port):
    ports.append(port)
    isopen.append(0)

    # 並列処理
    thread = pool.submit(scan(port,count), port)
    threads.append(thread)
    count = count + 1


for i in range(len(threads)):
    # 該当スレッドが終了するまで待機
    if isopen[i] == 1:
        isopenPorts.append(ports[i])
        print ("Port %d open!" %(ports[i]))

pool.shutdown()

print ("Scan Complete")

if len(isopenPorts) > 0:
    while True:
        port = input ("if you wanna connect open-port type the Num, else type [fin] :")
        if port == "fin":
            break
        try: 
            isopenPorts.index(int(port))
        except ValueError:
            print("The port isn't open port")
        else: 
            connect(port)

else:
    print("There isn't any open port so It will be closed bye!!")
