import os
import json
import pandas as pd
from datetime import datetime
import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import re

# Import configuration
from config import *

@dataclass
class JobOffer:
    """Structure pour stocker une offre d'emploi"""
    id: str
    title: str
    company: str
    location: str
    description: str
    requirements: str
    salary: Optional[str]
    url: str
    source: str
    date_scraped: datetime
    keywords: List[str] = None
    status: str = "scraped"

class JobDatabase:
    """Gestion de la base de données des offres"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DATABASE_CONFIG["path"]
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            requirements TEXT,
            salary TEXT,
            url TEXT,
            source TEXT,
            date_scraped TIMESTAMP,
            keywords TEXT,
            status TEXT DEFAULT 'scraped',
            cv_adapted TEXT,
            application_date TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_job(self, job: JobOffer):
        """Sauvegarde une offre en base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        keywords_str = json.dumps(job.keywords) if job.keywords else None
        
        cursor.execute('''
        INSERT OR REPLACE INTO jobs 
        (id, title, company, location, description, requirements, salary, url, source, date_scraped, keywords, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (job.id, job.title, job.company, job.location, job.description, 
              job.requirements, job.salary, job.url, job.source, job.date_scraped, keywords_str, job.status))
        
        conn.commit()
        conn.close()
    
    def get_jobs_by_status(self, status: str) -> List[JobOffer]:
        """Récupère les offres par statut"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE status = ?', (status,))
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            keywords = json.loads(row[10]) if row[10] else []
            job = JobOffer(
                id=row[0], title=row[1], company=row[2], location=row[3],
                description=row[4], requirements=row[5], salary=row[6],
                url=row[7], source=row[8], date_scraped=row[9],
                keywords=keywords, status=row[11]
            )
            jobs.append(job)
        return jobs

class JobScraper:
    """Scraper pour différentes plateformes d'emploi"""
    
    def __init__(self):
        self.setup_driver()
        self.db = JobDatabase()
    
    def setup_driver(self):
        """Configure le driver Selenium"""
        chrome_options = Options()
        if SELENIUM_CONFIG["headless"]:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={SELENIUM_CONFIG['user_agent']}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_window_size(*SELENIUM_CONFIG["window_size"])
        except Exception as e:
            print(f"❌ Erreur configuration Chrome: {e}")
            print("📝 Installez ChromeDriver: https://chromedriver.chromium.org/")
            raise
    
    def scrape_indeed(self, keywords: str, location: str = "France", max_pages: int = 5):
        """Scrape Indeed"""
        jobs = []
        base_url = f"https://fr.indeed.com/jobs?q={keywords.replace(' ', '+')}&l={location.replace(' ', '+')}"
        
        print(f"🔍 Scraping Indeed: {keywords} à {location}")
        
        for page in range(max_pages):
            try:
                url = f"{base_url}&start={page * 10}"
                print(f"📄 Page {page + 1}/{max_pages}")
                
                self.driver.get(url)
                time.sleep(random.uniform(2, 4))
                
                # Accepter les cookies si nécessaire
                try:
                    cookie_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
                    cookie_button.click()
                    time.sleep(1)
                except:
                    pass
                
                # Récupérer les offres
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                
                for card in job_cards[:5]:  # Limite pour éviter la détection
                    try:
                        job_id = card.get_attribute("data-jk")
                        
                        # Titre
                        title_elem = card.find_element(By.CSS_SELECTOR, "h2 a span")
                        title = title_elem.text.strip()
                        
                        # Entreprise
                        try:
                            company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text.strip()
                        except:
                            company = "Non spécifié"
                        
                        # Localisation
                        try:
                            location_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='job-location']").text.strip()
                        except:
                            location_elem = location
                        
                        # URL de l'offre
                        job_url = f"https://fr.indeed.com/viewjob?jk={job_id}"
                        
                        # Description (récupérée plus tard pour éviter les timeouts)
                        description = f"Offre {title} chez {company}"
                        
                        job = JobOffer(
                            id=f"indeed_{job_id}",
                            title=title,
                            company=company,
                            location=location_elem,
                            description=description,
                            requirements="",
                            salary=None,
                            url=job_url,
                            source="indeed",
                            date_scraped=datetime.now()
                        )
                        
                        jobs.append(job)
                        self.db.save_job(job)
                        print(f"✅ {title} - {company}")
                        
                    except Exception as e:
                        print(f"⚠️  Erreur scraping job: {e}")
                        continue
                
                # Pause entre pages
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"❌ Erreur page {page + 1}: {e}")
                continue
        
        print(f"🎉 Indeed: {len(jobs)} offres récupérées")
        return jobs
    
    def get_job_description(self, job_url: str) -> str:
        """Récupère la description complète d'une offre"""
        try:
            self.driver.get(job_url)
            time.sleep(2)
            
            description_elem = self.driver.find_element(By.ID, "jobDescriptionText")
            return description_elem.text
        except:
            return "Description non disponible"
    
    def close(self):
        """Ferme le driver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class CVAdapterFree:
    """Adapteur de CV GRATUIT (sans IA)"""
    
    def __init__(self):
        self.base_cv = self.load_base_cv()
    
    def load_base_cv(self) -> str:
        """Charge le CV de base depuis un fichier"""
        cv_path = CV_CONFIG["base_template_path"]
        if cv_path.exists():
            with open(cv_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"⚠️  Template CV non trouvé: {cv_path}")
            return "CV non disponible"
    
    def extract_keywords_from_job(self, job: JobOffer, profile_config: dict) -> List[str]:
        """Extrait les mots-clés importants d'une offre (version gratuite)"""
        text = f"{job.title} {job.description}".lower()
        target_keywords = profile_config.get("target_keywords", [])
        
        found_keywords = []
        for keyword in target_keywords:
            if keyword.lower() in text:
                found_keywords.append(keyword)
        
        # Ajouter quelques mots-clés du titre et de la description
        title_words = re.findall(r'\b[a-zA-Z]{4,}\b', job.title.lower())
        for word in title_words:
            if word not in [k.lower() for k in found_keywords] and len(word) > 4:
                found_keywords.append(word)
        
        return found_keywords[:10]  # Max 10 mots-clés
    
    def adapt_cv_for_job(self, job: JobOffer, profile_config: dict) -> str:
        """Adapte le CV pour une offre spécifique (version gratuite)"""
        keywords = self.extract_keywords_from_job(job, profile_config)
        job.keywords = keywords
        
        adapted_cv = self.base_cv
        
        # Adaptation du titre selon le profil
        if any(k.lower() in job.title.lower() for k in ["data scientist", "scientist"]):
            adapted_cv = adapted_cv.replace(
                "CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE",
                "DATA SCIENTIST | MACHINE LEARNING & INTELLIGENCE ARTIFICIELLE"
            )
        elif any(k.lower() in job.title.lower() for k in ["scrum", "agile", "project manager"]):
            adapted_cv = adapted_cv.replace(
                "CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE",
                "SCRUM MASTER | GESTION DE PROJET AGILE & TRANSFORMATION DIGITALE"
            )
        elif any(k.lower() in job.title.lower() for k in ["data analyst", "analyst"]):
            adapted_cv = adapted_cv.replace(
                "CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE",
                "DATA ANALYST | BUSINESS INTELLIGENCE & VISUALISATION DE DONNÉES"
            )
        
        # Ajouter une section avec les mots-clés identifiés
        if keywords:
            keywords_section = f"\n\n🎯 COMPÉTENCES MISES EN AVANT POUR CE POSTE\n"
            keywords_section += f"Technologies et compétences recherchées : {', '.join(keywords[:8])}\n"
            keywords_section += f"Poste visé : {job.title} chez {job.company}"
            adapted_cv += keywords_section
        
        return adapted_cv

class ApplicationBot:
    """Bot de candidature automatique (version simplifiée)"""
    
    def __init__(self):
        self.setup_driver()
        self.db = JobDatabase()
    
    def setup_driver(self):
        """Configure le driver pour les candidatures"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={SELENIUM_CONFIG['user_agent']}")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def apply_to_job(self, job: JobOffer, adapted_cv: str) -> bool:
        """Simule une candidature (version démo)"""
        print(f"📤 Simulation candidature: {job.title} chez {job.company}")
        
        # En mode démo, on simule juste l'envoi
        time.sleep(random.uniform(1, 3))
        
        # 80% de chance de "succès" pour la démo
        success = random.random() > 0.2
        
        if success:
            print(f"✅ Candidature simulée avec succès")
        else:
            print(f"❌ Échec de candidature simulé")
        
        return success
    
    def close(self):
        """Ferme le driver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class JobAutomationSystem:
    """Système principal (version gratuite)"""
    
    def __init__(self):
        print("🚀 Initialisation du système de candidature automatique (Version GRATUITE)")
        self.scraper = JobScraper()
        self.cv_adapter = CVAdapterFree()
        self.application_bot = ApplicationBot()
        self.db = JobDatabase()
    
    def run_full_cycle(self, search_keywords: str, location: str = "France", dry_run: bool = True):
        """Lance un cycle complet (version gratuite)"""
        print(f"🔍 Début du cycle: {search_keywords} à {location}")
        
        if dry_run:
            print("🧪 MODE TEST - Aucune vraie candidature ne sera envoyée")
        
        # 1. Scraping des offres
        jobs = self.scraper.scrape_indeed(search_keywords, location, max_pages=2)
        
        if not jobs:
            print("❌ Aucune offre trouvée")
            return
        
        # 2. Traitement des offres
        profile_config = get_profile_config("data_scientist")  # Par défaut
        
        for i, job in enumerate(jobs[:5]):  # Limite à 5 pour le test
            print(f"\n📝 Traitement {i+1}/{min(5, len(jobs))}: {job.title}")
            
            # 3. Adaptation du CV
            adapted_cv = self.cv_adapter.adapt_cv_for_job(job, profile_config)
            
            # 4. Candidature (simulée)
            if not dry_run:
                success = self.application_bot.apply_to_job(job, adapted_cv)
            else:
                print("🧪 Mode test - candidature non envoyée")
                success = True
            
            if success:
                # Mise à jour en base
                conn = sqlite3.connect(self.db.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE jobs SET status = ?, cv_adapted = ?, application_date = ? WHERE id = ?',
                    ('applied' if not dry_run else 'test', adapted_cv, datetime.now(), job.id)
                )
                conn.commit()
                conn.close()
            
            # Pause entre candidatures
            time.sleep(random.uniform(2, 5))
        
        print(f"\n🎉 Cycle terminé! {len(jobs)} offres traitées")
    
    def get_dashboard_data(self) -> Dict:
        """Récupère les données pour le dashboard"""
        conn = sqlite3.connect(self.db.db_path)
        
        try:
            stats = {
                'total_jobs': pd.read_sql('SELECT COUNT(*) as count FROM jobs', conn).iloc[0]['count'],
                'applied': pd.read_sql('SELECT COUNT(*) as count FROM jobs WHERE status="applied" OR status="test"', conn).iloc[0]['count'],
                'responded': 0,  # Pas de vraies réponses en mode demo
                'recent_jobs': pd.read_sql('SELECT * FROM jobs ORDER BY date_scraped DESC LIMIT 10', conn)
            }
        except:
            stats = {'total_jobs': 0, 'applied': 0, 'responded': 0, 'recent_jobs': pd.DataFrame()}
        
        conn.close()
        return stats
    
    def cleanup(self):
        """Nettoie les ressources"""
        self.scraper.close()
        self.application_bot.close()

# Script principal
if __name__ == "__main__":
    print("🤖 Système de Candidature Automatique - VERSION GRATUITE")
    print("=" * 60)
    
    # Test de configuration
    if not validate_config():
        print("❌ Erreur de configuration")
        exit(1)
    
    # Lancement du système
    system = JobAutomationSystem()
    
    try:
        # Test avec le profil data scientist
        profile_config = get_profile_config("data_scientist")
        system.run_full_cycle(
            search_keywords=profile_config["keywords"],
            location=profile_config["location"],
            dry_run=True  # Mode test par défaut
        )
        
        # Affichage des stats
        dashboard_data = system.get_dashboard_data()
        print("\n📊 RÉSULTATS:")
        print(f"Total offres scrapées: {dashboard_data['total_jobs']}")
        print(f"Tests de candidatures: {dashboard_data['applied']}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
    finally:
        system.cleanup()
        print("🧹 Nettoyage terminé")
