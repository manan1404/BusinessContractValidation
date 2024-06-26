# #app/streamlit_app.py
# import os
# import sys
# import fitz
# import streamlit as st
# import google.generativeai as genai
#
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
#
# from text_extraction import extract_text_from_pdf
# from text_classification import classify_text
# from pdf_highlighting import highlight_pdf, extract_text_and_highlight_locations
# from text_comparison import compare_texts
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from fpdf import FPDF
#
# YOUR_API_KEY = "AIzaSyA1qAuFbFEotbg49Cr6pihddohEqoTiclw"
# genai.configure(api_key=YOUR_API_KEY)
# generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
# model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
#
#
# def generate_standard_template():
#     pdf_path = "EMPLOYMENT_CONTRACT_0001.pdf"  # Adjust this path as per your file location
#     pdf_text = extract_text_from_pdf(pdf_path)
#     original_query = pdf_text
#     generated_queries = generate_queries_gemini(original_query)
#     return generated_queries
#
#
# def generate_queries_gemini(original_query):
#     content_prompts = [
#         f"{original_query}\n"
#         f"Extract the information from the above content and convert it into the given below headings and subheadings:\n"
#         f"1.Duties and Scope of Employment \n"
#         f"(a) Position \n"
#         f"(b) Obligations to the Company \n"
#         f"(c) No Conflicting Obligations \n"
#         f"2.Cash and Incentive Compensation\n"
#         f"(a) Salary\n"
#         f"(b) Bonus\n"
#         f"(c) Options\n"
#         f"(d) Insurance Coverage Reimbursement\n"
#         f"(e) Vacation\n"
#         f"3.Business Expenses\n"
#         f"4.Term of Employment\n"
#         f"(a) Term\n"
#         f"(b) Basic Rule\n"
#         f"(c) Termination\n"
#         f"(d) Rights Upon Termination\n"
#         f"5.Termination Benefits\n"
#         f"(a) General Release\n"
#         f"(b) Severance Pay\n"
#         f"(c) Stock Options\n"
#         f"(d) Disability\n"
#         f"(e) Definition of 'Cause'\n"
#         f"(f) Definition of 'Constructive Termination'\n"
#         f"6. Invention, Confidential Information, and Non-Competition Agreement\n"
#         f"7. Successors\n"
#         f"8. Miscellaneous Provisions\n"
#         f"(a) Notice\n"
#         f"(b) Modifications and Waivers\n"
#         f"(c) Indemnification\n"
#         f"(d) Whole Agreement\n"
#         f"(e) Withholding Taxes\n"
#         f"(f) Choice of Law and Severability\n"
#         f"(g) Arbitration\n"
#         f"(h) No Assignment\n"
#         f"(i) Counterparts\n"
#     ]
#     response = model.generate_content(content_prompts)
#     generated_queries = response.text.strip().split("\n")
#     return generated_queries
#
#
# def save_standard_template_to_pdf(standard_template):
#     pdf_filename = "standard_template.pdf"  # Adjust this path as per your desired output location
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#
#     for line in standard_template:
#         pdf.cell(200, 10, txt=line, ln=True)
#
#     pdf.output(pdf_filename)
#     return pdf_filename
#
#
# def main():
#     st.title("Business Contract Analyzer")
#     uploaded_file = st.file_uploader("Choose an input PDF file", type="pdf")
#     if uploaded_file:
#         # Save the uploaded file to disk
#         input_pdf_path = uploaded_file.name  # Adjust this path as per your file location
#         with open(input_pdf_path, "wb") as f:
#             f.write(uploaded_file.read())
#
#         # Extract text from the input PDF
#         input_text = extract_text_from_pdf(input_pdf_path)
#
#         # Generate standard template
#         standard_template = generate_standard_template()
#
#         # Save standard template as PDF
#         st.write("Standard Template PDF saved as:", save_standard_template_to_pdf(standard_template))
#
#         # Classify the extracted text
#         classified_text = classify_text([input_text], ['employment_contract'])
#
#         # Compare classified text against the standard template to find deviations
#         deviations = compare_texts(input_text, standard_template)  # Implement logic to find deviations
#
#         # Print deviations and coordinates
#         # for dev in deviations:
#         #     st.write("Deviation:", dev)
#
#         # Highlight deviations in the input PDF
#         output_pdf_path = f"highlighted_{input_pdf_path}"  # Adjust this path as per your desired output location
#         highlight_pdf(input_pdf_path, output_pdf_path, deviations)
#
#         # Display the extracted text and classified text
#         st.write("Extracted Text from Input PDF:", input_text)
#         # st.write("Classified Text according to Standard Template:", classified_text)
#
#         # Display the generated PDF with highlights
#         with open(output_pdf_path, "rb") as file:
#             st.download_button(
#                 label="Download Highlighted PDF",
#                 data=file,
#                 file_name=output_pdf_path,
#                 mime="application/pdf"
#             )
#
#
# if __name__ == "__main__":
#     main()

