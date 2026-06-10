Biomarker-Dashboard

The Life Sciences Research Intelligence Dashboard is a Streamlit-based analytics platform developed for biomarker research management and decision support.
🧬 Life Sciences Research Intelligence Dashboard
-------------------------------------------------------------------------------------------------------------------------
📌 Overview

A fully interactive **Life Sciences Research Intelligence Dashboard** built for **Biomarker Analytics** using Python and Streamlit. This application allows users to explore, search, filter, and analyze biomarker research data through a modern web-based interface.
--------------------------------------------------------------------------------------------------------------------------
🚀 Live Demo

👉 [Click here to view the live app](https://share.streamlit.io)

---------------------------------------------------------------------------------------------------------------------------

✨ Features

| Feature | Description |

| 🏠 Home | KPI summary cards and interactive charts |
| 📋 View Data | Browse all 120 biomarker records |
| 🔍 Search Data | Search by Biomarker Name, Researcher, or Disease Area |
| 🎛️ Filter Data | Filter by Status, Priority, Country, and Risk Level |
| 📊 Business Metrics | 10 key business metrics with visual charts |
| 💡 Research Insights | 8 automated research insights |
| 🛡️ Reliability Report | Biomarker reliability scoring and assessment |
| 🚨 Alert System | Auto-flags Critical, Warning, and Attention cases |
| 📤 Export Report | Download full dataset or reliability report as CSV |

---------------------------------------------------------------------------------------------------------------------------

🗂️ Project Structure

```
biomarker-dashboard/
│
├── research_intelligence_dashboard.py   # Main Streamlit application
├── biomarker_analytics_data.csv         # Dataset (120 records, 12 fields)
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```

-----------------------------------------------------------------------------------------------------------------------------

📊 Dataset

**File:** `biomarker_analytics_data.csv`

**Records:** 120 | **Fields:** 12

| Field | Description |

| Biomarker_ID | Unique identifier |
| Biomarker_Name | Name of the biomarker |
| Disease_Area | Associated disease domain |
| Researcher_Name | Lead researcher |
| Country | Research country |
| Validation_Status | Validated / Pending / In Review / Rejected |
| Priority_Level | High / Medium / Low |
| Risk_Level | High / Medium / Low |
| Sample_Type | Blood / Urine / Tissue / Plasma / Serum / CSF |
| Sample_Count | Number of samples analysed |
| Accuracy_Percentage | Detection accuracy (%) |
| Study_Year | Year of study |

⚙️ Technology Stack

| Technology | Purpose |
| Python 3.x | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data manipulation and analysis |
| CSV | Data storage |

🚨 Alert System Logic

|  Alert Level  | Condition |
| 🔴 Critical  | High Risk biomarker is NOT Validated |
| 🟠 Warning   | Accuracy below 70% |
| 🟡 Attention | High Priority but Reliability score too low |

👩‍💻 Author - Merina Roy
