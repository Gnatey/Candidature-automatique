import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from job_automation_system import JobAutomationSystem, JobDatabase
import threading
import time

# Configuration de la page
st.set_page_config(
    page_title="Job Automation Dashboard",
    page_icon="🤖",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-running {
        color: #28a745;
        font-weight: bold;
    }
    .status-stopped {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class JobDashboard:
    def __init__(self):
        self.db = JobDatabase()
        self.system = None
        
        # Session state pour le statut du système
        if 'system_running' not in st.session_state:
            st.session_state.system_running = False
        if 'last_run' not in st.session_state:
            st.session_state.last_run = None
    
    def get_stats(self):
        """Récupère les statistiques"""
        conn = sqlite3.connect(self.db.db_path)
        
        # Stats générales
        total_jobs = pd.read_sql('SELECT COUNT(*) as count FROM jobs', conn).iloc[0]['count']
        applied_jobs = pd.read_sql('SELECT COUNT(*) as count FROM jobs WHERE status="applied"', conn).iloc[0]['count']
        responded_jobs = pd.read_sql('SELECT COUNT(*) as count FROM jobs WHERE status="responded"', conn).iloc[0]['count']
        
        # Jobs par statut
        status_stats = pd.read_sql('''
            SELECT status, COUNT(*) as count 
            FROM jobs 
            GROUP BY status
        ''', conn)
        
        # Jobs par source
        source_stats = pd.read_sql('''
            SELECT source, COUNT(*) as count 
            FROM jobs 
            GROUP BY source
        ''', conn)
        
        # Jobs récents
        recent_jobs = pd.read_sql('''
            SELECT title, company, location, status, date_scraped, application_date
            FROM jobs 
            ORDER BY date_scraped DESC 
            LIMIT 20
        ''', conn)
        
        # Évolution temporelle
        daily_stats = pd.read_sql('''
            SELECT 
                DATE(date_scraped) as date,
                COUNT(*) as jobs_scraped,
                SUM(CASE WHEN status = 'applied' THEN 1 ELSE 0 END) as jobs_applied
            FROM jobs 
            WHERE date_scraped >= date('now', '-30 days')
            GROUP BY DATE(date_scraped)
            ORDER BY date
        ''', conn)
        
        conn.close()
        
        return {
            'total_jobs': total_jobs,
            'applied_jobs': applied_jobs,
            'responded_jobs': responded_jobs,
            'status_stats': status_stats,
            'source_stats': source_stats,
            'recent_jobs': recent_jobs,
            'daily_stats': daily_stats
        }
    
    def render_header(self):
        """Affiche l'en-tête"""
        st.markdown('<div class="main-header">🤖 Job Automation Dashboard</div>', unsafe_allow_html=True)
        
        # Statut du système
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.session_state.system_running:
                st.markdown('<div class="status-running">🟢 Système Actif</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-stopped">🔴 Système Arrêté</div>', unsafe_allow_html=True)
        
        with col2:
            if st.session_state.last_run:
                st.write(f"Dernière exécution: {st.session_state.last_run}")
        
        with col3:
            if st.button("🔄 Actualiser", key="refresh"):
                st.rerun()
    
    def render_metrics(self, stats):
        """Affiche les métriques principales"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total Offres",
                value=stats['total_jobs'],
                delta=None
            )
        
        with col2:
            st.metric(
                label="📤 Candidatures Envoyées",
                value=stats['applied_jobs'],
                delta=None
            )
        
        with col3:
            st.metric(
                label="📧 Réponses Reçues",
                value=stats['responded_jobs'],
                delta=None
            )
        
        with col4:
            success_rate = (stats['responded_jobs'] / stats['applied_jobs'] * 100) if stats['applied_jobs'] > 0 else 0
            st.metric(
                label="📈 Taux de Réponse",
                value=f"{success_rate:.1f}%",
                delta=None
            )
    
    def render_charts(self, stats):
        """Affiche les graphiques"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Répartition par Statut")
            if not stats['status_stats'].empty:
                fig = px.pie(
                    stats['status_stats'], 
                    values='count', 
                    names='status',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🌐 Répartition par Source")
            if not stats['source_stats'].empty:
                fig = px.bar(
                    stats['source_stats'], 
                    x='source', 
                    y='count',
                    color='source',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Évolution temporelle
        st.subheader("📈 Évolution des Candidatures (30 derniers jours)")
        if not stats['daily_stats'].empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=stats['daily_stats']['date'],
                y=stats['daily_stats']['jobs_scraped'],
                mode='lines+markers',
                name='Offres Scrapées',
                line=dict(color='#17becf')
            ))
            fig.add_trace(go.Scatter(
                x=stats['daily_stats']['date'],
                y=stats['daily_stats']['jobs_applied'],
                mode='lines+markers',
                name='Candidatures Envoyées',
                line=dict(color='#2ca02c')
            ))
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Nombre",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_controls(self):
        """Affiche les contrôles du système"""
        st.subheader("🎛️ Contrôles du Système")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Configuration de Recherche**")
            keywords = st.text_input("Mots-clés de recherche", value="data scientist python machine learning")
            location = st.text_input("Localisation", value="Île-de-France")
            max_pages = st.slider("Nombre de pages à scraper", 1, 10, 3)
            
            col_start, col_stop = st.columns(2)
            with col_start:
                if st.button("▶️ Démarrer le Système", disabled=st.session_state.system_running):
                    self.start_system(keywords, location, max_pages)
            
            with col_stop:
                if st.button("⏹️ Arrêter le Système", disabled=not st.session_state.system_running):
                    self.stop_system()
        
        with col2:
            st.write("**Configuration Avancée**")
            
            # Configuration OpenAI
            openai_key = st.text_input("Clé API OpenAI", type="password", help="Nécessaire pour l'adaptation du CV")
            
            # Filtres de candidature
            st.write("**Filtres de Candidature**")
            min_salary = st.number_input("Salaire minimum (€)", min_value=0, value=0)
            exclude_keywords = st.text_area("Mots-clés à exclure (séparés par des virgules)", 
                                          value="stage, intern, bénévole")
            
            # Délais
            delay_between_applications = st.slider("Délai entre candidatures (secondes)", 30, 300, 60)
    
    def render_job_list(self, stats):
        """Affiche la liste des offres"""
        st.subheader("📋 Offres Récentes")
        
        if not stats['recent_jobs'].empty:
            # Filtres
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Filtrer par statut", 
                                           ['Tous'] + list(stats['recent_jobs']['status'].unique()))
            with col2:
                company_filter = st.text_input("Filtrer par entreprise")
            with col3:
                title_filter = st.text_input("Filtrer par titre")
            
            # Application des filtres
            filtered_jobs = stats['recent_jobs'].copy()
            if status_filter != 'Tous':
                filtered_jobs = filtered_jobs[filtered_jobs['status'] == status_filter]
            if company_filter:
                filtered_jobs = filtered_jobs[filtered_jobs['company'].str.contains(company_filter, case=False, na=False)]
            if title_filter:
                filtered_jobs = filtered_jobs[filtered_jobs['title'].str.contains(title_filter, case=False, na=False)]
            
            # Affichage du tableau
            st.dataframe(
                filtered_jobs,
                use_container_width=True,
                column_config={
                    "date_scraped": st.column_config.DatetimeColumn("Date Scrapée"),
                    "application_date": st.column_config.DatetimeColumn("Date Candidature"),
                    "status": st.column_config.SelectboxColumn(
                        "Statut",
                        options=["scraped", "applied", "responded", "rejected"]
                    )
                }
            )
        else:
            st.info("Aucune offre trouvée. Lancez le système pour commencer le scraping.")
    
    def start_system(self, keywords, location, max_pages):
        """Démarre le système en arrière-plan"""
        st.session_state.system_running = True
        st.session_state.last_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ici on pourrait lancer le système en arrière-plan
        # Pour la démo, on simule juste
        st.success(f"🚀 Système démarré avec les paramètres:\n- Mots-clés: {keywords}\n- Localisation: {location}\n- Pages: {max_pages}")
        st.info("⚠️ Note: Dans cette version démo, le système ne fonctionne pas réellement en arrière-plan.")
    
    def stop_system(self):
        """Arrête le système"""
        st.session_state.system_running = False
        st.warning("⏹️ Système arrêté")
    
    def render_logs(self):
        """Affiche les logs du système"""
        st.subheader("📜 Logs du Système")
        
        # Simulation de logs
        logs = [
            f"{datetime.now().strftime('%H:%M:%S')} - INFO - Système initialisé",
            f"{datetime.now().strftime('%H:%M:%S')} - INFO - Scraping Indeed démarré",
            f"{datetime.now().strftime('%H:%M:%S')} - SUCCESS - 15 offres récupérées",
            f"{datetime.now().strftime('%H:%M:%S')} - INFO - Adaptation CV pour 'Data Scientist - Carrefour'",
            f"{datetime.now().strftime('%H:%M:%S')} - SUCCESS - Candidature envoyée",
        ]
        
        log_container = st.container()
        with log_container:
            for log in logs[-10:]:  # Derniers 10 logs
                st.text(log)
    
    def run(self):
        """Lance le dashboard"""
        self.render_header()
        
        # Récupération des données
        stats = self.get_stats()
        
        # Métriques
        self.render_metrics(stats)
        
        st.divider()
        
        # Graphiques
        self.render_charts(stats)
        
        st.divider()
        
        # Contrôles
        self.render_controls()
        
        st.divider()
        
        # Liste des offres
        self.render_job_list(stats)
        
        st.divider()
        
        # Logs
        self.render_logs()

# Point d'entrée
if __name__ == "__main__":
    dashboard = JobDashboard()
    dashboard.run()
