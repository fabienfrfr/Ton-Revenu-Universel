<!--
© 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info

SPDX-License-Identifier: CC-BY-SA-4.0+
SPDX-FileContributor:    Fabien FURFARO
-->

# **📌 Guide de déploiement**
- **Projet : Ton-Revenu-Universel**
- **Licence : Apache 2.0**
- **Copyright : 2025 Mouvement Français pour un Revenu de Base ([revenudebase.info](http://www.revenudebase.info))**

## **📋 Table des Matières**
1. [Prérequis](#-prérequis)
2. [Accès au Serveur](#-accès-au-serveur)
3. [Configuration des Secrets](#-configuration-des-secrets)
4. [Déploiement avec Docker](#-déploiement-avec-docker)
5. [Reverse Proxy et HTTPS](#-reverse-proxy-et-https)
6. [Maintenance et Sécurité](#-maintenance-et-sécurité)
7. [Cas d'Usage Spécifiques](#-cas-dusage-spécifiques)
8. [FAQ](#-faq)

---

## **🛠 Prérequis**
### **1. Environnement Nécessaire**
- **Un serveur** (Raspberry Pi, VPS, serveur dédié) avec :
  - **Système d'exploitation** : Debian/Ubuntu/Raspberry Pi OS.
  - **Docker** (≥ 20.10) et **Docker Compose** (≥ 1.29).
  - **Git** pour cloner le dépôt.
  - **Accès SSH** (avec une clé publique configurée).
  - **Un nom de domaine** (optionnel, mais recommandé pour HTTPS).
- **Un reverse proxy** (Traefik, Nginx, Caddy) pour gérer le trafic HTTP/HTTPS.
- **Un certificat SSL** (Let’s Encrypt recommandé).

---
### **2. Clé SSH**
Génère une paire de clés SSH (si ce n’est pas déjà fait) :
```bash
ssh-keygen -t ed25519 -C "ton_email@example.com"
```

Ta clé publique est dans `~/.ssh/id_ed25519.pub`.

- **Copie ta clé publique** sur le serveur :
  ```bash
  ssh-copy-id utilisateur@adresse_ip_ou_domaine
  ```
  *(Remplace `utilisateur` et `adresse_ip_ou_domaine` par les valeurs **de ton serveur**.)*

#### Home Server (ex: Raspberry-Pi)

La clé publique peut etre envoyé par mail à la personne concerné.

La personne doit ajouter ta clé publique au fichier `~/.ssh/authorized_keys`


#### Configurer la clé dans le cloud (ex: OVH)

Sur l’interface OVH, ajoute ta clé publique dans SSH Keys (dans la section "Serveur" > "SSH").


---
## **🔑 Accès au Serveur**
### **1. Se Connecter en SSH**
#### **Pour une adresse IPv4** :
```bash
ssh utilisateur@adresse_ipv4 -p 22
```
*(Remplace `utilisateur` et `adresse_ipv4` par les valeurs de ton serveur.)*

#### **Pour une adresse IPv6** :
```bash
ssh utilisateur@[adresse_ipv6] -p 22
```
*(Les crochets `[]` sont **obligatoires** pour les adresses IPv6. Remplace `adresse_ipv6` par l’adresse réelle.)*

---
### **2. Installer les Dépendances**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose git
sudo systemctl enable docker
sudo systemctl start docker
```

---
## **🔒 Configuration des Secrets**
### **1. Créer le Fichier `.env`**
Crée un fichier `.env` à la racine du projet :
```bash
nano .env
```
- Ajoute les variables suivantes (remplace les valeurs par les tiennes) :
  ```text
  # Base de données
  DB_USER=nom_utilisateur_bdd
  DB_PASSWORD=mot_de_passe_secure  # Généré via `openssl rand -base64 32`
  DB_NAME=nom_base_de_donnees

  # URLs
  FRONTEND_URL=http://localhost  # ou https://ton-domaine.com
  BACKEND_URL=http://backend:8000
  ```
- **Protège le fichier** :
  ```bash
  chmod 600 .env
  ```

---
### **2. Générer un Mot de Passe Sécurisé**
```bash
openssl rand -base64 32
```
*(Copie-colle le résultat dans `.env` pour `DB_PASSWORD`.)*

---
### **(Alternative). Utilisation de Docker Swarm**

TODO

---
## **🚀 Déploiement avec Docker**
### **1. Cloner le Dépôt**
```bash
git clone https://example.com/ton-org/ton-revenu-universel.git
cd ton-revenu-universel
```
*(Remplace l’URL par celle de ton dépôt GitHub/Codeberg.)*

---
### **2. Fichier `docker-compose.yml` Générique**
Changer dans le docker-compose (TODO ?) :
```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
    networks:
      - internal
    restart: unless-stopped

  frontend:
    build: ./frontend
    environment:
      - BACKEND_URL=${BACKEND_URL}
    networks:
      - internal
      - traefik_public
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`ton-domaine.com`)"  # Remplace par ton domaine
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"
    restart: unless-stopped

  db:
    image: postgres:13-alpine  # Version légère pour Raspberry Pi/VPS
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    restart: unless-stopped

  traefik:  # Reverse proxy avec Let’s Encrypt
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=ton_email@example.com"  # Remplace par ton email
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "./letsencrypt:/letsencrypt"
    networks:
      - traefik_public
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  internal:    # Réseau privé pour backend/db
  traefik_public:  # Réseau pour Traefik (exposé sur Internet)
```

---
### **3. Lancer le Déploiement**
```bash
docker-compose up -d --build
```
- **Vérifier les logs** :
  ```bash
  docker-compose logs -f
  ```

---
## **🌐 Reverse Proxy et HTTPS**
### **1. Configurer Traefik**
- Traefik est **déjà configuré** dans le `docker-compose.yml` ci-dessus.
- Il gère automatiquement :
  - Le **routing** vers le frontend/backend.
  - La **génération de certificats SSL** via Let’s Encrypt.

---
### **2. Configurer un Nom de Domaine**
1. **Sur ton registrar** (OVH, Gandi, Cloudflare, etc.) :
   - Ajoute un enregistrement `A` (IPv4) ou `AAAA` (IPv6) pointant vers l’adresse IP de ton serveur.
2. **Dans `docker-compose.yml`** :
   - Remplace `ton-domaine.com` par ton **nom de domaine réel**.

---
### **3. Accéder à l’Application**
- **Frontend** : `https://ton-domaine.com`
- **Backend** : `https://ton-domaine.com/api/`
- **En local** : `http://localhost:80`

---
## **🔧 Maintenance et Sécurité**
### **1. Sauvegardes**
#### **Base de données** :
```bash
docker exec db pg_dump -U ${DB_USER} ${DB_NAME} > backup_$(date +%Y-%m-%d).sql
```
#### **Automatiser avec cron** :
```bash
crontab -e
```
Ajoute cette ligne pour des sauvegardes quotidiennes :
```text
0 3 * * * docker exec db pg_dump -U ${DB_USER} ${DB_NAME} > /chemin/vers/backups/backup_$(date +\%Y-\%m-\%d).sql
```

---
### **2. Mises à Jour**
```bash
git pull origin main
docker-compose pull
docker-compose up -d --build
```

---
### **3. Sécurité**
- **Ferme les ports inutiles** sur le serveur (seuls 80/443 doivent être ouverts).
- **Désactive l’accès root en SSH** :
  ```bash
  sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
  sudo systemctl restart sshd
  ```
- **Met à jour Docker et le système** régulièrement :
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```

---
## **📌 Cas d'Usage Spécifiques**
### **1. Déploiement sur Raspberry Pi**
- **Utilise `postgres:13-alpine`** (version légère optimisée pour les architectures ARM).
- **Vérifie la compatibilité IPv6** :
  - Si ton FAI ne supporte pas IPv6, utilise un **tunnel IPv6** (ex: [Hurricane Electric](https://tunnelbroker.net/)).
  - Ou configure un **reverse proxy externe** (ex: Cloudflare Tunnel).

---
### **2. Déploiement sur un VPS (OVH, DigitalOcean, etc.)**
- **Configure le firewall** pour n’ouvrir que les ports 80/443 :
  ```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```
- **Utilise un reverse proxy** (Traefik/Nginx) pour sécuriser l’accès.

---
### **3. Déploiement Local (Test)**
- **Supprime la section `traefik`** du `docker-compose.yml`.
- **Accède au frontend** via `http://localhost:80`.


---
## **📬 Support**
Pour toute question :
- **Ouvrir une issue** sur [GitHub/Codeberg](https://example.com/ton-org/ton-revenu-universel/issues).
- **Email** : ton_email@example.com
