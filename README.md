# bezcisobe
ENG:
Starting Flask in Powershell Terminal in Visual Studio Code:

```
$env:FLASK_ENV="development"
$env:FLASK_APP="main.py"
$env:PASSWORD_RESET_KEY="give-the-key-from-heroku-here"
$env:DATABASE_URL="postgres://give-the-url-of-database-from-heroku-here"
$env:API_KEY_MAPS="give-the-api-key-to-Here-Maps-from-heroku-here"
$env:API_CODE_MAPS="give-the-api-code-to-Here-Maps-from-heroku-here"
flask run
```

You need to install the dependencies first in order to run this app.
This only needs to be done once:
`pip install -r requirements.txt`


For connecting with Heroku you also need to create a Procfile file in your repository(with this content in our application, may be different according to requirements of your application):
```
web: gunicorn -b 0.0.0.0:$PORT main:bezciSobe
```

CZE:
Spuštění Flasku v Powershell Terminálu ve Visual Studio Code:

```
$env:FLASK_ENV="development"
$env:FLASK_APP="main.py"
$env:PASSWORD_RESET_KEY="sem-dej-reset-key-z-heroku""
$env:DATABASE_URL="postgres://sem-dej-url-k-databazi-v-heroku"
$env:API_KEY_MAPS="sem-dej-api-klic-k-Here-mapam-z-heroku"
$env:API_CODE_MAPS="sem-dej-api-code-k-Here-mapam-v-heroku"
flask run
```

Je třeba nainstalovat následující požadavky prostřednictvím:
`pip install -r requirements.txt`


Pro propojení aplikace na Heroku je v repozitáři třeba vytvořit Procfile soubor(pro naši aplikaci s tímto obsahem, může se lišit), jinak se propojení nezdaří:
```
web: gunicorn -b 0.0.0.0:$PORT main:bezciSobe
```