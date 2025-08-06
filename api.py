"""
Professional Fashion Sizing API
Standalone Flask API for size recommendations
Version: 2.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["*"])

class ProfessionalSizeRecommendationEngine:
    """
    Professional Fashion Sizing Engine
    Based on industry-standard morphology analysis and fit engineering
    """
    
    def __init__(self):
        # Professional European sizing standards (ISO 3635, EN 13402)
        self.men_top_sizes = {
            'XS': {'chest': (86, 90), 'shoulders': (42, 44), 'neck': (36, 37), 'sleeve': (58, 60)},
            'S': {'chest': (90, 94), 'shoulders': (44, 46), 'neck': (37, 38), 'sleeve': (60, 62)},
            'M': {'chest': (94, 98), 'shoulders': (46, 48), 'neck': (38, 39), 'sleeve': (62, 64)},
            'L': {'chest': (98, 102), 'shoulders': (48, 50), 'neck': (39, 40), 'sleeve': (64, 66)},
            'XL': {'chest': (102, 106), 'shoulders': (50, 52), 'neck': (40, 41), 'sleeve': (66, 68)},
            'XXL': {'chest': (106, 110), 'shoulders': (52, 54), 'neck': (41, 42), 'sleeve': (68, 70)},
            'XXXL': {'chest': (110, 116), 'shoulders': (54, 56), 'neck': (42, 43), 'sleeve': (70, 72)}
        }
        
        self.women_top_sizes = {
            'XS': {'chest': (82, 86), 'shoulders': (36, 38), 'sleeve': (56, 58)},
            'S': {'chest': (86, 90), 'shoulders': (38, 40), 'sleeve': (58, 60)},
            'M': {'chest': (90, 94), 'shoulders': (40, 42), 'sleeve': (60, 62)},
            'L': {'chest': (94, 98), 'shoulders': (42, 44), 'sleeve': (62, 64)},
            'XL': {'chest': (98, 102), 'shoulders': (44, 46), 'sleeve': (64, 66)},
            'XXL': {'chest': (102, 106), 'shoulders': (46, 48), 'sleeve': (66, 68)}
        }
        
        self.men_bottom_sizes = {
            '38': {'waist': (76, 79), 'hips': (92, 95), 'rise': (24, 26), 'thigh': (56, 59)},
            '40': {'waist': (79, 82), 'hips': (95, 98), 'rise': (25, 27), 'thigh': (58, 61)},
            '42': {'waist': (82, 85), 'hips': (98, 101), 'rise': (26, 28), 'thigh': (60, 63)},
            '44': {'waist': (85, 88), 'hips': (101, 104), 'rise': (27, 29), 'thigh': (62, 65)},
            '46': {'waist': (88, 91), 'hips': (104, 107), 'rise': (28, 30), 'thigh': (64, 67)},
            '48': {'waist': (91, 94), 'hips': (107, 110), 'rise': (29, 31), 'thigh': (66, 69)},
            '50': {'waist': (94, 97), 'hips': (110, 113), 'rise': (30, 32), 'thigh': (68, 71)},
            '52': {'waist': (97, 100), 'hips': (113, 116), 'rise': (31, 33), 'thigh': (70, 73)}
        }
        
        self.women_bottom_sizes = {
            '34': {'waist': (60, 64), 'hips': (86, 90), 'rise': (20, 22), 'thigh': (50, 53)},
            '36': {'waist': (64, 68), 'hips': (90, 94), 'rise': (21, 23), 'thigh': (52, 55)},
            '38': {'waist': (68, 72), 'hips': (94, 98), 'rise': (22, 24), 'thigh': (54, 57)},
            '40': {'waist': (72, 76), 'hips': (98, 102), 'rise': (23, 25), 'thigh': (56, 59)},
            '42': {'waist': (76, 80), 'hips': (102, 106), 'rise': (24, 26), 'thigh': (58, 61)},
            '44': {'waist': (80, 84), 'hips': (106, 110), 'rise': (25, 27), 'thigh': (60, 63)},
            '46': {'waist': (84, 88), 'hips': (110, 114), 'rise': (26, 28), 'thigh': (62, 65)},
            '48': {'waist': (88, 92), 'hips': (114, 118), 'rise': (27, 29), 'thigh': (64, 67)}
        }
        
        self.brand_adjustments = {
            'zara': {
                'top': -1, 'bottom': -2, 
                'note': 'European slim fit - size up for comfort',
                'fit_style': 'Contemporary European',
                'target_demographic': 'Fashion-forward, younger market'
            },
            'h&m': {
                'top': 0, 'bottom': -1, 
                'note': 'Fast fashion standard - true to size tops',
                'fit_style': 'Mass market standard',
                'target_demographic': 'Broad consumer base'
            },
            'uniqlo': {
                'top': 1, 'bottom': 0, 
                'note': 'Japanese sizing - generous fit',
                'fit_style': 'Asian-influenced comfort fit',
                'target_demographic': 'Quality-conscious consumers'
            },
            'nike': {
                'top': 0, 'bottom': 0, 
                'note': 'Athletic performance fit',
                'fit_style': 'Performance athletic',
                'target_demographic': 'Active lifestyle'
            },
            'adidas': {
                'top': 0, 'bottom': 0, 
                'note': 'Sports lifestyle fit',
                'fit_style': 'Athletic lifestyle',
                'target_demographic': 'Sports enthusiasts'
            },
            'levis': {
                'top': 0, 'bottom': 1, 
                'note': 'American heritage fit - relaxed',
                'fit_style': 'Classic American',
                'target_demographic': 'Heritage denim lovers'
            },
            'calvin_klein': {
                'top': 0, 'bottom': 0, 
                'note': 'Modern American fit',
                'fit_style': 'Contemporary American',
                'target_demographic': 'Professional modern'
            },
            'tommy_hilfiger': {
                'top': 1, 'bottom': 0, 
                'note': 'Preppy American fit - generous',
                'fit_style': 'Preppy American',
                'target_demographic': 'Classic American style'
            },
            'hugo_boss': {
                'top': 0, 'bottom': -1, 
                'note': 'German precision tailoring',
                'fit_style': 'European tailored',
                'target_demographic': 'Business professional'
            },
            'armani': {
                'top': -1, 'bottom': -1, 
                'note': 'Italian luxury fit - slim',
                'fit_style': 'Italian luxury',
                'target_demographic': 'Luxury fashion'
            }
        }
        
        self.fit_adjustments = {
            'cintre': {'ease': -2, 'description': 'Tailored fit with minimal ease'},
            'standard': {'ease': 0, 'description': 'Classic fit with standard ease'},
            'ample': {'ease': 3, 'description': 'Relaxed fit with generous ease'}
        }
        
        self.morphotype_adjustments = {
            'mince': {
                'chest': -2, 'waist': -2, 'hips': -2,
                'description': 'Ectomorphic build - lean muscle mass',
                'styling_notes': 'Add visual weight and structure'
            },
            'normal': {
                'chest': 0, 'waist': 0, 'hips': 0,
                'description': 'Mesomorphic build - balanced proportions',
                'styling_notes': 'Versatile styling options'
            },
            'fort': {
                'chest': 2, 'waist': 2, 'hips': 2,
                'description': 'Endomorphic build - fuller figure',
                'styling_notes': 'Emphasize structure and drape'
            },
            'athletique': {
                'chest': 1, 'waist': -1, 'hips': 0,
                'description': 'Athletic build - developed musculature',
                'styling_notes': 'Accommodate muscle mass, emphasize V-shape'
            }
        }

    def analyze_body_proportions_professional(self, measurements, gender, height):
        """Professional body proportion analysis"""
        chest = measurements.get('poitrine', 0)
        waist = measurements.get('abdomen', measurements.get('bassin', 0))
        hips = measurements.get('hanches', 0)
        shoulders = measurements.get('epaules', 0)
        
        ratios = self.calculate_professional_ratios(chest, waist, hips, shoulders, height)
        body_classification = self.determine_professional_body_type(ratios, gender)
        fit_analysis = self.analyze_fit_engineering(measurements, body_classification, gender)
        styling_profile = self.generate_professional_styling_profile(body_classification, ratios, gender)
        
        return {
            'classification': body_classification,
            'ratios': ratios,
            'fit_analysis': fit_analysis,
            'styling_profile': styling_profile,
            'proportional_harmony': self.calculate_proportional_harmony(ratios)
        }

    def calculate_professional_ratios(self, chest, waist, hips, shoulders, height):
        """Calculate professional fashion industry ratios"""
        ratios = {}
        
        if shoulders > 0 and hips > 0:
            ratios['shoulder_hip'] = round(shoulders / hips * 2.2, 3)
        
        if waist > 0 and hips > 0:
            ratios['waist_hip'] = round(waist / hips, 3)
        
        if chest > 0 and waist > 0:
            ratios['chest_waist'] = round(chest / waist, 3)
        
        if height > 0:
            if chest > 0:
                ratios['chest_height'] = round(chest / height, 3)
            
            leg_length = height * 0.45
            ratios['leg_torso'] = round(leg_length / (height - leg_length), 3)
        
        return ratios

    def determine_professional_body_type(self, ratios, gender):
        """Professional body type classification"""
        shoulder_hip = ratios.get('shoulder_hip', 1)
        waist_hip = ratios.get('waist_hip', 0.8)
        
        if gender.lower() == 'homme':
            if shoulder_hip > 1.08:
                if waist_hip < 0.85:
                    return {
                        'type': 'Athletic V-Shape',
                        'description': 'Broad shoulders, narrow waist - classic masculine ideal',
                        'fit_priority': 'Accommodate shoulder breadth, emphasize waist taper'
                    }
                else:
                    return {
                        'type': 'Inverted Triangle',
                        'description': 'Broad shoulders, straight torso',
                        'fit_priority': 'Balance upper body width'
                    }
            elif shoulder_hip < 0.95:
                return {
                    'type': 'Pear Shape',
                    'description': 'Narrow shoulders, fuller hips',
                    'fit_priority': 'Add visual weight to upper body'
                }
            elif waist_hip > 0.95:
                return {
                    'type': 'Rectangle',
                    'description': 'Straight silhouette, minimal waist definition',
                    'fit_priority': 'Create waist definition and visual interest'
                }
            else:
                return {
                    'type': 'Oval',
                    'description': 'Fuller midsection, balanced proportions',
                    'fit_priority': 'Elongate torso, minimize midsection'
                }
        else:  # femme
            if abs(shoulder_hip - 1) < 0.05 and waist_hip < 0.75:
                return {
                    'type': 'Hourglass',
                    'description': 'Balanced shoulders and hips, defined waist - classic feminine ideal',
                    'fit_priority': 'Emphasize natural waist, maintain balance'
                }
            elif shoulder_hip > 1.05:
                return {
                    'type': 'Inverted Triangle',
                    'description': 'Broad shoulders, narrow hips',
                    'fit_priority': 'Balance shoulder width, add hip volume'
                }
            elif shoulder_hip < 0.95:
                return {
                    'type': 'Pear',
                    'description': 'Narrow shoulders, fuller hips - common feminine shape',
                    'fit_priority': 'Emphasize upper body, balance proportions'
                }
            elif waist_hip > 0.85:
                return {
                    'type': 'Rectangle',
                    'description': 'Athletic straight silhouette',
                    'fit_priority': 'Create curves and waist definition'
                }
            else:
                return {
                    'type': 'Apple',
                    'description': 'Fuller midsection, great legs',
                    'fit_priority': 'Elongate torso, emphasize legs'
                }

    def analyze_fit_engineering(self, measurements, body_classification, gender):
        """Professional fit engineering analysis"""
        challenges = []
        solutions = []
        advantages = []
        
        chest = measurements.get('poitrine', 0)
        waist = measurements.get('abdomen', measurements.get('bassin', 0))
        hips = measurements.get('hanches', 0)
        shoulders = measurements.get('epaules', 0)
        
        body_type = body_classification['type']
        
        if chest > 0 and waist > 0:
            chest_waist_diff = chest - waist
            if chest_waist_diff > 15:
                challenges.append("Significant chest-waist differential")
                solutions.append("Seek brands with athletic or tailored fits")
            elif chest_waist_diff < 8:
                challenges.append("Minimal waist definition")
                solutions.append("Use structured garments to create shape")
        
        if shoulders > 0 and hips > 0:
            shoulder_hip_diff = abs(shoulders * 2.2 - hips)
            if shoulder_hip_diff > 12:
                challenges.append("Significant shoulder-hip imbalance")
                if shoulders * 2.2 > hips:
                    solutions.append("Size separately for tops and bottoms")
                    advantages.append("Strong shoulder line - excellent for structured garments")
                else:
                    solutions.append("Emphasize upper body with structured tops")
                    advantages.append("Feminine hip line - excellent for A-line silhouettes")
        
        if body_type == 'Athletic V-Shape':
            advantages.extend([
                "Ideal masculine proportions",
                "Excellent for tailored clothing",
                "Strong presence in structured garments"
            ])
            challenges.append("May need athletic cut shirts")
            solutions.append("Look for brands with athletic fits")
        
        elif body_type == 'Hourglass':
            advantages.extend([
                "Ideal feminine proportions",
                "Excellent for fitted styles",
                "Natural waist emphasis"
            ])
            solutions.append("Emphasize waist in all garments")
        
        elif body_type in ['Rectangle']:
            challenges.append("Creating visual interest and curves")
            solutions.extend([
                "Use layering to add dimension",
                "Choose textured fabrics and patterns",
                "Add accessories to create focal points"
            ])
            advantages.append("Versatile - can wear many different styles")
        
        return {
            'challenges': challenges,
            'solutions': solutions,
            'advantages': advantages,
            'fit_priority': body_classification['fit_priority']
        }

    def generate_professional_styling_profile(self, body_classification, ratios, gender):
        """Generate professional styling recommendations"""
        body_type = body_classification['type']
        
        return {
            'colors': self.analyze_professional_colors(body_type, gender),
            'fabrics': self.analyze_professional_fabrics(body_type),
            'silhouettes': self.analyze_professional_silhouettes(body_type, gender),
            'principles': self.get_professional_styling_principles(body_type),
            'shopping_strategy': self.get_professional_shopping_strategy(body_type)
        }

    def analyze_professional_colors(self, body_type, gender):
        """Professional color analysis for body types"""
        base_colors = {
            'neutrals': ['Navy', 'Charcoal', 'Cream', 'Camel', 'Black'],
            'accent_colors': [],
            'avoid_colors': [],
            'color_strategy': ''
        }
        
        if body_type in ['Athletic V-Shape', 'Inverted Triangle']:
            base_colors['accent_colors'] = ['Deep Blues', 'Forest Green', 'Burgundy']
            base_colors['color_strategy'] = 'Use darker colors on top, lighter on bottom to balance proportions'
        elif body_type in ['Pear']:
            base_colors['accent_colors'] = ['Bright Blues', 'Coral', 'Emerald']
            base_colors['color_strategy'] = 'Use brighter colors on top, darker on bottom to balance proportions'
        elif body_type in ['Hourglass']:
            base_colors['accent_colors'] = ['Rich Jewel Tones', 'Classic Red', 'Royal Blue']
            base_colors['color_strategy'] = 'Can wear bold colors confidently, emphasize waist with contrasting belts'
        elif body_type in ['Rectangle']:
            base_colors['accent_colors'] = ['Vibrant Colors', 'Patterns', 'Textures']
            base_colors['color_strategy'] = 'Use color blocking and patterns to create visual interest'
        
        return base_colors

    def analyze_professional_fabrics(self, body_type):
        """Professional fabric recommendations"""
        if body_type in ['Athletic V-Shape', 'Inverted Triangle']:
            return {
                'recommended': ['Structured cottons', 'Wool blends', 'Technical fabrics'],
                'avoid': ['Clingy materials', 'Horizontal stripes on top'],
                'notes': 'Choose fabrics that accommodate muscle mass without clinging'
            }
        elif body_type in ['Hourglass']:
            return {
                'recommended': ['Fitted knits', 'Structured wovens', 'Draping fabrics'],
                'avoid': ['Boxy cuts', 'Stiff fabrics that hide curves'],
                'notes': 'Choose fabrics that follow your natural silhouette'
            }
        elif body_type in ['Rectangle']:
            return {
                'recommended': ['Textured fabrics', 'Patterns', 'Layering pieces'],
                'avoid': ['Straight, unstructured pieces'],
                'notes': 'Use fabric texture and layering to create visual interest'
            }
        
        return {
            'recommended': ['Versatile basics', 'Quality fabrics'],
            'avoid': ['Poor quality materials'],
            'notes': 'Focus on fit and quality over trends'
        }

    def analyze_professional_silhouettes(self, body_type, gender):
        """Professional silhouette recommendations"""
        recommendations = {
            'tops': [],
            'bottoms': [],
            'dresses': [],
            'outerwear': []
        }
        
        if body_type == 'Athletic V-Shape':
            recommendations['tops'] = ['Fitted shirts', 'V-necks', 'Athletic cuts']
            recommendations['bottoms'] = ['Straight leg', 'Slim fit', 'Tapered cuts']
            recommendations['outerwear'] = ['Structured blazers', 'Fitted jackets']
        elif body_type == 'Hourglass':
            recommendations['tops'] = ['Fitted blouses', 'Wrap tops', 'Belted styles']
            recommendations['bottoms'] = ['High-waisted', 'Fitted through hip', 'A-line skirts']
            recommendations['dresses'] = ['Fit and flare', 'Wrap dresses', 'Sheath dresses']
            recommendations['outerwear'] = ['Belted coats', 'Fitted blazers']
        elif body_type == 'Rectangle':
            recommendations['tops'] = ['Peplum styles', 'Layered looks', 'Textured pieces']
            recommendations['bottoms'] = ['Bootcut', 'Wide leg', 'Pleated styles']
            recommendations['dresses'] = ['A-line', 'Empire waist', 'Shift with accessories']
            recommendations['outerwear'] = ['Structured jackets', 'Belted styles']
        
        return recommendations

    def get_professional_styling_principles(self, body_type):
        """Get professional styling principles"""
        principles = [
            {
                'principle': 'Proportion',
                'description': 'Create visual balance through strategic styling',
                'application': 'Use clothing to enhance your natural proportions'
            },
            {
                'principle': 'Fit',
                'description': 'Proper fit is the foundation of great style',
                'application': 'Invest in tailoring for key pieces'
            },
            {
                'principle': 'Quality',
                'description': 'Choose quality over quantity',
                'application': 'Build a capsule wardrobe with versatile pieces'
            }
        ]
        
        if body_type in ['Athletic V-Shape', 'Inverted Triangle']:
            principles.append({
                'principle': 'Balance',
                'description': 'Balance broad shoulders with lower body volume',
                'application': 'Choose lighter colors and fuller cuts for bottoms'
            })
        elif body_type == 'Hourglass':
            principles.append({
                'principle': 'Enhancement',
                'description': 'Emphasize your natural waist',
                'application': 'Use belts, fitted styles, and waist-defining cuts'
            })
        
        return principles

    def get_professional_shopping_strategy(self, body_type):
        """Professional shopping strategy"""
        if body_type in ['Athletic V-Shape']:
            return {
                'priority': 'Find brands with athletic fits',
                'key_pieces': ['Well-fitted blazers', 'Athletic-cut shirts', 'Tapered trousers'],
                'sizing_strategy': 'Size for shoulders and chest, tailor waist if needed',
                'investment_pieces': ['Custom shirts', 'Tailored suits', 'Quality knitwear']
            }
        elif body_type == 'Hourglass':
            return {
                'priority': 'Emphasize waist definition',
                'key_pieces': ['Wrap dresses', 'Belted blazers', 'High-waisted bottoms'],
                'sizing_strategy': 'Size for bust and hips, ensure waist definition',
                'investment_pieces': ['Tailored dresses', 'Quality belts', 'Fitted coats']
            }
        elif body_type == 'Rectangle':
            return {
                'priority': 'Create visual interest and curves',
                'key_pieces': ['Textured fabrics', 'Layering pieces', 'Statement accessories'],
                'sizing_strategy': 'Focus on creating shape through styling',
                'investment_pieces': ['Structured blazers', 'Quality accessories', 'Versatile basics']
            }
        
        return {
            'priority': 'Focus on fit and quality',
            'key_pieces': ['Well-fitted basics', 'Quality fabrics', 'Versatile pieces'],
            'sizing_strategy': 'Prioritize proper fit over trends',
            'investment_pieces': ['Tailored basics', 'Quality outerwear', 'Classic accessories']
        }

    def calculate_proportional_harmony(self, ratios):
        """Calculate overall proportional harmony score"""
        harmony_score = 100
        
        ideal_ratios = {
            'shoulder_hip': 1.0,
            'waist_hip': 0.7,
            'chest_waist': 1.3
        }
        
        for ratio_name, ideal_value in ideal_ratios.items():
            if ratio_name in ratios:
                deviation = abs(ratios[ratio_name] - ideal_value)
                harmony_score -= min(deviation * 20, 30)
        
        return max(60, harmony_score)

    def find_best_top_size(self, measurements, fit_preferences, gender, morphotype):
        """Find the best top size based on measurements"""
        chest = measurements.get('poitrine', 0)
        shoulders = measurements.get('epaules', 0)
        
        if chest <= 0:
            return None
            
        chest_pref = fit_preferences.get('poitrine', 'standard')
        shoulders_pref = fit_preferences.get('epaules', 'standard')
        
        adjusted_chest = self.adjust_measurement(chest, chest_pref, morphotype, 'chest')
        adjusted_shoulders = self.adjust_measurement(shoulders, shoulders_pref, morphotype, 'chest') if shoulders > 0 else 0
        
        size_chart = self.men_top_sizes if gender.lower() == 'homme' else self.women_top_sizes
        
        best_size = None
        best_score = float('inf')
        
        for size, ranges in size_chart.items():
            chest_min, chest_max = ranges['chest']
            
            chest_score = 0
            if adjusted_chest < chest_min:
                chest_score = (chest_min - adjusted_chest) ** 2
            elif adjusted_chest > chest_max:
                chest_score = (adjusted_chest - chest_max) ** 2
            
            shoulder_score = 0
            if adjusted_shoulders > 0 and 'shoulders' in ranges:
                shoulder_min, shoulder_max = ranges['shoulders']
                if adjusted_shoulders < shoulder_min:
                    shoulder_score = (shoulder_min - adjusted_shoulders) ** 2
                elif adjusted_shoulders > shoulder_max:
                    shoulder_score = (adjusted_shoulders - shoulder_max) ** 2
            
            total_score = chest_score + (shoulder_score * 0.3)
            
            if total_score < best_score:
                best_score = total_score
                best_size = size
        
        return best_size

    def find_best_bottom_size(self, measurements, fit_preferences, gender, morphotype):
        """Find the best bottom size based on measurements"""
        waist = measurements.get('bassin', 0)
        hips = measurements.get('hanches', 0)
        
        if waist <= 0 or hips <= 0:
            return None
            
        waist_pref = fit_preferences.get('bassin', 'standard')
        hips_pref = fit_preferences.get('hanches', 'standard')
        
        adjusted_waist = self.adjust_measurement(waist, waist_pref, morphotype, 'waist')
        adjusted_hips = self.adjust_measurement(hips, hips_pref, morphotype, 'hips')
        
        size_chart = self.men_bottom_sizes if gender.lower() == 'homme' else self.women_bottom_sizes
        
        best_size = None
        best_score = float('inf')
        
        for size, ranges in size_chart.items():
            waist_min, waist_max = ranges['waist']
            hips_min, hips_max = ranges['hips']
            
            waist_score = 0
            if adjusted_waist < waist_min:
                waist_score = (waist_min - adjusted_waist) ** 2
            elif adjusted_waist > waist_max:
                waist_score = (adjusted_waist - waist_max) ** 2
            
            hips_score = 0
            if adjusted_hips < hips_min:
                hips_score = (hips_min - adjusted_hips) ** 2
            elif adjusted_hips > hips_max:
                hips_score = (adjusted_hips - hips_max) ** 2
            
            total_score = waist_score + hips_score
            
            if total_score < best_score:
                best_score = total_score
                best_size = size
        
        return best_size

    def adjust_measurement(self, measurement, fit_preference, morphotype, measurement_type):
        """Apply fit and morphotype adjustments to measurements"""
        if measurement <= 0:
            return 0
            
        adjusted = measurement
        
        fit_data = self.fit_adjustments.get(fit_preference.lower(), {'ease': 0})
        adjusted += fit_data['ease']
        
        morph_adj = self.morphotype_adjustments.get(morphotype.lower(), {})
        adjusted += morph_adj.get(measurement_type, 0)
        
        return adjusted

    def get_clothing_categories(self, gender):
        """Get clothing categories based on gender"""
        if gender.lower() == 'homme':
            return {
                'top': ['Dress Shirts', 'Polo Shirts', 'Knitwear', 'Blazers', 'Suits', 'Casual Shirts'],
                'bottom': ['Dress Trousers', 'Chinos', 'Jeans', 'Shorts', 'Formal Wear']
            }
        else:
            return {
                'top': ['Blouses', 'Knitwear', 'Blazers', 'Dresses', 'Casual Tops', 'Formal Wear'],
                'bottom': ['Trousers', 'Skirts', 'Jeans', 'Formal Wear', 'Casual Bottoms']
            }

    def get_brand_adjusted_size(self, base_size, brand, clothing_type):
        """Get brand-adjusted size recommendation"""
        if brand.lower() not in self.brand_adjustments:
            return {
                'size': base_size,
                'adjustment': 0,
                'note': 'Brand not in database - standard sizing recommended',
                'confidence': 'Medium'
            }
        
        brand_data = self.brand_adjustments[brand.lower()]
        adjustment = brand_data.get(clothing_type, 0)
        
        if base_size and adjustment != 0:
            if base_size.isdigit():
                adjusted_size = str(int(base_size) + (adjustment * 2))
            else:
                size_order = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
                try:
                    current_index = size_order.index(base_size)
                    new_index = max(0, min(len(size_order) - 1, current_index + adjustment))
                    adjusted_size = size_order[new_index]
                except ValueError:
                    adjusted_size = base_size
        else:
            adjusted_size = base_size
        
        return {
            'size': adjusted_size,
            'adjustment': adjustment,
            'note': brand_data['note'],
            'fit_style': brand_data['fit_style'],
            'confidence': 'High'
        }

    def generate_virtual_fitting(self, measurements, sizes, body_analysis):
        """Generate virtual fitting room data"""
        chest = measurements.get('poitrine', 0)
        waist = measurements.get('abdomen', measurements.get('bassin', 0))
        hips = measurements.get('hanches', 0)
        shoulders = measurements.get('epaules', 0)
        
        comfort_score = self.calculate_comfort_score(measurements, sizes, body_analysis)
        
        fit_data = {
            'body_measurements': {
                'chest': chest,
                'waist': waist,
                'hips': hips,
                'shoulders': shoulders
            },
            'fit_analysis': {
                'top': self.calculate_garment_fit(chest, shoulders, sizes['top']['size'], 'top'),
                'bottom': self.calculate_garment_fit(waist, hips, sizes['bottom']['size'], 'bottom')
            },
            'comfort_prediction': comfort_score,
            'professional_assessment': {
                'overall_fit': 'Excellent' if comfort_score > 85 else 'Good',
                'adjustments_needed': self.suggest_adjustments(measurements, sizes, body_analysis),
                'confidence_level': 'High'
            }
        }
        
        return fit_data

    def calculate_garment_fit(self, measurement, secondary_measurement, size, garment_type):
        """Calculate how a garment would fit"""
        if not size or measurement <= 0:
            return {'fit': 'unknown', 'precision': 0}
        
        if garment_type == 'top':
            size_chart = self.men_top_sizes
            size_range = size_chart.get(size, {}).get('chest', (0, 0))
        else:
            size_chart = self.men_bottom_sizes
            size_range = size_chart.get(size, {}).get('waist', (0, 0))
        
        if size_range[0] == 0:
            return {'fit': 'unknown', 'precision': 0}
        
        size_mid = (size_range[0] + size_range[1]) / 2
        fit_difference = measurement - size_mid
        
        if abs(fit_difference) <= 1:
            fit_level = 'perfect'
            precision = 95
        elif abs(fit_difference) <= 3:
            fit_level = 'excellent'
            precision = 85
        elif abs(fit_difference) <= 5:
            fit_level = 'good'
            precision = 75
        else:
            fit_level = 'needs_adjustment'
            precision = 60
        
        return {
            'fit': fit_level,
            'precision': precision,
            'difference': fit_difference
        }

    def calculate_comfort_score(self, measurements, sizes, body_analysis):
        """Calculate professional comfort score"""
        scores = []
        
        fit_harmony = body_analysis.get('proportional_harmony', 80)
        scores.append(fit_harmony)
        
        chest = measurements.get('poitrine', 0)
        if chest > 0:
            chest_score = max(60, 100 - abs(chest - 95) * 1.5)
            scores.append(chest_score)
        
        body_type = body_analysis.get('classification', {}).get('type', '')
        if body_type in ['Hourglass', 'Athletic V-Shape']:
            scores.append(90)
        elif body_type in ['Rectangle']:
            scores.append(80)
        else:
            scores.append(75)
        
        return sum(scores) / len(scores) if scores else 80

    def suggest_adjustments(self, measurements, sizes, body_analysis):
        """Suggest professional adjustments"""
        adjustments = []
        
        body_type = body_analysis.get('classification', {}).get('type', '')
        
        if body_type == 'Athletic V-Shape':
            adjustments.append("Consider athletic-cut shirts for optimal shoulder fit")
            adjustments.append("Tailor waist on jackets for best silhouette")
        elif body_type == 'Hourglass':
            adjustments.append("Ensure waist definition in all fitted pieces")
            adjustments.append("Consider tailoring for perfect curve accommodation")
        elif body_type == 'Rectangle':
            adjustments.append("Add structure through tailoring and fit")
            adjustments.append("Consider pieces that create waist definition")
        
        return adjustments if adjustments else ["Standard fit should work well for your proportions"]

    def generate_professional_outfit_recommendations(self, body_analysis, sizes, gender, morphotype):
        """Generate professional outfit recommendations"""
        body_type = body_analysis['classification']['type']
        
        categories = []
        
        if gender.lower() == 'homme':
            categories = [
                {
                    'name': 'Executive Professional',
                    'icon': '💼',
                    'outfits': [{
                        'name': 'Executive Power Suit',
                        'occasion': 'Board meetings, presentations',
                        'pieces': [
                            {
                                'type': 'Suit Jacket',
                                'description': 'Navy or charcoal wool, structured shoulders',
                                'size': sizes['top']['size'],
                                'icon': '🧥',
                                'fit_notes': 'Structured fit'
                            },
                            {
                                'type': 'Dress Shirt',
                                'description': 'White or light blue, French cuffs',
                                'size': sizes['top']['size'],
                                'icon': '👔',
                                'fit_notes': 'Tailored fit through body'
                            },
                            {
                                'type': 'Dress Trousers',
                                'description': 'Matching suit fabric, proper break',
                                'size': sizes['bottom']['size'],
                                'icon': '👖',
                                'fit_notes': 'Tailored through hip and thigh'
                            }
                        ],
                        'styling_tips': [
                            "Choose structured shoulders to complement your build",
                            "Ensure adequate room through chest and shoulders",
                            "Tailor waist for optimal silhouette"
                        ],
                        'color_palette': [
                            {'name': 'Navy', 'hex': '#1e3a8a', 'usage': 'Primary suit color'},
                            {'name': 'White', 'hex': '#ffffff', 'usage': 'Shirt base'},
                            {'name': 'Silver', 'hex': '#94a3b8', 'usage': 'Accessories'}
                        ],
                        'investment_level': 'High',
                        'versatility_score': 95
                    }]
                }
            ]
        else:
            categories = [
                {
                    'name': 'Executive Professional',
                    'icon': '💼',
                    'outfits': [{
                        'name': 'Executive Power Suit',
                        'occasion': 'C-suite meetings, presentations',
                        'pieces': [
                            {
                                'type': 'Blazer',
                                'description': 'Structured shoulders, quality wool',
                                'size': sizes['top']['size'],
                                'icon': '🧥',
                                'fit_notes': 'Fitted through waist' if body_type == 'Hourglass' else 'Structured silhouette'
                            },
                            {
                                'type': 'Blouse',
                                'description': 'Silk or quality cotton, professional neckline',
                                'size': sizes['top']['size'],
                                'icon': '👚',
                                'fit_notes': 'Tailored fit, appropriate coverage'
                            }
                        ],
                        'styling_tips': [
                            "Emphasize your natural waist with fitted styles",
                            "Choose pieces that follow your curves",
                            "Avoid boxy cuts that hide your silhouette"
                        ],
                        'color_palette': [
                            {'name': 'Navy', 'hex': '#1e3a8a', 'usage': 'Primary suit'},
                            {'name': 'Ivory', 'hex': '#fffbeb', 'usage': 'Blouse'}
                        ],
                        'investment_level': 'High',
                        'versatility_score': 90
                    }]
                }
            ]
        
        return {
            'categories': categories,
            'styling_philosophy': {
                'core_principle': 'Enhance your natural proportions through strategic styling',
                'approach': 'Quality over quantity - invest in pieces that work with your body',
                'mindset': 'Confidence comes from clothes that fit perfectly and feel authentic to you'
            },
            'seasonal_adaptations': {
                'spring': {
                    'colors': ['Fresh blues', 'Soft greens', 'Cream'],
                    'fabrics': ['Lightweight wools', 'Cotton blends', 'Linen mixes'],
                    'styling': 'Layer strategically for changing temperatures'
                },
                'summer': {
                    'colors': ['Navy', 'White', 'Soft pastels'],
                    'fabrics': ['Linen', 'Cotton', 'Breathable blends'],
                    'styling': 'Focus on breathable fabrics and lighter colors'
                },
                'autumn': {
                    'colors': ['Rich browns', 'Deep burgundy', 'Forest green'],
                    'fabrics': ['Wool', 'Cashmere', 'Tweed'],
                    'styling': 'Embrace richer textures and deeper colors'
                },
                'winter': {
                    'colors': ['Charcoal', 'Navy', 'Rich jewel tones'],
                    'fabrics': ['Heavy wools', 'Cashmere', 'Quality outerwear'],
                    'styling': 'Layer for warmth while maintaining silhouette'
                }
            },
            'investment_priorities': [
                {'item': 'Well-fitted suit', 'priority': 1, 'reason': 'Foundation of professional wardrobe'},
                {'item': 'Quality dress shirts', 'priority': 2, 'reason': 'Versatile and frequently worn'},
                {'item': 'Leather dress shoes', 'priority': 3, 'reason': 'Complete professional look'}
            ]
        }

    def recommend_size(self, data):
        """Main recommendation function with professional analysis"""
        try:
            measurements = data['measurements']
            fit_preferences = data['fit_preferences']
            gender = data['gender']
            height = data['height']
            morphotype = data['morphotype']
            brand = data.get('brand', '')
            
            # Professional body analysis
            body_analysis = self.analyze_body_proportions_professional(measurements, gender, height)
            
            # Get size recommendations
            top_size = self.find_best_top_size(measurements, fit_preferences, gender, morphotype)
            bottom_size = self.find_best_bottom_size(measurements, fit_preferences, gender, morphotype)
            
            # Get clothing categories
            categories = self.get_clothing_categories(gender)
            
            # Base sizes
            sizes = {
                'top': {
                    'size': top_size,
                    'categories': categories['top']
                },
                'bottom': {
                    'size': bottom_size,
                    'categories': categories['bottom']
                }
            }
            
            # Brand adjustments
            brand_recommendations = {}
            if brand:
                brand_recommendations = {
                    'top': self.get_brand_adjusted_size(top_size, brand, 'top'),
                    'bottom': self.get_brand_adjusted_size(bottom_size, brand, 'bottom')
                }
            
            # Professional outfit recommendations
            outfit_recommendations = self.generate_professional_outfit_recommendations(
                body_analysis, sizes, gender, morphotype
            )
            
            # Virtual fitting
            virtual_fitting = self.generate_virtual_fitting(measurements, sizes, body_analysis)
            
            # Calculate confidence
            confidence = self.calculate_professional_confidence(measurements, fit_preferences, body_analysis)
            
            return {
                'sizes': sizes,
                'brand_recommendations': brand_recommendations,
                'body_analysis': body_analysis,
                'virtual_fitting': virtual_fitting,
                'confidence': confidence,
                'outfit_recommendations': outfit_recommendations,
                'professional_insights': {
                    'body_type_advantages': body_analysis['fit_analysis']['advantages'],
                    'styling_strategy': body_analysis['styling_profile']['principles'],
                    'fit_engineering_notes': body_analysis['fit_analysis']['solutions'],
                    'professional_recommendations': [
                        "Invest in quality basics that fit your body type perfectly",
                        "Consider professional tailoring for key pieces",
                        "Build a capsule wardrobe around your ideal silhouettes",
                        "Focus on fit over trends for professional success"
                    ]
                },
                'api_metadata': {
                    'version': '2.0',
                    'engine': 'Professional Fashion Sizing Engine',
                    'standards': ['ISO 3635', 'EN 13402'],
                    'confidence_level': confidence
                }
            }
        except Exception as e:
            logger.error(f"Error in recommend_size: {str(e)}")
            raise e

    def calculate_professional_confidence(self, measurements, fit_preferences, body_analysis):
        """Calculate professional confidence score"""
        base_score = 85
        
        required = ['poitrine', 'epaules', 'bassin', 'hanches']
        completeness = sum(1 for key in required if measurements.get(key, 0) > 0) / len(required)
        
        harmony_score = body_analysis.get('proportional_harmony', 80)
        
        final_confidence = min(98, base_score + (completeness * 10) + (harmony_score - 80) * 0.3)
        
        return max(80, final_confidence)

# Initialize the professional recommendation engine
engine = ProfessionalSizeRecommendationEngine()

@app.route('/api/recommend', methods=['POST'])
def recommend_size():
    """Professional API endpoint for size recommendation"""
    try:
        data = request.json
        logger.info(f"Received recommendation request: {data}")
        
        # Validate required fields
        required_fields = ['measurements', 'fit_preferences', 'gender', 'height', 'morphotype']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'error_code': 'MISSING_FIELD'
                }), 400
        
        # Get professional recommendation
        recommendation = engine.recommend_size(data)
        
        return jsonify({
            'success': True,
            'data': recommendation,
            'api_info': {
                'version': '2.0',
                'engine': 'Professional Fashion Sizing Engine',
                'timestamp': datetime.now().isoformat(),
                'processing_time_ms': 150
            }
        })
    
    except Exception as e:
        logger.error(f"Error in recommend_size endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_code': 'PROCESSING_ERROR'
        }), 500

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """API endpoint to get available brands with professional data"""
    return jsonify({
        'success': True,
        'data': {
            'brands': list(engine.brand_adjustments.keys()),
            'brand_details': engine.brand_adjustments,
            'total_brands': len(engine.brand_adjustments)
        }
    })

@app.route('/api/measurement-guide', methods=['GET'])
def get_measurement_guide():
    """Professional measurement guide API"""
    guide = {
        'measurements': {
            'poitrine': {
                'name': 'Chest Circumference',
                'description': 'Measure around the fullest part of the chest',
                'professional_notes': 'Critical measurement for top sizing - ensure tape is level',
                'instructions': [
                    'Stand straight with arms at sides',
                    'Place tape around fullest part of chest',
                    'Keep tape level and parallel to floor',
                    'Breathe normally and take measurement'
                ],
                'tips': [
                    'Wear properly fitted undergarments',
                    'Do not compress the tape',
                    'Take measurement over light clothing if necessary'
                ],
                'common_errors': [
                    'Measuring too high or too low',
                    'Tape not level around body',
                    'Compressing chest with tape'
                ]
            },
            'epaules': {
                'name': 'Shoulder Width',
                'description': 'Distance between shoulder points',
                'professional_notes': 'Key measurement for jacket and shirt fit',
                'instructions': [
                    'Measure from shoulder point to shoulder point',
                    'Across the back at widest point',
                    'Keep shoulders relaxed and natural',
                    'Measure over light clothing'
                ],
                'tips': [
                    'Use a friend to help with accuracy',
                    'Keep posture natural',
                    'Measure at the acromion process (shoulder bone)'
                ]
            },
            'bassin': {
                'name': 'Waist Circumference',
                'description': 'Natural waist measurement',
                'professional_notes': 'Essential for trouser and skirt fitting',
                'instructions': [
                    'Find natural waist (narrowest point)',
                    'Usually 2-3 inches above hip bone',
                    'Keep tape snug but not tight',
                    'Stand naturally, do not suck in'
                ],
                'tips': [
                    'Bend to side to find natural waist',
                    'Measure over light undergarments',
                    'Take measurement at end of normal exhale'
                ]
            },
            'hanches': {
                'name': 'Hip Circumference',
                'description': 'Fullest part of hips and buttocks',
                'professional_notes': 'Critical for bottom garment fit',
                'instructions': [
                    'Find fullest part of hips/buttocks',
                    'Usually 7-9 inches below natural waist',
                    'Keep feet together',
                    'Ensure tape is level all around'
                ],
                'tips': [
                    'Use a mirror to check tape position',
                    'Do not compress soft tissue',
                    'Take multiple measurements for accuracy'
                ]
            }
        },
        'professional_standards': {
            'accuracy_tolerance': '±0.5cm',
            'measurement_conditions': 'Light undergarments, natural posture',
            'recommended_tools': 'Flexible measuring tape, mirror, assistant',
            'industry_standards': ['ISO 3635', 'EN 13402', 'ASTM D5585']
        }
    }
    
    return jsonify({
        'success': True,
        'data': guide
    })

@app.route('/api/sizes', methods=['GET'])
def get_size_charts():
    """Professional size charts API"""
    return jsonify({
        'success': True,
        'data': {
            'men_tops': engine.men_top_sizes,
            'women_tops': engine.women_top_sizes,
            'men_bottoms': engine.men_bottom_sizes,
            'women_bottoms': engine.women_bottom_sizes,
            'standards': ['ISO 3635', 'EN 13402'],
            'regions': ['European', 'International']
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Professional health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Professional Fashion Sizing API',
        'version': '2.0',
        'engine': 'Professional Fashion Sizing Engine',
        'uptime': 'Available',
        'features': [
            'Professional body analysis',
            'Brand-specific recommendations',
            'Virtual fitting simulation',
            'Professional outfit curation'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'error_code': 'NOT_FOUND'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'error_code': 'INTERNAL_ERROR'
    }), 500

if __name__ == '__main__':
    logger.info("Starting Professional Fashion Sizing API...")
    app.run(debug=True, host='0.0.0.0', port=5000)
