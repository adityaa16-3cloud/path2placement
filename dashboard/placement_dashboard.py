import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Path2Placement | Placement Analytics",
    page_icon="🎯",
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
        background: linear-gradient(135deg, #7c3aed, #ec4899);
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
st.title("🎯 Placement Analytics Dashboard")
st.caption("📊 Data-driven insights for placement readiness & outcomes")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/placement_data.csv")
    df["placed"] = df["placed"].map({"Yes": "Placed", "No": "Not Placed"})
    return df

df = load_data()

# ---------------------------------------------------
# ADVANCED SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.title("🎛 Advanced Filters")

min_cgpa = st.sidebar.slider("Minimum CGPA", 0.0, 10.0, 6.0)
min_projects = st.sidebar.slider("Minimum Projects", 0, int(df.projects.max()), 0)
min_internships = st.sidebar.slider("Minimum Internships", 0, int(df.internships.max()), 0)

filtered_df = df[
    (df.cgpa >= min_cgpa) &
    (df.projects >= min_projects) &
    (df.internships >= min_internships)
]

# ---------------------------------------------------
# SIDEBAR INSIGHTS (🔥 IMPORTANT UI FIX)
# ---------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Filter Summary")

st.sidebar.markdown(f"""
**Active Conditions**
- 🎓 CGPA ≥ **{min_cgpa}**
- 🛠 Projects ≥ **{min_projects}**
- 🏢 Internships ≥ **{min_internships}**
""")

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Live Insights")

total_students = len(filtered_df)
placed_count = filtered_df[filtered_df["placed"] == "Placed"].shape[0]
placement_rate = (placed_count / total_students * 100) if total_students else 0

if total_students > 0:
    st.sidebar.success(f"👨‍🎓 Students Selected: **{total_students}**")
    st.sidebar.info(f"📈 Placement Rate: **{placement_rate:.1f}%**")

    if placement_rate >= 70:
        st.sidebar.success("🎯 Strong placement potential")
    elif placement_rate >= 40:
        st.sidebar.warning("⚠️ Moderate readiness")
    else:
        st.sidebar.error("❌ High placement risk")
else:
    st.sidebar.warning("No students match current filters")

st.sidebar.markdown("---")
st.sidebar.subheader("💡 How to Use")

st.sidebar.markdown("""
- Increase **CGPA** to see high performers  
- Add **projects & internships** to boost chances  
- Identify **at-risk students** early  
""")

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
not_placed_count = total_students - placed_count

c1, c2, c3, c4 = st.columns(4)
c1.metric("👨‍🎓 Students", total_students)
c2.metric("✅ Placed", placed_count)
c3.metric("❌ Not Placed", not_placed_count)
c4.metric("📈 Placement Rate", f"{placement_rate:.2f}%")

st.divider()

# ---------------------------------------------------
# PLACEMENT OVERVIEW
# ---------------------------------------------------
st.subheader("📌 Placement Overview")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        filtered_df,
        names="placed",
        hole=0.45,
        title="Placed vs Not Placed",
        color_discrete_sequence=["#22c55e", "#ef4444"]
    )
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(
        filtered_df,
        x="cgpa",
        color="placed",
        barmode="group",
        title="CGPA Distribution by Placement",
        color_discrete_map={
            "Placed": "#22c55e",
            "Not Placed": "#ef4444"
        }
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------
# PLACEMENT PROBABILITY BANDS
# ---------------------------------------------------
st.subheader("🎯 Placement Probability Bands")

filtered_df["probability_band"] = pd.cut(
    filtered_df["cgpa"],
    bins=[0, 6, 7.5, 10],
    labels=["Low", "Medium", "High"]
)

fig_band = px.bar(
    filtered_df,
    x="probability_band",
    color="placed",
    title="Placement Probability Based on CGPA",
    color_discrete_map={
        "Placed": "#22c55e",
        "Not Placed": "#ef4444"
    }
)
fig_band.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(fig_band, use_container_width=True)

st.divider()

# ---------------------------------------------------
# SKILLS & INTERNSHIPS
# ---------------------------------------------------
st.subheader("🧠 Skills & Internship Impact")

col1, col2 = st.columns(2)

with col1:
    fig3 = px.box(
        filtered_df,
        x="placed",
        y="internships",
        title="Internships vs Placement",
        color="placed",
        color_discrete_map={
            "Placed": "#22c55e",
            "Not Placed": "#ef4444"
        }
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.box(
        filtered_df,
        x="placed",
        y="skills",
        title="Technical Skills vs Placement",
        color="placed",
        color_discrete_map={
            "Placed": "#22c55e",
            "Not Placed": "#ef4444"
        }
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---------------------------------------------------
# WHY NOT PLACED?
# ---------------------------------------------------
st.subheader("❌ Why Some Students Are Not Placed")

if not_placed_count > 0:
    st.warning("""
    **Common Factors Identified**
    • Lower CGPA  
    • Fewer internships & projects  
    • Weak aptitude & communication  
    • Higher backlogs
    """)
else:
    st.success("🎉 All filtered students are placed!")

st.divider()

# ---------------------------------------------------
# KEY INSIGHTS
# ---------------------------------------------------
st.subheader("📌 Key Insights")

st.success("CGPA above **8.0** significantly increases placement chances.")
st.info("Internships and projects strongly correlate with placement success.")
st.warning("Backlogs negatively affect placement probability.")

# ---------------------------------------------------
# DATA DOWNLOAD & VIEW
# ---------------------------------------------------
st.download_button(
    "📥 Download Filtered Placement Data",
    data=filtered_df.to_csv(index=False),
    file_name="placement_analysis.csv",
    mime="text/csv"
)

with st.expander("📄 View Placement Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
