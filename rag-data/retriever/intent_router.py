INTENT_MAP = {
    "symptoms" : ["mati", "hitam", "panas", "cepat habis"],
    "diagnosis": ["cek", "diagnosa", "test", "periksa", "langkah"],
    "cause" : ["penyebab", "kenapa", "karena apa", "alasan", "sebab"],
    "solution" : ["solusi", "cara mengatasi", "mengatasi", "perbaiki", "tindakan"],
    "risk" : ["resiko", "bahaya", "dampak", "akibat", "konsekuensi"],
    "cost" : ["biaya", "harga", "ongkos", "tarif", "cost"],
}

SECTION_PRIORITIES = {
    "symptoms": ["User Reports", "Common Symptoms", "Technical Overview"],
    "diagnosis": ["Diagnostic Steps", "Troubleshooting Guide", "Technical Overview"],
    "cause": ["Causes", "Technical Overview", "User Reports"],
    "solution": ["Solutions", "Troubleshooting Guide", "Technical Overview"],
    "risk": ["Risk Factors", "Technical Overview", "User Reports"],
    "cost": ["Costs", "Technical Overview", "User Reports"],
}

def get_intent_priority_sections(query: str, intent: str):
    intent_keywords = INTENT_MAP.get(intent, [])
    if any(keyword in query.lower() for keyword in intent_keywords):
        return SECTION_PRIORITIES.get(intent, [])
    return []