# REDES-DE-COMPUTADORES
Um sistema de chat multi-cliente em Python, implementado com as bibliotecas socket e threading  para a disciplina de Redes de Computadores

# 💬 Chat Multi-Cliente em Python com Sockets

Este projeto é uma implementação de um sistema de chat Cliente/Servidor desenvolvido em Python [cite: 3][cite_start], utilizando exclusivamente as bibliotecas nativas `socket`  [cite_start]e `threading`.

Foi criado como parte da avaliação da disciplina de Redes de Computadores  (2022.2) [cite_start]da Universidade Federal de Alagoas (UFAL).

## 🚀 Funcionalidades

* [cite_start]**Servidor Concorrente:** O servidor usa threads para gerenciar múltiplos clientes simultaneamente.
* **Chat Público:** Mensagens enviadas por um cliente são transmitidas (broadcast) para todos os outros clientes conectados.
* **Mensagens Privadas:** Suporte para mensagens diretas entre usuários através do comando `/msg <nickname> <mensagem>`.
* **Lista de Usuários:** O comando `/list` exibe todos os usuários atualmente conectados ao chat.
* **Gerenciamento de Nicknames:** O servidor valida os nicknames para garantir que sejam únicos.
* **Notificações de Status:** O chat exibe mensagens automáticas quando um usuário entra ou sai.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3 
* **Bibliotecas Principais:**
    * `socket`: Para a comunicação de rede baseada em TCP.
    * `threading`: Para permitir que o servidor lide com vários clientes de forma concorrente.

## 🚀 Como Rodar a Aplicação (Instruções Detalhadas)

Este guia assume que você está rodando o servidor e os clientes na **mesma máquina** (localhost). Veja a seção "Rodando em Máquinas Diferentes" para instruções de rede.

### Pré-requisitos

* **Python 3.x** instalado em sua máquina.
* Os arquivos `servidor.py` e `cliente.py` no mesmo diretório.

---

### Passo 1: Iniciar o Servidor

O servidor é o "cérebro" do chat. Ele deve ser o primeiro a ser iniciado e deve permanecer rodando o tempo todo.

1.  Abra um terminal (Prompt de Comando, PowerShell, Terminal, etc.).
2.  Navegue até o diretório onde você salvou os arquivos do projeto.
3.  Execute o script `servidor.py`:

    ```bash
    python servidor.py
    ```

4.  **Confirmação:** Se tudo der certo, você verá uma mensagem indicando que o servidor está online e aguardando conexões:

    ```
    [EXECUTANDO] Servidor de chat rodando em 127.0.0.1:12345
    ```

**Importante:** Não feche esta janela de terminal! Ela é o seu servidor.

---

### Passo 2: Conectar o Primeiro Cliente

Agora, vamos conectar o primeiro usuário ao seu servidor.

1.  Abra uma **NOVA** janela de terminal. (Não use a mesma janela do servidor).
2.  Navegue até o mesmo diretório do projeto.
3.  Execute o script `cliente.py`:

    ```bash
    python cliente.py
    ```

4.  O script fará duas perguntas:
    * `Digite o IP do Servidor (default 127.0.0.1):`
        * Pressione **Enter** para aceitar o padrão (`127.0.0.1`), já que o servidor está na sua própria máquina.
    * `Digite seu nickname:`
        * O servidor pedirá seu apelido. Digite um nome, por exemplo: `DONVICTON`

5.  **Confirmação:** Você verá as mensagens de boas-vindas do sistema e estará conectado. No terminal do **servidor**, você verá uma mensagem como: `[CONEXÃO BEM-SUCEDIDA] ... agora é DONVICTON.`

---

### Passo 3: Conectar o Segundo Cliente (e mais)

O objetivo é um chat *multi-cliente*. Para testar isso, você precisa de pelo menos dois clientes conectados ao mesmo tempo.

1.  Abra uma **TERCEIRA** janela de terminal (você agora terá 3 terminais abertos: 1 servidor, 2 clientes).
2.  Navegue até o mesmo diretório do projeto.
3.  Execute o script `cliente.py` novamente:

    ```bash
    python cliente.py
    ```

4.  O script fará as mesmas perguntas:
    * `Digite o IP do Servidor...:` Pressione **Enter**.
    * `Digite seu nickname:` Digite um nome **DIFERENTE**, por exemplo: `WICTOR`
        * (Se você usar o mesmo nome, o servidor recusará a conexão).

5.  **Confirmação:**
    * No terminal do **Cliente 1 (DONVICTON)**, você verá a mensagem: `[SYSTEM] WICTOR entrou no chat.`
    * No terminal do **Cliente 2 (WICTOR)**, você verá a mensagem de boas-vindas.

Agora, qualquer mensagem que você digitar em um terminal de cliente aparecerá no outro!

---

### Passo 4: Usando os Comandos do Chat

Com os clientes conectados, você pode usar os seguintes comandos:

* **(Mensagem Pública):** Apenas digite sua mensagem e pressione `Enter`. Todos no chat verão.
    * Exemplo: `Olá pessoal!`
* **(Listar Usuários):** Digite `/list` para ver quem está online.
    * Exemplo: `/list`
    * Retorno: `[SYSTEM] Usuários online: DONVICTON, WICTOR`
* **(Mensagem Privada):** Use o formato `/msg <nickname> <mensagem>`.
    * Exemplo: `/msg WICTOR tudo bem?`
    * (Note: **sem** os `<` `>`. O nickname é `WICTOR`, não `<WICTOR>`).
* **(Sair):** Digite `sair` para se desconectar.
    * Exemplo: `sair`

---

### 💡 Dica: Rodando em Máquinas Diferentes (Rede Local)

Se seu grupo quiser testar em computadores diferentes na mesma rede (ex: mesmo Wi-Fi):

1.  **No computador do Servidor:**
    * Descubra o IP da máquina na rede local (LAN IP).
        * No Windows: abra o `cmd` e digite `ipconfig`. Procure por "Endereço IPv4" (algo como `192.168.1.10`).
        * No macOS/Linux: abra o terminal e digite `ip addr` ou `ifconfig`.
    * **Importante:** Pode ser necessário criar uma regra de *firewall* no computador do servidor para permitir conexões de entrada na porta `12345`.

2.  **Nos computadores dos Clientes:**
    * Ao rodar `python cliente.py`, quando ele perguntar o IP do servidor, em vez de pressionar `Enter` (`127.0.0.1`), digite o IP da máquina servidora (ex: `192.168.1.10`).

### ⚠️ Solução de Problemas Comuns

* **Erro no Cliente: `ConnectionRefusedError` (Conexão recusada)**
    * **Causa:** O `servidor.py` não está rodando ou você digitou o IP/Porta errados.
    * **Solução:** Verifique se o terminal do servidor está aberto e mostrando a mensagem "[ESCUTANDO]".

* **Erro no Servidor: `OSError: [Errno 98] Address already in use` (Endereço já em uso)**
    * **Causa:** Você tentou rodar o `servidor.py` uma segunda vez sem fechar o primeiro.
    * **Solução:** Encontre o terminal onde o servidor já está rodando ou feche o processo anterior.

* **Erro no Cliente: `Nickname inválido ou já em uso`**
    * **Causa:** Você tentou se conectar com um nickname que já está sendo usado por outro cliente.
    * **Solução:** Reinicie o cliente (`python cliente.py`) e escolha um nome único.
