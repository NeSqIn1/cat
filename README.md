# Love Bot for Railway

This Telegram bot sends hourly love confessions to a user and forwards all incoming messages to the owner.

## Environment Variables

- `TELEGRAM_BOT_TOKEN` — your bot token.
- `TARGET_USER_ID` — Telegram ID of the user who will receive love messages.
- `OWNER_ID` — your Telegram ID to forward messages.

## Deployment on Railway

1. Create a new Railway project.
2. Link to your GitHub repo or upload files.
3. Set the environment variables above.
4. Provision a Python service.
5. Deploy.

Railway will read the `Procfile` and run `python heart.py`.
