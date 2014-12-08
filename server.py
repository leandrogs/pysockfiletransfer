from socket import *
from threading import Thread
import sys
import glob

class Server(object):
    
    def __init__(self):
        """ Função que prepara o socket """
        try:
            self.serverSocket = socket(AF_INET, SOCK_STREAM)
        except (error):
            print("Failed to create a Socket.")
            sys.exit()

    def connect(self, addr):
        """ Função que conecta o socket
        
        Args:
            addr (tupla): Tupla contendo ip em formato de string e porta em
                formato de inteiro
        """
        try:
            self.serverSocket.bind(addr)
        except (error):
            print ("Failed on binding.")
            sys.exit()

    def closeConnection(self):
        """ Função que encerra o socket """
        self.serverSocket.close()

    def waitClients(self, num):
        """Função que escuta 'o meio' esperando por um cliente

            Inicia uma thread para cada cliente conectado
        
        Args:
            num (inteiro): Quantidade de conexões simultâneas
        """
        while True:
            print("Waiting for clients...")
            self.serverSocket.listen(num)
            conn, addr = self.serverSocket.accept()
            print("New client found...")
            thread = Thread(target = self.clientThread, args = (conn,))
            thread.start()

    def clientThread(self, conn):
        """ Função executada pela thread da conexão

            Direciona as requisições do cliente de acordo com os códigos
            definidos no arquivo client.py

        Args:
            conn: Objeto de conexão do cliente
        """
        WELCOME_MSG = "Welcome to the server"
        conn.send(WELCOME_MSG.encode())
        while True:
            data = conn.recv(2024).decode()
            if(data):
                if(data == "#001"):
                    listOfFiles = self.getFileList()
                    strListOfFiles = ','.join(listOfFiles)
                    self._sendFileList(strListOfFiles, conn)
                    break
                else:
                    dataCode = data.split('#')
                    print(dataCode)
                    if(dataCode[1] == "002"):
                        print("Asking for file")
                        self._sendFile(int(dataCode[2]), conn)
                        break
                    if(dataCode[1] == "003"):
                        print("Pedido de login")
                        if self._authentication(dataCode[2]):
                            conn.send("OK".encode())
                            self._recvFile(conn)
                            break
                        else:
                            conn.send("FAILED".encode())
                            break



    def _sendFile(self, fileIndex, conn):
        """Função que envia arquivo ao cliente
        
        Args:
            fileIndex (inteiro): Índice do arquivo na lista exibida ao usuário.
                Lista do usuário começa de 1 e não de 0
            conn: Objeto de conexão do cliente
        """
        listOfFiles = self.getFileList()
        f = open(listOfFiles[fileIndex], "rb")
        while True:
            read = f.readline()
            if read:
                conn.send(read)     
            else:
                f.close()
                break
        conn.close()

    def _sendFileList(self, strList, conn):
        """Função que envia a lista de arquivos ao cliente
        
        Args:
            strList (string): lista de arquivos convertida em string
            conn: Objeto de conexão do cliente
        """
        try:
            conn.sendall(strList.encode())
        except (error):
            print("Failed to send list of files.")

        conn.close()

    def _recvFile(self, conn):
        """Função que recebe arquivo do cliente

        Args:
            conn: Objeto de conexão do cliente
        """
        print("Starting receiving file...")
        fileName = conn.recv(1024).decode()
        f = open(fileName, "wb")
        while True:
            read = conn.recv(1024)
            if read:
                f.write(read)
            else:
                f.close()
                break
        print("File received")
        conn.close()

    def _authentication(self, passwd):
        """Função que autentica um usuário
        
        Args:
            passwd (string): recebe senha criptografa por sha224

        Return:
            booleano: True se a senha estiver no registro. False caso contrário.
        """
        f = open("login.txt", "r")
        lines = f.readlines()
        for line in lines:
            if passwd == line:
                return True
        return False

    def getFileList(self):
        """Função que pega a lista de arquivos

        Return:
            Lista: Lista com o caminho dos arquivos a partir da raiz do servidor
        """
        return glob.glob("files/*")
