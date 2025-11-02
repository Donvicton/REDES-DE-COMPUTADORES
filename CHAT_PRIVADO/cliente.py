# cliente.py
import socket
import threading
import sys

def receber_mensagens(cliente_socket):
    """ Função alvo da Thread: Fica escutando por novas mensagens do servidor. """
    while True:
        try:
            # Espera receber dados do servidor (primitiva recv())
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            
            if not mensagem:
                print("\n[CONEXÃO PERDIDA] Desconectado do servidor.")
                break
            
            # Imprime a mensagem recebida (primitiva print())
            # O servidor já formata (ex: <Nick>, [SYSTEM], [PRIVADO])
            print(f"{mensagem}")

        except (ConnectionResetError, ConnectionAbortedError):
            print("\n[DESCONECTADO] A conexão com o servidor foi perdida.")
            break
        except Exception as e:
            print(f"[ERRO] Erro ao receber mensagem: {e}")
            break
    
    # Encerra o cliente se o loop quebrar
    cliente_socket.close()
    sys.exit()

def enviar_mensagens(cliente_socket):
    """ Função para a Thread Principal: Lê o input e envia ao servidor. """
    try:
        while True:
            # Usa input() (versão moderna do raw_input()) [cite: 2]
            mensagem = input()
            
            if mensagem.lower() == 'sair':
                break

            # Envia a mensagem para o servidor
            cliente_socket.sendall(mensagem.encode('utf-8'))
            
    except EOFError: # Captura Ctrl+D
        print("\nSaindo...")
    except KeyboardInterrupt: # Captura Ctrl+C
        print("\nSaindo...")
    finally:
        # Fecha o socket ao sair do loop
        cliente_socket.close()

def iniciar_cliente():
    """ Função principal para iniciar o cliente de chat. """
    HOST = input("Digite o IP do Servidor (default 127.0.0.1): ") or '127.0.0.1'
    PORTA = 12345

    # Cria o socket do cliente (primitiva socket())
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Tenta se conectar ao servidor
        cliente_socket.connect((HOST, PORTA))
    except ConnectionRefusedError:
        print(f"[ERRO] Não foi possível conectar ao servidor em {HOST}:{PORTA}.")
        print("Verifique se o servidor está online e o IP/Porta estão corretos.")
        return
    except Exception as e:
        print(f"[ERRO DE CONEXÃO] {e}")
        return

    # Inicia a Thread separada para receber mensagens
    thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente_socket,))
    thread_recebimento.daemon = True
    thread_recebimento.start()
    
    # A Thread principal cuidará do envio de mensagens
    enviar_mensagens(cliente_socket)

if __name__ == "__main__":
    iniciar_cliente()