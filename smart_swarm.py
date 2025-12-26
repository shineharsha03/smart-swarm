import streamlit as st
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Appeal Denial Swarm (Phase 1.5)", layout="wide")
st.title("🐝 Medical Appeal Swarm")
st.markdown("### The Digital Insurance Defense Employee")

# --- 1. THE AGENTS (Simulation Mode) ---

def radiologist_agent(image_file):
    """Agent 1: Simulates analyzing an X-Ray with varied results."""
    time.sleep(2) # Simulate processing time

    # Randomly pick a diagnosis so it feels "alive"
    diagnoses = [
        "Analysis: Severe vertical root fracture visible in Tooth #19. Prognosis hopeless.",
        "Analysis: Large periapical radiolucency (abscess) detected at apex of Tooth #30.",
        "Analysis: Class II caries extending into the pulp chamber. Direct pulp cap failed.",
        "Analysis: Significant bone loss (50%) indicating advanced Periodontitis.",
        "Analysis: Impacted wisdom tooth (#32) compressing the inferior alveolar nerve."
    ]
    return random.choice(diagnoses)

def intake_agent(audio_file):
    """Agent 2: Simulates listening to the doctor's voice note."""
    time.sleep(2) # Simulate transcription
    return "Transcript: 'Patient presents with excruciating pain. Previous conservative treatments have failed. This procedure is not elective; it is urgent and medically necessary.'"

def writer_agent(radiology_report, voice_notes, policy_rules):
    """Agent 3: Writes the letter using Evidence + Policy Rules."""
    time.sleep(2) # Simulate writing

    # Use generic rules if the user didn't paste any
    policy_text = policy_rules if policy_rules else "Standard Clinical Necessity Guidelines"

    return f"""
    SUBJECT: APPEAL FOR CLAIM DENIAL - CITING POLICY: {policy_text[:40]}...

    To Whom It May Concern,

    I am formally appealing the denial of this claim based on YOUR OWN internal coverage guidelines.

    1. THE RULE (Per Policy Provided):
    "{policy_text}"

    2. THE CLINICAL EVIDENCE (Radiology Scan):
    {radiology_report}

    3. PATIENT SYMPTOMS (Doctor's Note):
    {voice_notes}

    CONCLUSION:
    The patient's condition (see Evidence) clearly meets the criteria listed in your policy (see Rule).
    The denial is unfounded and contradicts your own documentation. 

    Please process this claim immediately.

    Sincerely,
    AI Appeal Swarm
    """

# --- 2. THE DASHBOARD (The 3 Workstations) ---

col1, col2, col3 = st.columns(3)

# COLUMN 1: THE EYE (Radiologist)
with col1:
    st.header("👁️ Radiologist")
    st.info("Upload Evidence")
    uploaded_file = st.file_uploader("Upload X-Ray", type=['png', 'jpg', 'jpeg'], key="rad")

    if uploaded_file and st.button("Analyze Image"):
        with st.spinner("Agent 1 is analyzing pixels..."):
            # Save result to memory (Session State)
            st.session_state['rad_result'] = radiologist_agent(uploaded_file)
            st.success("Evidence Extracted")

    # Show the result if it exists
    if 'rad_result' in st.session_state:
        st.warning(st.session_state['rad_result'])

# COLUMN 2: THE EAR (Intake Nurse)
with col2:
    st.header("👂 Intake Nurse")
    st.info("Record Dictation")
    audio_val = st.audio_input("Record Clinical Note", key="voice")

    if audio_val:
        with st.spinner("Agent 2 is transcribing..."):
            st.session_state['voice_result'] = intake_agent(audio_val)
            st.success("Transcribed")

    if 'voice_result' in st.session_state:
        st.warning(f"Dictation: '{st.session_state['voice_result']}'")

# COLUMN 3: THE BRAIN (Case Manager + Researcher Slot)
with col3:
    st.header("🧠 Case Manager")
    st.info("Review & Write")

    # --- NEW: The Researcher Slot ---
    st.markdown("**🛡️ Insurance Policy Rule**")
    policy_input = st.text_area("Paste the specific insurance rule here:", 
        placeholder="Example: 'Root canals are covered if decay penetrates >50% of dentin...'")

    st.markdown("---")

    if st.button("Generate Appeal Letter", type="primary"):
        # Check if agents 1 & 2 are done
        rad = st.session_state.get('rad_result')
        voice = st.session_state.get('voice_result')

        if rad and voice:
            with st.spinner("Cross-referencing Policy with Evidence..."):
                final_letter = writer_agent(rad, voice, policy_input)
                st.text_area("Final Appeal Draft", final_letter, height=500)
        else:
            st.error("⚠️ Please wait for the Radiologist and Nurse to finish first.")