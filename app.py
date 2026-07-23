# ============================================================
# Medication Information Translator
# File: app.py
#
# This file contains the Streamlit User Interface.
# All application logic is stored in medication.py
# ============================================================

# ----------------------------
# Import Libraries
# ----------------------------

import streamlit as st

# Import classes and functions from medication.py
from medication import (
    validate_medication_name,
    history_manager,
    fda_client,
    translator
)

# ----------------------------
# Streamlit Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Medication Information Translator",
    page_icon="💊",
    layout="wide"
)

# ----------------------------
# Application Title
# ----------------------------

st.title("💊 Medication Information Translator")

st.markdown("""
Welcome to the **Medication Information Translator**.

This application allows users to:

✅ Search for a medication

✅ View medication purpose

✅ Read dosage instructions

✅ View warnings and side effects

✅ Check FDA Drug Recall Status

✅ Use Gemini AI to explain the medication in simple everyday language
""")

st.divider()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("🔍 Medication Search")

st.sidebar.write(
    "Enter the name of a medication below."
)

# User Input
medication_name = st.sidebar.text_input(
    "Medication Name",
    placeholder="Example: Ibuprofen"
)

# Search Button
search_button = st.sidebar.button(
    "Search Medication",
    use_container_width=True
)

st.sidebar.divider()

# Project Information
st.sidebar.info(
    """
**Technology Used**

• Python

• Streamlit

• openFDA API

• Gemini AI

• JSON

• Requests

• Regular Expressions

• Object-Oriented Programming
"""
)

st.sidebar.divider()

st.sidebar.success(
    "Developed for Python Advanced Project"
)

# ============================================================
# Main Search Section
# ============================================================

if search_button:

    # Remove unwanted spaces
    medication_name = medication_name.strip()

    # Validate medication name
    if not validate_medication_name(medication_name):

        st.error(
            "Please enter a valid medication name."
        )

    else:

        # Show loading spinner
        with st.spinner(
            "Searching openFDA database..."
        ):

            medication = fda_client.search_medication(
                medication_name
            )

        # Check if medication exists
        if medication is None:

            st.error(
                "Medication not found."
            )

        else:

            # Save search to history
            history_manager.save_search(
                medication
            )

            st.success(
                "Medication information retrieved successfully."
            )

            st.divider()
                        # ============================================================
            # Medication Information
            # ============================================================

            st.header("💊 Medication Information")

            col1, col2 = st.columns(2)

            # ----------------------------
            # Left Column
            # ----------------------------
            with col1:

                st.subheader("General Information")

                st.write(
                    "**Medication Name:**",
                    medication.name
                )

                st.write(
                    "**Purpose:**"
                )

                st.info(
                    medication.purpose
                )

                st.write(
                    "**Active Ingredient:**"
                )

                st.success(
                    medication.active_ingredient
                )

                st.write(
                    "**Dosage Instructions:**"
                )

                st.write(
                    medication.dosage
                )

            # ----------------------------
            # Right Column
            # ----------------------------
            with col2:

                st.subheader("Safety Information")

                st.write(
                    "**Warnings:**"
                )

                st.warning(
                    medication.warnings
                )

                st.write(
                    "**Possible Side Effects:**"
                )

                st.error(
                    medication.side_effects
                )

            st.divider()

            # ============================================================
            # Medication Usage
            # ============================================================

            st.subheader("📖 Indications and Usage")

            st.write(
                medication.usage
            )

            st.divider()

            # ============================================================
            # FDA Drug Recall Status
            # ============================================================

            st.header("🚨 FDA Drug Recall Status")

            if medication.recall:

                st.error(
                    "⚠ This medication appears in the FDA recall database."
                )

                st.write(
                    "**Reason for Recall:**"
                )

                st.warning(
                    medication.recall_reason
                )

            else:
    
                st.success(
                    "✅ No FDA recall has been found for this medication."
                )

            st.divider()

            # ============================================================
            # Gemini AI Translation
            # ============================================================

            st.header("🤖 AI Medication Translator")

            st.markdown("""
            Click the button below to let **Gemini AI**
            rewrite the medication information into
            simple everyday language.
            """)

            if st.button(
                "✨ Generate Simple Explanation",
                use_container_width=True
            ):

                with st.spinner(
                    "Gemini AI is generating a simple explanation..."
                ):

                    explanation = translator.simplify_information(
                        medication
                    )

                st.success(
                    "Simple explanation generated successfully!"
                )

                st.markdown(explanation)

                st.download_button(
                    label="📥 Download Explanation",
                    data=explanation,
                    file_name=(
                        medication.name.lower().replace(" ", "_")
                        + "_simple_explanation.txt"
                    ),
                    mime="text/plain",
                    use_container_width=True
                )
# ============================================================
# Search History
# ============================================================

history = history_manager.load_history()

# ============================================================
# Search Statistics
# ============================================================

st.header("📊 Search Statistics")

if history:

    total_searches = len(history)

    recalled = sum(
        1 for item in history if item["recall"]
    )

    safe = total_searches - recalled

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Searches",
            total_searches
        )

    with col2:
        st.metric(
            "Recalled Drugs",
            recalled
        )

    with col3:
        st.metric(
            "Safe Drugs",
            safe
        )

else:

    st.info(
        "Search statistics will appear here."
    )

st.divider()

# ============================================================
# Sidebar - Clear Search History
# ============================================================

st.sidebar.divider()

st.sidebar.subheader(
    "History Management"
)

if st.sidebar.button(
    "🗑 Clear Search History",
    use_container_width=True
):

    history_manager.clear_history()

    st.sidebar.success(
        "History cleared successfully."
    )

    st.rerun()

# ============================================================
# About Project
# ============================================================

with st.expander(
    "ℹ About This Project"
):

    st.markdown("""
### Medication Information Translator

This application demonstrates:

- Object-Oriented Programming (OOP)
- File Handling
- Exception Handling
- Regular Expressions
- Streamlit User Interface
- JSON Processing
- Requests Library
- openFDA Drug Label API
- openFDA Drug Recall API
- Gemini AI Integration

This project was developed for the
Python Advanced practical assessment.
""")

# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "Medication Information Translator | "
    "Built with Python, Streamlit, openFDA API and Gemini AI"
)