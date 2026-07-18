# Telegram Task Bot

Bot para Telegram que gerencia uma lista de tarefas por usuario, com
persistencia em banco de dados SQLite — cada pessoa que conversa com o
bot tem sua propria lista, isolada das demais.

## Funcionalidades

| Comando | O que faz |
|---|---|
| `/start` | Mensagem de boas-vindas |
| `/add <tarefa>` | Adiciona uma nova tarefa |
| `/list` | Lista as tarefas pendentes |
| `/done <id>` | Marca uma tarefa como concluida |
| `/remove <id>` | Remove uma tarefa |
| `/help` | Mostra a lista de comandos |

## Como rodar

1. Crie um bot no Telegram falando com o [@BotFather](https://t.me/BotFather)
   e copie o token gerado.

2. Instale as dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Copie o arquivo de exemplo e cole seu token:
   ```bash
   cp .env.example .env
   ```
   Edite o `.env` e substitua pelo token real.

4. Rode o bot:
   ```bash
   python src/bot.py
   ```

5. Abra uma conversa com seu bot no Telegram e mande `/start`.

## Estrutura

```
telegram-bot-python/
├── src/
│   ├── bot.py          # comandos e integracao com a API do Telegram
│   └── database.py     # camada de persistencia (SQLite)
├── .env.example         # modelo do arquivo de variaveis de ambiente
├── .gitignore
└── requirements.txt
```

## Tecnologias

- **python-telegram-bot** — integracao com a API do Telegram (assincrona)
- **sqlite3** (biblioteca padrao do Python) — persistencia das tarefas
- **python-dotenv** — carrega o token do bot a partir do `.env`, mantendo
  a credencial fora do codigo-fonte

## Decisões de design

- Cada tarefa e associada ao `user_id` do Telegram, garantindo que um
  usuario nunca veja ou altere as tarefas de outro.
- O token do bot fica em uma variavel de ambiente (`.env`), nunca
  hardcoded no codigo — o arquivo `.env` esta no `.gitignore` por
  seguranca.

## Possiveis evoluções

- Lembretes agendados (ex: avisar a tarefa em um horario definido)
- Categorias/prioridades para as tarefas
- Edicao da descricao de uma tarefa existente
