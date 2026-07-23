# ============================================================
# Medication Information Translator
# File: medication.py
#
# This file contains:
# ✔ Object-Oriented Programming (OOP)
# ✔ File Handling
# ✔ Exception Handling
# ✔ Regular Expressions
# ✔ openFDA API
# ✔ Gemini AI
# ============================================================

# ============================================================
# Import Libraries
# ============================================================

import streamlit as st
import requests
import json
import os
import re
from datetime import datetime

# ============================================================
# API URLs
# ============================================================

OPENFDA_LABEL_URL = (
    "https://api.fda.gov/drug/label.json"
)

OPENFDA_RECALL_URL = (
    "https://api.fda.gov/drug/enforcement.json"
)

# ============================================================
# Search History File
# ============================================================

SEARCH_HISTORY_FILE = "search_history.json"

# ============================================================
# Gemini API Key
# ============================================================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

except Exception:
    GEMINI_API_KEY = ""

# ============================================================
# Create Search History File
# ============================================================

def create_history_file():
    """
    Creates the JSON file if it
    does not already exist.
    """

    if not os.path.exists(
        SEARCH_HISTORY_FILE
    ):

        with open(
            SEARCH_HISTORY_FILE,
            "w"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

create_history_file()

# ============================================================
# Regular Expression Validation
# ============================================================

def validate_medication_name(name):
    """
    Validate medication names.

    Allows:
    Letters
    Numbers
    Spaces
    Hyphen
    Parentheses
    """

    pattern = r"^[A-Za-z0-9\s\-()]{2,100}$"

    return bool(
        re.match(
            pattern,
            name.strip()
        )
    )

# ============================================================
# Medication Class
# ============================================================

class Medication:
    """
    Represents one medication.
    """

    def __init__(self, name):

        self.name = name

        self.purpose = "Not Available"

        self.usage = "Not Available"

        self.warnings = "Not Available"

        self.side_effects = "Not Available"

        self.dosage = "Not Available"

        self.active_ingredient = "Not Available"

        self.recall = False

        self.recall_reason = (
            "No FDA Recall Found"
        )

        self.date = datetime.now().strftime(
            "%d %B %Y %I:%M %p"
        )

    # --------------------------------------------------------

    def update_information(

        self,

        purpose,

        usage,

        warnings,

        side_effects,

        dosage,

        ingredient

    ):

        self.purpose = purpose

        self.usage = usage

        self.warnings = warnings

        self.side_effects = side_effects

        self.dosage = dosage

        self.active_ingredient = ingredient

    # --------------------------------------------------------

    def update_recall(

        self,

        recall,

        reason

    ):

        self.recall = recall

        self.recall_reason = reason

    # --------------------------------------------------------

    def to_dictionary(self):
        """
        Convert medication object
        into dictionary.
        """

        return {

            "Medication": self.name,

            "Purpose": self.purpose,

            "Usage": self.usage,

            "Warnings": self.warnings,

            "Side Effects": self.side_effects,

            "Dosage": self.dosage,

            "Active Ingredient":
            self.active_ingredient,

            "Recall":
            self.recall,

            "Recall Reason":
            self.recall_reason,

            "Date":
            self.date

        }
        # ============================================================
# Search History Class
# ============================================================

class SearchHistory:
    """
    Handles saving, loading and clearing
    medication search history using JSON.
    """

    def __init__(self, filename):

        self.filename = filename

    # --------------------------------------------------------

    def load_history(self):
        """
        Load previous searches from
        the JSON file.
        """

        try:

            with open(
                self.filename,
                "r"
            ) as file:

                return json.load(file)

        except FileNotFoundError:

            return []

        except json.JSONDecodeError:

            return []

        except Exception:

            return []

    # --------------------------------------------------------

    def save_search(self, medication):
        """
        Save a medication search
        to the JSON history file.
        """

        history = self.load_history()

        history.append({

            "medication":
            medication.name,

            "searched_at":
            datetime.now().strftime(
                "%d %B %Y %I:%M %p"
            ),

            "recall":
            medication.recall

        })

        try:

            with open(
                self.filename,
                "w"
            ) as file:

                json.dump(
                    history,
                    file,
                    indent=4
                )

        except Exception as error:

            st.error(
                f"Unable to save history: {error}"
            )

    # --------------------------------------------------------

    def clear_history(self):
        """
        Remove all saved searches.
        """

        try:

            with open(
                self.filename,
                "w"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

        except Exception as error:

            st.error(
                f"Unable to clear history: {error}"
            )
            # ============================================================
# FDA Client Class
# ============================================================

class FDAClient:
    """
    Handles communication with the
    openFDA Drug Label API and
    Drug Recall API.
    """

    def __init__(self):

        self.label_url = OPENFDA_LABEL_URL
        self.recall_url = OPENFDA_RECALL_URL

    # --------------------------------------------------------

    def search_medication(self, medication_name):
        """
        Search for medication information
        from the openFDA Drug Label API.
        """

        # Convert common medicine names
        search_name = medication_name.lower()

        if search_name == "paracetamol":
            search_name = "acetaminophen"

        parameters = {

            "search":
            (
                f'openfda.brand_name:"{search_name}" '
                f'OR openfda.generic_name:"{search_name}"'
            ),

            "limit": 1

        }

        try:

            response = requests.get(

                self.label_url,

                params=parameters,

                timeout=20

            )

            response.raise_for_status()

            data = response.json()

            if "results" not in data:

                return None

            result = data["results"][0]

            medication = Medication(
                medication_name
            )

            # -------------------------
            # Active Ingredient
            # -------------------------

            ingredient = self.extract_openfda(

                result,

                "substance_name"

            )

            if ingredient == "Not Available":

                ingredient = self.extract_openfda(

                    result,

                    "generic_name"

                )

            # -------------------------
            # Update Medication Object
            # -------------------------

            medication.update_information(

                purpose=self.extract_text(
                    result,
                    "purpose"
                ),

                usage=self.extract_text(
                    result,
                    "indications_and_usage"
                ),

                warnings=self.extract_text(
                    result,
                    "warnings"
                ),

                side_effects=self.extract_text(
                    result,
                    "adverse_reactions"
                ),

                dosage=self.extract_text(
                    result,
                    "dosage_and_administration"
                ),

                ingredient=ingredient

            )

            # -------------------------
            # Check Recall Status
            # -------------------------

            recall_status, recall_reason = self.check_recall(
                medication_name
            )

            medication.update_recall(

                recall_status,

                recall_reason

            )

            return medication

        except requests.exceptions.Timeout:

            st.error(
                "Connection timed out."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to openFDA."
            )

        except requests.exceptions.HTTPError as error:

            st.error(
                f"HTTP Error: {error}"
            )

        except Exception as error:

            st.error(
                f"Unexpected Error: {error}"
            )

        return None
        # --------------------------------------------------------
    # Check FDA Drug Recall
    # --------------------------------------------------------

    def check_recall(self, medication_name):
        """
        Check whether the medication
        appears in the FDA Recall API.
        """

        parameters = {

            "search":
            f'product_description:"{medication_name}"',

            "limit": 1

        }

        try:

            response = requests.get(

                self.recall_url,

                params=parameters,

                timeout=20

            )

            response.raise_for_status()

            data = response.json()

            if "results" in data:

                recall = data["results"][0]

                reason = recall.get(

                    "reason_for_recall",

                    "Reason not available."

                )

                return True, reason

        except requests.exceptions.Timeout:

            pass

        except requests.exceptions.ConnectionError:

            pass

        except requests.exceptions.HTTPError:

            pass

        except Exception:

            pass

        return False, "No FDA recall found."

    # --------------------------------------------------------
    # Extract Text from API
    # --------------------------------------------------------

    def extract_text(self, data, key):
        """
        Extract text values from
        the openFDA response.
        """

        value = data.get(key)

        if not value:

            return "Not Available"

        if isinstance(value, list):

            return "\n".join(value)

        return str(value)

    # --------------------------------------------------------
    # Extract openFDA Information
    # --------------------------------------------------------

    def extract_openfda(self, data, key):
        """
        Extract values from the
        openfda section.
        """

        openfda = data.get(
            "openfda",
            {}
        )

        value = openfda.get(key)

        if not value:

            return "Not Available"

        if isinstance(value, list):

            return ", ".join(value)

        return str(value)
    # ============================================================
# AI Translator Class
# ============================================================

class AITranslator:
    """
    Uses Gemini AI to translate
    medical information into
    simple everyday language.
    """

    def __init__(self, api_key):

        self.api_key = api_key

        self.url = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
)
    # --------------------------------------------------------

    def simplify_information(self, medication):
        """
        Use Gemini AI to rewrite medication
        information in simple language.
        """

        # Check if API key exists
        if not self.api_key:
            return (
                "Gemini API Key was not found.\n\n"
                "Please add your API key in "
                ".streamlit/secrets.toml"
            )

        prompt = f"""
You are a helpful medical assistant.

Rewrite the following medication information into simple everyday English.

Medication:
{medication.name}

Purpose:
{medication.purpose}

Usage:
{medication.usage}

Warnings:
{medication.warnings}

Side Effects:
{medication.side_effects}

Dosage:
{medication.dosage}

Active Ingredient:
{medication.active_ingredient}

Rules:
- Use simple English.
- Use bullet points.
- Keep the explanation short.
- Do not use difficult medical words.
"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:

            response = requests.post(
                f"{self.url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                st.error(response.text)
                return "Unable to generate explanation."

            data = response.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as error:
            return f"Gemini Error: {error}"
# ============================================================
# Create Objects
# ============================================================

history_manager = SearchHistory(
    SEARCH_HISTORY_FILE
)

fda_client = FDAClient()

translator = AITranslator(
    GEMINI_API_KEY
)