# 🎯 Professional Size Recommendation System

A comprehensive professional fashion sizing system with advanced morphology analysis and industry-standard fit engineering.

## 🚀 Features

- **Professional API** (`api.py`) - Standalone Flask API for size recommendations
- **Advanced Body Analysis** - Industry-standard morphology classification
- **Brand-Specific Recommendations** - Adjustments for 10+ major fashion brands
- **Virtual Fitting Room** - Professional fit analysis and comfort prediction
- **Professional Outfit Curation** - Styled recommendations by body type
- **Measurement Guide** - Interactive professional measurement instructions
- **Responsive Web Interface** - Complete HTML/CSS/JS frontend

## 📋 Quick Start

### 1. Install Dependencies
\`\`\`bash
pip install flask flask-cors
\`\`\`

### 2. Start the API Server
\`\`\`bash
python api.py
\`\`\`

### 3. Open the Web Interface
Open `index.html` in your browser or serve it via a local server.

## 🔧 API Usage

### Main Recommendation Endpoint
\`\`\`bash
POST http://localhost:5000/api/recommend
\`\`\`

**Request Body:**
\`\`\`json
{
  "measurements": {
    "poitrine": 95,
    "epaules": 45,
    "bassin": 85,
    "hanches": 95
  },
  "fit_preferences": {
    "poitrine": "standard",
    "epaules": "cintre",
    "bassin": "standard",
    "hanches": "standard"
  },
  "gender": "homme",
  "height": 175,
  "morphotype": "normal",
  "brand": "zara"
}
\`\`\`

**Response:**
\`\`\`json
{
  "success": true,
  "data": {
    "sizes": {
      "top": {"size": "M", "categories": ["Dress Shirts", "Blazers"]},
      "bottom": {"size": "42", "categories": ["Trousers", "Jeans"]}
    },
    "body_analysis": {
      "classification": {"type": "Athletic V-Shape"},
      "ratios": {"shoulder_hip": 1.05, "waist_hip": 0.89},
      "fit_analysis": {"advantages": [], "solutions": []}
    },
    "brand_recommendations": {
      "top": {"size": "S", "adjustment": -1, "note": "European slim fit"},
      "bottom": {"size": "40", "adjustment": -2, "note": "Size down for Zara"}
    },
    "virtual_fitting": {
      "comfort_prediction": 87,
      "professional_assessment": {"overall_fit": "Excellent"}
    },
    "outfit_recommendations": {
      "categories": [{"name": "Executive Professional", "outfits": []}]
    },
    "confidence": 92
  }
}
\`\`\`

### Other Endpoints

- `GET /api/brands` - Available brands and their adjustments
- `GET /api/measurement-guide` - Professional measurement instructions
- `GET /api/sizes` - Size charts for men and women
- `GET /api/health` - API health check

## 🏗️ Architecture

### Backend (`api.py`)
- **ProfessionalSizeRecommendationEngine** - Core sizing algorithm
- **Professional Body Analysis** - Advanced morphology classification
- **Brand Integration** - 10+ major fashion brands with fit adjustments
- **Virtual Fitting** - Comfort prediction and fit analysis
- **Professional Standards** - ISO 3635, EN 13402 compliance

### Frontend
- **Progressive Web App** - 4-step measurement and analysis process
- **Professional UI/UX** - Modern, responsive design
- **Real-time Validation** - Input validation with professional feedback
- **Local Storage** - Persistent data storage
- **Interactive Guides** - Professional measurement instructions

## 🎨 Professional Features

### Body Analysis
- **7 Body Types** - Athletic V-Shape, Hourglass, Rectangle, etc.
- **Professional Ratios** - Shoulder-hip, waist-hip, chest-waist analysis
- **Fit Engineering** - Challenge identification and solutions
- **Proportional Harmony** - Overall body proportion scoring

### Brand Intelligence
- **Zara** - European slim fit, size up for comfort
- **H&M** - Fast fashion standard, true to size tops
- **Uniqlo** - Japanese sizing, generous fit
- **Nike/Adidas** - Athletic performance fits
- **Luxury Brands** - Armani, Hugo Boss with precision tailoring

### Professional Styling
- **Seasonal Adaptations** - Color and fabric recommendations by season
- **Investment Priorities** - Wardrobe building strategy
- **Styling Philosophy** - Professional approach to dressing
- **Outfit Curation** - Complete looks by occasion and body type

## 🔌 Integration

### As a Microservice
```python
import requests

response = requests.post('http://localhost:5000/api/recommend', json={
    "measurements": {"poitrine": 95, "epaules": 45, "bassin": 85, "hanches": 95},
    "fit_preferences": {"poitrine": "standard", "epaules": "cintre"},
    "gender": "homme",
    "height": 175,
    "morphotype": "normal"
})

recommendation = response.json()['data']
