# bezcisobe
Spusteni flasku v Powershell Terminalu ve Viscual Studio Code:
PS C:\Users\Iva\Desktop\PROJEKT\bezcisobe> $env:FLASK_ENV="development"
PS C:\Users\Iva\Desktop\PROJEKT\bezcisobe> $env:FLASK_APP="main.py"
PS C:\Users\Iva\Desktop\PROJEKT\bezcisobe> $env:DATABASE_URL="posgtres://sem-dej-url-k-databazi-v-heroku"
PS C:\Users\Iva\Desktop\PROJEKT\bezcisobe> flask run
Je třeba nainstalovat geopy modul:
pip install geopy
requierements:
flask==1.0.2
gunicorn==19.9.0
psycopg2==2.7.6
geopy==1.17.0
