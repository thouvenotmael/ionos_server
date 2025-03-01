from flask import Flask, request, render_template_string
from datetime import datetime
import os
app = Flask(__name__)
PATH = "/app/log/"
LogFile = "logfile.log"

def ajouter_date_au_fichier(nom_fichier, chaine):
    # Vérifie si le fichier existe
    if not os.path.exists(nom_fichier):
        # Crée le fichier
        with open(nom_fichier, 'w') as f:
            pass  # Fichier créé, rien à écrire pour l'instant

    # Obtient la date actuelle
    date_aujourdhui = datetime.now().strftime("%d-%m-%Y")

    # Ajoute la date et la chaîne au fichier
    with open(nom_fichier, 'a') as f:
        f.write(f"{date_aujourdhui} {chaine}\n")

@app.route('/')
def index():
    user_ip = request.remote_addr
    ajouter_date_au_fichier(PATH+LogFile,user_ip)
    # HTML pour afficher l'adresse IP
    html = f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Afficher l'IP de l'utilisateur</title>
    </head>
    <body>
        <h1>Votre adresse IP est :</h1>
        <h1>{user_ip}</h1>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

