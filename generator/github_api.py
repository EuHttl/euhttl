"""
Cliente para GitHub API (GraphQL e REST)
"""
import os
import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class GitHubAPI:
    """Cliente para buscar dados do GitHub"""
    
    GRAPHQL_URL = "https://api.github.com/graphql"
    REST_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {}
        
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    def fetch_user_stats(self, username: str) -> Dict:
        """Busca estatísticas do usuário"""
        if self.token:
            return self._fetch_stats_graphql(username)
        else:
            return self._fetch_stats_rest(username)
    
    def _fetch_stats_graphql(self, username: str) -> Dict:
        """Busca stats via GraphQL (mais completo, requer token)"""
        query = """
        query($username: String!) {
          user(login: $username) {
            contributionsCollection {
              totalCommitContributions
              totalPullRequestContributions
              totalIssueContributions
            }
            repositories(first: 100, ownerAffiliations: OWNER) {
              totalCount
              nodes {
                stargazerCount
                primaryLanguage {
                  name
                }
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                self.GRAPHQL_URL,
                json={"query": query, "variables": {"username": username}},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"GraphQL errors: {data['errors']}")
                return self._fetch_stats_rest(username)
            
            user = data["data"]["user"]
            contrib = user["contributionsCollection"]
            repos = user["repositories"]
            
            total_stars = sum(
                repo["stargazerCount"] for repo in repos["nodes"]
            )
            
            languages = {}
            for repo in repos["nodes"]:
                if repo.get("primaryLanguage"):
                    lang = repo["primaryLanguage"]["name"]
                    languages[lang] = languages.get(lang, 0) + 1
            
            return {
                "commits": contrib["totalCommitContributions"],
                "stars": total_stars,
                "prs": contrib["totalPullRequestContributions"],
                "issues": contrib["totalIssueContributions"],
                "repos": repos["totalCount"],
                "languages": languages,
            }
        
        except Exception as e:
            print(f"Erro no GraphQL, fallback para REST: {e}")
            return self._fetch_stats_rest(username)
    
    def _fetch_stats_rest(self, username: str) -> Dict:
        """Busca stats via REST API (público, limitado)"""
        try:
            # Busca informações do usuário
            user_response = requests.get(
                f"{self.REST_URL}/users/{username}",
                headers=self.headers,
                timeout=10
            )
            user_response.raise_for_status()
            user_data = user_response.json()
            
            # Busca repositórios
            repos_response = requests.get(
                f"{self.REST_URL}/users/{username}/repos?per_page=100",
                headers=self.headers,
                timeout=10
            )
            repos_response.raise_for_status()
            repos = repos_response.json()
            
            total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
            
            languages = {}
            for repo in repos:
                if repo.get("language"):
                    lang = repo["language"]
                    languages[lang] = languages.get(lang, 0) + 1
            
            return {
                "commits": 0,  # Não disponível via REST público
                "stars": total_stars,
                "prs": 0,  # Não disponível via REST público
                "issues": 0,  # Não disponível via REST público
                "repos": user_data.get("public_repos", 0),
                "languages": languages,
            }
        
        except Exception as e:
            print(f"Erro ao buscar dados do GitHub: {e}")
            return {
                "commits": 0,
                "stars": 0,
                "prs": 0,
                "issues": 0,
                "repos": 0,
                "languages": {},
            }
    
    def fetch_languages(self, username: str) -> Dict[str, int]:
        """Busca linguagens usadas pelo usuário"""
        stats = self.fetch_user_stats(username)
        return stats.get("languages", {})
