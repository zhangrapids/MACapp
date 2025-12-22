"""
normalizer.py - Normalize test names for consistent matching
"""

def normalize_name(name):
    """Normalize test names for matching"""
    name = ' '.join(name.split()).strip()
    name_lower = name.lower()
    
    # Common normalizations
    if 'glucose' in name_lower:
        return 'Glucose'
    
    # WBC must be checked before RBC
    if name_lower.startswith('wbc'):
        return 'WBC'
    if name_lower.startswith('rbc'):
        return 'RBC'
    
    if 'hgb' in name_lower or 'hemoglobin' in name_lower:
        return 'Hemoglobin'
    if 'hematocrit' in name_lower:
        return 'Hematocrit'
    if name_lower in ['potassium', 'k']:
        return 'Potassium'
    if name_lower in ['sodium', 'na']:
        return 'Sodium'
    if name_lower in ['chloride', 'cl']:
        return 'Chloride'
    if 'bun' in name_lower:
        return 'BUN'
    if 'creatinine' in name_lower:
        return 'Creatinine'
    if 'platelet' in name_lower:
        return 'Platelets'
    if name_lower.startswith('mcv'):
        return 'MCV'
    if name_lower.startswith('mch') and 'mchc' not in name_lower:
        return 'MCH'
    if name_lower.startswith('mchc'):
        return 'MCHC'
    if 'mpv' in name_lower:
        return 'MPV'
    if 'rdw' in name_lower:
        return 'RDW'
    
    return name