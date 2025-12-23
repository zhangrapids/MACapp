"""
matcher.py - Find matching test names from queries
"""
from difflib import get_close_matches
from normalizer import normalize_name

def find_test(query, test_names):
    """Find matching test name(s) - can return multiple matches"""
    query_normalized = normalize_name(query)
    query_lower = query.lower()
    
    matches = []
    
    # Exact match on normalized name
    for name in test_names:
        if name.lower() == query_normalized.lower():
            matches.append(name)
    
    if matches:
        return matches
    
    # Exact match on original query
    for name in test_names:
        if name.lower() == query_lower:
            matches.append(name)
    
    if matches:
        return matches
    
    # If query has multiple words (like "calcium urine"), require all words
    query_words = query_lower.split()
    if len(query_words) > 1:
        for name in test_names:
            name_lower = name.lower()
            if all(word in name_lower for word in query_words):
                matches.append(name)
        if matches:
            return matches
    
    # Single word query - find all tests containing that word
    for name in test_names:
        if query_lower in name.lower():
            matches.append(name)
    
    if matches:
        return matches
    
    # Fuzzy match as last resort
    fuzzy = get_close_matches(query_lower, [n.lower() for n in test_names], n=3, cutoff=0.8)
    if fuzzy:
        for name in test_names:
            if name.lower() in fuzzy:
                matches.append(name)
    
    return matches if matches else None