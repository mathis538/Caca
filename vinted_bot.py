name: Vinted Watch Bot

on:
  schedule:
    - cron: "*/10 * * * *"   # toutes les 10 minutes
  workflow_dispatch: {}       # permet de le lancer manuellement depuis GitHub

permissions:
  contents: write            # nécessaire pour sauvegarder seen_items.json

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - name: Récupérer le dépôt
        uses: actions/checkout@v4

      - name: Installer Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Installer les dépendances
        run: pip install requests

      - name: Lancer le bot
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python vinted_bot.py

      - name: Sauvegarder les annonces déjà vues
        run: |
          git config user.name "vinted-bot"
          git config user.email "vinted-bot@users.noreply.github.com"
          git add seen_items.json
          git diff --staged --quiet || git commit -m "update seen items"
          git push
