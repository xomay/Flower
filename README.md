# Guide d'installation et d'utilisation de Flower

Flower est l'ERP CRM développé par l'équipe SI de Ouest INSA.
Cette application est hébergée sur un VPS mis à disposition par la DSI.

## Architecture du projet

Le projet est divisé en deux parties principales:
- flower_backend : le backend Django qui gère la logique métier, la base de données et les API REST.
- flower_frontend : le frontend Vue.js qui gère l'interface utilisateur et les interactions.

Flower utilise également Google Auth pour l'authentification avec les comptes Google.

## Pré-requis

- Node.js et npm (gestionnaire de paquets Node)
- Python3 et pip (gestionnaire de paquets Python)
- MySQL ou MariaDB
- Éditeur de code (Visual Studio Code, PyCharm, WebStorm, ...)

## Installation en local

### Configuration de la base de données

Se connecter en ligne de commande à MySQL:

```bash
mysql -u <username> -p
```
Après avoir saisi votre mot de passe, créer une base de données pour Flower:

```sql
CREATE DATABASE flower;
```

### Configuration de l'application

- Cloner ce dépôt GitLab.
- Dans flower_frontend, exécuter `npm install`.
- Ajouter un fichier `.env` dans flower_frontend avec le contenu suivant:
    ```
    VUE_APP_SITE_URL=http://127.0.0.1:8000
    WINDOW_LOCATION_HREF=http://127.0.0.1:8000/accounts/google/login/
    ```    

Dans flower_backend, exécuter `pip install -r requirements.txt`.
- Ajouter dans le même dossier un fichier `.env` pour les variables d'environnement avec le contenu suivant:
    ```
    DEBUG=True
    LOGIN_REDIRECT_URL=http://127.0.0.1:8080/
    DATABASE_NAME=flower
    DATABASE_USER=django
    DATABASE_PASSWORD=coucou
    FRONTEND_URL=http://localhost:8080
    DOCTYPES_LOCATION=flower/flower_backend/doctypes/
    USE_X_FORWARDED_HOST=False
    SECURE_PROXY_SSL_HEADER=None
    SITE_ID=3
    ALLOWED_HOSTS=[]
    CORS_ALLOWED_ORIGINS=["http://localhost:8080","http://127.0.0.1:8080"]
    CSRF_TRUSTED_ORIGINS=['http://localhost:8080','http://127.0.0.1:8080','http://127.0.0.1:8000']
    STATIC_URL=static/
    API_TOKEN='API_TOKEN'
    PROJECT_ID=3115
    SLACK_TOKEN='SLACK_TOKEN'
    ```

Il faut à présent peupler la base de données avec un set de données initiales.
Exécuter dans flower_backend:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata fixture.json
```

### Lancer l'application
- Lancer le serveur Django dans flower_backend:
```bash
python3 manage.py runserver
```
- Lancer le serveur de développement Vue dans flower_frontend:
```bash
npm run serve
```

## Installation sur le VPS pour les utilisateurs et la production

Se connecter au VPN de l'INSA Rennes. Les utilisateurs administrateurs ont accès au VPS.
Pour ajouter un nouvel utilisateur, il faut faire un ticket à la DSI.

L'installation de Flower sur le VPS est quasi identique à l'installation en local.
L'emplacement du projet est dans '/var/http/flower'.

Cloner le dépôt GitHub dans ce dossier. Pour les accès root à la base de données, les identifiants sont dans le keypass de la SI.
Il faut également ajouter les variables d'environnement pour les deux fichiers.

### Configuration supplémentaire (Déploiement)

Nginx est le point d'entrée au VPS qui reçoit les requêtes HTTP.
Chaque application a son propre fichier nginx dans `/etc/nginx/sites-available/`.

Pour activer un site, il faut créer un lien symbolique dans `/etc/nginx/sites-enabled/`:
```bash
sudo ln -s /etc/nginx/sites-available/flower /etc/nginx/sites-enabled/
```

La configuration Nginx n'est pas forcément évidente, il faut se référer aux fichiers de configuration déjà existants.

La configuration Nginx va pointer par défaut sur les fichiers de build de Vue.js.
Il faut donc construire l'application Vue.js pour la production:
```bash
cd /var/http/flower/flower_frontend
npm run build
```
Ça va créer un dossier `dist` qui contient les fichiers statiques.

Pour que le backend reste actif en permanence, il faut créer un service systemd dans `/etc/systemd/system/flower.service`.

Pour démarrer le service:
```bash
sudo systemctl start flower
```

## Mise à jour du projet sur le VPS

Pour mettre à jour le projet, il faut se rendre dans `/var/http/flower` et faire un `git pull`.
Si le frontend a été modifié, il faut refaire un `npm run build` dans le dossier flower_frontend.
Si le backend a été modifié, il faut redémarrer le service:
```bash
sudo systemctl restart flower
```

Si des modifications ont été faites dans les modèles de données, il faut faire une migration:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
sudo systemctl restart flower
```

ATTENTION: Certains changements majeurs dans le modèle de données peuvent entraîner des conflits de migration/relations et peuvent être difficiles à résoudre.
Il est conseillé de faire une copie de la base de données avant toute migration majeure:
```bash
mysqldump -u <username> -p flower > flower_backup.sql
```
Cela crée une copie dans votre home.

## Pour développer Flower

Si possible, créer une branche numérotée pour chaque nouvelle fonctionnalité. Ça permet de séparer les développements en cours.
Merge les branches dans la branche develop (penser à squash les commits pour qu'on ait la correspondance 1 branche, 1 numéro, 1 fonctionnalité)
