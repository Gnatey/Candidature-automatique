"""
Configuration du système de candidature automatique - VERSION GRATUITE
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
# CONFIGURATION API (OPTIONNELLE)
# =============================================================================

# OpenAI (optionnel - si pas de clé, utilise l'adaptation basique)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_AI_ADAPTATION = bool(OPENAI_API_KEY)

if not OPENAI_API_KEY:
    print("ℹ️  Mode GRATUIT : Pas de clé OpenAI détectée")
    print("   → Utilisation de l'adaptation basique du CV (gratuite)")
else:
    print("🤖 Mode IA : Clé OpenAI détectée, adaptation intelligente activée")

# =============================================================================
# CONFIGURATION RECHERCHE D'EMPLOI
# =============================================================================

# Profil de recherche de Juliana
SEARCH_PROFILES = {
    "data_scientist": {
        "keywords": "data scientist python machine learning",
        "location": "Île-de-France",
        "exclude_keywords": ["stage", "intern", "bénévole", "freelance"],
        "min_salary": 40000,
        "max_pages_per_site": 5,
        # Mots-clés pour adaptation basique (sans IA)
        "target_keywords": [
            "python", "machine learning", "data science", "sql", "pandas",
            "numpy", "scikit-learn", "tensorflow", "pytorch", "jupyter",
            "matplotlib", "seaborn", "plotly", "power bi", "tableau",
            "big data", "analytics", "statistics", "deep learning",
            "nlp", "computer vision", "ai", "artificial intelligence"
        ]
    },
    
    "scrum_master": {
        "keywords": "scrum master agile project manager",
        "location": "Île-de-France", 
        "exclude_keywords": ["stage", "intern", "bénévole"],
        "min_salary": 45000,
        "max_pages_per_site": 3,
        "target_keywords": [
            "scrum", "agile", "kanban", "jira", "confluence", "sprint",
            "backlog", "product owner", "stakeholder", "ceremonies",
            "retrospective", "planning", "daily", "review", "safe",
            "scaled agile", "project management", "team management"
        ]
    },
    
    "data_analyst": {
        "keywords": "data analyst business intelligence power bi",
        "location": "Île-de-France",
        "exclude_keywords": ["stage", "intern", "bénévole"],
        "min_salary": 35000,
        "max_pages_per_site": 4,
        "target_keywords": [
            "power bi", "tableau", "excel", "sql", "business intelligence",
            "dashboard", "reporting", "kpi", "analytics", "data visualization",
            "etl", "data warehouse", "qlik", "looker", "google analytics"
        ]
    }
}

# Profil par défaut
DEFAULT_PROFILE = "data_scientist"

# =============================================================================
# CONFIGURATION ADAPTATION CV (GRATUITE)
# =============================================================================

# Adaptation basique sans IA (gratuite)
CV_ADAPTATION_CONFIG = {
    "use_ai": USE_AI_ADAPTATION,
    
    # Règles d'adaptation basique (sans IA)
    "basic_adaptation": {
        "emphasize_matching_keywords": True,  # Met en avant les mots-clés qui matchent
        "reorder_skills": True,  # Réorganise l'ordre des compétences
        "adapt_title": True,  # Adapte le titre du poste recherché
        "max_keywords_to_emphasize": 5,
        
        # Synonymes pour enrichir (sans IA)
        "synonyms": {
            "python": ["Python", "programmation Python", "développement Python"],
            "sql": ["SQL", "bases de données", "requêtes SQL"],
            "machine learning": ["Machine Learning", "ML", "apprentissage automatique"],
            "data science": ["Data Science", "science des données", "analyse de données"],
            "agile": ["Agile", "méthodologie Agile", "gestion Agile"],
            "scrum": ["Scrum", "framework Scrum", "méthode Scrum"],
            "power bi": ["Power BI", "Microsoft Power BI", "tableaux de bord"]
        }
    }
}

# =============================================================================
# CONFIGURATION SITES DE RECHERCHE
# =============================================================================

SITES_CONFIG = {
    "indeed": {
        "enabled": True,
        "base_url": "https://fr.indeed.com/jobs",
        "priority": 1,
        "delay_between_requests": (2, 5),
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
        "variation": 0.2
    },
    
    # Limites journalières
    "daily_limits": {
        "max_applications_per_day": 50,
        "max_applications_per_hour": 10,
        "pause_after_applications": 5,
        "pause_duration": 300
    },
    
    # Filtres qualité
    "quality_filters": {
        "min_description_length": 200,
        "exclude_companies": [],
        "require_salary": False,
        "max_application_age_days": 7
    }
}

# =============================================================================
# CONFIGURATION CV
# =============================================================================

CV_CONFIG = {
    "base_template_path": CV_DIR / "cv_base.txt",
    
    # Sections adaptables
    "adaptable_sections": {
        "title": True,
        "skills": True,
        "experience_descriptions": True,
        "keywords_integration": True
    },
    
    # Règles d'adaptation
    "adaptation_rules": {
        "keep_structure": True,
        "max_keywords_per_section": 5,
        "synonym_replacement": True,
        "preserve_achievements": True
    }
}

# =============================================================================
# CONFIGURATION BASE DE DONNÉES
# =============================================================================

DATABASE_CONFIG = {
    "path": DATA_DIR / "jobs.db",
    "backup_frequency": "daily",
    "cleanup_old_jobs_days": 90,
    "export_formats": ["csv", "excel"]
}

# =============================================================================
# CONFIGURATION LOGS
# =============================================================================

LOGGING_CONFIG = {
    "level": "INFO",
    "file_path": LOGS_DIR / "job_automation.log",
    "max_file_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# =============================================================================
# CONFIGURATION SELENIUM
# =============================================================================

SELENIUM_CONFIG = {
    "headless": True,
    "window_size": (1920, 1080),
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "implicit_wait": 10,
    "page_load_timeout": 30,
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
    if not USE_AI_ADAPTATION:
        print("ℹ️  Mode adaptation basique (gratuit) activé")
    else:
        print("🤖 Mode adaptation IA activé")
    
    return True

def extract_keywords_basic(job_title: str, job_description: str, profile_keywords: list) -> list:
    """Extraction basique de mots-clés (sans IA)"""
    text = f"{job_title} {job_description}".lower()
    found_keywords = []
    
    for keyword in profile_keywords:
        if keyword.lower() in text:
            found_keywords.append(keyword)
    
    return found_keywords[:10]  # Max 10 mots-clés

def adapt_cv_basic(base_cv: str, keywords: list, profile_config: dict) -> str:
    """Adaptation basique du CV (sans IA)"""
    adapted_cv = base_cv
    
    # Remplace le titre si nécessaire
    if "data scientist" in keywords:
        adapted_cv = adapted_cv.replace(
            "CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE",
            "DATA SCIENTIST | MACHINE LEARNING & INTELLIGENCE ARTIFICIELLE"
        )
    elif "scrum master" in [k.lower() for k in keywords]:
        adapted_cv = adapted_cv.replace(
            "CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE", 
            "SCRUM MASTER | GESTION DE PROJET AGILE & TRANSFORMATION DIGITALE"
        )
    
    # Ajoute les mots-clés trouvés dans une section dédiée
    if keywords:
        keywords_section = f"\n\nMOTS-CLÉS TECHNIQUES RECHERCHÉS\n{', '.join(keywords[:8])}"
        adapted_cv += keywords_section
    
    return adapted_cv
