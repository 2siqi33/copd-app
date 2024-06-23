

import streamlit as st
import lightgbm as lgb
import numpy as np

# Load the AKD and CKD models
aki_model = lgb.Booster(model_file='aki_model.txt')
akd_model = lgb.Booster(model_file='akd_model.txt')
mortality_model = lgb.Booster(model_file='mortality_model.txt')

# Mapping for Urine_protein and AKIGrade values
AKIGrade_mapping = {"Stage 0": 0, "Stage 1": 1, "Stage 2": 2, "Stage 3": 3}
Renal_function_trajectory_mapping = {"NKD": 0, "AKI recovery": 1, "subacute AKD": 2, "AKD with AKI": 3}
Aspirin_mapping = {"NO": 0, "Yes": 1}
Dopamine_and_epinephrine_drugs_mapping = {"NO": 0, "Yes": 1}
MODS_mapping = {"NO": 0, "Yes": 1}
Digitalis_drugs_mapping = {"NO": 0, "Yes": 1}
Coronary_heart_disease_mapping = {"NO": 0, "Yes": 1}
Shock_mapping = {"NO": 0, "Yes": 1}
def predict_aki_probability(features):
    aki_prob = aki_model.predict(features)
    return aki_prob[0]


def predict_akd_probability(features):
    akd_prob = akd_model.predict(features)
    return akd_prob[0]

def predict_mortality_probability(features):
    mortality_prob = mortality_model.predict(features)
    return mortality_prob[0]


def main():
    st.title('AKI, AKD and mortality Probability Prediction in COPD patients')

