# REDES-DE-COMPUTADORES
Um sistema de chat multi-cliente em Python, implementado com as bibliotecas socket e threading  para a disciplina de Redes de Computadores

# Chat Multi-Cliente em Python com Sockets

Este projeto é uma implementação de um sistema de chat Cliente/Servidor desenvolvido em Python, utilizando exclusivamente as bibliotecas nativas socket e threading.

## Funcionalidades

* **Servidor Concorrente:** O servidor usa threads para gerenciar múltiplos clientes simultaneamente.
* **Chat Público:** Mensagens enviadas por um cliente são transmitidas (broadcast) para todos os outros clientes conectados.
* **Mensagens Privadas:** Suporte para mensagens privadas entre usuários através do comando /msg <nickname> <mensagem>.
* **Lista de Usuários:** O comando /list exibe todos os usuários atualmente conectados ao chat.
* **Gerenciamento de Nicknames:** O servidor valida os nicknames para garantir que sejam únicos.
* **Notificações de Status:** O chat exibe mensagens automáticas quando um usuário entra ou sai.

## Tecnologias Utilizadas

* Linguagem: Python 3 
* Bibliotecas Principais:
    * socket: Para a comunicação de rede baseada em TCP.
    * threading: Para permitir que o servidor lide com vários clientes de forma concorrente.

## Passos de como rodar o chat

Estes passos assume que você está rodando o servidor e os clientes na mesma máquina (localhost). 

### Pré-requisitos

* Python 3. instalado em sua máquina.
* Os arquivos servidor.py e cliente.py no mesmo diretório.

### Passo 1: Iniciar o Servidor

O servidor deve ser o primeiro a ser iniciado e deve permanecer rodando o tempo todo.

1.  Abra um terminal (O terminal utlizado será o do VScode, mas pode ser qualquer outro terminal).
2.  Navegue até o diretório onde foi salvo os arquivos do projeto.
3.  Execute o servidor.py
4.  Para confirmar que o servidor está online essa mensagem será exibida no terminal utilizado: [EXECUTANDO] Servidor de chat rodando em 127.0.0.1:12345
    
### Passo 2: Conectar o Primeiro Usuário
1.  Abra uma NOVA janela de terminal.
2.  Navegue até o mesmo diretório do projeto.
3.  Execute o cliente.py:
4.  O script fará duas perguntas:
    * Digite o IP do Servidor (127.0.0.1):
    * Digite seu nickname
5. Para ter certeza que a conexão foi bem sucedida o chat gerá uma mensagem de Bem-vindo.

### Passo 3: Conectar o Segundo Cliente (e mais)
1.  Abra uma TERCEIRA janela de terminal.
2.  Navegue até o mesmo diretório do projeto.
3.  Execute o cliente.py novamente:
4.  O script fará as mesmas perguntas:
    * Digite o IP do Servidor...: Pressione Enter.
    * Digite seu nickname: Digite um nome diferente, pois o chat verfica se os nicknames são diferentes.
5.  Para sabe que outro usuário se conectou ao chat, o terminal vai exibir uma mensagem que o novo usuário faz parte do chat.
    
### Passo 4: Usando os Comandos do Chat

Com os clientes conectados, você pode usar os seguintes comandos:

* **(Mensagem Pública):** Apenas digite sua mensagem e pressione Enter. Todos no chat verão.
* **(Listar Usuários):** Digite /list para ver quem está online.
* **(Mensagem Privada):** Use o formato /msg <nickname> <mensagem>.
* **(Sair):** Digite sair para se desconectar.

### Dica: Rodando em Máquinas Diferentes (Rede Local)

Se seu grupo quiser testar em computadores diferentes na mesma rede (ex: mesmo Wi-Fi):

1.  **No computador do Servidor:**
    * Descubra o IP da máquina na rede local (LAN IP).
        * No Windows: abra o `cmd` e digite ipconfig. Procure por "Endereço IPv4" (algo como 192.168.1.10).
        * No macOS/Linux: abra o terminal e digite ip addr ou ifconfig.
    * **Importante:** Pode ser necessário criar uma regra de *firewall* no computador do servidor para permitir conexões de entrada na porta 12345.

2.  **Nos computadores dos Clientes:**
    * Ao rodar python cliente.py, quando ele perguntar o IP do servidor, em vez de pressionar Enter (127.0.0.1), digite o IP da máquina servidora (ex: 192.168.1.10).

### Solução de Problemas Comuns

* **Erro no Cliente: `ConnectionRefusedError` (Conexão recusada)**
    * **Causa:** O `servidor.py` não está rodando ou você digitou o IP/Porta errados.
    * **Solução:** Verifique se o terminal do servidor está aberto e mostrando a mensagem "[ESCUTANDO]".

* **Erro no Servidor: `OSError: [Errno 98] Address already in use` (Endereço já em uso)**
    * **Causa:** Você tentou rodar o servidor.py uma segunda vez sem fechar o primeiro.
    * **Solução:** Encontre o terminal onde o servidor já está rodando ou feche o processo anterior.

* **Erro no Cliente: `Nickname inválido ou já em uso`**
    * **Causa:** Você tentou se conectar com um nickname que já está sendo usado por outro cliente.
    * **Solução:** Reinicie o cliente (`python cliente.py`) e escolha um nome único.
