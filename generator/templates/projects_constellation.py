"""
Template: Projects Constellation - Projetos em destaque
"""
from generator.utils import escape_xml


def generate_projects_constellation(config, theme: dict) -> str:
    """Gera SVG da constelação de projetos"""
    
    width = 850
    height = 220
    
    projects = config.projects
    if not projects:
        # SVG vazio se não houver projetos
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="{theme['nebula_bg']}" rx="10"/>
  <text x="425" y="110" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="16" 
        fill="{theme['text_dim']}">
    Nenhum projeto em destaque configurado
  </text>
</svg>'''
    
    # Calcula espaçamento
    project_width = 250
    project_spacing = (width - project_width * min(len(projects), 3)) / 4
    
    # Cores dos braços
    arm_colors = [
        theme["synapse_cyan"],
        theme["dendrite_violet"],
        theme["axon_amber"],
    ]
    
    # Gera cards de projetos
    project_cards = []
    for i, project in enumerate(projects[:3]):  # Máximo 3 projetos
        x = project_spacing + i * (project_width + project_spacing)
        
        repo = escape_xml(project.get("repo", ""))
        description = escape_xml(project.get("description", ""))
        arm = project.get("arm", 0)
        color = arm_colors[arm % len(arm_colors)]
        
        # Extrai nome do repositório
        repo_name = repo.split("/")[-1] if "/" in repo else repo
        
        project_cards.append(f'''
    <g transform="translate({x}, 60)">
      <!-- Card background -->
      <rect width="{project_width}" height="130" 
            fill="{theme['starfield_dim']}" stroke="{color}" 
            stroke-width="2" opacity="0.8" rx="8"/>
      
      <!-- Ícone orbital -->
      <g transform="translate({project_width/2}, 25)">
        <circle cx="0" cy="0" r="15" fill="none" stroke="{color}" stroke-width="2">
          <animateTransform attributeName="transform" type="rotate" 
                            from="0 0 0" to="360 0 0" dur="10s" repeatCount="indefinite"/>
        </circle>
        <circle cx="15" cy="0" r="4" fill="{color}">
          <animateTransform attributeName="transform" type="rotate" 
                            from="0 0 0" to="360 0 0" dur="10s" repeatCount="indefinite"/>
        </circle>
      </g>
      
      <!-- Nome do repositório -->
      <text x="{project_width/2}" y="70" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="600" 
            fill="{theme['text_bright']}">
        {repo_name[:20]}
      </text>
      
      <!-- Descrição -->
      <text x="{project_width/2}" y="95" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="11" 
            fill="{theme['text_dim']}">
        {description[:35] + "..." if len(description) > 35 else description}
      </text>
      
      <!-- Link sutil -->
      <text x="{project_width/2}" y="115" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="10" 
            fill="{color}">
        {repo}
      </text>
    </g>''')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['nebula_bg']}" rx="10"/>
  
  <!-- Borda -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" 
        fill="none" stroke="{theme['axon_amber']}" stroke-width="1" 
        opacity="0.3" rx="10"/>
  
  <!-- Título -->
  <text x="425" y="30" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="20" font-weight="600" 
        fill="{theme['text_bright']}">
    ⭐ Featured Systems
  </text>
  
  <!-- Cards de projetos -->
  {''.join(project_cards)}
</svg>'''
    
    return svg
