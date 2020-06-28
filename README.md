# Descripció
Aquest repositori conté una eina web desenvolupada amb Django per tal d'autogestionar-nos el
contingut del servidor multimèdia. A part del formulari per pujar fitxers i el taulell per
administrar-ho també ha d'integrar l'API.

# Codi font
Tots els fitxers d'aquest repositori, excepte que s'indiqui el contrari, estan llicenciats
sota la **GNU Affero General Public License 3**, o qualsevol versió posterior.

# Instal·lació
## Desenvolupament
Instruccions per preparar l'entorn de desenvolupament.
1. Crear el fitxer `VideoManager/settings_secret.py`:
```python
# Create a settings_secret.py for DB credentials following this format:
SECRET_KEY_SAVED = 'SECRET_KEY'
DATABASE_MYSQL = 'DBName'
USER_NAME = 'user'
PASSWORD = 'password'
HOST = '127.0.0.1'
AUTH_LDAP_BIND_PASSWORD = 'LDAP_PASSWORD'
```
2. Crear els directoris `migrations`:
```
mkdir dashboard/migrations
touch dashboard/migrations/__init__.py
```
3. Instal·lar el programari:
```bash
sudo apt install docker.io
```
4. Construir la imatge del Docker:
```bash
docker build --tag=xarxacat-video .
```
5. Crear el contenidor:
```bash
docker run -it -p 8000:8000 -v $(pwd):/app xarxacat-video
```

## Producció
El VideoManager utilitza dos serveis separats per funcionar:

* **VideoManager:** és el gestor (Django) com a tal. Dona accés a la web, etc.
* **QClusterVideoManager:** s'ocupa de codificar vídeos en segon pla (django-q).

Tots dos fitxers i la configuració del servidor web (nginx) es troben al directori `prod-files`.