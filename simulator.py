import time
from datetime import datetime

from firebase_service import save_reading
from risk_engine import check_risk
from telegram_service import send_telegram_message


# =========================================================
# PATIENT INFORMATION
# =========================================================

PATIENT_ID = "mother_001"
PATIENT_NAME = "Demo Mother"
PATIENT_TYPE = "Mother"


# =========================================================
# DEMO SENSOR READINGS
# =========================================================

demo_readings = [

    # 1. NORMAL
    {
        "bp_systolic": 128,
        "bp_diastolic": 82,
        "spo2": 98,
        "urine_protein": "Negative",
        "bilirubin": 8.4
    },

    # 2. HIGH BLOOD PRESSURE
    {
        "bp_systolic": 153,
        "bp_diastolic": 94,
        "spo2": 97,
        "urine_protein": "Negative",
        "bilirubin": 9.1
    },

    # 3. NORMAL
    {
        "bp_systolic": 132,
        "bp_diastolic": 84,
        "spo2": 98,
        "urine_protein": "Negative",
        "bilirubin": 8.8
    },

    # 4. LOW OXYGEN
    {
        "bp_systolic": 134,
        "bp_diastolic": 85,
        "spo2": 91,
        "urine_protein": "Negative",
        "bilirubin": 9.2
    },

    # 5. NORMAL
    {
        "bp_systolic": 129,
        "bp_diastolic": 81,
        "spo2": 97,
        "urine_protein": "Negative",
        "bilirubin": 8.6
    },

    # 6. PROTEINURIA
    {
        "bp_systolic": 136,
        "bp_diastolic": 86,
        "spo2": 98,
        "urine_protein": "+",
        "bilirubin": 9.4
    },

    # 7. NORMAL
    {
        "bp_systolic": 130,
        "bp_diastolic": 83,
        "spo2": 99,
        "urine_protein": "Negative",
        "bilirubin": 8.9
    },

    # 8. MULTIPLE ABNORMALITIES
    {
        "bp_systolic": 166,
        "bp_diastolic": 98,
        "spo2": 89,
        "urine_protein": "++",
        "bilirubin": 14.09
    },

    # 9. NORMAL
    {
        "bp_systolic": 127,
        "bp_diastolic": 80,
        "spo2": 98,
        "urine_protein": "Negative",
        "bilirubin": 8.2
    },

    # 10. HIGH BILIRUBIN
    {
        "bp_systolic": 133,
        "bp_diastolic": 84,
        "spo2": 97,
        "urine_protein": "Negative",
        "bilirubin": 14.3
    },

    # 11. NORMAL
    {
        "bp_systolic": 131,
        "bp_diastolic": 82,
        "spo2": 98,
        "urine_protein": "Negative",
        "bilirubin": 9.0
    },

    # 12. HIGH BP + LOW OXYGEN
    {
        "bp_systolic": 160,
        "bp_diastolic": 96,
        "spo2": 88,
        "urine_protein": "Negative",
        "bilirubin": 10.2
    }
]


# =========================================================
# CREATE TELEGRAM ALERT
# =========================================================

def create_alert_message(reading, risks, timestamp):

    message = (
        "🚨 HEALTH ALERT 🚨\n\n"
        "Smart Maternal & Neonatal Health Monitoring\n\n"
        f"Patient: {PATIENT_NAME}\n"
        f"Patient ID: {PATIENT_ID}\n"
        f"Patient Type: {PATIENT_TYPE}\n\n"
        "Detected Risks:\n"
    )

    for risk in risks:
        message += f"⚠️ {risk}\n"

    message += (
        "\n"
        "📊 Current Readings\n\n"
        f"Blood Pressure: "
        f"{reading['bp_systolic']}/"
        f"{reading['bp_diastolic']} mmHg\n"
        f"SpO₂: {reading['spo2']}%\n"
        f"Urine Protein: {reading['urine_protein']}\n"
        f"Bilirubin: {reading['bilirubin']} mg/dL\n\n"
        f"🕒 Time: {timestamp}\n\n"
        "⚠️ Prototype alert — verify with "
        "appropriate clinical measurements."
    )

    return message


# =========================================================
# SIMULATION
# =========================================================

def simulate_patient():

    reading_index = 0

    while True:

        # -------------------------------------------------
        # Get next simulated sensor reading
        # -------------------------------------------------

        reading = demo_readings[reading_index]


        # -------------------------------------------------
        # Run risk engine
        # -------------------------------------------------

        risks = check_risk(
            reading["bp_systolic"],
            reading["bp_diastolic"],
            reading["spo2"],
            reading["urine_protein"],
            reading["bilirubin"]
        )


        # -------------------------------------------------
        # Timestamp
        # -------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # -------------------------------------------------
        # Determine risk flag
        # -------------------------------------------------

        if risks == "Normal":

            risk_flag = "Normal"

        else:

            risk_flag = risks


        # -------------------------------------------------
        # Build Firebase data
        # -------------------------------------------------

        data = {
            **reading,

            "patient_id": PATIENT_ID,

            "patient_name": PATIENT_NAME,

            "patient_type": PATIENT_TYPE,

            "risk_flag": risk_flag,

            "timestamp": timestamp
        }


        # -------------------------------------------------
        # Save reading to Firebase
        # -------------------------------------------------

        save_reading(
            PATIENT_ID,
            data
        )


        # -------------------------------------------------
        # Display reading in terminal
        # -------------------------------------------------

        print("\n====================================")
        print(f"Patient: {PATIENT_NAME}")
        print(f"Patient ID: {PATIENT_ID}")
        print(f"Reading: {reading_index + 1}")
        print(
            f"BP: "
            f"{reading['bp_systolic']}/"
            f"{reading['bp_diastolic']}"
        )
        print(f"SpO₂: {reading['spo2']}%")
        print(
            f"Protein: "
            f"{reading['urine_protein']}"
        )
        print(
            f"Bilirubin: "
            f"{reading['bilirubin']} mg/dL"
        )
        print(f"Risk: {risk_flag}")
        print(f"Time: {timestamp}")
        print("====================================")


        # -------------------------------------------------
        # TELEGRAM ALERT
        # -------------------------------------------------

        if risks != "Normal":

            alert_message = create_alert_message(
                reading,
                risks,
                timestamp
            )

            send_telegram_message(
                alert_message
            )


        # -------------------------------------------------
        # Move to next reading
        # -------------------------------------------------

        reading_index += 1


        # Restart after final reading

        if reading_index >= len(demo_readings):

            reading_index = 0


        # -------------------------------------------------
        # Wait before next sensor reading
        # -------------------------------------------------

        time.sleep(3)


# =========================================================
# START SIMULATION
# =========================================================

if __name__ == "__main__":

    simulate_patient()