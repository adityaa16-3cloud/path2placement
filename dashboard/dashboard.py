import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Path2Placement | Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM STYLING (MATCH WEBSITE)
# ---------------------------------------------------
st.markdown("""
<style>
    .main {
        background: radial-gradient(circle at top, #1e293b, #020617);
    }
    h1, h2, h3, h4 {
        color: #f8fafc;
    }
    .stMetric {
        background: linear-gradient(135deg, #2563eb, #0ea5e9);
        padding: 18px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🎓 Student Performance Analytics Dashboard")
st.caption("📊 Academic insights to track performance, risk & improvement areas")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/student_data.csv")
    df["result"] = df["result"].map({"Pass": "Pass", "Fail": "Fail"})
    return df

df = load_data()

# ---------------------------------------------------
# ADVANCED SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.title("🎛 Advanced Filters")

min_attendance = st.sidebar.slider(
    "Minimum Attendance (%)",
    int(df.attendance.min()),
    int(df.attendance.max()),
    60
)

min_study = st.sidebar.slider(
    "Minimum Study Hours / Day",
    int(df.study_hours.min()),
    int(df.study_hours.max()),
    1
)

min_internal = st.sidebar.slider(
    "Minimum Internal Marks",
    int(df.internal_marks.min()),
    int(df.internal_marks.max()),
    40
)

filtered_df = df[
    (df.attendance >= min_attendance) &
    (df.study_hours >= min_study) &
    (df.internal_marks >= min_internal)
]

# ---------------------------------------------------
# SIDEBAR INSIGHTS
# ---------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Filter Summary")

st.sidebar.markdown(f"""
**Active Criteria**
- 📅 Attendance ≥ **{min_attendance}%**
- ⏱ Study Hours ≥ **{min_study}**
- 📝 Internal Marks ≥ **{min_internal}**
""")

total_students = len(filtered_df)
pass_count = filtered_df[filtered_df["result"] == "Pass"].shape[0]
fail_count = total_students - pass_count
pass_rate = (pass_count / total_students * 100) if total_students else 0

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Live Academic Health")

if total_students > 0:
    st.sidebar.success(f"👨‍🎓 Students: **{total_students}**")
    st.sidebar.info(f"✅ Pass Rate: **{pass_rate:.1f}%**")

    if pass_rate >= 75:
        st.sidebar.success("🎯 Strong academic performance")
    elif pass_rate >= 50:
        st.sidebar.warning("⚠️ Moderate risk detected")
    else:
        st.sidebar.error("❌ High failure risk")
else:
    st.sidebar.warning("No students match current filters")

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Academic Tips")

st.sidebar.markdown("""
- Increase **attendance** to reduce risk  
- Study **2–3 hrs/day consistently**  
- Focus on **internals & assignments**  
""")

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("👨‍🎓 Students", total_students)
c2.metric("✅ Passed", pass_count)
c3.metric("❌ Failed", fail_count)
c4.metric("📈 Pass Rate", f"{pass_rate:.2f}%")

st.divider()

# ---------------------------------------------------
# PERFORMANCE OVERVIEW
# ---------------------------------------------------
st.subheader("📌 Performance Overview")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        filtered_df,
        names="result",
        hole=0.45,
        title="Pass vs Fail",
        color_discrete_sequence=["#22c55e", "#ef4444"]
    )
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(
        filtered_df,
        x="attendance",
        color="result",
        barmode="group",
        title="Attendance Distribution by Result",
        color_discrete_map={
            "Pass": "#22c55e",
            "Fail": "#ef4444"
        }
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------
# STUDY & MARKS ANALYSIS
# ---------------------------------------------------
st.subheader("📘 Study & Marks Impact")

col1, col2 = st.columns(2)

with col1:
    fig3 = px.box(
        filtered_df,
        x="result",
        y="study_hours",
        title="Study Hours vs Result",
        color="result",
        color_discrete_map={
            "Pass": "#22c55e",
            "Fail": "#ef4444"
        }
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.box(
        filtered_df,
        x="result",
        y="internal_marks",
        title="Internal Marks vs Result",
        color="result",
        color_discrete_map={
            "Pass": "#22c55e",
            "Fail": "#ef4444"
        }
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---------------------------------------------------
# PERFORMANCE RISK BANDS
# ---------------------------------------------------
st.subheader("🚦 Academic Risk Bands")

filtered_df["risk_band"] = pd.cut(
    filtered_df["attendance"],
    bins=[0, 65, 80, 100],
    labels=["High Risk", "Medium Risk", "Low Risk"]
)

fig_band = px.bar(
    filtered_df,
    x="risk_band",
    color="result",
    title="Academic Risk Based on Attendance",
    color_discrete_map={
        "Pass": "#22c55e",
        "Fail": "#ef4444"
    }
)
fig_band.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(fig_band, use_container_width=True)

st.divider()

# ---------------------------------------------------
# WHY STUDENTS FAIL?
# ---------------------------------------------------
st.subheader("❌ Why Some Students Fail")

if fail_count > 0:
    st.warning("""
    **Common Academic Issues**
    • Low attendance  
    • Inconsistent study hours  
    • Poor internal & assignment scores  
    • Last-minute preparation
    """)
else:
    st.success("🎉 All filtered students are passing!")

st.divider()

# ---------------------------------------------------
# KEY INSIGHTS
# ---------------------------------------------------
st.subheader("📌 Key Insights")

st.success("Attendance above **80%** strongly correlates with passing.")
st.info("Students studying **2+ hours/day** perform significantly better.")
st.warning("Low internal marks increase failure probability.")

# ---------------------------------------------------
# DATA DOWNLOAD & VIEW
# ---------------------------------------------------
st.download_button(
    "📥 Download Filtered Student Data",
    data=filtered_df.to_csv(index=False),
    file_name="student_performance_analysis.csv",
    mime="text/csv"
)

with st.expander("📄 View Student Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
