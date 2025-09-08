# On part d'une image Python officielle et légère
FROM python:3.10-slim

# On définit des variables d'environnement pour éviter les questions interactives
# et on s'assure que le système utilise l'encodage UTF-8 partout
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

#
# === L'ÉTAPE D'INSTALLATION UNIQUE ET COMPLÈTE POUR LA V1 ===
#
RUN apt-get update && apt-get install -y \
    # 1. Le convertisseur de documents universel
    pandoc \
    \
    # 2. Le moteur LaTeX le plus moderne (pour images, polices, et Unicode)
    texlive-luatex \
    \
    # 3. Les paquets LaTeX essentiels (structure, tables des matières, etc.)
    texlive-latex-base \
    texlive-latex-extra \
    \
    # 4. Les paquets pour la gestion avancée des images (includegraphics, etc.)
    texlive-pictures \
    \
    # 5. Les polices LaTeX recommandées
    texlive-fonts-recommended \
    \
    # 6. Une police complète pour les emojis et caractères spéciaux
    fonts-noto-color-emoji \
    \
    # On supprime le cache à la fin pour garder l'image légère
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# On prépare l'environnement pour notre application
WORKDIR /app

# On installe les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste de notre code
COPY . .