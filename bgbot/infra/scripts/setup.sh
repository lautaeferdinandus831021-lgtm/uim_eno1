#!/bin/bash
set -e
echo "=== BG-BOT v5 Setup ==="
[ ! -f .env ] && cp .env.example .env && echo "Created .env — EDIT YOUR SECRETS!"
pip install -r backend/requirements.txt
pip install -r worker/requirements.txt
pip install pytest
cd frontend && npm install && cd ..
echo "=== Setup complete ==="