# User selects which content to display
    selected_content = st.radio("", ("Model Introduction", "AKI, AKD and mortality Prediction"))

    if selected_content == "Model Introduction":
        st.subheader("Model Introduction")
        st.write("The online application employs the LightGBM model to forecast the probability of acute kidney injury (AKI), acute kidney disease (AKD), and mortality in patients with chronic obstructive pulmonary disease (COPD) using patient metrics.")
        # Disclaimer
        st.subheader("Disclaimer")
        st.write("The predictions generated by this model are based on historical data and statistical patterns, and they may not be entirely accurate or applicable to every individual.")
        st.write("**For Patients:**")
        st.write("- The predictions presented by this platform are intended for informational purposes only and should not be regarded as a substitute for professional medical advice, diagnosis, or treatment.")
        st.write("- Consult with your healthcare provider for personalized medical guidance and decisions concerning your health.")
        st.write("**For Healthcare Professionals:**")
        st.write("- This platform should be considered as a supplementary tool to aid clinical decision-making and should not be the sole determinant of patient care.")
        st.write("- Clinical judgment and expertise should always take precedence in medical practice.")
        st.write("**For Researchers:**")
        st.write("- While this platform can serve as a valuable resource for research purposes, it is crucial to validate its predictions within your specific clinical context and patient population.")
        st.write("- Ensure that your research adheres to all ethical and regulatory standards.")
        st.write("The creators of this online platform and model disclaim any responsibility for decisions or actions taken based on the predictions provided herein. Please use this tool responsibly and always consider individual patient characteristics and clinical context when making medical decisions.")
        st.write("By utilizing this online platform, you agree to the terms and conditions outlined in this disclaimer.")

    elif selected_content == "AKI, AKD and mortality Prediction":
        st.subheader("AKI, AKD and mortality Prediction in COPD patients")

    # User selects prediction type (AKD or AKI)
        prediction_type = st.radio("Select Prediction Type", ("AKI Prediction", "AKD Prediction", "mortality Prediction"))

    # Feature input
        features = []

        if prediction_type == "AKI Prediction":
            st.subheader("AKI Features")
 
            Scr = st.number_input("Scr (umol/L)", value=0.0, format="%.2f", key="Scr_AKI") 
            NEU_percentage = st.number_input("NEU percentage (%)", value=0.0, format="%.2f", key="NEU_percentage_AKI")
            cystatin_C = st.number_input("cystatin C (mg/L)", value=0.0, format="%.2f", key="cystatin_C_AKI")
            BUN = st.number_input("BUN(mmol/L)", value=0.0, format="%.2f", key="BUN_AKI")
            LDH = st.number_input("LDH (U/L)", value=0.0, format="%.2f", key="LDH_AKI")
            Dopamine_and_epinephrine_drugs = st.selectbox("Dopamine and epinephrine drugs", ["NO", "Yes"], key="Dopamine_and_epinephrine_drugs_AKI")
            Age = st.number_input("Age (years)", value=0, format="%d", key="Age_AKI")
            HDL_C = st.number_input("HDL-C (mmol/L)", value=0.0, format="%.2f", key="HDL_C_AKI")
            TBIL = st.number_input("TBIL (umol/L)", value=0.0, format="%.2f", key="TBIL_AKI")
            CRP = st.number_input("CRP (mg/L)", value=0.0, format="%.2f", key="CRP_AKI")
            ADA = st.number_input("ADA (U/L)", value=0.0, format="%.2f", key="ADA_AKI")
            RBC = st.number_input("RBC (10^12/L)", value=0.0, format="%.2f", key="RBC_AKI")
            PCT = st.number_input("PCT (ng/ml)", value=0.0, format="%.2f", key="PCT_AKI")
            MODS = st.selectbox("MODS", ["NO", "Yes"], key="MODS_AKI")
            Glucose = st.number_input("Glucose (mmol/L)", value=0.0, format="%.2f", key="Glucose_AKI")

            Dopamine_and_epinephrine_drugs_encoded = Dopamine_and_epinephrine_drugs_mapping[Dopamine_and_epinephrine_drugs]
            MODS_encoded = MODS_mapping[MODS]

            features.extend([Scr, NEU_percentage, cystatin_C, BUN, LDH, Dopamine_and_epinephrine_drugs_encoded, Age, HDL_C, TBIL, CRP, ADA, RBC, PCT,MODS_encoded, Glucose])
            if st.button("Predict AKI Probability"):
                aki_prob = predict_aki_probability(np.array(features).reshape(1, -1))
                st.write(f"AKI Probability: {aki_prob:.2f}")

        elif prediction_type == "AKD Prediction":
            st.subheader("AKD Features")
 
            Age = st.number_input("Age (years)", value=0, format="%d", key="Age_AKD")
            AKIGrade = st.selectbox("AKI Grade", ["Stage 0", "Stage 1", "Stage 2", "Stage 3"], key="AKIGrade_AKD")
            HDL_C = st.number_input("HDL-C (mmol/L)", value=0.0, format="%.2f", key="HDL_C_AKD")
            Scr = st.number_input("Scr (umol/L)", value=0.0, format="%.2f", key="Scr_AKD") 
            BUN = st.number_input("BUN(mmol/L)", value=0.0, format="%.2f", key="BUN_AKD")
            NEU_percentage = st.number_input("NEU percentage (%)", value=0.0, format="%.2f", key="NEU_percentage_AKD")
            Monocyte_count = st.number_input("Monocyte count (10^9/L)", value=0.0, format="%.2f", key="Monocyte_count_AKD")
            Albumin_globuin = st.number_input("Albumin/globulin", value=0.0, format="%.2f", key="Albumin_globulin_AKD")
            Fibrinogen = st.number_input("Fibrinogen (g/L)", value=0.0, format="%.2f", key="Fibrinogen_AKD")
            PCO2 = st.number_input("PCO2 (mmHg)", value=0.0, format="%.2f", key="PCO2_AKD")
            TCO2 = st.number_input("TCO2 (mmol/L)", value=0.0, format="%.2f", key="TCO2_AKD")
            Glucose = st.number_input("Glucose (mmol/L)", value=0.0, format="%.2f", key="Glucose_AKD")
            HCO3_ = st.number_input("HCO3- (mmol/L)", value=0.0, format="%.2f", key="HCO3_AKD")
            Aspirin = st.selectbox("Aspirin", ["NO", "Yes"], key="Aspirin_AKD")
            Albumin = st.number_input("Albumin (g/L)", value=0.0, format="%.2f", key="Albumin_AKD")

        # Map AKIGrade back to 0, 1, 2, 3 for prediction
            AKIGrade_encoded = AKIGrade_mapping[AKIGrade]
            Aspirin_encoded = Aspirin_mapping[Aspirin]
            features.extend([Age, AKIGrade_encoded, HDL_C, Scr, BUN, NEU_percentage, Monocyte_count, Albumin_globuin, Fibrinogen, PCO2, TCO2, Glucose, HCO3_, Aspirin_encoded, Albumin])

            if st.button("Predict AKD Probability"):
                akd_prob = predict_akd_probability(np.array(features).reshape(1, -1))
                st.write(f"AKD Probability: {akd_prob:.2f}")


        elif prediction_type == "mortality Prediction":
            st.subheader("Mortality Features")

            Dopamine_and_epinephrine_drugs = st.selectbox("Dopamine and epinephrine drugs", ["NO", "Yes"], key="Dopamine_and_epinephrine_drugs_mortality")
            cystatin_C = st.number_input("cystatin C (mg/L)", value=0.0, format="%.2f", key="cystatin_C_mortality")
            Renal_function_trajectory = st.selectbox("Renal function trajectory", ["NKD" ,"AKI recovery","subacute AKD","AKD with AKI"], key="Renal_function_trajectory_mortality")
            Albumin = st.number_input("Albumin (g/L)", value=0.0, format="%.2f", key="Albumin_mortality")
            NEU_percentage = st.number_input("NEU percentage (%)", value=0.0, format="%.2f", key="NEU_percentage_mortality")
            Digitalis_drugs = st.selectbox("Digitalis drugs", ["NO", "Yes"], key="Digitalis_drugs_mortality")
            AST = st.number_input("AST (U/L)", value=0.0, format="%.2f", key="AST_mortality")
            LDH = st.number_input("LDH (U/L)", value=0.0, format="%.2f", key="LDH_mortality")
            Hemoglobin = st.number_input("Hemoglobin (g/L)", value=0.0, format="%.2f", key="Hemoglobin_mortality")
            Monocyte_count = st.number_input("Monocyte count (10^9/L)", value=0.0, format="%.2f", key="Monocyte_count_mortality")
            CRP = st.number_input("CRP (mg/L)", value=0.0, format="%.2f", key="CRP_mortality")
            Coronary_heart_disease = st.selectbox("Coronary heart disease", ["NO", "Yes"], key="Coronary_heart_disease_mortality")
            MODS = st.selectbox("MODS", ["NO", "Yes"], key="MODS_mortality")
            Age = st.number_input("Age (years)", value=0, format="%d", key="Age_mortality") 
            Shock = st.selectbox("Shock", ["NO", "Yes"], key="Shock_mortality")
        
            Dopamine_and_epinephrine_drugs_encoded = Dopamine_and_epinephrine_drugs_mapping[Dopamine_and_epinephrine_drugs]
            Renal_function_trajectory_encoded = Renal_function_trajectory_mapping[Renal_function_trajectory]
            Digitalis_drugs_encoded = Digitalis_drugs_mapping[Digitalis_drugs]
            Coronary_heart_disease_encoded = Coronary_heart_disease_mapping[Coronary_heart_disease]
            MODS_encoded = MODS_mapping[MODS]
            Shock_encoded = Shock_mapping[Shock]
            features.extend([Dopamine_and_epinephrine_drugs_encoded, cystatin_C, Renal_function_trajectory_encoded, Albumin, NEU_percentage, Digitalis_drugs_encoded, AST,LDH,Hemoglobin,Monocyte_count,CRP,Coronary_heart_disease_encoded,MODS_encoded,Age, Shock_encoded])

            if st.button("Predict Mortality Probability"):
                mortality_prob = predict_mortality_probability(np.array(features).reshape(1, -1))
                st.write(f"Mortality Probability: {mortality_prob:.2f}")

if __name__ == '__main__':
    main()
