#!/bin/bash
set -e

echo "=== Setting up einmerker on VPS ==="

# Install dependencies
apt-get update
apt-get install -y python3-venv python3-pip nginx git

# Create app directory
mkdir -p /var/www/einmerker
cd /var/www/einmerker

# Clone repository
if [ -d ".git" ]; then
    git pull origin master
else
    git clone https://github.com/OliverWithClaude/einmerker.git .
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > .env << EOF
APP_NAME=einmerker
DEBUG=False
SECRET_KEY=$SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite+aiosqlite:///./einmerker.db
EOF
fi

# Set permissions
chown -R www-data:www-data /var/www/einmerker

# Setup systemd service
cp deploy/einmerker.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable einmerker
systemctl restart einmerker

# Setup nginx
cp deploy/nginx.conf /etc/nginx/sites-available/einmerker
ln -sf /etc/nginx/sites-available/einmerker /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo "=== einmerker deployed successfully ==="
echo "Access at: http://$(curl -s ifconfig.me)"
