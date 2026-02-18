"""
Configuração e validação do Galaxy Profile
"""
import yaml
from typing import Dict, List, Optional
from pathlib import Path


class Config:
    """Classe para carregar e validar configuração"""
    
    DEFAULT_THEME = {
        "void_black": "#0a0e27",
        "nebula_bg": "#0f1420",
        "starfield_dim": "#1a1f35",
        "synapse_cyan": "#00d9ff",
        "dendrite_violet": "#a970ff",
        "axon_amber": "#ffb800",
        "text_bright": "#e0e6f7",
        "text_dim": "#8892b0",
        "glow_core": "#ffffff",
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.yml"
        self.data = self._load_config()
        self._validate()
    
    def _load_config(self) -> Dict:
        """Carrega arquivo de configuração YAML"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.config_path}\n"
                "Copie config.example.yml para config.yml e personalize."
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Erro ao parsear YAML: {e}")
    
    def _validate(self):
        """Valida campos obrigatórios"""
        if not self.data.get("username"):
            raise ValueError("Campo 'username' é obrigatório em config.yml")
        
        if not self.data.get("profile", {}).get("name"):
            raise ValueError("Campo 'profile.name' é obrigatório em config.yml")
    
    @property
    def username(self) -> str:
        return self.data["username"]
    
    @property
    def profile(self) -> Dict:
        return self.data.get("profile", {})
    
    @property
    def social(self) -> Dict:
        return self.data.get("social", {})
    
    @property
    def galaxy_arms(self) -> List[Dict]:
        return self.data.get("galaxy_arms", [])
    
    @property
    def projects(self) -> List[Dict]:
        return self.data.get("projects", [])
    
    @property
    def theme(self) -> Dict:
        """Retorna tema com fallback para valores padrão"""
        user_theme = self.data.get("theme", {})
        return {**self.DEFAULT_THEME, **user_theme}
    
    @property
    def stats_metrics(self) -> Dict:
        return self.data.get("stats", {}).get("metrics", {
            "commits": True,
            "stars": True,
            "prs": True,
            "issues": True,
            "repos": True,
        })
    
    @property
    def languages_config(self) -> Dict:
        return self.data.get("languages", {
            "exclude": [],
            "max_display": 6,
        })


def load_demo_config() -> Config:
    """Carrega configuração de demonstração"""
    demo_data = {
        "username": "EuHttl",
        "profile": {
            "name": "Hyttalo Costa",
            "tagline": "Desenvolvedor Fullstack",
            "bio": "Apaixonado por código e soluções escaláveis",
        },
        "galaxy_arms": [
            {
                "name": "Backend",
                "color": "synapse_cyan",
                "tech": ["Java", "Spring Boot", "Node.js"],
            },
            {
                "name": "Frontend",
                "color": "dendrite_violet",
                "tech": ["React", "TypeScript", "Next.js"],
            },
            {
                "name": "DevOps",
                "color": "axon_amber",
                "tech": ["Docker", "PostgreSQL", "Git"],
            },
        ],
        "projects": [],
    }
    
    config = Config.__new__(Config)
    config.data = demo_data
    return config
