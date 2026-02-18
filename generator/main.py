"""
Galaxy Profile Generator - Main Entry Point
Gera SVGs animados para perfil do GitHub
"""
import argparse
import sys
from pathlib import Path

from generator.config import Config, load_demo_config
from generator.github_api import GitHubAPI
from generator.templates.galaxy_header import generate_galaxy_header
from generator.templates.stats_card import generate_stats_card
from generator.templates.tech_stack import generate_tech_stack
from generator.templates.projects_constellation import generate_projects_constellation


def generate_all_svgs(config: Config, demo_mode: bool = False):
    """Gera todos os SVGs do perfil"""
    
    print(f"🌌 Galaxy Profile Generator")
    print(f"📝 Usuário: {config.username}")
    print(f"🎨 Modo: {'DEMO' if demo_mode else 'PRODUÇÃO'}")
    print()
    
    # Inicializa GitHub API
    if demo_mode:
        print("⚠️  Modo DEMO ativado - usando dados de exemplo")
        stats = {
            "commits": 1234,
            "stars": 89,
            "prs": 156,
            "issues": 78,
            "repos": 23,
        }
        languages = {
            "JavaScript": 45,
            "TypeScript": 38,
            "Python": 12,
            "Java": 25,
            "HTML": 8,
            "CSS": 6,
        }
    else:
        print("🔍 Buscando dados do GitHub...")
        api = GitHubAPI()
        user_stats = api.fetch_user_stats(config.username)
        stats = user_stats
        languages = user_stats.get("languages", {})
        print(f"✅ Dados obtidos: {stats.get('repos', 0)} repositórios")
    
    print()
    
    # Obtém tema
    theme = config.theme
    
    # Cria diretório de saída
    output_dir = Path("assets/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gera cada SVG
    svgs = {
        "galaxy-header.svg": generate_galaxy_header(config, theme),
        "stats-card.svg": generate_stats_card(stats, config.stats_metrics, theme),
        "tech-stack.svg": generate_tech_stack(config, languages, theme),
        "projects-constellation.svg": generate_projects_constellation(config, theme),
    }
    
    print("🎨 Gerando SVGs...")
    for filename, svg_content in svgs.items():
        output_path = output_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"  ✓ {filename}")
    
    print()
    print("✨ Todos os SVGs foram gerados com sucesso!")
    print(f"📁 Localização: {output_dir.absolute()}")
    print()
    print("🚀 Próximos passos:")
    print("  1. Verifique os SVGs gerados abrindo-os no navegador")
    print("  2. Faça commit das mudanças")
    print("  3. Os SVGs serão atualizados automaticamente via GitHub Actions")


def main():
    """Ponto de entrada principal"""
    parser = argparse.ArgumentParser(
        description="Galaxy Profile Generator - Gera SVGs animados para GitHub"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Modo demo: usa dados de exemplo ao invés de buscar da API",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yml",
        help="Caminho para arquivo de configuração (padrão: config.yml)",
    )
    
    args = parser.parse_args()
    
    try:
        # Carrega configuração
        if args.demo:
            config = load_demo_config()
        else:
            config = Config(args.config)
        
        # Gera SVGs
        generate_all_svgs(config, demo_mode=args.demo)
        
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        print()
        print("💡 Dica: Copie config.example.yml para config.yml e personalize:")
        print("   cp config.example.yml config.yml")
        sys.exit(1)
    
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
