# ============================================================
# TASK 5
# LIFE SCIENCES RESEARCH INTELLIGENCE DASHBOARD
# ============================================================
#
# Domain:        Biomarker Analytics
# Author:        Merina Roy
# Framework:     Streamlit (web deployment)
# Dataset:       biomarker_analytics_data.csv

# ============================================================
# PROJECT DESCRIPTION
# ============================================================
#
# The Life Sciences Research Intelligence Dashboard is a
# Streamlit-based analytics platform developed for biomarker
# research management and decision support.
#
# The dashboard loads biomarker research data from a CSV dataset
# and provides interactive functionalities such as:

# • Viewing and exploring biomarker records
# • Searching biomarkers, researchers, and disease areas
# • Applying multi-parameter filters
# • Generating business and research metrics
# • Producing biomarker reliability assessments
# • Identifying high-risk and low-performing biomarkers through
#   an automated alert system
# • Exporting datasets and reliability reports for further analysis
#
# The application helps research teams, scientists, and
# life-science organizations monitor biomarker performance,
# validation status, research activity, risk levels, and
# overall data quality through a user-friendly web interface.
#
# Built using:
# • Python
# • Streamlit
# • Pandas
# • CSV-based data processing
#
# Objective:
# To transform raw biomarker research data into actionable
# insights that support evidence-based decision-making and
# research intelligence in life sciences.
# ============================================================

import csv                      # Provides functionality for reading and writing CSV files
import logging                  # Used to record errors and application events in log files
import io                       # Supports in-memory text and file operations
from collections import Counter # Counts occurrences of elements efficiently
from pathlib import Path        # Handles file and directory paths in an OS-independent way

import streamlit as st          # Streamlit framework for building the web dashboard interface
import pandas as pd             # Pandas library for data loading, manipulation, and analysis

# ============================================================
# CONFIGURE ERROR LOGGING
# ============================================================
# Set up logging to capture errors in a file named 'dashboard_errors.log' 
# with timestamps and error levels

