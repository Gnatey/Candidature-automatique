# config.py
"""
Configuration du système de candidature automatique
"""

import os
from pathlib import Path

# =============================================================================
# CONFIGURATION GÉNÉRALE
# =============================================================================

# Répertoire de travail
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
CV_DIR = BASE_DIR / "cv_templates"

# Création des dossiers s'ils n'existent pas
for directory in [DATA_DIR, LOGS_DIR, CV_DIR]:
    directory.mkdir(exist_ok=True)

# =============================================================================
# CONFIGURATION API
# =============================================================================

# OpenAI (obligatoire pour l'adaptation du CV)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    print("⚠️  ATTENTION: Clé OpenAI manquante. Définissez OPENAI_API_KEY dans vos variables d'environnement")

# =============================================================================
# CONFIGURATION RECHERCHE D'EMPLOI
# =============================================================================

# Profil de recherche de Juliana
SEARCH_PROFILES = {
    "data_scientist": {
        "keywords": "data scientist python machine learning",
        "location": "Île-de-France",
        "exclude_keywords": ["stage", "intern", "bénévole", "freelance"],
        "min_salary": 40000,  # Salaire minimum attendu
        "max_pages_per_site": 5
    },
    
    "scrum_master": {
        "keywords": "scrum master agile project manager",
        "location": "Île-de-France", 
        "exclude_keywords": ["stage", "intern", "bénévole"],
        "min_salary": 45000,
        "max_pages_per_site": 3
    },
    
    "data_analyst": {
        "keywords": "data analyst business intelligence power bi",
        "location": "Île-de-France",
        "exclude_keywords": ["stage", "intern", "bénévole"],
        "min_salary": 35000,
        "max_pages_per_site": 4
    }
}

# Profil par défaut
DEFAULT_PROFILE = "data_scientist"

# =============================================================================
# CONFIGURATION SITES DE RECHERCHE
# =============================================================================

SITES_CONFIG = {
    "indeed": {
        "enabled": True,
        "base_url": "https://fr.indeed.com/jobs",
        "priority": 1,  # Plus prioritaire
        "delay_between_requests": (2, 5),  # secondes (min, max)
    },
    
    "linkedin": {
        "enabled": False,  # Nécessite une connexion
        "base_url": "https://www.linkedin.com/jobs/search/",
        "priority": 2,
        "delay_between_requests": (3, 7),
    },
    
    "welcome_to_the_jungle": {
        "enabled": True,
        "base_url": "https://www.welcometothejungle.com/fr/jobs",
        "priority": 3,
        "delay_between_requests": (2, 4),
    }
}

# =============================================================================
# CONFIGURATION CANDIDATURE
# =============================================================================

APPLICATION_CONFIG = {
    # Délais pour éviter la détection
    "delay_between_applications": {
        "min": 30,  # secondes
        "max": 120,
        "variation": 0.2  # Variation aléatoire ±20%
    },
    
    # Limites journalières
    "daily_limits": {
        "max_applications_per_day": 50,
        "max_applications_per_hour": 10,
        "pause_after_applications": 5,  # Pause après X candidatures
        "pause_duration": 300  # Durée de pause en secondes
    },
    
    # Filtres qualité
    "quality_filters": {
        "min_description_length": 200,  # Caractères minimum dans la description
        "exclude_companies": [],  # Entreprises à éviter
        "require_salary": False,  # Exiger que le salaire soit mentionné
        "max_application_age_days": 7  # Ne pas postuler aux offres de plus de 7 jours
    }
}

# =============================================================================
# CONFIGURATION CV
# =============================================================================

CV_CONFIG = {
    # Template de base (sera adapté pour chaque offre)
    "base_template_path": CV_DIR / "juliana_base_cv.txt",
    
    # Sections adaptables
    "adaptable_sections": {
        "title": True,  # Titre du poste recherché
        "skills": True,  # Ordre et emphase des compétences
        "experience_descriptions": True,  # Reformulation des expériences
        "keywords_integration": True  # Intégration naturelle des mots-clés
    },
    
    # Règles d'adaptation
    "adaptation_rules": {
        "keep_structure": True,  # Garder la structure originale
        "max_keywords_per_section": 5,  # Max mots-clés à intégrer par section
        "synonym_replacement": True,  # Remplacer par des synonymes
        "preserve_achievements": True  # Garder les chiffres et résultats
    }
}

# =============================================================================
# CONFIGURATION BASE DE DONNÉES
# =============================================================================

DATABASE_CONFIG = {
    "path": DATA_DIR / "jobs.db",
    "backup_frequency": "daily",  # daily, weekly
    "cleanup_old_jobs_days": 90,  # Supprimer les jobs de plus de 90 jours
    "export_formats": ["csv", "excel"]  # Formats d'export disponibles
}

