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
import openai
from pathlib import Path

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
    status: str = "scraped"  # scraped, applied, responded, rejected

class JobDatabase:
    """Gestion de la base de données des offres"""
    
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def scrape_indeed(self, keywords: str, location: str = "France", max_pages: int = 5):
        """Scrape Indeed"""
        jobs = []
        base_url = f"https://fr.indeed.com/jobs?q={keywords}&l={location}"
        
        for page in range(max_pages):
            url = f"{base_url}&start={page * 10}"
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
            
            for card in job_cards:
                try:
                    job_id = card.get_attribute("data-jk")
                    title = card.find_element(By.CSS_SELECTOR, "h2 a span").text
                    company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='job-location']").text
                    
                    # Clic pour récupérer la description
                    card.find_element(By.CSS_SELECTOR, "h2 a").click()
                    time.sleep(1)
                    
                    description = self.driver.find_element(By.ID, "jobDescriptionText").text
                    job_url = self.driver.current_url
                    
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
                    
                except Exception as e:
                    print(f"Erreur scraping job: {e}")
                    continue
        
        return jobs
    
    def scrape_linkedin(self, keywords: str, location: str = "France"):
        """Scrape LinkedIn Jobs (nécessite une connexion)"""
        # Implementation LinkedIn
        pass
    
    def close(self):
        """Ferme le driver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class CVAdapter:
    """Adapteur de CV basé sur l'IA"""
    
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.base_cv = self.load_base_cv()
    
    def load_base_cv(self) -> str:
        """Charge le CV de base depuis un fichier"""
        # Ici on chargerait votre CV depuis un fichier
        return """
        JULIANA NIAPOH
        CDI DATA & IA | SCRUM MASTER & GESTION DE PROJET AGILE
        
        EXPÉRIENCES PROFESSIONNELLES
        
        Alternance Assistante cheffe de projet numérique (2024/2025)
        SNCF, Saint-Denis - FERROVIAIRE
        • Coordination de projets IT en mode Agile (Scrum)
        • Gestion d'un portail collaboratif réduisant les délais de 30%
        • Support utilisateur niveau 3 et résolution d'incidents complexes
        
        Alternance Chargée de projet Digital (2022/2023)
        ORANO, Châtillon - ÉNERGIE NUCLÉAIRE
        • Analyse et optimisation des flux de données
        • Développement de solutions de visualisation
        • Formation des équipes aux nouveaux outils
        
        COMPÉTENCES
        • Python, SQL, R
        • Machine Learning, IA, NLP
        • Power BI, Tableau de bord
        • Agile (Scrum, Kanban)
        • Big Data, Data visualisation
        """
    
    def extract_keywords_from_job(self, job: JobOffer) -> List[str]:
        """Extrait les mots-clés importants d'une offre"""
        text = f"{job.title} {job.description} {job.requirements}"
        
        prompt = f"""
        Extrait les mots-clés techniques et compétences importantes de cette offre d'emploi dans le domaine Data/IA:
        
        {text[:2000]}
        
        Renvoie uniquement une liste de mots-clés séparés par des virgules, focalisés sur:
        - Technologies et langages
        - Compétences techniques
        - Méthodologies
        - Outils spécifiques
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            
            keywords = [k.strip() for k in response.choices[0].message.content.split(',')]
            return keywords
            
        except Exception as e:
            print(f"Erreur extraction keywords: {e}")
            return []
    
    def adapt_cv_for_job(self, job: JobOffer) -> str:
        """Adapte le CV pour une offre spécifique"""
        keywords = self.extract_keywords_from_job(job)
        job.keywords = keywords
        
        prompt = f"""
        Adapte ce CV pour correspondre à cette offre d'emploi.
        
        CV de base:
        {self.base_cv}
        
        Offre d'emploi:
        Titre: {job.title}
        Entreprise: {job.company}
        Description: {job.description[:1000]}
        
        Mots-clés identifiés: {', '.join(keywords)}
        
        Instructions:
        1. Garde la même structure et les mêmes expériences
        2. Reformule avec le vocabulaire de l'offre
        3. Met en avant les compétences demandées
        4. Réorganise l'ordre des compétences si nécessaire
        5. Adapte le titre du poste recherché
        6. N'invente aucune expérience ou compétence
        
        Renvoie le CV adapté:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500
            )
            
            adapted_cv = response.choices[0].message.content
            return adapted_cv
            
        except Exception as e:
            print(f"Erreur adaptation CV: {e}")
            return self.base_cv

