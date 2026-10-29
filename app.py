from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="NETGUARD AI | Security Console",
    page_icon="🛡️",
    layout="wide"
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #0b1220;
            color: #f4f8ff;
        }

        h1, h2, h3, p, label {
            color: #f4f8ff !important;
        }

        .dashboard-subtitle {
            color: #c7d6ed !important;
            font-size: 18px;
        }

        [data-testid="stMetric"] {
            background-color: #151f32;
            border: 1px solid #3b5278;
            border-radius: 12px;
            padding: 16px;
        }

        [data-testid="stMetricLabel"] {
            color: #c7d6ed !important;
        }

        [data-testid="stMetricValue"] {
            color: #37d4a2 !important;
        }

        button[data-baseweb="tab"] {
            color: #d9e6f7 !important;
            background-color: #151f32 !important;
            border-radius: 8px 8px 0 0;
            font-weight: 600;
        }

        button[data-baseweb="tab"] p {
            color: #d9e6f7 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ffffff !important;
            background-color: #243756 !important;
            border-bottom: 3px solid #37d4a2 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] p {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] {
            background-color: #101a2b;
        }

        [data-testid="stSidebar"] * {
            color: #e5edf8 !important;
        }
                [data-testid="stFileUploaderDropzone"] {
            background-color: #151f32 !important;
            border: 1px dashed #4c6a98 !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            color: #f4f8ff !important;
        }

        [data-testid="stFileUploaderDropzone"] button,
        [data-testid="stDownloadButton"] button,
        .stButton > button {
            background-color: #243756 !important;
            color: #ffffff !important;
            border: 1px solid #4c6a98 !important;
            font-weight: 600 !important;
        }

        [data-testid="stFileUploaderDropzone"] button *,
        [data-testid="stDownloadButton"] button *,
        .stButton > button * {
            color: #ffffff !important;
        }

        [data-testid="stFileUploaderDropzone"] button:hover,
        [data-testid="stDownloadButton"] button:hover,
        .stButton > button:hover {
            background-color: #31517f !important;
            border-color: #37d4a2 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

PROJECT_FOLDER = Path(__file__).resolve().parent
MODEL_FILE = PROJECT_FOLDER / "models" / "netguard_model.pkl"


@st.cache_resource
def load_model():
    """Load the saved NETGUARD AI model."""
    return joblib.load(MODEL_FILE)


model = load_model()

st.title("🛡️ NETGUARD AI")
st.markdown(
    '<p class="dashboard-subtitle">'
    'Network Threat Detection & Incident Analysis Console'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:
    st.header("Security Controls")

    uploaded_file = st.file_uploader(
        "Upload network traffic CSV",
        type="csv"
    )

    risk_threshold = st.slider(
        "Alert risk threshold",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="Only records at or above this risk score become security alerts."
    )

    st.caption("A higher threshold produces fewer, higher-confidence alerts.")
    st.caption("All analysis runs locally on this computer.")

if uploaded_file is None:
    st.info("Upload a CSV file from the left panel to begin threat analysis.")
    st.stop()

uploaded_data = pd.read_csv(uploaded_file)
expected_columns = list(model.feature_names_in_)

missing_columns = [
    column for column in expected_columns
    if column not in uploaded_data.columns
]

if missing_columns:
    st.error("This file is missing required network-data columns.")
    st.write("Missing columns:", missing_columns)
    st.stop()

# Run the model
input_data = uploaded_data[expected_columns]

attack_class_index = list(model.classes_).index(1)
attack_probabilities = model.predict_proba(input_data)[:, attack_class_index] * 100

results = uploaded_data.copy()
results["risk_score"] = attack_probabilities.round(2)

# The slider controls which records are considered alerts
results["prediction"] = (
    results["risk_score"] >= risk_threshold
).astype(int)

results["status"] = results["prediction"].map(
    {0: "Normal Traffic", 1: "Possible Attack"}
)

results["risk_level"] = pd.cut(
    results["risk_score"],
    bins=[-1, 30, 70, 100],
    labels=["Low", "Medium", "High"]
)

total_records = len(results)
attack_count = int((results["prediction"] == 1).sum())
normal_count = int((results["prediction"] == 0).sum())
attack_rate = (attack_count / total_records * 100) if total_records else 0

# Summary cards
st.subheader("Security Overview")

metric_one, metric_two, metric_three, metric_four = st.columns(4)

metric_one.metric("Total Traffic Records", f"{total_records:,}")
metric_two.metric("Possible Attacks", f"{attack_count:,}")
metric_three.metric("Normal Traffic", f"{normal_count:,}")
metric_four.metric("Attack Rate", f"{attack_rate:.2f}%")

st.caption(
    f"Alerts currently use a risk threshold of {risk_threshold}%."
)

st.divider()

overview_tab, incidents_tab, profile_tab, explain_tab, export_tab = st.tabs(
    [
        "Overview",
        "🚨 Incident Queue",
        "Threat Profile",
        "Explainable AI",
        "Download Report"
    ]
)

with overview_tab:
    chart_one, chart_two = st.columns(2)

    with chart_one:
        traffic_summary = pd.DataFrame(
            {
                "Traffic Type": ["Normal Traffic", "Possible Attack"],
                "Records": [normal_count, attack_count]
            }
        )

        traffic_chart = px.pie(
            traffic_summary,
            names="Traffic Type",
            values="Records",
            title="Traffic Classification",
            color="Traffic Type",
            color_discrete_map={
                "Normal Traffic": "#37d4a2",
                "Possible Attack": "#ff5c77"
            },
            hole=0.55
        )

        traffic_chart.update_layout(
            paper_bgcolor="#151f32",
            plot_bgcolor="#151f32",
            font_color="#e5edf8"
        )

        st.plotly_chart(traffic_chart, use_container_width=True)

    with chart_two:
        risk_summary = (
            results["risk_level"]
            .value_counts()
            .reindex(["Low", "Medium", "High"], fill_value=0)
            .reset_index()
        )
        risk_summary.columns = ["Risk Level", "Records"]

        risk_chart = px.bar(
            risk_summary,
            x="Risk Level",
            y="Records",
            title="Risk-Level Distribution",
            color="Risk Level",
            color_discrete_map={
                "Low": "#37d4a2",
                "Medium": "#ffca3a",
                "High": "#ff5c77"
            }
        )

        risk_chart.update_layout(
            paper_bgcolor="#151f32",
            plot_bgcolor="#151f32",
            font_color="#e5edf8",
            showlegend=False
        )

        st.plotly_chart(risk_chart, use_container_width=True)

    st.subheader("Traffic Analysis Results")
    st.caption("Showing the first 200 records.")

    display_columns = ["status", "risk_score", "risk_level"] + expected_columns

    st.dataframe(
        results[display_columns].head(200),
        use_container_width=True,
        hide_index=True
    )

with incidents_tab:
    st.subheader("Potential Security Incidents")

    incidents = results[
        results["prediction"] == 1
    ].sort_values("risk_score", ascending=False)

    if incidents.empty:
        st.success(
            "No records meet the current alert threshold. "
            "Try lowering the threshold in the sidebar."
        )
    else:
        st.warning(
            f"{len(incidents):,} possible attack record(s) need review."
        )

        incident_columns = ["risk_score", "risk_level"] + expected_columns

        st.dataframe(
            incidents[incident_columns].head(200),
            use_container_width=True,
            hide_index=True
        )

with profile_tab:
    st.subheader("Threat Profile")

    incidents = results[results["prediction"] == 1]

    if incidents.empty:
        st.info("No incidents are available at the current threshold.")
    else:
        profile_one, profile_two = st.columns(2)

        with profile_one:
            if "proto" in incidents.columns:
                protocol_summary = (
                    incidents["proto"]
                    .value_counts()
                    .head(10)
                    .reset_index()
                )
                protocol_summary.columns = ["Protocol", "Alerts"]

                protocol_chart = px.bar(
                    protocol_summary,
                    x="Protocol",
                    y="Alerts",
                    title="Alerts by Network Protocol",
                    color="Alerts",
                    color_continuous_scale="Reds"
                )

                protocol_chart.update_layout(
                    paper_bgcolor="#151f32",
                    plot_bgcolor="#151f32",
                    font_color="#e5edf8"
                )

                st.plotly_chart(protocol_chart, use_container_width=True)
            else:
                st.info("Protocol information is not available in this CSV.")

        with profile_two:
            if "service" in incidents.columns:
                service_summary = (
                    incidents["service"]
                    .value_counts()
                    .head(10)
                    .reset_index()
                )
                service_summary.columns = ["Service", "Alerts"]

                service_chart = px.bar(
                    service_summary,
                    x="Service",
                    y="Alerts",
                    title="Alerts by Network Service",
                    color="Alerts",
                    color_continuous_scale="Oranges"
                )

                service_chart.update_layout(
                    paper_bgcolor="#151f32",
                    plot_bgcolor="#151f32",
                    font_color="#e5edf8"
                )

                st.plotly_chart(service_chart, use_container_width=True)
            else:
                st.info("Service information is not available in this CSV.")

        st.info(
            "Use this page to identify which network protocols and services "
            "appear most often in the detected incidents."
        )

with explain_tab:
    st.subheader("Model Transparency")
    st.write(
        "This chart shows the network features that most influenced the "
        "trained Random Forest model overall."
    )

    importance_data = pd.DataFrame(
        {
            "Feature": expected_columns,
            "Importance": model.feature_importances_
        }
    ).sort_values("Importance", ascending=False).head(15)

    importance_chart = px.bar(
        importance_data.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 15 Most Important Detection Features",
        color="Importance",
        color_continuous_scale="Teal"
    )

    importance_chart.update_layout(
        paper_bgcolor="#151f32",
        plot_bgcolor="#151f32",
        font_color="#e5edf8",
        yaxis_title="",
        xaxis_title="Model Importance"
    )

    st.plotly_chart(importance_chart, use_container_width=True)

    st.info(
        "Higher importance means the model relied more on that feature "
        "when deciding whether network traffic looked suspicious."
    )

with export_tab:
    st.subheader("Download Security Report")
    st.write(
        "Download the full analysis, including predicted status, "
        "risk score, and risk level."
    )

    report_data = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Full Security Report (CSV)",
        data=report_data,
        file_name="netguard_security_report.csv",
        mime="text/csv"
    )