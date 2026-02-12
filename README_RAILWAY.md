# Deploying the bot to Railway (24/7)

Quick checklist:
- Remove any sensitive values from the repo (`.env`) and rotate the bot token if it's already committed.
- Create a Railway project and set the environment variables there: `TELEGRAM_BOT_TOKEN`, `TARGET_CHAT_ID`, `TZ`, `GROQ_API_KEY` (and any other keys).

Steps (CLI)

1. Install Railway CLI:

```bash
npm install -g railway
railway login
```

2. From the repo root, create or link a project and deploy:

```bash
railway init    # create a new project (follow prompts)
railway up      # deploy; Railway will detect the Procfile
```

3. Set environment variables (either in the Railway UI or via CLI):

```bash
railway variables set TELEGRAM_BOT_TOKEN="<your-token>"
railway variables set TARGET_CHAT_ID="-1002324283164"
railway variables set TZ="America/Argentina/Buenos_Aires"
railway variables set GROQ_API_KEY="<your-groq-key>"
```

Railway project & automated setup
---------------------------------

- Project used: `beexo-telegram-bot` (your Railway project)
- Service used: `beexo-bot` (worker process)
- I added the `TARGET_CHAT_ID` for the Beexo Wallet - Comunidad de LatAm group (`-1002324283164`) to the `beexo-bot` service variables, and set `TELEGRAM_BOT_TOKEN` there as well. These variables were set in Railway (not committed to the repo) using:

```bash
# example (already executed via CLI in this environment)
railway variable set "TARGET_CHAT_ID=-1002324283164" -s beexo-bot --skip-deploys
railway variable set "TELEGRAM_BOT_TOKEN=<your-token>" -s beexo-bot --skip-deploys
```

- Security: tokens and API keys were not added to the repository. If any secret was previously committed, rotate it now.

Notes & important caveats

- The repo contains a `Procfile` that runs `python beexo-telegram-bot/bot.py` as a worker process. Railway will start this worker automatically.
- Do NOT keep secrets in committed `.env` files. Add `.env` to `.gitignore` locally and use Railway variables/secrets.
- SQLite (`beexy_history.db`) is stored on the instance filesystem and is ephemeral on Railway: it will be lost on redeploy / instance replacement. For durable storage use a managed DB (Postgres) and update `ai_chat.py` to use that instead of SQLite.
- Polling is supported and simpler to run on Railway. If you prefer webhooks you must expose an HTTPS endpoint (Railway can provide a URL) and change `bot.py` to use webhooks instead of polling.

If you want, I can:

1) Add a small Dockerfile and `railway.json` if you prefer Docker-based deploys.
2) Replace SQLite with a Postgres-backed small adapter and create migration + README.
3) Remove `.env` from the repo and help you rotate the token.

Tell me which of the above you want me to do next and I’ll implement it.
