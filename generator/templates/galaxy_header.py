"""
Template: Galaxy Header - Banner com espiral galáctica animada
"""
from generator.utils import escape_xml, generate_stars


def generate_galaxy_header(config, theme: dict) -> str:
    """Gera SVG do cabeçalho galáctico"""
    
    name = escape_xml(config.profile.get("name", ""))
    tagline = escape_xml(config.profile.get("tagline", ""))
    
    width = 850
    height = 280
    
    # Gera campo de estrelas de fundo
    stars = generate_stars(200, width, height, seed=42)
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <!-- Gradientes -->
    <radialGradient id="coreGlow" cx="50%" cy="50%">
      <stop offset="0%" style="stop-color:{theme['glow_core']};stop-opacity:1" />
      <stop offset="50%" style="stop-color:{theme['synapse_cyan']};stop-opacity:0.6" />
      <stop offset="100%" style="stop-color:{theme['void_black']};stop-opacity:0" />
    </radialGradient>
    
    <linearGradient id="spiralGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{theme['synapse_cyan']};stop-opacity:0.8" />
      <stop offset="50%" style="stop-color:{theme['dendrite_violet']};stop-opacity:0.6" />
      <stop offset="100%" style="stop-color:{theme['axon_amber']};stop-opacity:0.4" />
    </linearGradient>
    
    <!-- Animações -->
    <animateTransform
      id="rotateGalaxy"
      attributeName="transform"
      type="rotate"
      from="0 425 140"
      to="360 425 140"
      dur="120s"
      repeatCount="indefinite"
    />
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['void_black']}"/>
  
  <!-- Starfield -->
  <g opacity="0.6">
    {stars}
  </g>
  
  <!-- Galáxia espiral -->
  <g>
    <animateTransform
      attributeName="transform"
      type="rotate"
      from="0 425 140"
      to="360 425 140"
      dur="120s"
      repeatCount="indefinite"
    />
    
    <!-- Núcleo galáctico -->
    <circle cx="425" cy="140" r="40" fill="url(#coreGlow)" opacity="0.8">
      <animate attributeName="r" values="40;45;40" dur="4s" repeatCount="indefinite"/>
    </circle>
    
    <!-- Braços espirais -->
    <path d="M 425 140 Q 450 120, 480 110 T 540 100 T 600 110" 
          stroke="url(#spiralGrad)" stroke-width="3" fill="none" opacity="0.5"/>
    <path d="M 425 140 Q 400 160, 370 170 T 310 180 T 250 170" 
          stroke="url(#spiralGrad)" stroke-width="3" fill="none" opacity="0.5"/>
    <path d="M 425 140 Q 440 165, 460 185 T 500 220 T 540 245" 
          stroke="url(#spiralGrad)" stroke-width="2.5" fill="none" opacity="0.4"/>
  </g>
  
  <!-- Estrelas cadentes -->
  <g>
    <line x1="100" y1="50" x2="150" y2="80" stroke="{theme['text_bright']}" stroke-width="1.5" opacity="0">
      <animate attributeName="opacity" values="0;1;0" dur="3s" begin="0s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" 
                        from="0 0" to="50 30" dur="3s" begin="0s" repeatCount="indefinite"/>
    </line>
    <line x1="700" y1="80" x2="750" y2="110" stroke="{theme['text_bright']}" stroke-width="1.5" opacity="0">
      <animate attributeName="opacity" values="0;1;0" dur="3s" begin="1.5s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" 
                        from="0 0" to="50 30" dur="3s" begin="1.5s" repeatCount="indefinite"/>
    </line>
  </g>
  
  <!-- Texto -->
  <text x="{width/2}" y="60" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="48" font-weight="bold" 
        fill="{theme['text_bright']}">
    {name}
  </text>
  
  <text x="{width/2}" y="240" text-anchor="middle" 
        font-family="'Segoe UI', Arial, sans-serif" font-size="20" 
        fill="{theme['text_dim']}">
    {tagline}
  </text>
</svg>'''
    
    return svg
