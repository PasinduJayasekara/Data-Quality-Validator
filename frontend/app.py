import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dataset Quality Validator")
st.title("Dataset Quality Validator")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    st.info("File uploaded successfully.")

    # ---- Read file ONCE ----
    file_bytes = uploaded_file.getvalue()

    # ---- Dataset Preview (BEFORE validation) ----
    st.subheader("Dataset Preview")
    try:
        preview_df = pd.read_csv(
            pd.io.common.BytesIO(file_bytes),
            encoding="utf-8-sig",
            thousands=",",
            nrows=5
        )
        st.dataframe(preview_df, width="stretch")
        st.caption("Showing first 5 rows of the dataset (including column names).")
    except Exception as e:
        st.error("Unable to preview CSV file.")
        st.caption(str(e))

    st.divider()

    if st.button("Check Dataset"):
        files = {
            "file": (uploaded_file.name, file_bytes, "text/csv")
        }

        # ---- Validate ----
        with st.spinner("Validating dataset..."):
            response = requests.post(
                "http://localhost:8000/validate",
                files=files,
                timeout=60
            )

        if response.status_code == 200:
            report = response.json()

            st.subheader("Summary")
            st.write(f"Rows : {report['rows']}")
            st.write(f"Columns : {report['columns']}")

            st.subheader("Missing Values")
            st.json(report["missing_values"])

            st.subheader("Duplicate Rows")
            st.write(report["duplicate_rows"])

            st.subheader("Outliers")
            st.json(report["outliers"])

            st.subheader("Column Profiling")
            st.json(report["profiling"])

            st.subheader("Schema Issues")
            if report["schema_issues"]:
                st.write(report["schema_issues"])
            else:
                st.success("No schema issues detected")

            st.metric("Data Quality Score", report["quality_score"])

            st.subheader("Cleaning Suggestions")
            for s in report["suggestions"]:
                st.write("- ", s)

            st.divider()

            # ---- Download Cleaned CSV ----
            st.subheader("Download Cleaned CSV")
            with st.spinner("Cleaning dataset..."):
                clean_response = requests.post(
                    "http://localhost:8000/clean",
                    files=files,
                    timeout=60
                )

            if clean_response.status_code == 200:
                st.download_button(
                    label="Download Cleaned CSV",
                    data=clean_response.content,
                    file_name=f"cleaned_{uploaded_file.name}",
                    mime="text/csv"
                )
