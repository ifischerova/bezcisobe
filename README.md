# bezcisobe
Spusteni flasku v Powershell Terminalu ve Viscual Studio Code:
```
$env:FLASK_ENV="development"
$env:FLASK_APP="main.py"
$env:PASSWORD_RESET_KEY="sem-dej-reset-key-z-heroku"
$env:DATABASE_URL="postgres://sem-dej-url-k-databazi-v-heroku"
flask run
```

Je třeba nainstalovat geopy modul:
pip install geopy
requirements:
flask==1.0.2
flask-login==0.4.1
gunicorn==19.9.0
psycopg2==2.7.6
geopy==1.17.0
flask-wtf==2.2.1
