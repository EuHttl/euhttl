"""
Template: Tech Stack
"""
from generator.utils import escape_xml, get_language_color
import math


def generate_tech_stack(config, languages: dict, theme: dict) -> str:
    """Gera SVG da pilha de tecnologias com barras e gráfico de pizza"""
    
    width = 850
    height = 350
    
    # Processa linguagens
    lang_config = config.languages_config
    exclude = lang_config.get("exclude", [])
    max_display = lang_config.get("max_display", 8)
    
    # Filtra e ordena linguagens
    filtered_langs = {
        lang: count for lang, count in languages.items() 
        if lang not in exclude
    }
    
    sorted_langs = sorted(
        filtered_langs.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:max_display]
    
    # Calcula total para porcentagens
    total = sum(count for _, count in sorted_langs) or 1
    
    # Gera barras de linguagem (lado esquerdo)
    lang_bars = []
    y_offset = 80
    bar_height = 18
    bar_spacing = 28
    bar_max_width = 180
    
    for i, (lang, count) in enumerate(sorted_langs):
        percentage = (count / total) * 100
        bar_width = bar_max_width * (count / total)
        color = get_language_color(lang)
        y = y_offset + i * bar_spacing
        
        lang_bars.append(f'''
    <g>
      <rect x="30" y="{y}" width="{bar_max_width}" height="{bar_height}" 
            fill="{theme['starfield_dim']}" rx="3"/>
      
      <rect x="30" y="{y}" width="0" height="{bar_height}" 
            fill="{color}" opacity="0.9" rx="3">
        <animate attributeName="width" from="0" to="{bar_width}" 
                 dur="1.2s" begin="0.{i}s" fill="freeze"/>
      </rect>
      
      <text x="220" y="{y + bar_height/2 + 5}" 
            font-family="'Courier New', monospace" font-size="13" font-weight="600" 
            fill="{theme['text_bright']}">
        {escape_xml(lang)}
      </text>
      
      <text x="360" y="{y + bar_height/2 + 5}" text-anchor="end"
            font-family="'Courier New', monospace" font-size="13" 
            fill="{theme['text_dim']}">
        {percentage:.1f}%
      </text>
    </g>''')
    
    # Gera gráfico de pizza para Focus Sectors (lado direito)
    focus_sectors = []
    if config.galaxy_arms:
        # Calcula total de tecnologias por área
        sector_data = []
        for arm in config.galaxy_arms:
            name = arm.get("name", "")
            tech_count = len(arm.get("tech", []))
            sector_data.append((name, tech_count))
        
        total_sectors = sum(count for _, count in sector_data) or 1
        
        # Cores para setores
        sector_colors = [
            theme["axon_amber"],
            theme["dendrite_violet"],
            theme["synapse_cyan"],
        ]
        
        # Desenha gráfico de pizza
        center_x = 630
        center_y = 180
        radius = 90
        
        start_angle = -90  # Começa no topo
        
        for i, (name, count) in enumerate(sector_data):
            percentage = (count / total_sectors) * 100
            angle = (count / total_sectors) * 360
            end_angle = start_angle + angle
            
            # Converte para radianos
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calcula pontos do arco
            x1 = center_x + radius * math.cos(start_rad)
            y1 = center_y + radius * math.sin(start_rad)
            x2 = center_x + radius * math.cos(end_rad)
            y2 = center_y + radius * math.sin(end_rad)
            
            large_arc = 1 if angle > 180 else 0
            
            # Label position (meio do setor)
            mid_angle = math.radians((start_angle + end_angle) / 2)
            label_x = center_x + (radius * 0.6) * math.cos(mid_angle)
            label_y = center_y + (radius * 0.6) * math.sin(mid_angle)
            
            color = sector_colors[i % len(sector_colors)]
            
            focus_sectors.append(f'''
    <g>
      <path d="M {center_x} {center_y} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
            fill="{color}" opacity="0.7" stroke="{theme['void_black']}" stroke-width="2">
        <animate attributeName="opacity" values="0.7;0.85;0.7" dur="3s" repeatCount="indefinite"/>
      </path>
      
      <text x="{label_x}" y="{label_y + 5}" text-anchor="middle"
            font-family="'Courier New', monospace" font-size="16" font-weight="bold"
            fill="{theme['text_bright']}">
        ({count})
      </text>
    </g>''')
            
            start_angle = end_angle
        
        # Labels externos
        legend_y = 295
        legend_spacing = 160
        for i, (name, count) in enumerate(sector_data):
            x = 450 + i * legend_spacing
            color = sector_colors[i % len(sector_colors)]
            
            focus_sectors.append(f'''
    <g>
      <circle cx="{x}" cy="{legend_y}" r="5" fill="{color}" opacity="0.9"/>
      <text x="{x + 12}" y="{legend_y + 5}"
            font-family="'Courier New', monospace" font-size="12" font-weight="600"
            fill="{color}">
        {escape_xml(name)}
      </text>
      <text x="{x + 12}" y="{legend_y + 20}"
            font-family="'Courier New', monospace" font-size="10"
            fill="{theme['text_dim']}">
        ({count})
      </text>
    </g>''')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['nebula_bg']}" rx="10"/>
  
  <!-- Borda -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" 
        fill="none" stroke="{theme['starfield_dim']}" stroke-width="1" 
        opacity="0.3" rx="10"/>
  
  <!-- Título Language Telemetry -->
  <text x="30" y="35" 
        font-family="'Courier New', monospace" font-size="14" font-weight="600" 
        fill="{theme['text_dim']}" letter-spacing="2">
    LANGUAGE TELEMETRY
  </text>
  
  <!-- Título Focus Sectors -->
  <text x="470" y="35" 
        font-family="'Courier New', monospace" font-size="14" font-weight="600" 
        fill="{theme['text_dim']}" letter-spacing="2">
    FOCUS SECTORS
  </text>
  
  <!-- Barras de linguagem -->
  {''.join(lang_bars)}
  
  <!-- Gráfico de pizza -->
  {''.join(focus_sectors)}
  
  <!-- Linha divisória vertical -->
  <line x1="420" y1="60" x2="420" y2="280" 
        stroke="{theme['starfield_dim']}" stroke-width="1" opacity="0.3"/>
</svg>'''
    
    return svg
