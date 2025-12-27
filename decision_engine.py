def decision_logic(label, confidence):
    if label == "Deepfake" and confidence > 80:
        return "HIGH", "Do not trust source. Verify identity immediately."
    elif confidence > 60:
        return "MEDIUM", "Secondary verification recommended."
    else:
        return "LOW", "Likely authentic."
