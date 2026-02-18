"""
Template: Stats Card - Cartão de estatísticas do GitHub
"""
from generator.utils import escape_xml, format_number


def generate_stats_card(stats: dict, metrics_config: dict, theme: dict) -> str:
    """Gera SVG do cartão de estatísticas"""
    
    width = 850
    height = 180
    
    # Define métricas a serem exibidas
    metrics = []
    if metrics_config.get("commits", True):
        metrics.append(("Commits", stats.get("commits", 0), "M 10 15 L 10 5 L 15 0 L 25 0 L 30 5 L 30 15 Z"))
    
    if metrics_config.get("stars", True):
        metrics.append(("Stars", stats.get("stars", 0), "M 20 5 L 23 15 L 33 15 L 25 21 L 28 31 L 20 25 L 12 31 L 15 21 L 7 15 L 17 15 Z"))
    
    if metrics_config.get("prs", True):
        metrics.append(("Pull Requests", stats.get("prs", 0), "M 10 5 L 30 5 M 20 5 L 20 25 M 15 20 L 20 25 L 25 20"))
    
    if metrics_config.get("issues", True):
        metrics.append(("Issues", stats.get("issues", 0), "M 20 5 A 10 10 0 1 1 20 25 A 10 10 0 1 1 20 5 M 20 10 L 20 18 M 20 22 L 20 24"))
    
    if metrics_config.get("repos", True):
        metrics.append(("Repositórios", stats.get("repos", 0), "M 10 10 L 10 30 L 30 30 L 30 10 Z M 15 5 L 15 10 M 25 5 L 25 10"))
    
    # Calcula espaçamento
    total_metrics = len(metrics)
    if total_metrics == 0:
        total_metrics = 1
    
    spacing = width / total_metrics
    
    # Gera elementos de métrica
    metric_elements = []
    for i, (label, value, icon_path) in enumerate(metrics):
        x = spacing * i + spacing / 2
        
        metric_elements.append(f'''
    <g transform="translate({x}, 90)">
      <!-- Ícone -->
      <g transform="translate(-20, -40)">
        <path d="{icon_path}" stroke="{theme['synapse_cyan']}" stroke-width="2" 
              fill="none" opacity="0.8"/>
      </g>
      
      <!-- Valor -->
      <text y="0" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="36" font-weight="bold" 
            fill="{theme['text_bright']}">
        {format_number(value)}
      </text>
      
      <!-- Label -->
      <text y="25" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="14" 
            fill="{theme['text_dim']}">
        {escape_xml(label)}
      </text>
    </g>''')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['nebula_bg']}" rx="10"/>
  
  <!-- Borda brilhante -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" 
        fill="none" stroke="{theme['synapse_cyan']}" stroke-width="1" 
        opacity="0.3" rx="10"/>
  
  <!-- Título -->
  <text x="425" y="30" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="20" font-weight="600" 
        fill="{theme['text_bright']}">
    📊 Mission Telemetry
  </text>
  
  <!-- Métricas -->
  {''.join(metric_elements)}
</svg>'''
    
    return svg
