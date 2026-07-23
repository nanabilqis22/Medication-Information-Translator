# 💊 Medication Information Translator

## Description

Medication Information Translator is a Python-based application that helps users search for medication information and understand medical details in simple everyday language.

The application retrieves drug information from the **openFDA API**, checks FDA drug recall status, displays medication details, stores search history, and uses **Gemini AI** to rewrite complex medical information into an easier explanation.

---

# ✨ Features

✅ Search medication information  
✅ View medication purpose and usage  
✅ Display dosage instructions  
✅ Show warnings and precautions  
✅ Display possible side effects  
✅ Check FDA drug recall status  
✅ AI-powered simple explanation using Gemini AI  
✅ Save medication search history  
✅ View search statistics  

---

# 🛠 Technologies Used

- Python
- Streamlit
- openFDA API
- Gemini AI API
- Requests Library
- JSON File Handling
- Regular Expressions

---

# 🐍 Python Concepts Demonstrated

This project demonstrates:

- Object-Oriented Programming (OOP)
- File Handling
- Exception Handling
- API Integration
- JSON Processing
- Regular Expressions
- Modular Programming

---

# 📂 Project Structure

```
Medication-Information-Translator/
│
├── app.py                  # Streamlit user interface
│
├── medication.py           # Main application logic, classes and API handling
│
├── search_history.json     # Stores previous medication searches
│
├── requirements.txt        # Required Python libraries
│
└── README.md               # Project documentation
```

---

# ⚙️ How The Application Works

1. User enters a medication name.

2. The application validates the medication name using Regular Expressions.

3. The application connects to the openFDA Drug Label API.

4. Medication information is retrieved:

   - Medication purpose
   - Active ingredient
   - Usage instructions
   - Dosage information
   - Warnings
   - Possible side effects

5. The FDA Drug Recall API checks whether the medication has any recall information.

6. Gemini AI processes the medical information and converts complex terms into simple everyday English.

7. The search result is saved into a JSON history file.

---

# 🔌 APIs Used

## openFDA API

The openFDA API is used to retrieve official drug information from the U.S. Food and Drug Administration.

It provides:

- Drug labels
- Medication usage
- Warnings
- Dosage information
- Recall information


## Gemini AI API

Gemini AI is used to simplify medical information and explain it in a way that is easier for users to understand.

---

# 📥 Installation and Setup

## Step 1: Clone Repository

```bash
git clone https://github.com/nanabilqis22/Medication-Information-Translator.git
```

---

## Step 2: Open Project Folder

```bash
cd Medication-Information-Translator
```

---

## Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Setup

Create a folder named:

```
.streamlit
```

Inside the folder create a file named:

```
secrets.toml
```

Add your Gemini API key:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

---

# ▶️ Running The Application

Run the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🖥 Application Features

## Medication Search

Users can enter medication names such as:

- Paracetamol
- Ibuprofen
- Aspirin

The application retrieves available information from the FDA database.

---

## Medication Information Display

The application displays:

### General Information

- Medication name
- Purpose
- Active ingredient
- Dosage instructions


### Safety Information

- Warnings
- Precautions
- Possible side effects


### FDA Recall Status

The application checks whether the medication has been recalled.

---

## AI Medication Translator

Gemini AI explains medical information using:

- Simple English
- Bullet points
- Easy-to-understand descriptions

---

## Search History Management

The application uses JSON file handling to:

- Save previous searches
- Store search dates
- Track recalled and safe medications

---

# 📊 Example Output

Example medication search:

```
Medication Name: Paracetamol

Purpose:
Pain reliever and fever reducer

Active Ingredient:
Acetaminophen

Recall Status:
No FDA recall found.

AI Explanation:
This medicine helps reduce pain and lower fever.
```

---

# 🚀 Future Improvements

Future versions of this project may include:

- User authentication
- More language translation options
- Downloadable medication reports
- Improved medication suggestions
- Cloud database storage
- Better user interface design

---

# 👩‍💻 Developer

Developed as a **Python Advanced Project**.

Technologies:

Python | Streamlit | openFDA API | Gemini AI

---

# 📜 Disclaimer

This application is created for educational purposes only.

It provides information from public sources and should not replace professional medical advice from qualified healthcare providers.