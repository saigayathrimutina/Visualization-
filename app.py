import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Boxplot & Heatmap Explorer", layout="wide")

st.title("📊 Box Plot & Heatmap Explorer")
st.markdown(
    "Upload a CSV or Excel file (manual upload). Then pick numeric columns to visualize a box plot and a correlation heatmap."
)

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls", "txt"])

@st.cache_data
def load_file(file):
    try:
        if hasattr(file, "name") and file.name.lower().endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        else:
            # try csv
            df = pd.read_csv(file)
    except Exception as e:
        st.warning(f"Could not read file automatically: {e}")
        # fallback: try read csv with different separators
        try:
            df = pd.read_csv(file, sep=";")
        except Exception:
            raise
    return df

if uploaded_file is not None:
    try:
        df = load_file(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        st.stop()

    st.sidebar.header("Data preview & options")
    if st.sidebar.checkbox("Show raw data", False):
        st.dataframe(df.head(200))

    # Detect numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    all_cols = df.columns.tolist()

    if not numeric_cols:
        st.error("No numeric columns detected in the uploaded file. Please upload a file with numeric data.")
        st.stop()

    st.sidebar.markdown(f"**Detected numeric columns:** {', '.join(numeric_cols)}")

    # Missing value handling
    na_strategy = st.sidebar.radio("Missing-value handling", ["Drop rows with NA", "Fill numeric with mean", "Fill numeric with median"], index=0)
    df_work = df.copy()
    if na_strategy == "Drop rows with NA":
        df_work = df_work.dropna(subset=numeric_cols)
    elif na_strategy == "Fill numeric with mean":
        for c in numeric_cols:
            df_work[c] = df_work[c].fillna(df_work[c].mean())
    else:
        for c in numeric_cols:
            df_work[c] = df_work[c].fillna(df_work[c].median())

    st.sidebar.markdown("---")

    st.header("Box Plot")
    cols_for_box = st.multiselect("Select numeric columns for boxplot (1 or more)", numeric_cols, default=numeric_cols[:2])

    # Optional grouping column
    cat_candidates = df.select_dtypes(exclude=[np.number]).columns.tolist()
    group_col = st.selectbox("Optional: Group by (categorical) column for grouped boxplot", options=[None] + cat_candidates)

    if cols_for_box:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        try:
            if group_col:
                # grouped boxplot: melt
                plot_df = df_work[cols_for_box + [group_col]].melt(id_vars=group_col, var_name="variable", value_name="value")
                sns.boxplot(x="variable", y="value", hue=group_col, data=plot_df, ax=ax1)
                ax1.set_xlabel("")
                ax1.set_ylabel("Value")
                ax1.set_title("Grouped boxplot")
                ax1.legend(title=group_col, bbox_to_anchor=(1.02, 1), loc="upper left")
            else:
                sns.boxplot(data=df_work[cols_for_box], ax=ax1)
                ax1.set_title("Boxplot")
                ax1.set_xlabel("")
                ax1.set_ylabel("Value")
            st.pyplot(fig1)
        except Exception as e:
            st.error(f"Could not draw boxplot: {e}")

    st.markdown("---")

    st.header("Correlation Heatmap")
    cols_for_heat = st.multiselect("Select numeric columns for heatmap (at least 2)", numeric_cols, default=numeric_cols)
    cmap_choice = st.selectbox("Choose colormap (matplotlib names)", ["viridis", "coolwarm", "magma", "plasma", "cividis"], index=1)

    if len(cols_for_heat) >= 2:
        corr_method = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"], index=0)
        corr = df_work[cols_for_heat].corr(method=corr_method)

        fig2, ax2 = plt.subplots(figsize=(max(6, len(cols_for_heat) * 0.8), max(4, len(cols_for_heat) * 0.6)))
        sns.heatmap(corr, annot=True, fmt=".2f", square=True, linewidths=0.5, cbar_kws={"shrink": 0.6}, ax=ax2, cmap=cmap_choice)
        ax2.set_title(f"Correlation heatmap ({corr_method})")
        st.pyplot(fig2)

        st.markdown("**Correlation matrix (numeric values)**")
        st.dataframe(corr)
    else:
        st.info("Select at least two numeric columns to generate a heatmap.")

    st.sidebar.markdown("---")
    st.sidebar.write("If you need the processed dataset used for the plots, you can download it.")
    if st.sidebar.button("Download processed CSV"):
        csv = df_work.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button("Download CSV", data=csv, file_name="processed_data.csv", mime="text/csv")

    st.write("---")
    st.markdown("*Tip: Use tidy datasets where each column is a variable and each row is an observation for best results.*")
else:
    st.info("Please upload a CSV or Excel file using the file uploader at the top.")
          
