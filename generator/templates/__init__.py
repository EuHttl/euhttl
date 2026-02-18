"""
Template: Templates __init__
"""

from generator.templates.galaxy_header import generate_galaxy_header
from generator.templates.stats_card import generate_stats_card
from generator.templates.tech_stack import generate_tech_stack
from generator.templates.projects_constellation import generate_projects_constellation

__all__ = [
    'generate_galaxy_header',
    'generate_stats_card',
    'generate_tech_stack',
    'generate_projects_constellation',
]
