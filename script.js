class ProfessionalSizeRecommendationApp {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.apiUrl = 'http://localhost:5000/api';
        this.measurements = {};
        this.fitPreferences = {};
        this.morphotype = {};
        
        this.init();
    }

    init() {
        this.loadSavedData();
        this.setupFitPreferences();
        this.setupEventListeners();
        this.setupBrandSelection();
        this.addMeasurementGuideButtons();
        this.initializeAnimations();
    }

    initializeAnimations() {
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.5s ease';
            document.body.style.opacity = '1';
        }, 100);
    }

    setupEventListeners() {
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener('change', (e) => this.saveMeasurement(e.target));
            input.addEventListener('focus', (e) => this.highlightInputGroup(e.target));
            input.addEventListener('blur', (e) => this.validateMeasurement(e.target));
        });

        document.querySelectorAll('input[type="radio"]').forEach(input => {
            input.addEventListener('change', (e) => this.saveSelection(e.target));
        });
    }

    highlightInputGroup(input) {
        const inputGroup = input.closest('.input-group');
        if (inputGroup) {
            inputGroup.style.transform = 'translateY(-2px)';
            inputGroup.style.transition = 'transform 0.2s ease';
        }
    }

    validateMeasurement(input) {
        const inputGroup = input.closest('.input-group');
        if (inputGroup) {
            inputGroup.style.transform = 'translateY(0)';
        }
        
        const value = parseFloat(input.value);
        const name = input.name;
        
        const validationRanges = {
            'poitrine': { min: 70, max: 150 },
            'epaules': { min: 35, max: 60 },
            'bassin': { min: 60, max: 130 },
            'hanches': { min: 70, max: 140 },
            'height': { min: 140, max: 220 }
        };
        
        if (validationRanges[name] && value > 0) {
            const range = validationRanges[name];
            if (value < range.min || value > range.max) {
                this.showValidationWarning(input, `Value should be between ${range.min} and ${range.max}cm`);
            } else {
                this.clearValidationWarning(input);
            }
        }
    }

    showValidationWarning(input, message) {
        const inputGroup = input.closest('.input-group');
        let warning = inputGroup.querySelector('.validation-warning');
        
        if (!warning) {
            warning = document.createElement('div');
            warning.className = 'validation-warning';
            inputGroup.appendChild(warning);
        }
        
        warning.textContent = message;
        warning.style.color = '#f59e0b';
        warning.style.fontSize = '0.8125rem';
        warning.style.marginTop = '4px';
        warning.style.animation = 'fadeIn 0.3s ease';
    }

    clearValidationWarning(input) {
        const inputGroup = input.closest('.input-group');
        const warning = inputGroup.querySelector('.validation-warning');
        if (warning) {
            warning.remove();
        }
    }

    setupFitPreferences() {
        const topMeasurements = ['cou', 'poitrine', 'abdomen', 'epaules', 'longueur_bras'];
        const bottomMeasurements = ['bassin', 'hanches', 'cuisse', 'mollet', 'jambe_interieur', 'hauteur_hanches'];
        
        const fitOptions = [
            { value: 'cintre', label: 'Tailored', description: 'Precision fit with minimal ease' },
            { value: 'standard', label: 'Classic', description: 'Traditional fit with standard ease' },
            { value: 'ample', label: 'Relaxed', description: 'Comfortable fit with generous ease' }
        ];

        this.createFitSection('fit-top', topMeasurements, fitOptions, 'Upper Body');
        this.createFitSection('fit-bottom', bottomMeasurements, fitOptions, 'Lower Body');
    }

    createFitSection(containerId, measurements, fitOptions, sectionTitle) {
        const container = document.getElementById(containerId);
        
        measurements.forEach(measurement => {
            const measurementName = this.getMeasurementDisplayName(measurement);
            
            const item = document.createElement('div');
            item.className = 'fit-preference-item';
            
            item.innerHTML = `
                <h4>${measurementName}</h4>
                <div class="radio-group">
                    ${fitOptions.map(option => `
                        <label class="radio-label">
                            <input type="radio" name="fit_${measurement}" value="${option.value}" required>
                            <span>${option.label}</span>
                        </label>
                    `).join('')}
                </div>
            `;
            
            container.appendChild(item);
        });
    }

    getMeasurementDisplayName(measurement) {
        const names = {
            'cou': 'Neck Circumference',
            'poitrine': 'Chest Circumference',
            'abdomen': 'Waist Circumference',
            'epaules': 'Shoulder Width',
            'longueur_bras': 'Arm Length',
            'bassin': 'Natural Waist',
            'hanches': 'Hip Circumference',
            'cuisse': 'Thigh Circumference',
            'mollet': 'Calf Circumference',
            'jambe_interieur': 'Inseam Length',
            'hauteur_hanches': 'Hip Height'
        };
        return names[measurement] || measurement;
    }

    saveMeasurement(input) {
        this.measurements[input.name] = parseFloat(input.value) || 0;
        this.saveToLocalStorage();
        this.updateProgressIndicator();
    }

    saveSelection(input) {
        if (input.name.startsWith('fit_')) {
            const measurement = input.name.replace('fit_', '');
            this.fitPreferences[measurement] = input.value;
        } else {
            this.morphotype[input.name] = input.value;
        }
        this.saveToLocalStorage();
        this.updateProgressIndicator();
    }

    updateProgressIndicator() {
        const requiredMeasurements = ['poitrine', 'epaules', 'bassin', 'hanches'];
        const completedMeasurements = requiredMeasurements.filter(key => 
            this.measurements[key] && this.measurements[key] > 0
        ).length;
        
        const progressPercentage = (completedMeasurements / requiredMeasurements.length) * 100;
        
        const progressIndicator = document.querySelector('.progress-indicator');
        if (progressIndicator) {
            progressIndicator.style.width = `${progressPercentage}%`;
        }
    }

    saveToLocalStorage() {
        const data = {
            measurements: this.measurements,
            fitPreferences: this.fitPreferences,
            morphotype: this.morphotype,
            currentStep: this.currentStep,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('professionalSizeRecommendationData', JSON.stringify(data));
    }

    loadSavedData() {
        const saved = localStorage.getItem('professionalSizeRecommendationData');
        if (saved) {
            const data = JSON.parse(saved);
            this.measurements = data.measurements || {};
            this.fitPreferences = data.fitPreferences || {};
            this.morphotype = data.morphotype || {};
            
            this.restoreFormValues();
        }
    }

    restoreFormValues() {
        Object.entries(this.measurements).forEach(([name, value]) => {
            const input = document.querySelector(`input[name="${name}"]`);
            if (input && value > 0) {
                input.value = value;
            }
        });

        Object.entries(this.fitPreferences).forEach(([measurement, value]) => {
            const input = document.querySelector(`input[name="fit_${measurement}"][value="${value}"]`);
            if (input) {
                input.checked = true;
            }
        });

        Object.entries(this.morphotype).forEach(([name, value]) => {
            const input = document.querySelector(`input[name="${name}"][value="${value}"]`);
            if (input) {
                input.checked = true;
            }
        });
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep < this.totalSteps) {
                this.animateStepTransition(() => {
                    this.currentStep++;
                    this.updateStepDisplay();
                    this.saveToLocalStorage();
                });
            }
        }
    }

    prevStep() {
        if (this.currentStep > 1) {
            this.animateStepTransition(() => {
                this.currentStep--;
                this.updateStepDisplay();
            });
        }
    }

    animateStepTransition(callback) {
        const currentStepEl = document.querySelector('.step.active');
        if (currentStepEl) {
            currentStepEl.style.transform = 'translateX(-20px)';
            currentStepEl.style.opacity = '0';
            
            setTimeout(() => {
                callback();
                const newStepEl = document.querySelector('.step.active');
                if (newStepEl) {
                    newStepEl.style.transform = 'translateX(20px)';
                    newStepEl.style.opacity = '0';
                    
                    setTimeout(() => {
                        newStepEl.style.transition = 'all 0.3s ease';
                        newStepEl.style.transform = 'translateX(0)';
                        newStepEl.style.opacity = '1';
                    }, 50);
                }
            }, 150);
        } else {
            callback();
        }
    }

    validateCurrentStep() {
        switch (this.currentStep) {
            case 1:
                return this.validateMeasurements();
            case 2:
                return this.validateFitPreferences();
            case 3:
                return this.validateMorphotype();
            default:
                return true;
        }
    }

    validateMeasurements() {
        const required = ['poitrine', 'epaules', 'bassin', 'hanches'];
        const missing = required.filter(field => !this.measurements[field] || this.measurements[field] <= 0);
        
        if (missing.length > 0) {
            this.showProfessionalError(`Please complete the following required measurements: ${missing.map(f => this.getMeasurementDisplayName(f)).join(', ')}`);
            return false;
        }
        return true;
    }

    validateFitPreferences() {
        const validMeasurementFields = [
            'cou', 'poitrine', 'abdomen', 'epaules', 'longueur_bras',
            'bassin', 'hanches', 'cuisse', 'mollet', 'jambe_interieur', 'hauteur_hanches'
        ];
        
        const enteredMeasurements = Object.keys(this.measurements).filter(key => 
            validMeasurementFields.includes(key) && 
            this.measurements[key] && 
            this.measurements[key] > 0
        );
        
        const missingPreferences = enteredMeasurements.filter(measurement => 
            !this.fitPreferences[measurement] || this.fitPreferences[measurement] === ''
        );
        
        if (missingPreferences.length > 0) {
            const missingNames = missingPreferences.map(m => this.getMeasurementDisplayName(m));
            this.showProfessionalError(`Please define fit preferences for: ${missingNames.join(', ')}`);
            return false;
        }
        return true;
    }

    validateMorphotype() {
        const genderInput = document.querySelector('input[name="gender"]:checked');
        const heightInput = document.querySelector('input[name="height"]');
        const morphotypeInput = document.querySelector('input[name="morphotype"]:checked');
        
        if (!genderInput) {
            this.showProfessionalError('Please select your gender');
            return false;
        }
        
        if (!heightInput || !heightInput.value) {
            this.showProfessionalError('Please enter your height');
            return false;
        }
        
        if (!morphotypeInput) {
            this.showProfessionalError('Please select your body type');
            return false;
        }
        
        const height = parseInt(heightInput.value);
        if (height < 140 || height > 220) {
            this.showProfessionalError('Please enter a valid height between 140 and 220 cm');
            return false;
        }
        
        this.morphotype.gender = genderInput.value;
        this.morphotype.height = heightInput.value;
        this.morphotype.morphotype = morphotypeInput.value;
        
        const brandSelect = document.getElementById('brand-select');
        if (brandSelect) {
            this.morphotype.brand = brandSelect.value;
        }
        
        return true;
    }

    updateStepDisplay() {
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.toggle('active', index + 1 === this.currentStep);
        });

        document.querySelectorAll('.progress-step').forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.toggle('active', stepNumber === this.currentStep);
            step.classList.toggle('completed', stepNumber < this.currentStep);
        });
    }

    async getRecommendation() {
        if (!this.validateCurrentStep()) {
            return;
        }

        this.currentStep = 4;
        this.updateStepDisplay();
        
        document.getElementById('loading').style.display = 'block';
        document.getElementById('results').style.display = 'none';

        try {
            const requestData = {
                measurements: this.measurements,
                fit_preferences: this.fitPreferences,
                gender: this.morphotype.gender,
                height: parseInt(this.morphotype.height),
                morphotype: this.morphotype.morphotype,
                brand: this.morphotype.brand || ''
            };

            console.log('Sending request:', requestData);

            const response = await fetch(`${this.apiUrl}/recommend`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Received response:', data);
            
            if (data.success) {
                this.displayProfessionalResults(data.data);
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }

        } catch (error) {
            console.error('Error:', error);
            this.showProfessionalError(`Analysis failed: ${error.message}. Please ensure the API server is running on port 5000.`);
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    }

    displayProfessionalResults(recommendation) {
        const resultsContainer = document.getElementById('results');
        
        const bodyAnalysis = recommendation.body_analysis;
        const sizes = recommendation.sizes;
        const outfitRecs = recommendation.outfit_recommendations;
        const virtualFitting = recommendation.virtual_fitting;
        const brandRecs = recommendation.brand_recommendations;
        
        resultsContainer.innerHTML = `
        <!-- Professional Confidence Score -->
        <div class="confidence-score">
            <div class="section-icon-large">📊</div>
            Professional Analysis Complete: ${Math.round(recommendation.confidence)}% Precision
        </div>
        
        <!-- Size Recommendations -->
        <div class="results-section">
            <h3>
                <div class="section-icon-large">📐</div>
                Professional Size Recommendations
            </h3>
            <div class="results-grid">
                <div class="result-card size-card">
                    <h4>Upper Body</h4>
                    <div class="size-display">${sizes.top.size || 'N/A'}</div>
                    <div class="categories">
                        ${sizes.top.categories.map(cat => 
                            `<span class="category-tag">${cat}</span>`
                        ).join('')}
                    </div>
                </div>
                
                <div class="result-card size-card">
                    <h4>Lower Body</h4>
                    <div class="size-display">${sizes.bottom.size || 'N/A'}</div>
                    <div class="categories">
                        ${sizes.bottom.categories.map(cat => 
                            `<span class="category-tag">${cat}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        </div>

        <!-- Professional Body Analysis -->
        <div class="results-section">
            <h3>
                <div class="section-icon-large">🔬</div>
                Professional Body Analysis
            </h3>
            <div class="body-analysis-professional">
                <div class="analysis-primary">
                    <h4>Body Classification</h4>
                    <div class="body-type-display">${bodyAnalysis.classification.type}</div>
                    <p class="body-description">${bodyAnalysis.classification.description}</p>
                    <div class="fit-priority">
                        <strong>Fit Priority:</strong> ${bodyAnalysis.classification.fit_priority}
                    </div>
                </div>
                
                <div class="analysis-details">
                    <div class="analysis-section">
                        <h5>Professional Ratios</h5>
                        <div class="ratios-display">
                            ${Object.entries(bodyAnalysis.ratios).map(([key, value]) => `
                                <div class="ratio-item">
                                    <span class="ratio-label">${key.replace('_', '/')}:</span>
                                    <span class="ratio-value">${value}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="analysis-section">
                        <h5>Fit Engineering Analysis</h5>
                        <div class="fit-analysis">
                            <div class="advantages">
                                <strong>Advantages:</strong>
                                <ul>
                                    ${bodyAnalysis.fit_analysis.advantages.map(adv => 
                                        `<li>${adv}</li>`
                                    ).join('')}
                                </ul>
                            </div>
                            <div class="solutions">
                                <strong>Professional Solutions:</strong>
                                <ul>
                                    ${bodyAnalysis.fit_analysis.solutions.map(sol => 
                                        `<li>${sol}</li>`
                                    ).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Brand Recommendations -->
        ${this.displayProfessionalBrandRecommendations(brandRecs)}

        <!-- Virtual Fitting -->
        ${this.displayProfessionalVirtualFitting(virtualFitting)}

        <!-- Professional Outfit Recommendations -->
        ${this.displayProfessionalOutfitRecommendations(outfitRecs)}

        <!-- Professional Insights -->
        <div class="results-section">
            <h3>
                <div class="section-icon-large">💡</div>
                Professional Styling Insights
            </h3>
            <div class="professional-insights">
                <div class="styling-philosophy">
                    <h4>Styling Philosophy</h4>
                    <p>${outfitRecs.styling_philosophy.core_principle}</p>
                    <div class="philosophy-details">
                        <div class="approach">
                            <strong>Approach:</strong> ${outfitRecs.styling_philosophy.approach}
                        </div>
                        <div class="mindset">
                            <strong>Mindset:</strong> ${outfitRecs.styling_philosophy.mindset}
                        </div>
                    </div>
                </div>
                
                <div class="investment-priorities">
                    <h4>Investment Priorities</h4>
                    <div class="priority-list">
                        ${outfitRecs.investment_priorities.map((item, index) => `
                            <div class="priority-item">
                                <div class="priority-number">${item.priority}</div>
                                <div class="priority-details">
                                    <strong>${item.item}</strong>
                                    <p>${item.reason}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
    
        resultsContainer.style.display = 'block';
        document.getElementById('results-buttons').style.display = 'flex';
        
        this.animateResultsDisplay();
        
        this.lastRecommendation = recommendation;
        this.saveToLocalStorage();
    }

    animateResultsDisplay() {
        const sections = document.querySelectorAll('.results-section');
        sections.forEach((section, index) => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                section.style.transition = 'all 0.5s ease';
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    displayProfessionalBrandRecommendations(brandRecs) {
        if (!brandRecs || (!brandRecs.top && !brandRecs.bottom)) return '';
        
        return `
            <div class="results-section brand-recommendations">
                <h3>
                    <div class="section-icon-large">🏷️</div>
                    Brand-Specific Recommendations
                </h3>
                <div class="brand-grid">
                    ${brandRecs.top ? `
                        <div class="brand-card">
                            <h4>Upper Body</h4>
                            <div class="brand-size-display">${brandRecs.top.size}</div>
                            <div class="brand-details">
                                <div class="fit-style">${brandRecs.top.fit_style}</div>
                                <div class="brand-adjustment">
                                    ${brandRecs.top.adjustment !== 0 ? 
                                        `<span class="adjustment-badge ${brandRecs.top.adjustment > 0 ? 'size-up' : 'size-down'}">
                                            ${brandRecs.top.adjustment > 0 ? '+' : ''}${brandRecs.top.adjustment} size adjustment
                                        </span>` : 
                                        '<span class="adjustment-badge neutral">True to size</span>'
                                    }
                                </div>
                                <p class="brand-note">${brandRecs.top.note}</p>
                            </div>
                        </div>
                    ` : ''}
                    
                    ${brandRecs.bottom ? `
                        <div class="brand-card">
                            <h4>Lower Body</h4>
                            <div class="brand-size-display">${brandRecs.bottom.size}</div>
                            <div class="brand-details">
                                <div class="fit-style">${brandRecs.bottom.fit_style}</div>
                                <div class="brand-adjustment">
                                    ${brandRecs.bottom.adjustment !== 0 ? 
                                        `<span class="adjustment-badge ${brandRecs.bottom.adjustment > 0 ? 'size-up' : 'size-down'}">
                                            ${brandRecs.bottom.adjustment > 0 ? '+' : ''}${brandRecs.bottom.adjustment} size adjustment
                                        </span>` : 
                                        '<span class="adjustment-badge neutral">True to size</span>'
                                    }
                                </div>
                                <p class="brand-note">${brandRecs.bottom.note}</p>
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    displayProfessionalVirtualFitting(virtualFitting) {
        if (!virtualFitting) return '';
        
        return `
            <div class="results-section virtual-fitting">
                <h3>
                    <div class="section-icon-large">👗</div>
                    Professional Fit Analysis
                </h3>
                <div class="virtual-fitting-professional">
                    <div class="fit-assessment">
                        <h4>Overall Fit Assessment</h4>
                        <div class="assessment-score">
                            <div class="score-circle">
                                <div class="score-value">${Math.round(virtualFitting.comfort_prediction)}%</div>
                                <div class="score-label">Fit Precision</div>
                            </div>
                        </div>
                        <div class="professional-assessment">
                            <div class="assessment-item">
                                <strong>Overall Fit:</strong> ${virtualFitting.professional_assessment.overall_fit}
                            </div>
                            <div class="assessment-item">
                                <strong>Confidence Level:</strong> ${virtualFitting.professional_assessment.confidence_level}
                            </div>
                        </div>
                    </div>
                    
                    <div class="fit-recommendations">
                        <h4>Professional Adjustments</h4>
                        <ul class="adjustment-list">
                            ${virtualFitting.professional_assessment.adjustments_needed.map(adj => 
                                `<li>${adj}</li>`
                            ).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    displayProfessionalOutfitRecommendations(outfitRecs) {
        if (!outfitRecs) return '';
        
        return `
            <div class="results-section outfit-recommendations">
                <h3>
                    <div class="section-icon-large">👔</div>
                    Professional Outfit Curation
                </h3>
                <div class="outfit-categories-professional">
                    ${outfitRecs.categories.map(category => `
                        <div class="outfit-category-professional">
                            <h4>
                                <span class="category-icon">${category.icon}</span>
                                ${category.name}
                            </h4>
                            <div class="outfit-items-professional">
                                ${category.outfits.map(outfit => `
                                    <div class="outfit-card-professional">
                                        <div class="outfit-header-professional">
                                            <h5>${outfit.name}</h5>
                                            <div class="outfit-meta">
                                                <span class="occasion-tag">${outfit.occasion}</span>
                                                <span class="investment-level">${outfit.investment_level} Investment</span>
                                            </div>
                                        </div>
                                        
                                        <div class="outfit-pieces-professional">
                                            ${outfit.pieces.map(piece => `
                                                <div class="piece-item-professional">
                                                    <div class="piece-icon">${piece.icon}</div>
                                                    <div class="piece-details-professional">
                                                        <strong>${piece.type}</strong>
                                                        <p>${piece.description}</p>
                                                        <small>Size: ${piece.size}</small>
                                                        ${piece.fit_notes ? `<div class="fit-notes">${piece.fit_notes}</div>` : ''}
                                                    </div>
                                                </div>
                                            `).join('')}
                                        </div>
                                        
                                        <div class="styling-tips-professional">
                                            <h6>Professional Styling Tips</h6>
                                            <ul>
                                                ${outfit.styling_tips.map(tip => `<li>${tip}</li>`).join('')}
                                            </ul>
                                        </div>
                                        
                                        <div class="color-palette-professional">
                                            <h6>Color Palette</h6>
                                            <div class="color-swatches-professional">
                                                ${outfit.color_palette.map(color => `
                                                    <div class="color-swatch-professional" 
                                                         style="background-color: ${color.hex}" 
                                                         title="${color.name} - ${color.usage}">
                                                    </div>
                                                `).join('')}
                                            </div>
                                        </div>
                                        
                                        <div class="outfit-metrics">
                                            <div class="versatility-score">
                                                Versatility: ${outfit.versatility_score}%
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="seasonal-adaptations-professional">
                    <h4>Seasonal Styling Adaptations</h4>
                    <div class="seasons-grid-professional">
                        ${Object.entries(outfitRecs.seasonal_adaptations).map(([season, data]) => `
                            <div class="season-card-professional">
                                <h5>${season.charAt(0).toUpperCase() + season.slice(1)}</h5>
                                <div class="season-details">
                                    <div class="season-colors">
                                        <strong>Colors:</strong>
                                        <span>${data.colors.join(', ')}</span>
                                    </div>
                                    <div class="season-fabrics">
                                        <strong>Fabrics:</strong>
                                        <span>${data.fabrics.join(', ')}</span>
                                    </div>
                                    <div class="season-styling">
                                        <strong>Approach:</strong>
                                        <span>${data.styling}</span>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    showProfessionalError(message) {
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <div class="error-icon">⚠️</div>
            <div class="error-content">
                <strong>Validation Required</strong>
                <p>${message}</p>
            </div>
        `;
        
        const currentStepEl = document.querySelector('.step.active');
        const buttonsEl = currentStepEl.querySelector('.step-buttons') || currentStepEl.querySelector('.btn-primary');
        
        if (buttonsEl) {
            buttonsEl.parentNode.insertBefore(errorDiv, buttonsEl);
        } else {
            currentStepEl.appendChild(errorDiv);
        }
        
        errorDiv.style.opacity = '0';
        errorDiv.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            errorDiv.style.transition = 'all 0.3s ease';
            errorDiv.style.opacity = '1';
            errorDiv.style.transform = 'translateY(0)';
        }, 50);
        
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.style.opacity = '0';
                errorDiv.style.transform = 'translateY(-10px)';
                setTimeout(() => errorDiv.remove(), 300);
            }
        }, 7000);
    }

    async setupBrandSelection() {
        const brandContainer = document.createElement('div');
        brandContainer.className = 'brand-selection';
        brandContainer.innerHTML = `
            <div class="input-group">
                <label for="brand-select">Brand Preference (Optional)</label>
                <select id="brand-select" name="brand">
                    <option value="">Select a brand for specific recommendations</option>
                </select>
                <span class="help-text">Get brand-specific size adjustments and fit insights</span>
            </div>
        `;
        
        const morphotypeForm = document.querySelector('.morphotype-form');
        if (morphotypeForm) {
            morphotypeForm.appendChild(brandContainer);
        }
        
        await this.loadBrands();
    }

    async loadBrands() {
        try {
            const response = await fetch(`${this.apiUrl}/brands`);
            const data = await response.json();
            const select = document.getElementById('brand-select');
            
            if (select && data.success && data.data.brands) {
                data.data.brands.forEach(brand => {
                    const option = document.createElement('option');
                    option.value = brand;
                    option.textContent = brand.charAt(0).toUpperCase() + brand.slice(1).replace('_', ' ');
                    select.appendChild(option);
                });
                
                select.addEventListener('change', (e) => {
                    this.morphotype.brand = e.target.value;
                    this.saveToLocalStorage();
                });
            }
        } catch (error) {
            console.error('Error loading brands:', error);
        }
    }

    addMeasurementGuideButtons() {
        const measurementInputs = document.querySelectorAll('input[type="number"]');
        measurementInputs.forEach(input => {
            const inputGroup = input.closest('.input-group');
            if (inputGroup && ['poitrine', 'epaules', 'bassin', 'hanches'].includes(input.name)) {
                const guideButton = document.createElement('button');
                guideButton.type = 'button';
                guideButton.className = 'guide-button';
                guideButton.innerHTML = 'Guide';
                guideButton.onclick = () => this.showMeasurementGuide(input.name);
                
                inputGroup.appendChild(guideButton);
            }
        });
    }

    async showMeasurementGuide(measurementType) {
        try {
            const response = await fetch(`${this.apiUrl}/measurement-guide`);
            const data = await response.json();
            
            if (data.success && data.data.measurements[measurementType]) {
                const measurementData = data.data.measurements[measurementType];
                this.displayProfessionalMeasurementGuide(measurementData);
            }
        } catch (error) {
            console.error('Error loading measurement guide:', error);
        }
    }

    displayProfessionalMeasurementGuide(measurementData) {
        const modal = document.createElement('div');
        modal.className = 'measurement-guide-modal';
        modal.innerHTML = `
            <div class="guide-content">
                <div class="guide-header">
                    <h3>${measurementData.name}</h3>
                    <button class="close-guide" onclick="this.closest('.measurement-guide-modal').remove()">×</button>
                </div>
                <div class="guide-body">
                    <p class="guide-description">${measurementData.description}</p>
                    
                    ${measurementData.professional_notes ? `
                        <div class="professional-note">
                            <strong>Professional Note:</strong> ${measurementData.professional_notes}
                        </div>
                    ` : ''}
                    
                    <div class="guide-section">
                        <h4>📋 Step-by-Step Instructions</h4>
                        <ol>
                            ${measurementData.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                        </ol>
                    </div>
                    
                    <div class="guide-section">
                        <h4>💡 Professional Tips</h4>
                        <ul>
                            ${measurementData.tips.map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    </div>
                    
                    ${measurementData.common_errors ? `
                        <div class="guide-section">
                            <h4>⚠️ Common Errors to Avoid</h4>
                            <ul>
                                ${measurementData.common_errors.map(error => `<li>${error}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.transition = 'opacity 0.3s ease';
            modal.style.opacity = '1';
        }, 50);
    }

    saveResults() {
        if (this.lastRecommendation) {
            const resultsData = {
                timestamp: new Date().toISOString(),
                measurements: this.measurements,
                fitPreferences: this.fitPreferences,
                morphotype: this.morphotype,
                recommendation: this.lastRecommendation,
                version: '2.0'
            };
            
            const savedResults = JSON.parse(localStorage.getItem('professionalSavedRecommendations') || '[]');
            savedResults.push(resultsData);
            localStorage.setItem('professionalSavedRecommendations', JSON.stringify(savedResults));
            
            this.showSuccessMessage('Professional analysis saved successfully');
        }
    }

    showSuccessMessage(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <div class="success-icon">✅</div>
            <div class="success-content">${message}</div>
        `;
        
        document.body.appendChild(successDiv);
        
        successDiv.style.position = 'fixed';
        successDiv.style.top = '20px';
        successDiv.style.right = '20px';
        successDiv.style.background = 'var(--accent-gradient)';
        successDiv.style.color = 'white';
        successDiv.style.padding = '16px 24px';
        successDiv.style.borderRadius = 'var(--radius-md)';
        successDiv.style.boxShadow = 'var(--shadow-lg)';
        successDiv.style.zIndex = '1001';
        successDiv.style.opacity = '0';
        successDiv.style.transform = 'translateX(100px)';
        
        setTimeout(() => {
            successDiv.style.transition = 'all 0.3s ease';
            successDiv.style.opacity = '1';
            successDiv.style.transform = 'translateX(0)';
        }, 50);
        
        setTimeout(() => {
            successDiv.style.opacity = '0';
            successDiv.style.transform = 'translateX(100px)';
            setTimeout(() => successDiv.remove(), 300);
        }, 3000);
    }

    resetForm() {
        if (confirm('Are you sure you want to start over? All current data will be lost.')) {
            localStorage.removeItem('professionalSizeRecommendationData');
            location.reload();
        }
    }
}

// Global functions for button clicks
let app;

function nextStep() {
    app.nextStep();
}

function prevStep() {
    app.prevStep();
}

function getRecommendation() {
    app.getRecommendation();
}

function saveResults() {
    app.saveResults();
}

function resetForm() {
    app.resetForm();
}

// Initialize professional app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app = new ProfessionalSizeRecommendationApp();
});
