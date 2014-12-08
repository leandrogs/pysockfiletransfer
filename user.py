def main():
    whoAmI = input("Digite 'S' se você for um servidor e 'C' se for um cliente: ")
    
    if (whoAmI == "S"):
        import server as s

        MY_IP = input("Digite seu IP [localhost]: ")
        if not MY_IP: MY_IP = "localhost"

        MY_PORT = input("Digite sua Porta: ")
        while not MY_PORT:
            MY_PORT = input("Digite sua Porta: ")
        MY_PORT = int(MY_PORT)

        srv = s.Server()
        srv.connect((MY_IP,MY_PORT))
        srv.waitClients(5)
    else:
        import client as c
        clt = c.Client()
        
        SRV_IP = input("Digite o IP do servidor [localhost]: ")
        if not SRV_IP: SRV_IP = "localhost"

        SRV_PORT = input("Digite a Porta do servidor: ")
        while not SRV_PORT:
            SRV_PORT = input("Digite a Porta do servidor: ")
        SRV_PORT = int(SRV_PORT)

        while True:
            print("Selecione a opção desejada")
            print("[1] - Ver arquivos no servidor")
            print("[2] - Baixar arquivo do servidor")
            print("[3] - Enviar arquivo ao servidor")
            print("--------------------------------")
            print("[0] - Sair")
            print("\n")
            OPT = int(input("Escolha uma opção: "))
            print("\n")

            if(OPT == 1):
                clt.connect((SRV_IP, SRV_PORT))
                showListOfFiles(clt._askFileList())
                clt.closeConnection()
            if(OPT == 2):
                clt.connect((SRV_IP, SRV_PORT))
                showListOfFiles(clt._askFileList())
                clt.closeConnection()
                index = int(input("Digite o índice do arquivo: "))
                clt.connect((SRV_IP, SRV_PORT))
                clt._askForFile(index)
            if(OPT == 3):
                showListOfFiles(clt.getFileList())
                fileIndex = int(input("Escolha o arquivo a ser enviado: "))
                passwd = input("Digite sua senha: ")
                clt.connect((SRV_IP,SRV_PORT))
                clt._sendFile(passwd, fileIndex)
            if(OPT == 0):
                break

                

def showListOfFiles(listOfFile):
    """ Função que imprime a lista de arquivos
        
    Args:
        listOfFile (lista de strings): Lista dos arquivos presentes no diretório
    """
    i = 1
    print("\n")
    print("LISTA DE ARQUIVOS NO SERVIDOR")
    print("-----------------------------------")
    for fileName in listOfFile:
        print("["+str(i)+"] - " + fileName)
        i += 1
    print("-----------------------------------")
    print("\n")

if __name__ == "__main__":
    main()