# =============================================================================
# CONFIGURATION LOGS
# =============================================================================

LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "file_path": LOGS_DIR / "job_automation.log",
    "max_file_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# =============================================================================
# CONFIGURATION SELENIUM
# =============================================================================

SELENIUM_CONFIG = {
    "headless": True,  # Mode sans interface graphique
    "window_size": (1920, 1080),
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "implicit_wait": 10,  # Attente implicite en secondes
    "page_load_timeout": 30,  # Timeout de chargement de page
    "download_dir": DATA_DIR / "downloads"
}

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_profile_config(profile_name: str = None) -> dict:
    """Récupère la configuration d'un profil de recherche"""
    if profile_name is None:
        profile_name = DEFAULT_PROFILE
    
    return SEARCH_PROFILES.get(profile_name, SEARCH_PROFILES[DEFAULT_PROFILE])

def validate_config() -> bool:
    """Valide la configuration"""
    errors = []
    
    # Vérification des clés API
    if not OPENAI_API_KEY:
        errors.append("Clé OpenAI manquante")
    
    # Vérification des fichiers requis
    if not CV_CONFIG["base_template_path"].exists():
        errors.append(f"Template CV manquant: {CV_CONFIG['base_template_path']}")
    
    # Vérification des profils
    if not SEARCH_PROFILES:
        errors.append("Aucun profil de recherche défini")
    
    if errors:
        print("❌ Erreurs de configuration:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Configuration valide")
    return True

# startup.py
"""
Script de démarrage du système de candidature automatique
"""

import sys
import argparse
from pathlib import Path
import logging
from config import *
from job_automation_system import JobAutomationSystem
import subprocess

def setup_logging():
    """Configure le système de logging"""
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["file_path"]),
            logging.StreamHandler(sys.stdout)
        ]
    )

def create_cv_template():
    """Crée le template de CV s'il n'existe pas"""
    cv_path = CV_CONFIG["base_template_path"]
    
    if not cv_path.exists():
        print(f"📝 Création du template CV: {cv_path}")
        
        cv_content = """JULIANA NIAPOH
CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE

CONTACT
📍 93300, Aubervilliers | 🕒 Disponibilité : Octobre 2025
📧 Jniapoh@gmail.com | 📞 0622855341
🔗 LinkedIn | Portfolio/website

EXPÉRIENCES PROFESSIONNELLES

Alternance Assistante cheffe de projet numérique (2024/2025)
SNCF, Saint-Denis - FERROVIAIRE
• Coordination de projets IT en mode Agile (Scrum), pilotage de projets de transformation numérique
• Gestion d'un portail collaboratif pour la médecine du travail, réduisant les délais de communication de 30%
• Support utilisateur niveau 3 et résolution d'incidents complexes
• Animation de formations techniques et fonctionnelles pour les nouveaux outils déployés

Alternance Chargée de projet Digital (2022/2023)
ORANO, Châtillon - ÉNERGIE NUCLÉAIRE
• Analyse et optimisation des flux de données existants
• Développement de solutions de données et coordination des équipes
• Formation des équipes à l'utilisation des nouveaux outils de visualisation
• Création de guides et documentation utilisateur

FORMATION
Master Data Management (2023/2025) - Paris School of Business, Paris
Bachelor E-commerce & Marketing numérique (2022/2023) - Paris School of Business, Paris
DUT Statistiques & Informatiques Décisionnelles (2020/2022) - Université Sorbonne Paris Nord

COMPÉTENCES TECHNIQUES
• Langages: Python, SQL, R, JavaScript, HTML/CSS
• Machine Learning: Scikit-learn, algorithmes prédictifs, NLP
• Data Visualisation: Power BI, Tableau de bord, Jupyter Notebook
• Big Data: Analyse de grands ensembles de données, nettoyage de données
• Gestion de Projet: Méthode Agile (Scrum, Kanban), Jira, Trello
• Bases de Données: Requêtes complexes, optimisation, migration

PROJETS ACADÉMIQUES
• Base de données SQL WorkBench: Conception et optimisation d'une base de données relationnelle
• IA Student Assistance: Développement d'une solution d'assistance étudiante basée sur l'IA (NLP)
• Tableau de bord RH (Python): Outil de visualisation des données RH avec Python (Pandas, Matplotlib, Streamlit)

SOFT SKILLS
• Esprit d'analyse et résolution de problèmes complexes
• Collaboration en équipe et coordination
• Adaptabilité et gestion du changement
• Communication et formation d'équipes"""
        
        with open(cv_path, 'w', encoding='utf-8') as f:
            f.write(cv_content)
        
        print("✅ Template CV créé avec succès")

