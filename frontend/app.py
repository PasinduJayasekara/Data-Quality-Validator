import streamlit as st
import requests

st.set_page_config(
    page_title="Dataset Quality Validator",
)


st.title("Dataset Quality Validator")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    st.info("File uploaded successfully. Click **Check Dataset** to validate.")

    if st.button("Check Dataset"):
        files = {
            "file": (uploaded_file.name, uploaded_file, "text/csv")
        }

        # Validate
        with st.spinner("Validating dataset..."):
            response = requests.post(
                "http://localhost:8000/validate",
                files=files
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

            # Download cleaned CSV file
            st.subheader("Download Cleaned CSV")
            # Reset the file pointer so backend can read it
            uploaded_file.seek(0)

            with st.spinner("Cleaning dataset..."):
                clean_response = requests.post(
                    "http://localhost:8000/clean",
                    files=files
                )

            if clean_response.status_code == 200:
                original_name = uploaded_file.name
                cleaned_filename = f"cleaned_{original_name}"

                st.download_button(
                    label="Download Cleaned CSV",
                    data=clean_response.content,
                    file_name=cleaned_filename,
                    mime="text/csv"
                )