class ApplicationBot:
    """Bot de candidature automatique"""
    
    def __init__(self):
        self.setup_driver()
        self.db = JobDatabase()
    
    def setup_driver(self):
        """Configure le driver pour les candidatures"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def apply_to_job(self, job: JobOffer, adapted_cv: str) -> bool:
        """Candidate automatiquement à une offre"""
        try:
            self.driver.get(job.url)
            time.sleep(2)
            
            # Logique spécifique selon la plateforme
            if "indeed" in job.source:
                return self._apply_indeed(job, adapted_cv)
            elif "linkedin" in job.source:
                return self._apply_linkedin(job, adapted_cv)
            
            return False
            
        except Exception as e:
            print(f"Erreur candidature pour {job.title}: {e}")
            return False
    
    def _apply_indeed(self, job: JobOffer, adapted_cv: str) -> bool:
        """Candidature spécifique Indeed"""
        try:
            # Cherche le bouton "Postuler"
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Postuler')]"))
            )
            apply_button.click()
            
            # Remplir le formulaire si nécessaire
            # Implementation détaillée selon l'interface Indeed
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"Erreur candidature Indeed: {e}")
            return False
    
    def close(self):
        """Ferme le driver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class JobAutomationSystem:
    """Système principal qui orchestre tout"""
    
    def __init__(self, openai_api_key: str):
        self.scraper = JobScraper()
        self.cv_adapter = CVAdapter(openai_api_key)
        self.application_bot = ApplicationBot()
        self.db = JobDatabase()
    
    def run_full_cycle(self, search_keywords: str, location: str = "France"):
        """Lance un cycle complet: scraping + adaptation + candidature"""
        print("🔍 Début du scraping des offres...")
        
        # 1. Scraping des offres
        jobs = self.scraper.scrape_indeed(search_keywords, location)
        print(f"✅ {len(jobs)} offres récupérées")
        
        # 2. Traitement des offres non traitées
        unprocessed_jobs = self.db.get_jobs_by_status("scraped")
        
        for job in unprocessed_jobs:
            print(f"📝 Traitement: {job.title} chez {job.company}")
            
            # 3. Adaptation du CV
            adapted_cv = self.cv_adapter.adapt_cv_for_job(job)
            
            # 4. Candidature automatique
            success = self.application_bot.apply_to_job(job, adapted_cv)
            
            if success:
                # Update status in database
                conn = sqlite3.connect(self.db.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE jobs SET status = ?, cv_adapted = ?, application_date = ? WHERE id = ?',
                    ('applied', adapted_cv, datetime.now(), job.id)
                )
                conn.commit()
                conn.close()
                print(f"✅ Candidature envoyée pour {job.title}")
            else:
                print(f"❌ Échec candidature pour {job.title}")
            
            # Pause entre candidatures
            time.sleep(random.uniform(30, 60))
        
        print("🎉 Cycle terminé!")
    
    def get_dashboard_data(self) -> Dict:
        """Récupère les données pour le dashboard"""
        conn = sqlite3.connect(self.db.db_path)
        
        stats = {
            'total_jobs': pd.read_sql('SELECT COUNT(*) as count FROM jobs', conn).iloc[0]['count'],
            'applied': pd.read_sql('SELECT COUNT(*) as count FROM jobs WHERE status="applied"', conn).iloc[0]['count'],
            'responded': pd.read_sql('SELECT COUNT(*) as count FROM jobs WHERE status="responded"', conn).iloc[0]['count'],
            'recent_jobs': pd.read_sql('SELECT * FROM jobs ORDER BY date_scraped DESC LIMIT 10', conn)
        }
        
        conn.close()
        return stats
    
    def cleanup(self):
        """Nettoie les ressources"""
        self.scraper.close()
        self.application_bot.close()

# Script principal
if __name__ == "__main__":
    # Configuration
    OPENAI_API_KEY = "your-openai-api-key"  # À remplacer
    SEARCH_KEYWORDS = "data scientist python machine learning"
    LOCATION = "Île-de-France"
    
    # Lancement du système
    system = JobAutomationSystem(OPENAI_API_KEY)
    
    try:
        system.run_full_cycle(SEARCH_KEYWORDS, LOCATION)
        
        # Affichage des stats
        dashboard_data = system.get_dashboard_data()
        print("\n📊 TABLEAU DE BORD:")
        print(f"Total offres: {dashboard_data['total_jobs']}")
        print(f"Candidatures envoyées: {dashboard_data['applied']}")
        print(f"Réponses reçues: {dashboard_data['responded']}")
        
    finally:
        system.cleanup()