def run_dashboard():
    """Lance le dashboard web"""
    print("🚀 Lancement du dashboard web...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erreur lors du lancement du dashboard")
        print("Installez streamlit: pip install streamlit")

def run_automation(profile: str, dry_run: bool = False):
    """Lance l'automatisation"""
    print(f"🤖 Démarrage de l'automatisation avec le profil: {profile}")
    
    if not validate_config():
        return False
    
    profile_config = get_profile_config(profile)
    
    if dry_run:
        print("🧪 Mode DRY RUN - Aucune candidature ne sera envoyée")
        print(f"Configuration utilisée: {profile_config}")
        return True
    
    try:
        system = JobAutomationSystem(OPENAI_API_KEY)
        system.run_full_cycle(
            search_keywords=profile_config["keywords"],
            location=profile_config["location"]
        )
        
        # Affichage des résultats
        dashboard_data = system.get_dashboard_data()
        print("\n📊 RÉSULTATS:")
        print(f"Total offres scrapées: {dashboard_data['total_jobs']}")
        print(f"Candidatures envoyées: {dashboard_data['applied']}")
        print(f"Réponses reçues: {dashboard_data['responded']}")
        
        return True
        
    except Exception as e:
        logging.error(f"Erreur lors de l'automatisation: {e}")
        return False
    finally:
        if 'system' in locals():
            system.cleanup()

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Système de candidature automatique")
    
    parser.add_argument("command", choices=["dashboard", "run", "setup", "validate"], 
                       help="Commande à exécuter")
    
    parser.add_argument("--profile", default=DEFAULT_PROFILE,
                       choices=list(SEARCH_PROFILES.keys()),
                       help="Profil de recherche à utiliser")
    
    parser.add_argument("--dry-run", action="store_true",
                       help="Mode test sans envoi de candidatures")
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging()
    
    print("🤖 Système de Candidature Automatique - Juliana Niapoh")
    print("=" * 60)
    
    if args.command == "setup":
        print("⚙️  Configuration initiale...")
        create_cv_template()
        validate_config()
        print("\n✅ Configuration terminée!")
        print("\nCommandes disponibles:")
        print("  - python startup.py dashboard  # Lance l'interface web")
        print("  - python startup.py run        # Lance l'automatisation")
        print("  - python startup.py validate   # Valide la configuration")
    
    elif args.command == "validate":
        validate_config()
    
    elif args.command == "dashboard":
        run_dashboard()
    
    elif args.command == "run":
        success = run_automation(args.profile, args.dry_run)
        if not success:
            sys.exit(1)
    
    print("\n🎉 Terminé!")

if __name__ == "__main__":
    main()

# requirements.txt
"""
Dépendances Python nécessaires
"""

# Web scraping
selenium==4.15.2
beautifulsoup4==4.12.2
requests==2.31.0

# Data processing
pandas==2.1.3
numpy==1.24.3

# AI/ML
openai==0.28.1
scikit-learn==1.3.2

# Database
sqlite3  # Inclus dans Python

# Dashboard
streamlit==1.28.1
plotly==5.17.0

# Utilities
python-dotenv==1.0.0
pathlib  # Inclus dans Python

# Development
pytest==7.4.3
black==23.11.0

# install.bat (pour Windows)
@echo off
echo Installation du systeme de candidature automatique
echo ==================================================

echo Installation des dependances Python...
pip install -r requirements.txt

echo Verification de Chrome et ChromeDriver...
echo ATTENTION: Vous devez installer ChromeDriver manuellement
echo Telechargez-le sur: https://chromedriver.chromium.org/
echo Et placez-le dans votre PATH

echo Configuration initiale...
python startup.py setup

echo Installation terminee!
echo Lancez le dashboard avec: python startup.py dashboard
pause

# install.sh (pour Linux/Mac)
#!/bin/bash
echo "Installation du système de candidature automatique"
echo "=================================================="

echo "Installation des dépendances Python..."
pip install -r requirements.txt

echo "Vérification de Chrome et ChromeDriver..."
if ! command -v google-chrome &> /dev/null; then
    echo "ATTENTION: Google Chrome n'est pas installé"
fi

if ! command -v chromedriver &> /dev/null; then
    echo "ATTENTION: ChromeDriver n'est pas installé"
    echo "Installez-le avec: sudo apt-get install chromium-chromedriver"
fi

echo "Configuration initiale..."
python startup.py setup

echo "Installation terminée!"
echo "Lancez le dashboard avec: python startup.py dashboard"
