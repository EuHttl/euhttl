"""
Utilidades para o Galaxy Profile Generator
"""
import re
from typing import Dict, Tuple
import math


def escape_xml(text: str) -> str:
    """Escapa caracteres especiais XML/SVG"""
    if not text:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Converte cor hexadecimal para RGB"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def calculate_spiral_position(
    angle: float, 
    arm_index: int, 
    total_arms: int, 
    radius_scale: float = 1.0
) -> Tuple[float, float]:
    """Calcula posição em uma espiral galáctica"""
    arm_offset = (2 * math.pi * arm_index) / total_arms
    spiral_angle = angle + arm_offset
    
    # Equação de espiral logarítmica
    radius = radius_scale * math.exp(0.2 * angle)
    
    x = radius * math.cos(spiral_angle)
    y = radius * math.sin(spiral_angle)
    
    return (x, y)


def generate_stars(count: int, width: int, height: int, seed: int = 42) -> str:
    """Gera elementos SVG de estrelas com distribuição pseudo-aleatória"""
    import random
    random.seed(seed)
    
    stars_svg = []
    for i in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.uniform(0.5, 2.5)
        opacity = random.uniform(0.3, 1.0)
        
        stars_svg.append(
            f'<circle cx="{x}" cy="{y}" r="{size}" '
            f'fill="#ffffff" opacity="{opacity}"/>'
        )
    
    return "\n".join(stars_svg)


def format_number(num: int) -> str:
    """Formata números grandes com K/M sufixos"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def get_language_color(language: str) -> str:
    """Retorna cor padrão para linguagens de programação"""
    colors = {
        "Python": "#3572A5",
        "JavaScript": "#f1e05a",
        "TypeScript": "#2b7489",
        "Java": "#b07219",
        "C#": "#178600",
        "C++": "#f34b7d",
        "Go": "#00ADD8",
        "Rust": "#dea584",
        "PHP": "#4F5D95",
        "Ruby": "#701516",
        "Swift": "#ffac45",
        "Kotlin": "#F18E33",
        "Dart": "#00B4AB",
        "HTML": "#e34c26",
        "CSS": "#563d7c",
        "Shell": "#89e051",
    }
    return colors.get(language, "#858585")