#app/streamlit_app.py
import os
import sys
import fitz
import streamlit as st
import google.generativeai as genai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from text_extraction import extract_text_from_pdf
from pdf_highlighting import highlight_pdf, extract_headings_and_content
from text_comparison import compare_headings_and_content
from fpdf import FPDF

YOUR_API_KEY = "AIzaSyA1qAuFbFEotbg49Cr6pihddohEqoTiclw"
genai.configure(api_key=YOUR_API_KEY)
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

def generate_standard_template():
    pdf_path = "EMPLOYMENT_CONTRACT_0001.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    original_query = pdf_text
    generated_queries = generate_queries_gemini(original_query)
    return generated_queries

def generate_queries_gemini(original_query):
    content_prompts = [
        f"{original_query}\n"
        f"Extract the information from the above content and convert it into the given below headings and subheadings:\n"
        f"1. Duties and Scope of Employment\n"
        f"(a) Position\n"
        f"(b) Obligations to the Company\n"
        f"(c) No Conflicting Obligations\n"
        f"2. Cash and Incentive Compensation\n"
        f"(a) Salary\n"
        f"(b) Bonus\n"
        f"(c) Options\n"
        f"(d) Insurance Coverage Reimbursement\n"
        f"(e) Vacation\n"
        f"3. Business Expenses\n"
        f"4. Term of Employment\n"
        f"(a) Term\n"
        f"(b) Basic Rule\n"
        f"(c) Termination\n"
        f"(d) Rights Upon Termination\n"
        f"5. Termination Benefits\n"
        f"(a) General Release\n"
        f"(b) Severance Pay\n"
        f"(c) Stock Options\n"
        f"(d) Disability\n"
        f"(e) Definition of 'Cause'\n"
        f"(f) Definition of 'Constructive Termination'\n"
        f"6. Invention, Confidential Information, and Non-Competition Agreement\n"
        f"7. Successors\n"
        f"8. Miscellaneous Provisions\n"
        f"(a) Notice\n"
        f"(b) Modifications and Waivers\n"
        f"(c) Indemnification\n"
        f"(d) Whole Agreement\n"
        f"(e) Withholding Taxes\n"
        f"(f) Choice of Law and Severability\n"
        f"(g) Arbitration\n"
        f"(h) No Assignment\n"
        f"(i) Counterparts\n"
    ]
    response = model.generate_content(content_prompts)
    generated_queries = response.text.strip().split("\n")
    return generated_queries

def save_standard_template_to_pdf(standard_template):
    pdf_filename = "standard_template.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in standard_template:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(pdf_filename)
    return pdf_filename

def main():
    st.title("Business Contract Analyzer")
    uploaded_file = st.file_uploader("Choose an input PDF file", type="pdf")
    if uploaded_file:
        # Save the uploaded file to disk
        input_pdf_path = uploaded_file.name
        with open(input_pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract headings and content from the input PDF
        input_headings, input_content = extract_headings_and_content(input_pdf_path)

        # Generate standard template
        standard_template = generate_standard_template()

        # Save standard template as PDF
        standard_template_pdf_path = save_standard_template_to_pdf(standard_template)

        # Extract headings and content from the standard template PDF
        template_headings, template_content = extract_headings_and_content(standard_template_pdf_path)

        # Compare headings and content to find deviations
        deviations = compare_headings_and_content(input_headings, template_headings, input_content, template_content)

        # Highlight deviations in the input PDF
        output_pdf_path = f"highlighted_{input_pdf_path}"
        highlight_pdf(input_pdf_path, output_pdf_path, deviations)

        # Display the extracted text (optional)
        input_text = extract_text_from_pdf(input_pdf_path)
        st.write("Extracted Text from Input PDF:", input_text)

        # Display the generated PDF with highlights
        with open(output_pdf_path, "rb") as file:
            st.download_button(
                label="Download Highlighted PDF",
                data=file,
                file_name=output_pdf_path,
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
