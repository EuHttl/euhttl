"""
Template: Stats Card
"""
from generator.utils import escape_xml, format_number


def generate_stats_card(stats: dict, metrics_config: dict, theme: dict) -> str:
    """Gera SVG do cartão de estatísticas"""
    
    width = 850
    height = 160
    
    # Define métricas a serem exibidas
    metrics = []
    metric_icons = {
        "commits": "💠",
        "stars": "⭐",
        "prs": "🔄",
        "issues": "❓",
        "repos": "📦"
    }
    
    metric_labels = {
        "commits": "Commits",
        "stars": "Stars", 
        "prs": "PRs",
        "issues": "Issues",
        "repos": "Repos"
    }
    
    if metrics_config.get("commits", True):
        metrics.append(("commits", stats.get("commits", 0)))
    
    if metrics_config.get("stars", True):
        metrics.append(("stars", stats.get("stars", 0)))
    
    if metrics_config.get("prs", True):
        metrics.append(("prs", stats.get("prs", 0)))
    
    if metrics_config.get("issues", True):
        metrics.append(("issues", stats.get("issues", 0)))
    
    if metrics_config.get("repos", True):
        metrics.append(("repos", stats.get("repos", 0)))
    
    # Calcula espaçamento com margens
    total_metrics = len(metrics)
    if total_metrics == 0:
        total_metrics = 1
    
    left_margin = 60
    right_margin = 60
    usable_width = width - left_margin - right_margin
    spacing = usable_width / (total_metrics - 1) if total_metrics > 1 else 0
    
    # Cores alternadas para métricas
    colors = [
        theme["synapse_cyan"],
        theme["axon_amber"],
        theme["synapse_cyan"],
        theme["axon_amber"],
        theme["dendrite_violet"],
    ]
    
    # Gera elementos de métrica
    metric_elements = []
    for i, (key, value) in enumerate(metrics):
        x = left_margin + (spacing * i) if total_metrics > 1 else width / 2
        color = colors[i % len(colors)]
        icon = metric_icons.get(key, "📊")
        label = metric_labels.get(key, key.capitalize())
        
        metric_elements.append(f'''
    <g>
      <!-- Ícone -->
      <text x="{x}" y="60" text-anchor="middle" font-size="28">
        {icon}
      </text>
      
      <!-- Valor -->
      <text x="{x}" y="100" text-anchor="middle" 
            font-family="'Courier New', monospace" font-size="32" font-weight="bold" 
            fill="{color}">
        {format_number(value)}
      </text>
      
      <!-- Label -->
      <text x="{x}" y="125" text-anchor="middle" 
            font-family="'Courier New', monospace" font-size="12" font-weight="600"
            fill="{theme['text_dim']}">
        {escape_xml(label)}
      </text>
    </g>''')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['nebula_bg']}" rx="10"/>
  
  <!-- Borda -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" 
        fill="none" stroke="{theme['starfield_dim']}" stroke-width="1" 
        opacity="0.3" rx="10"/>
  
  <!-- Título -->
  <text x="30" y="28" 
        font-family="'Courier New', monospace" font-size="14" font-weight="600" 
        fill="{theme['text_dim']}" letter-spacing="2">
    MISSION TELEMETRY
  </text>
  
  <!-- Métricas -->
  {''.join(metric_elements)}
</svg>'''
    
    return svg
