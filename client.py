from socket import *
import sys
import hashlib
import glob

class Client(object):
    
    ASK_LIST_FILES    = "#001" # 001 is the requisition code to list 
                               # all the files
    ASK_SPECIFIC_FILE = "#002" # 002 is the requisition code to a 
                               # specific file
    SEND_FILE         = "#003" # 003 is the requisition code to send one 
                               # file
    AUTHENTICATION    = "#004" # 004 is the requisition code to user
                               # authentication
                                
    listOfFiles = []

    def __init__(self):
        """ Função que prepara o socket """
        try:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
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
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.connect(addr)
        except (error):
            print("Failed to connect.")
            sys.exit()

        print(self.clientSocket.recv(1024).decode())

    def closeConnection(self):
        """Função que encerra o socket"""
        self.clientSocket.close()

    def _logIn(self, passwd):
        """Função que realiza o login do cliente no servidor

        Realiza a encriptação da senha antes de enviá-la ao servidor

        Args:
            passwd (string): Senha do cliente

        Return:
            boolean: Verdadeiro se a senha está cadastrada no servidor. Falso
                caso contrário.
        """
        print("Encrypting password")
        passwd = hashlib.sha224(passwd.encode()).hexdigest()

        try:
            print("Trying to log in")
            data = Client.SEND_FILE + "#" + str(passwd)
            self.clientSocket.sendall(data.encode())
        except (error):
            print("Failed to log in.")
            self.closeConnection()

        if self.clientSocket.recv(1024).decode() == "OK":
            print("Access guaranteed")
            return True
        else:
            print("Failed to log in.")
            return False

    def _sendFile(self, passwd, fileIndex):
        """ Função que envia arquivo para o servidor

        Arquivo só será enviado caso o usuário possua a senha correta para
        envio de dados ao servidor

        Args:
            passwd (string): Senha do cliente
            fileIndex (inteiro): Indice do arquivo no qual se deseja enviar
        """
        if self._logIn(passwd):
            fileIndex -= 1
            listOfFiles = self.getFileList()
            self.clientSocket.sendall(listOfFiles[fileIndex][1:].encode())
            f = open(listOfFiles[fileIndex], "rb")
            while True:
                read = f.readline()
                if read:
                    self.clientSocket.send(read)     
                else:
                    f.close()
                    break
            self.closeConnection()

    def getFileList(self):
        """Função que pega a lista de arquivos

        Return:
            Lista: Lista com o caminho dos arquivos a partir da raiz do servidor
        """
        return glob.glob("_files/*")

    def _askFileList(self):
        """Função que pede pela lista de arquivos no servidor

        Return:
            Lista: Retorno lista de caminhos dos arquivos no servidor
        """
        try:
            data = Client.ASK_LIST_FILES
            self.clientSocket.sendall(data.encode())
        except (error):
            print("Failed asking for the list of files.")
            self.closeConnection()

        return self._recvFileList()

    def _recvFileList(self):
        """Função que recebe a lista de arquivos
        
        Return:
            Lista: Retorna lista de caminhos dos arquivos
        """
        print("Waiting for the list...")
        self.listOfFiles = []
        while len(self.listOfFiles) == 0:
            data = self.clientSocket.recv(1024).decode()
            if (data):
                self.listOfFiles = data.split(',')
                if(len(self.listOfFiles) > 0):
                    self.closeConnection()
                    return self.listOfFiles

    def _askForFile(self, fileIndex):
        """Função que pede por um arquivo específico no servidor

        Args:
            fileIndex: Indice do arquivo no qual se deseja baixar (indice começa
                em um).
        """
        fileIndex = fileIndex - 1

        try:
            data = Client.ASK_SPECIFIC_FILE + "#" + str(fileIndex)
            self.clientSocket.sendall(data.encode())
        except(error):
            print("Failed to ask for an specific file.")
            self.closeConnection()

        self._downloadFile(fileIndex)

    def _downloadFile(self, fileIndex):
        """Função que recebe arquivo do servidor

        Args:
            fileIndex: Índice do arquivo presente na lista
        """
        print("Starting receiving file...")
        f = open("_" + self.listOfFiles[fileIndex], "wb")
        while True:
            read = self.clientSocket.recv(1024)
            if read:
                f.write(read)
            else:
                f.close()
                break
        print("File received")
        self.closeConnection()
