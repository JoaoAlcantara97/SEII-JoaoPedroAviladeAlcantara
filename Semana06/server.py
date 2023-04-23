'''O socket possui influencia ao tratar de servidores
com grande quantidade de requisicoes e chamadas'''

#Importando os modulos necessarios
import socket       # modulo de sockets
import threading    # modulo de threads
import time         # modulo de tempo e data

SERVER_IP = socket.gethostbyname(socket.gethostname())  # Forma padrao para adquirir o IP do host
PORT = 5050                 # Porta de acesso
ADDR = (SERVER_IP, PORT)    # Endereco para realizar o server bind (utilizando o Server IP e a Porta de Acesso)
FORMATO = 'utf-8'           # Formato de decodificacao

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #declarando o servidor
server.bind(ADDR)       # Metodo bind com a Server IP e a Porta de Acesso

conexoes = []           # Vetor conexoes
mensagens = []          # Vetor para armazenar as mensagens

# envia uma mensagem para unica pessoa
def enviar_mensagem_individual(conexao):
    print(f"[ENVIANDO] Enviando mensagens para {conexao['addr']}")
    for i in range(conexao['last'], len(mensagens)):    # Percorre todos os elementos
        mensagem_de_envio = "msg=" + mensagens[i]       # Criação da mensagem de envio
        conexao['conn'].send(mensagem_de_envio.encode()) # Envio da mensagem de acordo com a conexao com cliente estabelecido
        conexao['last'] = i + 1                         # Incremento do numero da conexao
        time.sleep(0.2)                                 # Delay

# envia mensagem para todos (cliente)
def enviar_mensagem_todos():
    global conexoes     
    for conexao in conexoes:    # Envia conexao por conexao percorrendo todos os elementos
        enviar_mensagem_individual(conexao)


# Realiza o controle de conexoes dos clientes
def handle_clientes(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}")
    global conexoes     # define as conexoes globalmente
    global mensagens    # define as mensagens globalmente
    nome = False

    while(True):
        msg = conn.recv(1024).decode(FORMATO)   # Define o tamanho maximo da mensagem com com o formato da decodificaçao
        if(msg):    # verifica se nao recebeu uma mensagem nula
            if(msg.startswith("nome=")): # separa o nome recebido pela mensagem   
                mensagem_separada = msg.split("=") # separa o nome e a mensagem da chamada
                nome = mensagem_separada[1] # atribui o nome recebido pela chamada (mensagem)
                mapa_da_conexao = {  # define o mapa da conexao a partir do nome do cliente
                    "conn": conn,
                    "addr": addr,
                    "nome": nome,
                    "last": 0     
                }
                conexoes.append(mapa_da_conexao)    #adiciona os elementos do mapa da conexao
                enviar_mensagem_individual(mapa_da_conexao)     #chamda da funcao de mensagem individual
            elif(msg.startswith("msg=")):   #separa a parte da msg recebida pela mensagem completa
                mensagem_separada = msg.split("=") #separa a parte da mensagem a partir do msg do cliente
                mensagem = nome + "=" + mensagem_separada[1]
                mensagens.append(mensagem)  #adiciona os elementos da mensagem
                enviar_mensagem_todos()     #chamada da funcao que envia para todos



def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()  # com esse comando o socket 'ouve/escuta' as solicitacoes do cliente
    while(True):     # fica travado neste laço
        conn, addr = server.accept()  # aceita a chamada de um cliente e ao conectar salva a conexao e o endereço do cliente
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))  # a thread é utilizada para realizar as ações solicitadas pelo cliente 
        thread.start()                # inicia a thread            

start()     
