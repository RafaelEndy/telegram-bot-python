# Telegram Task Bot

Fiz esse bot pra resolver um problema bem comum: lembrar das tarefas do
dia sem precisar abrir outro app. É só chamar o bot no Telegram e
gerenciar tudo direto na conversa.

Cada pessoa que fala com o bot tem sua própria lista de tarefas, salva
num banco SQLite — ninguém vê a lista de outra pessoa.

## Comandos

| Comando | O que faz |
|---|---|
| `/start` | Mensagem de boas-vindas |
| `/add <tarefa>` | Adiciona uma nova tarefa |
| `/list` | Lista as tarefas pendentes |
| `/done <id>` | Marca uma tarefa como concluída |
| `/remove <id>` | Remove uma tarefa |
| `/help` | Mostra os comandos disponíveis |

## Como rodar

1. Cria um bot com o [@BotFather](https://t.me/BotFather) no Telegram e
   copia o token que ele te dá.

2. Instala as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Copia o `.env.example` pra `.env` e cola seu token lá dentro:
   ```bash
   cp .env.example .env
   ```

4. Roda:
   ```bash
   python src/bot.py
   ```

5. Abre uma conversa com o bot no Telegram e manda `/start`.

## Estrutura

```
telegram-bot-python/
├── src/
│   ├── bot.py          # comandos e integração com a API do Telegram
│   └── database.py     # tudo relacionado ao banco (SQLite)
├── .env.example
├── .gitignore
└── requirements.txt
```

## Tecnologias usadas

- **python-telegram-bot** pra falar com a API do Telegram
- **SQLite** pra guardar as tarefas (sem precisar de servidor de banco externo)
- **python-dotenv** pra manter o token fora do código

## Por que separei o token num `.env`

Token de bot é tipo senha — se alguém pegar, consegue controlar o bot.
Por isso ele fica numa variável de ambiente, e o arquivo `.env` está no
`.gitignore`, então nunca vai parar no GitHub por acidente.

## Próximas ideias

- Lembretes agendados (o bot te avisa num horário marcado)
- Prioridade nas tarefas
- Editar uma tarefa já criada, sem precisar apagar e adicionar de novo
