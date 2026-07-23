# ============================================================
# Medication Information Translator
# File: app.py
# Streamlit User Interface
# ============================================================

# ----------------------------
# Import Libraries
# ----------------------------

import streamlit as st

from medication import (
    validate_medication_name,
    history_manager,
    fda_client,
    translator
)

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Medication Information Translator",
    page_icon="💊",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------

if "medication" not in st.session_state:
    st.session_state.medication = None

# ----------------------------
# Title
# ----------------------------

st.title("💊 Medication Information Translator")

st.write("""
Welcome to the **Medication Information Translator**.

This application allows you to:

✅ Search for a medication

✅ View medication purpose

✅ Read dosage instructions

✅ View warnings and side effects

✅ Check FDA Drug Recall Status

✅ Generate a simple explanation using Gemini AI.
""")

st.divider()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.header("🔍 Medication Search")

medication_name = st.sidebar.text_input(
    "Medication Name",
    placeholder="Example: Ibuprofen"
)

search_button = st.sidebar.button(
    "Search Medication",
    use_container_width=True
)

st.sidebar.divider()

st.sidebar.subheader("Technology Used")

st.sidebar.markdown("""
- Python
- Streamlit
- openFDA API
- Gemini AI
- JSON
- Requests
- Regular Expressions
- OOP
""")

st.sidebar.success("Developed for Python Advanced Project")

# ============================================================
# Search Medication
# ============================================================

if search_button:

    medication_name = medication_name.strip()

    if not validate_medication_name(medication_name):

        st.error("Please enter a valid medication name.")

    else:

        with st.spinner("Searching openFDA database..."):

            medication = fda_client.search_medication(
                medication_name
            )

        if medication is None:

            st.error("Medication not found.")

        else:

            # Save medication for later use
            st.session_state.medication = medication

            # Save search history
            history_manager.save_search(medication)

            st.success(
                "Medication information retrieved successfully."
            )

# ============================================================
# Display Saved Medication
# ============================================================

medication = st.session_state.medication

if medication:

    st.divider()

    st.header("💊 Medication Information")
        # ============================================================
    # Medication Information
    # ============================================================

    col1, col2 = st.columns(2)

    # ----------------------------
    # General Information
    # ----------------------------

    with col1:

        st.subheader("General Information")

        st.write("**Medication Name:**", medication.name)

        st.write("**Purpose:**")
        st.info(medication.purpose)

        st.write("**Active Ingredient:**")
        st.success(medication.active_ingredient)

        st.write("**Dosage Instructions:**")
        st.write(medication.dosage)

    # ----------------------------
    # Safety Information
    # ----------------------------

    with col2:

        st.subheader("Safety Information")

        st.write("**Warnings:**")
        st.warning(medication.warnings)

        st.write("**Possible Side Effects:**")
        st.error(medication.side_effects)

    st.divider()

    # ============================================================
    # Indications and Usage
    # ============================================================

    st.subheader("📖 Indications and Usage")

    st.write(medication.usage)

    st.divider()

    # ============================================================
    # FDA Recall Status
    # ============================================================

    st.header("🚨 FDA Drug Recall Status")

    if medication.recall:

        st.error(
            "⚠ This medication appears in the FDA recall database."
        )

        st.write("**Reason for Recall:**")

        st.warning(
            medication.recall_reason
        )

    else:

        st.success(
            "✅ No FDA recall has been found for this medication."
        )

    st.divider()

    # ============================================================
    # Gemini AI Translator
    # ============================================================

    st.header("🤖 AI Medication Translator")

    st.write(
        "Click the button below to let Gemini AI explain "
        "this medication in simple everyday language."
    )

    if st.button(
        "✨ Generate Simple Explanation",
        use_container_width=True
    ):

        with st.spinner("Gemini AI is thinking..."):

            explanation = translator.simplify_information(
                medication
            )

        st.success("Explanation generated successfully!")

        st.markdown(explanation)

        st.download_button(
            label="📥 Download Explanation",
            data=explanation,
            file_name=f"{medication.name.lower().replace(' ', '_')}_simple_explanation.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()
    # ============================================================
# Search History
# ============================================================

history = history_manager.load_history()

# ============================================================
# Search Statistics
# ============================================================

st.header("📊 Search Statistics")

if history:

    total = len(history)
    recalled = sum(1 for item in history if item["recall"])
    safe = total - recalled

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Searches", total)
    col2.metric("Recalled Drugs", recalled)
    col3.metric("Safe Drugs", safe)

else:

    st.info("No search history available.")

st.divider()

# ============================================================
# Sidebar - History Management
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("History Management")

if st.sidebar.button(
    "🗑 Clear Search History",
    use_container_width=True
):

    history_manager.clear_history()

    st.success("Search history cleared.")

    # Remove saved medication
    st.session_state.medication = None

    st.rerun()

# ============================================================
# About Project
# ============================================================

with st.expander("ℹ About This Project"):

    st.markdown("""
### Medication Information Translator

This project demonstrates:

- Object-Oriented Programming (OOP)
- File Handling
- Exception Handling
- Regular Expressions
- Streamlit User Interface
- JSON Processing
- Requests Library
- openFDA API
- Gemini AI Integration

The application helps users search for medication information,
check FDA recalls, and understand medicine in simple English.
""")

st.divider()

# ============================================================
# Footer
# ============================================================

st.caption(
    "Medication Information Translator | "
    "Built with Python, Streamlit, openFDA API and Gemini AI"
)