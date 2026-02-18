"""
Template: Tech Stack - Visualização de linguagens e tecnologias
"""
from generator.utils import escape_xml, get_language_color
import math


def generate_tech_stack(config, languages: dict, theme: dict) -> str:
    """Gera SVG da pilha de tecnologias"""
    
    width = 850
    base_height = 250
    
    # Processa linguagens
    lang_config = config.languages_config
    exclude = lang_config.get("exclude", [])
    max_display = lang_config.get("max_display", 6)
    
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
    
    # Gera barras de linguagem
    lang_bars = []
    y_offset = 80
    bar_height = 30
    bar_spacing = 45
    
    for i, (lang, count) in enumerate(sorted_langs):
        percentage = (count / total) * 100
        bar_width = (width - 100) * (count / total)
        color = get_language_color(lang)
        y = y_offset + i * bar_spacing
        
        lang_bars.append(f'''
    <g>
      <!-- Barra de fundo -->
      <rect x="50" y="{y}" width="{width - 100}" height="{bar_height}" 
            fill="{theme['starfield_dim']}" rx="5"/>
      
      <!-- Barra de progresso -->
      <rect x="50" y="{y}" width="{bar_width}" height="{bar_height}" 
            fill="{color}" opacity="0.8" rx="5">
        <animate attributeName="width" from="0" to="{bar_width}" 
                 dur="1.5s" begin="0.{i}s" fill="freeze"/>
      </rect>
      
      <!-- Nome da linguagem -->
      <text x="60" y="{y + bar_height/2 + 5}" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="600" 
            fill="{theme['text_bright']}">
        {escape_xml(lang)}
      </text>
      
      <!-- Porcentagem -->
      <text x="{width - 60}" y="{y + bar_height/2 + 5}" text-anchor="end"
            font-family="'Segoe UI', Arial, sans-serif" font-size="14" 
            fill="{theme['text_dim']}">
        {percentage:.1f}%
      </text>
    </g>''')
    
    # Calcula altura dinâmica
    height = base_height + len(sorted_langs) * bar_spacing
    
    # Gera áreas de foco (radar simplificado)
    focus_elements = []
    if config.galaxy_arms:
        focus_y = y_offset + len(sorted_langs) * bar_spacing + 60
        focus_spacing = (width - 100) / len(config.galaxy_arms)
        
        color_map = {
            "synapse_cyan": theme["synapse_cyan"],
            "dendrite_violet": theme["dendrite_violet"],
            "axon_amber": theme["axon_amber"],
        }
        
        for i, arm in enumerate(config.galaxy_arms):
            x = 50 + focus_spacing * i + focus_spacing / 2
            color = color_map.get(arm.get("color", "synapse_cyan"), theme["synapse_cyan"])
            
            tech_list = arm.get("tech", [])[:3]  # Máximo 3 itens
            tech_text = " • ".join(escape_xml(t) for t in tech_list)
            
            focus_elements.append(f'''
    <g transform="translate({x}, {focus_y})">
      <!-- Ponto focal -->
      <circle cx="0" cy="0" r="8" fill="{color}" opacity="0.8">
        <animate attributeName="r" values="8;12;8" dur="2s" repeatCount="indefinite"/>
      </circle>
      
      <!-- Nome da área -->
      <text y="25" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="600" 
            fill="{color}">
        {escape_xml(arm.get("name", ""))}
      </text>
      
      <!-- Tecnologias -->
      <text y="45" text-anchor="middle" 
            font-family="'Segoe UI', Arial, sans-serif" font-size="11" 
            fill="{theme['text_dim']}">
        {tech_text}
      </text>
    </g>''')
        
        height = focus_y + 80
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['nebula_bg']}" rx="10"/>
  
  <!-- Borda -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" 
        fill="none" stroke="{theme['dendrite_violet']}" stroke-width="1" 
        opacity="0.3" rx="10"/>
  
  <!-- Título -->
  <text x="425" y="35" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="20" font-weight="600" 
        fill="{theme['text_bright']}">
    🚀 Tech Stack & Focus Sectors
  </text>
  
  <!-- Barras de linguagem -->
  {''.join(lang_bars)}
  
  <!-- Áreas de foco -->
  {''.join(focus_elements)}
</svg>'''
    
    return svg
