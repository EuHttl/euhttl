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
      <stop offset="0%" style="stop-color:{theme['glow_core']};stop-opacity:0.9" />
      <stop offset="30%" style="stop-color:{theme['synapse_cyan']};stop-opacity:0.7" />
      <stop offset="70%" style="stop-color:{theme['dendrite_violet']};stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:{theme['void_black']};stop-opacity:0" />
    </radialGradient>
    
    <linearGradient id="spiralGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{theme['synapse_cyan']};stop-opacity:0.9" />
      <stop offset="50%" style="stop-color:{theme['dendrite_violet']};stop-opacity:0.7" />
      <stop offset="100%" style="stop-color:{theme['axon_amber']};stop-opacity:0.5" />
    </linearGradient>
    
    <linearGradient id="textGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{theme['synapse_cyan']};stop-opacity:0.8" />
      <stop offset="50%" style="stop-color:{theme['text_bright']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{theme['dendrite_violet']};stop-opacity:0.8" />
    </linearGradient>
    
    <!-- Filtros para glow -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background com gradiente -->
  <rect width="{width}" height="{height}" fill="{theme['void_black']}"/>
  <rect width="{width}" height="{height}" fill="url(#coreGlow)" opacity="0.15"/>
  
  <!-- Starfield -->
  <g opacity="0.7">
    {stars}
  </g>
  
  <!-- Galáxia espiral central -->
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
    <circle cx="425" cy="140" r="50" fill="url(#coreGlow)" opacity="0.6" filter="url(#glow)">
      <animate attributeName="r" values="50;55;50" dur="4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.6;0.8;0.6" dur="4s" repeatCount="indefinite"/>
    </circle>
    
    <circle cx="425" cy="140" r="30" fill="{theme['synapse_cyan']}" opacity="0.4">
      <animate attributeName="r" values="30;35;30" dur="3s" repeatCount="indefinite"/>
    </circle>
    
    <!-- Braços espirais melhorados -->
    <path d="M 425 140 Q 470 120, 520 110 Q 570 105, 620 115 Q 670 125, 710 145" 
          stroke="url(#spiralGrad)" stroke-width="4" fill="none" opacity="0.6" 
          stroke-linecap="round" filter="url(#softGlow)"/>
    
    <path d="M 425 140 Q 380 160, 330 170 Q 280 175, 230 165 Q 180 155, 140 135" 
          stroke="url(#spiralGrad)" stroke-width="4" fill="none" opacity="0.6" 
          stroke-linecap="round" filter="url(#softGlow)"/>
    
    <path d="M 425 140 Q 445 175, 475 200 Q 510 225, 550 240 Q 590 250, 630 245" 
          stroke="url(#spiralGrad)" stroke-width="3.5" fill="none" opacity="0.5" 
          stroke-linecap="round"/>
    
    <path d="M 425 140 Q 405 105, 375 80 Q 340 55, 300 45 Q 260 35, 220 40" 
          stroke="url(#spiralGrad)" stroke-width="3.5" fill="none" opacity="0.5" 
          stroke-linecap="round"/>
  </g>
  
  <!-- Partículas brilhantes -->
  <g opacity="0.8">
    <circle cx="200" cy="80" r="2" fill="{theme['synapse_cyan']}" filter="url(#softGlow)">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="650" cy="200" r="2" fill="{theme['dendrite_violet']}" filter="url(#softGlow)">
      <animate attributeName="opacity" values="0.5;1;0.5" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="750" cy="100" r="2" fill="{theme['axon_amber']}" filter="url(#softGlow)">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/>
    </circle>
  </g>
  
  <!-- Estrelas cadentes -->
  <g>
    <line x1="120" y1="40" x2="170" y2="70" stroke="{theme['synapse_cyan']}" stroke-width="2" opacity="0" stroke-linecap="round">
      <animate attributeName="opacity" values="0;0.8;0" dur="2.5s" begin="0s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" 
                        from="0 0" to="50 30" dur="2.5s" begin="0s" repeatCount="indefinite"/>
    </line>
    <line x1="680" y1="60" x2="730" y2="90" stroke="{theme['dendrite_violet']}" stroke-width="2" opacity="0" stroke-linecap="round">
      <animate attributeName="opacity" values="0;0.8;0" dur="2.5s" begin="1.2s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" 
                        from="0 0" to="50 30" dur="2.5s" begin="1.2s" repeatCount="indefinite"/>
    </line>
  </g>
  
  <!-- Texto com efeitos -->
  <g filter="url(#softGlow)">
    <text x="{width/2}" y="75" text-anchor="middle" 
          font-family="'Segoe UI', 'SF Pro Display', -apple-system, sans-serif" 
          font-size="52" font-weight="700" 
          fill="url(#textGlow)" 
          letter-spacing="1">
      {name}
    </text>
  </g>
  
  <text x="{width/2}" y="230" text-anchor="middle" 
        font-family="'Segoe UI', 'SF Pro Display', -apple-system, sans-serif" 
        font-size="22" font-weight="400"
        fill="{theme['text_dim']}" 
        letter-spacing="0.5">
    {tagline}
  </text>
  
  <!-- Linha decorativa -->
  <line x1="250" y1="245" x2="600" y2="245" 
        stroke="{theme['synapse_cyan']}" stroke-width="1" opacity="0.3">
    <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite"/>
  </line>
</svg>'''
    
    return svg
