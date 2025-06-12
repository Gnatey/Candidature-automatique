# 🤖 Système de Candidature Automatique

**Automatisez votre recherche d'emploi avec l'IA : scraping d'offres, adaptation du CV et candidatures automatiques.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)

## 📋 Fonctionnalités

- ✅ **Scraping multi-plateformes** (Indeed, LinkedIn, Welcome to the Jungle)
- ✅ **Adaptation automatique du CV** via IA selon chaque offre
- ✅ **Candidatures automatiques** avec délais anti-détection
- ✅ **Dashboard interactif** pour suivre vos candidatures
- ✅ **Base de données intégrée** pour tracker les offres
- ✅ **Filtres intelligents** (salaire, mots-clés, localisation)
- ✅ **Métriques en temps réel** (taux de réponse, statistiques)

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- Google Chrome + ChromeDriver
- Clé API OpenAI

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/candidature-automatique.git
cd candidature-automatique
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration
```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer avec vos paramètres
nano .env
```

### 4. Configuration initiale
```bash
python startup.py setup
```

### 5. Lancer le dashboard
```bash
python startup.py dashboard
```

## ⚙️ Configuration

### Variables d'environnement (.env)
```bash
# API OpenAI (obligatoire)
OPENAI_API_KEY=sk-your-key-here

# Configuration optionnelle
DEFAULT_LOCATION=Île-de-France
MAX_APPLICATIONS_PER_DAY=50
```

### Profils de recherche
Le système inclut 3 profils pré-configurés :
- **data_scientist** : Data Scientist, Machine Learning, Python
- **scrum_master** : Scrum Master, Agile, Project Manager  
- **data_analyst** : Data Analyst, Business Intelligence, Power BI

## 🎯 Utilisation

### Mode Dashboard (Interface Web)
```bash
python startup.py dashboard
```
Accédez à http://localhost:8501 pour l'interface complète.

### Mode Automatique (Ligne de commande)
```bash
# Lancer avec le profil data_scientist
python startup.py run --profile data_scientist

# Mode test (pas de vraies candidatures)
python startup.py run --profile data_scientist --dry-run

# Validation de la configuration
python startup.py validate
```

## 📊 Dashboard

Le dashboard web offre :
- **Métriques en temps réel** : offres scrapées, candidatures envoyées, taux de réponse
- **Graphiques d'évolution** sur 30 jours
- **Liste des offres** avec filtres avancés
- **Contrôles start/stop** du système
- **Logs en temps réel**

## 🧠 Comment ça marche

### 1. Scraping Intelligent
- Parcourt Indeed, LinkedIn, Welcome to the Jungle
- Extrait : titre, entreprise, description, salaire, localisation
- Filtre selon vos critères (salaire minimum, mots-clés exclus)

### 2. Adaptation du CV
- Analyse chaque offre avec l'IA OpenAI
- Extrait les mots-clés techniques importants
- Reformule votre CV avec le vocabulaire de l'offre
- Garde la même structure, adapte seulement le contenu

### 3. Candidature Automatique  
- Délais aléatoires pour éviter la détection
- Remplissage automatique des formulaires
- Sauvegarde de toutes les actions en base

### 4. Suivi et Analytics
- Base de données SQLite pour tracker tout
- Métriques de performance (taux de réponse, etc.)
- Export des données en CSV/Excel

## 📁 Structure du Projet

```
candidature-automatique/
├── README.md                           # Documentation
├── requirements.txt                    # Dépendances Python
├── .env.example                       # Variables d'environnement
├── startup.py                         # Script de démarrage
├── config.py                          # Configuration globale
├── job_automation_system.py           # Système principal
├── dashboard.py                       # Interface Streamlit
├── templates/
│   └── cv_base.txt                   # Template CV
├── data/
│   └── jobs.db                       # Base de données
└── logs/
    └── job_automation.log            # Logs système
```

## 🔧 Personnalisation

### Adapter pour votre profil
1. Modifiez `templates/cv_base.txt` avec votre CV
2. Ajustez les profils dans `config.py`
3. Configurez vos critères de recherche

### Ajouter de nouveaux sites
1. Créez un nouveau scraper dans `job_automation_system.py`
2. Ajoutez la configuration dans `SITES_CONFIG`
3. Implémentez la logique de candidature

## ⚠️ Important - Utilisation Responsable

- **Respectez les CGU** des sites de recherche d'emploi
- **Utilisez des délais** pour éviter la surcharge des serveurs
- **Personnalisez vos candidatures** autant que possible
- **Vérifiez** les candidatures importantes manuellement

## 🐛 Dépannage

### Problèmes courants

**ChromeDriver non trouvé**
```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver

# Windows : télécharger sur https://chromedriver.chromium.org/
```

**Erreur OpenAI**
- Vérifiez votre clé API dans `.env`
- Assurez-vous d'avoir du crédit sur votre compte OpenAI

**Selenium TimeoutException** 
- Vérifiez votre connexion internet
- Certains sites peuvent bloquer l'automatisation

## 📈 Roadmap

- [ ] Support de plus de sites (Monster, StepStone, etc.)
- [ ] Génération de lettres de motivation personnalisées
- [ ] Intégration avec les calendriers pour le suivi d'entretiens
- [ ] API REST pour intégration externe
- [ ] Mode Docker pour déploiement facile
- [ ] Notifications par email/Slack

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez votre branche feature (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

## ⭐ Support

Si ce projet vous aide dans votre recherche d'emploi, n'hésitez pas à lui donner une étoile ! ⭐

Pour des questions ou du support :
- Ouvrez une [Issue](https://github.com/votre-username/candidature-automatique/issues)
- Consultez la [documentation](docs/)

---

**⚡ Automatisez votre recherche d'emploi et concentrez-vous sur ce qui compte : les entretiens !**
