
import socket
import ipaddress
import pymongo
import requests

minIp = ipaddress.IPv4Address("127.0.0.1")
maxIp = ipaddress.IPv4Address("127.0.0.10")
minPort = 27015
maxPort = 27060
socketTimeout = 1

def isOpenPort(ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(socketTimeout)
    sock_chk = soc.connect_ex((str(ip),int(port)))
    soc.close()
    if sock_chk == 0:
        return True
    return False
def wFile(file, ip, port, database):
    f = open(file, "a")
    f.write("db: {}-{}:{}\n".format(database, ip, port))
    f.close()

def checkMongo(ip, port):
    connection_str = "mongodb://{}:{}/".format(ip, port)
    http_content = requests.get("http://{}:{}/".format(ip, port))
    if http_content.text.find("MongoDB"):
        print("Mongodb\ntry connect: {}".format(connection_str))
    else:
        print("no Mongodb\ntry connect: {}".format(connection_str))
    try:
        mongo_client = pymongo.MongoClient(connection_str)
        print(mongo_client.server_info())
        return True
    except:
        return False
    

for ip in range(int(minIp), int(maxIp)):
    target = ipaddress.IPv4Address(ip)
    for port in range(minPort, maxPort):
        check_open = isOpenPort(target, port)
        print("Target: {} {} {}".format(target, port, check_open))
        if check_open:
            if checkMongo(target, port):
                wFile("find.txt", target, port, "MongoDB")
                print("Done")
            
