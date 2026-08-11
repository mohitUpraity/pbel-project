<![CDATA[<div align="center">

# ⚖️ LexAI — Legal Document Risk Analyzer

**AI-powered contract analysis platform that extracts clauses, profiles risks, and tracks obligations from any legal document.**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[Features](#-features) · [Quick Start](#-quick-start) · [Architecture](#-architecture) · [Usage](#-usage) · [Tech Stack](#-tech-stack)

</div>

---

## 📋 Overview

**LexAI** is an end-to-end legal document analysis tool that combines OCR-based text extraction with Google Gemini's structured AI output to perform deep contract audits. Upload any PDF — native text or scanned — and receive a comprehensive risk assessment dashboard with:

- **Structured metadata extraction** (parties, dates, governing law, term duration)
- **Clause-by-clause risk profiling** with severity ratings, impact analysis, and mitigation strategies
- **Key terms & definitions** with legal significance annotations
- **Action item tracking** with deadlines, responsible parties, and priority levels
- **Interactive analytics** with donut charts, bar graphs, and a composite risk gauge

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Hybrid Text Extraction** | Native PDF text via PyMuPDF + Tesseract OCR fallback for scanned pages |
| 🤖 **Gemini AI Analysis** | Structured JSON output using Pydantic schemas for validated, type-safe results |
| 📊 **Interactive Dashboard** | 4-tab Streamlit UI with Plotly charts — overview, key terms, risk audit, action items |
| ⚠️ **Risk Scoring Engine** | Composite risk score (0–100) with weighted severity calculation |
| 🔄 **Model Fallback Chain** | Automatic retry across 7 Gemini models if the primary model is unavailable |
| 📝 **Demo Mode** | Pre-loaded sample lease analysis — no API key required to explore the dashboard |
| 🎨 **Professional UI** | Custom CSS with Inter font, color-coded severity pills, and responsive cards |

---

## 🏗 Architecture

### System Overview

```mermaid
graph TB
    subgraph User["👤 User"]
        PDF["📄 PDF Upload"]
        BROWSER["🌐 Browser"]
    end

    subgraph App["⚖️ LexAI Application"]
        direction TB
        DASH["dashboard.py<br/>Streamlit UI Layer"]
        
        subgraph Core["app/ — Core Modules"]
            OCR["ocr.py<br/>Text Extraction"]
            ANALYZER["analyzer.py<br/>AI Analysis Engine"]
            SAMPLE["sample_data.py<br/>Demo Data"]
        end
    end

    subgraph External["☁️ External Services"]
        GEMINI["Google Gemini API"]
        TESS["Tesseract OCR"]
    end

    PDF --> DASH
    BROWSER --> DASH
    DASH --> OCR
    DASH --> ANALYZER
    DASH --> SAMPLE
    OCR --> TESS
    ANALYZER --> GEMINI

    style App fill:#eff6ff,stroke:#1d4ed8,stroke-width:2px
    style Core fill:#ffffff,stroke:#e2e8f0
    style External fill:#f0fdf4,stroke:#16a34a
    style User fill:#fefce8,stroke:#ca8a04
```

### Processing Pipeline

```mermaid
flowchart LR
    A["📄 PDF Input"] --> B{"Native Text<br/>≥ 100 chars?"}
    B -- Yes --> C["PyMuPDF<br/>Native Extract"]
    B -- No --> D["Render to<br/>150 DPI Image"]
    D --> E["Tesseract OCR"]
    C --> F["📝 Full Document Text"]
    E --> F
    F --> G["Gemini API<br/>Structured Prompt"]
    G --> H["Pydantic<br/>Schema Validation"]
    H --> I["Risk Score<br/>Computation"]
    I --> J["📊 Dashboard<br/>Render"]

    style A fill:#fefce8,stroke:#ca8a04
    style F fill:#eff6ff,stroke:#1d4ed8
    style J fill:#f0fdf4,stroke:#16a34a
```

### AI Analysis Schema

```mermaid
classDiagram
    class LegalAnalysis {
        DocumentMetadata document_metadata
        List~KeyTerm~ key_terms
        List~Risk~ risks
        List~ActionItem~ action_items
    }

    class DocumentMetadata {
        +String title
        +String document_type
        +List~String~ parties
        +String date
        +String term_duration
        +String summary
        +String governing_law
        +String overall_risk_rating
    }

    class KeyTerm {
        +String term
        +String definition
        +String location
        +String significance
    }

    class Risk {
        +String risk_id
        +String severity
        +String category
        +String title
        +String description
        +String clause
        +String impact
        +String mitigation
        +String probability
    }

    class ActionItem {
        +String action_id
        +String action
        +String deadline
        +String responsible_party
        +String priority
        +String significance
        +String reference_clause
    }

    LegalAnalysis --> DocumentMetadata
    LegalAnalysis --> KeyTerm
    LegalAnalysis --> Risk
    LegalAnalysis --> ActionItem
```

### Risk Scoring Formula

```mermaid
graph LR
    subgraph Weights["Severity Weights"]
        C["Critical = 15"]
        H["High = 8"]
        M["Medium = 3"]
        L["Low = 1"]
    end

    subgraph Calculation["Score Computation"]
        SUM["Raw Score =<br/>Σ (count × weight)"]
        CLAMP["Clamped to<br/>range [5, 100]"]
    end

    subgraph Rating["Risk Rating"]
        R1["0–19 → 🟢 Low"]
        R2["20–39 → 🟡 Moderate"]
        R3["40–69 → 🟠 High"]
        R4["70–100 → 🔴 Very High"]
    end

    C --> SUM
    H --> SUM
    M --> SUM
    L --> SUM
    SUM --> CLAMP
    CLAMP --> R1
    CLAMP --> R2
    CLAMP --> R3
    CLAMP --> R4

    style Weights fill:#eff6ff,stroke:#1d4ed8
    style Calculation fill:#ffffff,stroke:#e2e8f0
    style Rating fill:#fefce8,stroke:#ca8a04
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Purpose |
|---|---|
| **Python 3.8+** | Runtime |
| **Tesseract OCR** *(optional)* | Required only for scanned PDFs |
| **Gemini API Key** | AI analysis — get one free at [Google AI Studio](https://aistudio.google.com/apikey) |

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/mohitUpraity/pbel-project.git
cd pbel-project

# Run the automated setup script
chmod +x setup.sh
./setup.sh
```

The setup script will:
1. Create a Python virtual environment
2. Install all dependencies from `requirements.txt`
3. Create a `.env` file from `.env.example`
4. Run diagnostics and launch the app

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/mohitUpraity/pbel-project.git
cd pbel-project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Launch the app
streamlit run dashboard.py
```

### Install Tesseract (Optional — for scanned PDFs)

```bash
# macOS
brew install tesseract

# Ubuntu / Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Then set TESSERACT_CMD in .env to the install path
```

---

## 🔧 Configuration

All configuration is managed through the `.env` file:

```env
# Required — Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional — Path to Tesseract executable
TESSERACT_CMD=/usr/local/bin/tesseract
```

You can also enter the API key directly in the sidebar at runtime — it takes precedence over the `.env` value.

---

## 📖 Usage

### Upload & Analyze

1. **Launch the app** → `streamlit run dashboard.py` or `python run.py`
2. **Enter your Gemini API key** in the sidebar (or set it in `.env`)
3. **Upload a PDF** — drag and drop any legal document
4. **Wait for analysis** — extraction + AI analysis typically takes 15–30 seconds
5. **Explore the dashboard** across 4 tabs

### Dashboard Tabs

```mermaid
graph LR
    subgraph Tabs["📊 Dashboard Tabs"]
        T1["📊 Dashboard<br/>Overview + Charts"]
        T2["🔍 Key Terms<br/>Clause Definitions"]
        T3["⚠️ Risk Assessment<br/>Severity Audit"]
        T4["📋 Action Items<br/>Obligation Tracking"]
    end

    T1 --> D1["Document metadata<br/>Severity donut chart<br/>Category bar chart<br/>Risk gauge"]

    T2 --> D2["Searchable terms list<br/>Clause locations<br/>Legal significance"]

    T3 --> D3["Filterable by severity/category<br/>Quoted clauses<br/>Impact + mitigation"]

    T4 --> D4["Priority-sorted tasks<br/>Deadlines & owners<br/>Mark-complete checkboxes"]

    style Tabs fill:#eff6ff,stroke:#1d4ed8
```

### Try the Demo

Click **"Load Sample Lease →"** on the home page to explore a pre-analyzed commercial lease agreement without needing an API key.

---

## 📂 Project Structure

```
pbel-project/
├── dashboard.py            # Main Streamlit application (UI + routing)
├── run.py                  # Launcher with dependency checks & diagnostics
├── setup.sh                # Automated setup script (venv + deps + config)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
│
├── app/                    # Core application modules
│   ├── __init__.py         # Package marker
│   ├── ocr.py              # PDF text extraction (PyMuPDF + Tesseract)
│   ├── analyzer.py         # Gemini AI analysis with Pydantic schemas
│   └── sample_data.py      # Pre-built demo analysis data
│
└── .streamlit/             # Streamlit configuration
    ├── config.toml         # Theme colors & settings
    └── credentials.toml    # Telemetry opt-out
```

---

## 🛠 Tech Stack

```mermaid
graph TB
    subgraph Frontend["🎨 Frontend"]
        ST["Streamlit"]
        PL["Plotly"]
        CSS["Custom CSS<br/>Inter Font"]
    end

    subgraph Backend["⚙️ Backend"]
        PY["Python 3.8+"]
        PD["Pydantic v2"]
        DE["python-dotenv"]
    end

    subgraph AI["🤖 AI & OCR"]
        GEM["Google Gemini API<br/>google-genai SDK"]
        TESS["Tesseract OCR<br/>pytesseract"]
        MU["PyMuPDF<br/>Native PDF Parser"]
        PIL["Pillow<br/>Image Processing"]
    end

    Frontend --> Backend
    Backend --> AI

    style Frontend fill:#eff6ff,stroke:#1d4ed8
    style Backend fill:#fefce8,stroke:#ca8a04
    style AI fill:#f0fdf4,stroke:#16a34a
```

| Layer | Technology | Version |
|---|---|---|
| **UI Framework** | Streamlit | ≥ 1.35.0 |
| **Charts** | Plotly | ≥ 5.18.0 |
| **AI Engine** | Google Gemini (`google-genai`) | ≥ 1.0.0 |
| **PDF Parser** | PyMuPDF | ≥ 1.24.0 |
| **OCR** | pytesseract + Tesseract | ≥ 0.3.10 |
| **Image Processing** | Pillow | ≥ 10.0.0 |
| **Schema Validation** | Pydantic | ≥ 2.0.0 |
| **Environment** | python-dotenv | ≥ 1.0.0 |

---

## 🤖 Model Fallback Chain

LexAI uses a cascading model strategy. If the primary model is unavailable, it automatically tries the next one:

```
gemini-3.1-flash-lite-preview  (default)
       ↓
gemini-3.1-flash-lite
       ↓
gemini-3-flash-preview
       ↓
gemini-2.5-flash
       ↓
gemini-2.0-flash
       ↓
gemini-2.0-flash-lite
       ↓
gemini-1.5-flash
```

You can also select any available model from the sidebar dropdown — the app dynamically fetches your account's available models from the Gemini API.

---

## 🔒 Security

- **API keys are never committed** — `.env` is in `.gitignore`
- **Keys entered in the sidebar** are stored only in Streamlit session state (ephemeral)
- **Document text is sent to Google Gemini API** — review [Google's AI data policies](https://ai.google.dev/terms) for compliance requirements
- **No data persistence** — uploaded documents and analysis results are discarded when the session ends

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| `Tesseract not found` | Install Tesseract or set `TESSERACT_CMD` in `.env`. Native PDFs still work without it. |
| `Gemini API error: 404 not found` | The selected model may not be available in your region. The app will auto-fallback to the next model. |
| `Could not extract readable text` | The PDF may be image-only with very low resolution. Try a higher-quality scan. |
| `Analysis failed: API key not set` | Add your key to `.env` or enter it in the sidebar. Get one at [Google AI Studio](https://aistudio.google.com/apikey). |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using Google Gemini AI & Streamlit**

</div>
]]>
