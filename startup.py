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
