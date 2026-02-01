import streamlit as st
import requests

st.title("Data Quality Validator")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}

    # Validate
    response = requests.post("http://localhost:8000/validate", files=files)
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

        # Download cleaned CSV file
        st.subheader("Download Cleaned CSV")
        # Reset the file pointer so backend can read it
        uploaded_file.seek(0)
        clean_response = requests.post("http://localhost:8000/clean", files=files)
        if clean_response.status_code == 200:
            st.download_button(
                label="Download Cleaned CSV",
                data=clean_response.content,
                file_name="cleaned.csv",
                mime="text/csv"
            )
