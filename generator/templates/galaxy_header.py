"""
Template: Galaxy Header
"""
from generator.utils import escape_xml, generate_stars
import math


def generate_galaxy_header(config, theme: dict) -> str:
    """Gera SVG do cabeçalho com órbitas de tecnologias"""
    
    name = escape_xml(config.profile.get("name", ""))
    tagline = escape_xml(config.profile.get("tagline", ""))
    philosophy = escape_xml(config.profile.get("philosophy", ""))
    
    width = 850
    height = 300
    
    # Tecnologias para órbitas (baseado nas galaxy_arms do config)
    tech_orbits = []
    colors = {
        "synapse_cyan": theme['synapse_cyan'],
        "dendrite_violet": theme['dendrite_violet'],
        "axon_amber": theme['axon_amber'],
    }
    
    # Coleta todas as tecnologias das áreas de foco
    for arm in config.galaxy_arms:
        color = colors.get(arm.get("color", "synapse_cyan"), theme['synapse_cyan'])
        for tech in arm.get("tech", [])[:3]:  # Máximo 3 por área
            tech_orbits.append((tech, color))
    
    # Gera campo de estrelas
    stars = generate_stars(150, width, height, seed=42)
    
    # Calcula posições das tecnologias nas órbitas
    orbit_tech = []
    num_orbits = 3  # 3 órbitas
    orbit_radii = [80, 130, 180]  # Raios das órbitas
    
    tech_per_orbit = len(tech_orbits) // num_orbits + 1
    
    for i, (tech, color) in enumerate(tech_orbits[:12]):  # Máximo 12 tecnologias
        orbit_idx = i // tech_per_orbit
        if orbit_idx >= len(orbit_radii):
            orbit_idx = len(orbit_radii) - 1
        
        radius = orbit_radii[orbit_idx]
        angle = (2 * math.pi * (i % tech_per_orbit)) / tech_per_orbit + (orbit_idx * 0.5)
        
        x = 425 + radius * math.cos(angle)
        y = 150 + radius * math.sin(angle) * 0.6  # Achatado
        
        orbit_tech.append(f'''
    <g>
      <circle cx="{x}" cy="{y}" r="4" fill="{color}" opacity="0.8">
        <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="{x}" y="{y-10}" text-anchor="middle" 
            font-family="'Courier New', monospace" font-size="11" 
            fill="{color}" opacity="0.9">
        {escape_xml(tech)}
      </text>
    </g>''')
    
    # Gera linhas das órbitas
    orbit_paths = []
    for radius in orbit_radii:
        orbit_paths.append(f'''
    <ellipse cx="425" cy="150" rx="{radius}" ry="{radius * 0.6}" 
             stroke="{theme['starfield_dim']}" stroke-width="1" 
             fill="none" opacity="0.3"/>''')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <radialGradient id="centerGlow" cx="50%" cy="50%">
      <stop offset="0%" style="stop-color:{theme['synapse_cyan']};stop-opacity:0.8" />
      <stop offset="50%" style="stop-color:{theme['dendrite_violet']};stop-opacity:0.4" />
      <stop offset="100%" style="stop-color:{theme['void_black']};stop-opacity:0" />
    </radialGradient>
    
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['void_black']}"/>
  
  <!-- Starfield -->
  <g opacity="0.5">
    {stars}
  </g>
  
  <!-- Órbitas -->
  <g opacity="0.8">
    {''.join(orbit_paths)}
  </g>
  
  <!-- Centro com inicial -->
  <g filter="url(#glow)">
    <circle cx="425" cy="150" r="35" fill="url(#centerGlow)" opacity="0.6">
      <animate attributeName="r" values="35;38;35" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="425" cy="150" r="30" stroke="{theme['synapse_cyan']}" 
            stroke-width="2" fill="{theme['void_black']}" opacity="0.9"/>
    <text x="425" y="162" text-anchor="middle" 
          font-family="'Segoe UI', Arial, sans-serif" font-size="32" font-weight="bold" 
          fill="{theme['synapse_cyan']}">
      {name[0] if name else "H"}
    </text>
  </g>
  
  <!-- Tecnologias orbitando -->
  <g>
    {''.join(orbit_tech)}
  </g>
  
  <!-- Nome -->
  <text x="425" y="45" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="38" font-weight="700" 
        fill="{theme['text_bright']}">
    {name}
  </text>
  
  <!-- Subtítulo -->
  <text x="425" y="72" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="400"
        fill="{theme['text_dim']}">
    {tagline}
  </text>
  
  <!-- Filosofia -->
  <text x="425" y="270" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="14" 
        font-style="italic" fill="{theme['text_dim']}" opacity="0.8">
    {philosophy}
  </text>
</svg>'''
    
    return svg
