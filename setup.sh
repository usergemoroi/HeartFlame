#!/bin/bash

echo "🔥 Friendship Flames Bot Setup 🔥"
echo "================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Ask for bot token
echo "📱 Enter your Bot Token from @BotFather:"
read -r BOT_TOKEN

# Ask for admin IDs (optional)
echo ""
echo "👤 Enter Admin IDs (comma-separated, or press Enter to skip):"
read -r ADMIN_IDS

# Create .env file
cat > .env << EOF
BOT_TOKEN=$BOT_TOKEN
ADMIN_IDS=$ADMIN_IDS
DATABASE_PATH=data/bot.db
LOG_LEVEL=INFO
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_PERIOD=60
EOF

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Install dependencies: pip install -r requirements.txt"
echo "2. Run the bot: python main.py"
echo ""
echo "📚 Read README.md for more information"