logging.basicConfig(
    filename="dashboard_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================================================
# PAGE CONFIG
# ============================================================
# Configure Streamlit page settings such as title, icon, layout, and sidebar state
# This sets the title to "Biomarker Analytics Dashboard", uses a DNA emoji as the icon
# sets the layout to wide for better use of screen space, and expands the sidebar by default
# This configuration enhances the user experience by providing a clear title, an intuitive icon, 
# and an optimized layout for data visualization and interaction.

st.set_page_config(
    page_title="Biomarker Analytics Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
# Inject custom CSS styles to enhance the visual appearance of the dashboard
# This CSS defines the background colors, text colors, styles for metric cards, 
# section headers,insight cards, reliability badges, and alert banners. It also hides 
# Streamlit's default branding for a cleaner look. The styles are designed to create
# a modern,professional, and user-friendly interface

st.markdown("""
<style>
    /* Main background - light grey */
    .stApp { background-color: #f0f4f8 !important; }

    /* Force all main content text to dark */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3,
    .stApp label, .stApp div, .stApp span, .stApp li,
    .stMarkdown, .stMarkdown p, .stMarkdown h1,
    .stMarkdown h2, .stMarkdown h3 {
        color: #1f2937 !important;
    }

    /* Sidebar dark gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3c 0%, #2d3561 100%) !important;
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #e8eaf6 !important;
    }

    /* Metric cards */
    .metric-card {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        border-left: 5px solid #4f46e5;
        margin-bottom: 12px;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 13px;
        color: #6b7280 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card p {
        margin: 4px 0 0;
        font-size: 28px;
        font-weight: 700;
        color: #1f2937 !important;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: #ffffff !important;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    /* Insight cards */
    .insight-card {
        background: #ffffff !important;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.09);
        border-left: 4px solid #7c3aed;
    }
    .insight-label {
        font-size: 12px;
        color: #6b7280 !important;
        font-weight: 600;
        text-transform: uppercase;
    }
    .insight-value {
        font-size: 20px;
        font-weight: 700;
        color: #1f2937 !important;
        margin-top: 2px;
    }

    /* Reliability badges */
    .badge-excellent { background:#d1fae5; color:#065f46 !important; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
    .badge-good      { background:#dbeafe; color:#1e40af !important; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
    .badge-needs     { background:#fee2e2; color:#991b1b !important; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }

    /* Alert banner */
    .alert-banner {
        background: #fef3c7;
        border-left: 5px solid #f59e0b;
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #92400e !important;
    }
    .alert-banner b { color: #92400e !important; }
    .alert-banner small { color: #92400e !important; }

    /* Page titles */
    h1, h2, h3 { color: #1f2937 !important; }

    /* Hide streamlit branding */
    #MainMenu {visibility:hidden;} footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
# Load the biomarker analytics dataset from a CSV file with error handling and caching
# The function `load_data` attempts to read the specified CSV file and returns a DataFrame.
# If the file does not exist or an error occurs during loading, it logs the error and
# returns an empty DataFrame. The `@st.cache_data` decorator is used to cache the loaded data
# for improved performance on subsequent accesses, avoiding redundant file reads.

@st.cache_data
def load_data(filename="biomarker_analytics_data.csv"):
    try:
        if not Path(filename).exists():
            return pd.DataFrame()
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        logging.error(f"Load Data Error: {e}")
        return pd.DataFrame()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

# Set up the sidebar with a title and navigation options for different pages of the dashboard
# The sidebar includes a title "Biomarker Analytics" and a radio button navigation menu with options
# for Home, View Data, Search Data, Filter Data, Business Metrics, Research Insights,
# Reliability Report, Alert System, and Export Report. It also displays the dataset name and
# shows a success message with the number of records loaded from the dataset.

st.sidebar.markdown("## 🧬 Biomarker Analytics")
st.sidebar.markdown("---")

nav = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📋 View Data",
        "🔍 Search Data",
        "🎛️ Filter Data",
        "📊 Business Metrics",
        "💡 Research Insights",
        "🛡️ Reliability Report",
        "🚨 Alert System",
        "📤 Export Report",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** biomarker_analytics_data.csv")

df = load_data()

if df.empty:
    st.error("⚠️ Dataset not found. Please place `biomarker_analytics_data.csv` in the app directory.")
    st.stop()

st.sidebar.success(f"✅ {len(df)} records loaded")

# ============================================================
# HELPERS
# ============================================================

# Helper functions to create styled metric cards, insight cards, section headers, reliability badges,
# and to compute reliability scores based on accuracy and sample count. These functions generate
# HTML content with custom CSS classes for consistent styling across the dashboard.

def metric_card(label, value, accent="#4f46e5"):
    st.markdown(
        f"""<div class="metric-card" style="border-left-color:{accent}">
                <h3>{label}</h3><p>{value}</p>
            </div>""",
        unsafe_allow_html=True
    )

def insight_card(label, value):
    st.markdown(
        f"""<div class="insight-card">
                <div class="insight-label">{label}</div>
                <div class="insight-value">{value}</div>
            </div>""",
        unsafe_allow_html=True
    )

def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def reliability_badge(status):
    if status == "Excellent":
        return '<span class="badge-excellent">✅ Excellent</span>'
    elif status == "Good":
        return '<span class="badge-good">🔵 Good</span>'
    else:
        return '<span class="badge-needs">⚠️ Needs Validation</span>'

def compute_reliability(row):
    score = round((row["Accuracy_Percentage"] * row["Sample_Count"]) / 100, 2)
    if score >= 500:
        status = "Excellent"
    elif score >= 300:
        status = "Good"
    else:
        status = "Needs Validation"
    return score, status

# ============================================================
# PAGE: HOME
# ============================================================

# The Home page provides an overview of the biomarker analytics dashboard with key metrics,
# visualizations of disease area distribution, validation status breakdown, and accuracy by
# disease area.

if nav == "🏠 Home":
    st.markdown("# 🧬 Life Sciences Research Intelligence Dashboard")
    st.markdown("### Biomarker Analytics — Excelra")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Biomarkers", len(df), "#4f46e5")
    with col2:
        validated = len(df[df["Validation_Status"] == "Validated"])
        metric_card("Validated", validated, "#059669")
    with col3:
        pending = len(df[df["Validation_Status"] == "Pending"])
        metric_card("Pending", pending, "#f59e0b")
    with col4:
        high = len(df[df["Priority_Level"] == "High"])
        metric_card("High Priority", high, "#dc2626")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        section_header("📌 Disease Area Distribution")
        disease_counts = df["Disease_Area"].value_counts().reset_index()
        disease_counts.columns = ["Disease Area", "Count"]
        st.bar_chart(disease_counts.set_index("Disease Area"))

    with col_b:
        section_header("📌 Validation Status Breakdown")
        status_counts = df["Validation_Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        st.bar_chart(status_counts.set_index("Status"))

    st.markdown("---")
    section_header("📌 Accuracy by Disease Area")
    acc_by_disease = df.groupby("Disease_Area")["Accuracy_Percentage"].mean().round(2).reset_index()
    acc_by_disease.columns = ["Disease Area", "Avg Accuracy (%)"]
    st.bar_chart(acc_by_disease.set_index("Disease Area"))

# ============================================================
# PAGE: VIEW DATA
# ============================================================

# The View Data page displays the entire biomarker dataset in a tabular format 
# with a count of total records.


elif nav == "📋 View Data":
    section_header("📋 Biomarker Records")
    st.markdown(f"Showing all **{len(df)}** records")
    st.dataframe(df, use_container_width=True, height=550)

# ============================================================
# PAGE: SEARCH DATA
# ============================================================

# The Search Data page allows users to search the biomarker dataset based on selected fields
# such as Biomarker Name, Researcher Name, or Disease Area. Users can enter keywords
# to find matching records, and the results are displayed in a table with a count of matches found.
# The search is case-insensitive and handles empty input by prompting the user to enter a keyword.
    
elif nav == "🔍 Search Data":
    section_header("🔍 Search Biomarker Data")

    col1, col2 = st.columns([1, 2])
    with col1:
        search_field = st.selectbox(
            "Search By",
            ["Biomarker Name", "Researcher Name", "Disease Area"]
        )
    with col2:
        keyword = st.text_input("Enter search keyword", placeholder="e.g. CRP, Oncology, Dr. Sharma")

    if keyword.strip():
        field_map = {
            "Biomarker Name": "Biomarker_Name",
            "Researcher Name": "Researcher_Name",
            "Disease Area": "Disease_Area"
        }
        col = field_map[search_field]
        results = df[df[col].str.contains(keyword.strip(), case=False, na=False)]

        st.markdown(f"**{len(results)}** matching record(s) found")
        if not results.empty:
            st.dataframe(results, use_container_width=True)
        else:
            st.info("No records matched your search.")
    else:
        st.info("Enter a keyword above to search.")

# ============================================================
# PAGE: FILTER DATA
# ============================================================

# The Filter Data page provides interactive filters for users to narrow down the biomarker dataset
# based on multiple parameters such as Validation Status, Priority Level, Country, and Risk Level.
# Users can select specific values for each parameter or choose "All" to include all records.
# The filtered results are displayed in a table with a count of matching records. The filtering logic
# applies all selected criteria to the dataset, allowing users to easily explore subsets of data that meet
# their specific research interests or requirements.

elif nav == "🎛️ Filter Data":
    section_header("🎛️ Filter Biomarker Data")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_opts = ["All"] + sorted(df["Validation_Status"].unique().tolist())
        sel_status = st.selectbox("Validation Status", status_opts)
    with col2:
        priority_opts = ["All"] + sorted(df["Priority_Level"].unique().tolist())
        sel_priority = st.selectbox("Priority Level", priority_opts)
    with col3:
        country_opts = ["All"] + sorted(df["Country"].unique().tolist())
        sel_country = st.selectbox("Country", country_opts)
    with col4:
        risk_opts = ["All"] + sorted(df["Risk_Level"].unique().tolist())
        sel_risk = st.selectbox("Risk Level", risk_opts)

    filtered = df.copy()
    if sel_status   != "All": filtered = filtered[filtered["Validation_Status"] == sel_status]
    if sel_priority != "All": filtered = filtered[filtered["Priority_Level"]    == sel_priority]
    if sel_country  != "All": filtered = filtered[filtered["Country"]           == sel_country]
    if sel_risk     != "All": filtered = filtered[filtered["Risk_Level"]        == sel_risk]

    st.markdown(f"**{len(filtered)}** record(s) match your filters")
    st.dataframe(filtered, use_container_width=True, height=480)

# ============================================================
# PAGE: BUSINESS METRICS
# ============================================================

# The Business Metrics page calculates and displays key performance indicators 
# (KPIs) related to the biomarker dataset, such as total biomarkers, validation status
# counts, average accuracy.

elif nav == "📊 Business Metrics":
    section_header("📊 Business Metrics Dashboard")

    total        = len(df)
    validated    = len(df[df["Validation_Status"] == "Validated"])
    pending      = len(df[df["Validation_Status"] == "Pending"])
    in_review    = len(df[df["Validation_Status"] == "In Review"])
    rejected     = len(df[df["Validation_Status"] == "Rejected"])
    avg_accuracy = round(df["Accuracy_Percentage"].mean(), 2)
    high_prio    = len(df[df["Priority_Level"] == "High"])
    total_samples= int(df["Sample_Count"].sum())
    high_risk    = len(df[df["Risk_Level"] == "High"])
    unique_researchers = df["Researcher_Name"].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("Total Biomarkers",    total,              "#4f46e5")
    with c2: metric_card("Validated",           validated,          "#059669")
    with c3: metric_card("Pending Review",      pending,            "#f59e0b")
    with c4: metric_card("High Priority",       high_prio,          "#dc2626")
    with c5: metric_card("Avg Accuracy (%)",    avg_accuracy,       "#0891b2")

    st.markdown("")
    c6, c7, c8, c9, c10 = st.columns(5)
    with c6:  metric_card("Total Samples",        f"{total_samples:,}", "#7c3aed")
    with c7:  metric_card("High Risk Biomarkers", high_risk,            "#b45309")
    with c8:  metric_card("In Review",            in_review,            "#0284c7")
    with c9:  metric_card("Rejected",             rejected,             "#9f1239")
    with c10: metric_card("Active Researchers",   unique_researchers,   "#065f46")

    st.markdown("---")
    section_header("📈 Accuracy Distribution by Priority")
    acc_priority = df.groupby("Priority_Level")["Accuracy_Percentage"].mean().round(2).reset_index()
    acc_priority.columns = ["Priority", "Avg Accuracy (%)"]
    st.bar_chart(acc_priority.set_index("Priority"))

# ============================================================
# PAGE: RESEARCH INSIGHTS
# ============================================================

# The Research Insights page generates actionable insights from the biomarker dataset, 
# such as the most studied disease area, the most active researcher, the country with the 
# most research activity, the most common risk level, the biomarker with the highest and 
# lowest accuracy.

elif nav == "💡 Research Insights":
    section_header("💡 Research Insights")

    most_disease     = df["Disease_Area"].value_counts().idxmax()
    most_researcher  = df["Researcher_Name"].value_counts().idxmax()
    top_country      = df["Country"].value_counts().idxmax()
    most_risk        = df["Risk_Level"].value_counts().idxmax()
    highest_acc_row  = df.loc[df["Accuracy_Percentage"].idxmax()]
    lowest_acc_row   = df.loc[df["Accuracy_Percentage"].idxmin()]
    most_sample_row  = df.loc[df["Sample_Count"].idxmax()]
    most_sample_type = df["Sample_Type"].value_counts().idxmax()

    col1, col2 = st.columns(2)
    with col1:
        insight_card("🔬 Most Studied Disease Area",          most_disease)
        insight_card("🏆 Highest Accuracy Biomarker",
                     f"{highest_acc_row['Biomarker_Name']} ({highest_acc_row['Accuracy_Percentage']}%)")
        insight_card("📉 Lowest Accuracy Biomarker",
                     f"{lowest_acc_row['Biomarker_Name']} ({lowest_acc_row['Accuracy_Percentage']}%)")
        insight_card("🧪 Most Common Sample Type",            most_sample_type)

    with col2:
        insight_card("👩‍🔬 Most Active Researcher",            most_researcher)
        insight_card("🌍 Country with Max Research Activity", top_country)
        insight_card("⚠️ Most Common Risk Level",             most_risk)
        insight_card("📦 Biomarker with Most Samples",
                     f"{most_sample_row['Biomarker_Name']} ({int(most_sample_row['Sample_Count']):,})")

    st.markdown("---")
    section_header("📊 Researcher Activity")
    researcher_counts = df["Researcher_Name"].value_counts().reset_index()
    researcher_counts.columns = ["Researcher", "Studies"]
    st.bar_chart(researcher_counts.set_index("Researcher"))

# ============================================================
# PAGE: RELIABILITY REPORT
# ============================================================

# The Reliability Report page computes a reliability score for each biomarker based on its 
# accuracy percentage and sample count.

elif nav == "🛡️ Reliability Report":
    section_header("🛡️ Biomarker Reliability Report")
    st.markdown("**Reliability Score** = (Accuracy % × Sample Count) / 100")
    st.markdown("- **≥ 500** → Excellent &nbsp;|&nbsp; **≥ 300** → Good &nbsp;|&nbsp; **< 300** → Needs Validation")
    st.markdown("---")

    rel_df = df.copy()
    rel_df["Reliability_Score"]  = rel_df.apply(lambda r: compute_reliability(r)[0], axis=1)
    rel_df["Reliability_Status"] = rel_df.apply(lambda r: compute_reliability(r)[1], axis=1)

    # Summary counts
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("Excellent", len(rel_df[rel_df["Reliability_Status"]=="Excellent"]), "#059669")
    with c2: metric_card("Good",      len(rel_df[rel_df["Reliability_Status"]=="Good"]),      "#0891b2")
    with c3: metric_card("Needs Validation", len(rel_df[rel_df["Reliability_Status"]=="Needs Validation"]), "#dc2626")

    st.markdown("---")

    show_cols = ["Biomarker_ID", "Biomarker_Name", "Disease_Area",
                 "Accuracy_Percentage", "Sample_Count",
                 "Reliability_Score", "Reliability_Status"]
    sort_col = st.selectbox("Sort by", ["Reliability_Score", "Accuracy_Percentage", "Sample_Count"])
    sorted_df = rel_df[show_cols].sort_values(sort_col, ascending=False).reset_index(drop=True)
    st.dataframe(sorted_df, use_container_width=True, height=480)

# ============================================================
# PAGE: ALERT SYSTEM  (Custom Feature — Task 7)
# ============================================================

# The Alert System page implements an automated monitoring system that flags biomarkers needing
# immediate attention based on criteria such as high risk without validation, low accuracy, and 
# high priority with low reliability scores. It generates alerts categorized by severity (Critical, 
# Warning, Attention) and displays them in a user-friendly format with counts of each alert type.
    section_header("🚨 Alert System — Biomarker Risk Monitor")
    st.markdown("Automatically flags biomarkers that need immediate attention.")
    st.markdown("---")

    rel_df = df.copy()
    rel_df["Reliability_Score"]  = rel_df.apply(lambda r: compute_reliability(r)[0], axis=1)
    rel_df["Reliability_Status"] = rel_df.apply(lambda r: compute_reliability(r)[1], axis=1)

    alerts = []

    # Alert 1: High risk + not validated
    a1 = rel_df[
        (rel_df["Risk_Level"] == "High") &
        (rel_df["Validation_Status"] != "Validated")
    ][["Biomarker_ID","Biomarker_Name","Risk_Level","Validation_Status","Disease_Area"]]
    for _, row in a1.iterrows():
        alerts.append({
            "Severity": "🔴 CRITICAL",
            "Biomarker": row["Biomarker_Name"],
            "ID": row["Biomarker_ID"],
            "Alert": f"High Risk biomarker is NOT Validated ({row['Validation_Status']})",
            "Disease Area": row["Disease_Area"]
        })

    # Alert 2: Accuracy < 70%
    a2 = rel_df[rel_df["Accuracy_Percentage"] < 70.0]
    for _, row in a2.iterrows():
        alerts.append({
            "Severity": "🟠 WARNING",
            "Biomarker": row["Biomarker_Name"],
            "ID": row["Biomarker_ID"],
            "Alert": f"Low accuracy: {row['Accuracy_Percentage']}%",
            "Disease Area": row["Disease_Area"]
        })

    # Alert 3: Reliability Needs Validation + High Priority
    a3 = rel_df[
        (rel_df["Reliability_Status"] == "Needs Validation") &
        (rel_df["Priority_Level"] == "High")
    ]
    for _, row in a3.iterrows():
        alerts.append({
            "Severity": "🟡 ATTENTION",
            "Biomarker": row["Biomarker_Name"],
            "ID": row["Biomarker_ID"],
            "Alert": f"High Priority but reliability score too low ({row['Reliability_Score']})",
            "Disease Area": row["Disease_Area"]
        })

    if alerts:
        alert_df = pd.DataFrame(alerts).drop_duplicates(subset=["ID","Alert"])
        critical = alert_df[alert_df["Severity"]=="🔴 CRITICAL"]
        warning  = alert_df[alert_df["Severity"]=="🟠 WARNING"]
        attention= alert_df[alert_df["Severity"]=="🟡 ATTENTION"]

        c1, c2, c3 = st.columns(3)
        with c1: metric_card("Critical Alerts",  len(critical),  "#dc2626")
        with c2: metric_card("Warnings",         len(warning),   "#f59e0b")
        with c3: metric_card("Attention Needed", len(attention), "#ca8a04")

        st.markdown("---")
        for sev, group in [("🔴 CRITICAL", critical), ("🟠 WARNING", warning), ("🟡 ATTENTION", attention)]:
            if not group.empty:
                st.markdown(f"### {sev}")
                for _, row in group.iterrows():
                    st.markdown(
                        f'<div class="alert-banner">'
                        f'<b>{row["Biomarker"]} ({row["ID"]})</b> — {row["Alert"]}'
                        f'<br><small>Disease Area: {row["Disease Area"]}</small></div>',
                        unsafe_allow_html=True
                    )
    else:
        st.success("✅ No alerts — all biomarkers are within acceptable thresholds.")

# ============================================================
# PAGE: EXPORT REPORT
# ============================================================

# The Export Report page allows users to download the full biomarker dataset or a computed
# reliability report as CSV files.

elif nav == "📤 Export Report":
    section_header("📤 Export Report")
    st.markdown("Download the dataset or a computed reliability report as CSV.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Full Dataset")
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Full Dataset (CSV)",
            data=csv_data,
            file_name="biomarker_analytics_data.csv",
            mime="text/csv"
        )

    with col2:
        st.markdown("### Reliability Report")
        rel_df = df.copy()
        rel_df["Reliability_Score"]  = rel_df.apply(lambda r: compute_reliability(r)[0], axis=1)
        rel_df["Reliability_Status"] = rel_df.apply(lambda r: compute_reliability(r)[1], axis=1)
        rel_csv = rel_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Reliability Report (CSV)",
            data=rel_csv,
            file_name="biomarker_reliability_report.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.markdown("### Preview")
    st.dataframe(df.head(20), use_container_width=True)


#--------------------------------------------------------------------------------------------------
#END OF FILE
#--------------------------------------------------------------------------------------------------