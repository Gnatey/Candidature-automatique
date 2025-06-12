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
