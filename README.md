# Makeup Style Advisor Bot

**Makeup Style Advisor Bot** is a smart Streamlit application that helps you discover personalized makeup looks tailored to your facial features and preferences. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, this bot analyzes a natural, makeup-free photo of your face and curates a custom beauty guide—complete with tutorials, product recommendations, and styling techniques.

## Folder Structure

```
Makeup-Style-Advisor-Bot/
├── makeup-style-advisor-bot.py
├── README.md
└── requirements.txt
```

* **makeup-style-advisor-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Face Image Upload & Preferences Form**
  Upload a clear, natural (makeup-free) face photo. Select your makeup style, occasion, feature to highlight, and product budget range.

* **AI-Powered Facial Analysis**
  The Facial Feature Analyzer agent studies the image to infer your face shape, skin tone, lip structure, and eye shape—without identifying you.

* **Personalized Makeup Research**
  The Makeup Research Assistant agent creates targeted search prompts using SerpAPI and fetches high-quality tutorials, product links, and application techniques tailored to your features and goals.

* **Structured Markdown Makeup Report**
  The Makeup Report Generator agent combines all insights and resources to produce a clean, professional Markdown guide with embedded links and styling recommendations.

* **Download Option**
  Download the final makeup report as a `.md` file for future reference or sharing.

* **Responsive Streamlit UI**
  A modern and user-friendly Streamlit interface designed for effortless interaction.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Makeup-Style-Advisor-Bot.git
   cd Makeup-Style-Advisor-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run makeup-style-advisor-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and SerpAPI keys in the sidebar.
   * Upload a natural, makeup-free face photo.
   * Choose your style, occasion, focus area, and product budget.
   * Click **💄 Generate Makeup Report**.
   * View and download your personalized makeup report.

3. **Download Option**
   Use the **📥 Download Makeup Report** button to save your AI-generated beauty guide as a `.md` file.



## Code Overview

* **`render_sidebar()`**: Handles secure collection of OpenAI and SerpAPI keys.

* **`render_makeup_preferences()`**: Collects user preferences and a natural face image.

* **`generate_makeup_report()`**:

  * Uses the `Facial Feature Analyzer` to evaluate the uploaded image.
  * Fetches tutorials and products via the `Makeup Research Assistant`.
  * Produces a structured, personalized guide using the `Makeup Report Generator`.

* **`main()`**: Manages the layout, flow, and session state for a smooth end-to-end user experience.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your additions are relevant, clean, and tested.
