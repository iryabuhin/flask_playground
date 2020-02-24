

python3 -m pip -V
if [ $? -eq 0 ]; then
  echo '[INSTALL] Found pip'
  python3 -m pip install --upgrade pip
else
  echo '[ERROR] python3-pip not installed'
  exit 1
fi

echo '[INSTALL] Using python virtualenv'
rm -rf ./venv
python3 -m venv ./venv
if [ $? -eq 0 ]; then
    echo '[INSTALL] Activating virtualenv'
    source venv/bin/activate
    pip install --upgrade pip
else
    echo '[ERROR] Failed to create virtualenv. Please install MobSF requirements mentioned in Documentation.'
    exit 1
fi

echo '[INSTALL] Installing Requirements'
pip install --no-cache-dir -r requirements.txt

echo '[INSTALL] Creating Database'
if [ -f "app.db" ]; then
    rm -f app.db
fi
flask db init

echo '[INSTALL] Installation Complete'