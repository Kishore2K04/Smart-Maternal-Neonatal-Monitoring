def check_risk(sys, dia, spo2, protein, bili):
    """
    Evaluate a patient reading against the
    configured health thresholds.
    """

    risks = []

    if sys > 140 or dia > 90:
        risks.append("High Blood Pressure")

    if spo2 < 94:
        risks.append("Low Oxygen Level")

    if protein in ["+", "++"]:
        risks.append("Proteinuria Risk")

    if bili > 12:
        risks.append("Neonatal Jaundice Risk")

    if not risks:
        return "Normal"

    return risks