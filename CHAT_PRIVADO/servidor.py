# servidor.py
import socket
import threading

HOST = '127.0.0.1' # Localhost
PORTA = 12345

# Dicionário para armazenar os clientes conectados
# A chave será o socket do cliente, o valor será o nickname
clientes = {} 
# Lock para proteger o acesso ao dicionário 'clientes' (necessário por causa das threads)
clientes_lock = threading.Lock()

def broadcast(mensagem, remetente_socket=None):
    """ Envia uma mensagem para todos os clientes, exceto o remetente. """
    with clientes_lock:
        for cliente_socket in clientes:
            if cliente_socket != remetente_socket:
                try:
                    cliente_socket.send(mensagem.encode('utf-8'))
                except socket.error:
                    # Se houver erro, assume que o cliente desconectou
                    remover_cliente(cliente_socket)

def remover_cliente(cliente_socket):
    """ Remove um cliente do dicionário de forma segura. """
    if cliente_socket in clientes:
        nickname = clientes.pop(cliente_socket)
        cliente_socket.close()
        print(f"[DESCONEXÃO] {nickname} desconectou.")
        # Avisa a todos que o usuário saiu
        broadcast(f"[SYSTEM] {nickname} saiu do chat.", None)

def lidar_com_cliente(conexao, endereco):
    """ Função alvo da Thread: gerencia a conexão com um único cliente. """
    print(f"[NOVA CONEXÃO] {endereco} tentando se conectar...")
    
    try:
        # 1. Solicitar e validar o nickname
        conexao.send("Digite seu nickname: ".encode('utf-8'))
        nickname = conexao.recv(1024).decode('utf-8').strip()

        # Garante que o nickname seja único
        with clientes_lock:
            while not nickname or nickname in clientes.values():
                conexao.send("[ERRO] Nickname inválido ou já em uso. Tente outro: ".encode('utf-8'))
                nickname = conexao.recv(1024).decode('utf-8').strip()
            
            # Adiciona o cliente ao dicionário
            clientes[conexao] = nickname

        # 2. Informar o cliente que ele foi conectado e avisar os outros
        print(f"[CONEXÃO BEM-SUCEDIDA] {endereco} agora é {nickname}.")
        conexao.send(f"[SYSTEM] Bem-vindo, {nickname}!\n[SYSTEM] Digite /list para ver usuários online.\n[SYSTEM] Digite /msg <nick> <mensagem> para chat privado.\n".encode('utf-8'))
        broadcast(f"[SYSTEM] {nickname} entrou no chat.", conexao)

        # 3. Loop principal para receber mensagens
        while True:
            # Espera receber dados do cliente (função primitiva)
            dados = conexao.recv(1024)
            if not dados:
                break # Cliente desconectou (recv() retornou 0 bytes)
            
            mensagem = dados.decode('utf-8').strip()

            # --- Processamento de Comandos ---
            if mensagem.startswith('/list'):
                # Envia a lista de usuários online apenas para este cliente
                with clientes_lock:
                    lista_usuarios = ", ".join(clientes.values())
                    conexao.send(f"[SYSTEM] Usuários online: {lista_usuarios}\n".encode('utf-8'))
            
            elif mensagem.startswith('/msg'):
                # Envia uma mensagem privada
                try:
                    # Formato esperado: /msg <nickname_alvo> <mensagem>
                    _, nick_alvo, msg_privada = mensagem.split(' ', 2)
                    encontrado = False
                    
                    with clientes_lock:
                        for socket_alvo, nick in clientes.items():
                            if nick == nick_alvo:
                                # Envia a msg para o alvo
                                socket_alvo.send(f"[PRIVADO de {nickname}] {msg_privada}".encode('utf-8'))
                                # Confirma o envio para o remetente
                                conexao.send(f"[PRIVADO para {nick_alvo}] {msg_privada}".encode('utf-8'))
                                encontrado = True
                                break
                    
                    if not encontrado:
                        conexao.send(f"[SYSTEM] Erro: Usuário '{nick_alvo}' não encontrado.".encode('utf-8'))
                
                except ValueError:
                    conexao.send("[SYSTEM] Erro: Formato inválido. Use: /msg <nickname> <mensagem>".encode('utf-8'))

            else:
                # Mensagem pública (broadcast)
                print(f"[{nickname}] {mensagem}") # Mostra no console do servidor (primitiva print())
                broadcast_msg = f"<{nickname}> {mensagem}"
                broadcast(broadcast_msg, conexao)
            
    except (ConnectionResetError, ConnectionAbortedError):
        print(f"[ERRO] Conexão com {nickname} ({endereco}) perdida abruptamente.")
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")
    finally:
        # Garante que o cliente seja removido ao sair do loop
        with clientes_lock:
            remover_cliente(conexao)

def iniciar_servidor():
    """ Função principal para iniciar o servidor de chat. """
    
    # Cria o socket (primitiva socket())
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor_socket.bind((HOST, PORTA))
        servidor_socket.listen(10) # Fila de até 10 conexões
        print(f"[EXECUTANDO] Servidor de chat rodando em {HOST}:{PORTA}")

        while True:
            # Aceita uma nova conexão
            conexao_cliente, endereco_cliente = servidor_socket.accept()
            
            # Cria e inicia uma nova Thread para cada cliente (Obrigatório) [cite: 3]
            thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conexao_cliente, endereco_cliente))
            thread_cliente.daemon = True # Permite que o programa feche
            thread_cliente.start()

    except KeyboardInterrupt:
        print("\n[DESLIGANDO] Desligando o servidor...")
    finally:
        # Fecha todas as conexões de clientes restantes
        with clientes_lock:
            for cliente_socket in list(clientes.keys()):
                cliente_socket.send("[SYSTEM] O servidor está sendo desligado.".encode('utf-8'))
                cliente_socket.close()
        servidor_socket.close()
        print("[FINALIZADO] Servidor desligado.")

if __name__ == "__main__":

    iniciar_servidor()
