from flask import Flask, jsonify
import asyncio
from playwright.async_api import async_playwright
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

HTML_FILE_PATH = "https://corporate.restory.in/api/assets/common/1739788533.html"
OUTPUT_PDF_PATH = os.path.abspath("LyfTrac_output.pdf")

async def convert_html_to_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(HTML_FILE_PATH)
        await page.pdf(
            path=OUTPUT_PDF_PATH,
            format="A4",
            print_background=True,
            margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"},
            scale=1.0
        )
        await browser.close()

def remove_pages_by_numbers(pdf_path, pages_to_remove):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    pages_to_remove_set = set(pages_to_remove)
    for i in range(total_pages):
        # Pages are zero-indexed internally, user pages are 1-indexed
        if (i + 1) not in pages_to_remove_set:
            writer.add_page(reader.pages[i])
    with open(pdf_path, "wb") as f_out:
        writer.write(f_out)

@app.route('/generate-pdf', methods=['GET'])
def convert_to_pdf():
    try:
        asyncio.run(convert_html_to_pdf())
        # Removed page removal to keep all pages
        # pages_to_remove = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46]
        # remove_pages_by_numbers(OUTPUT_PDF_PATH, pages_to_remove)
        return jsonify({"message": f"Lyftrac_Output.pdf generated successfully in the path {OUTPUT_PDF_PATH}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Flask App is running. Use /generate-pdf to generate pdf"

if __name__ == '__main__':
    app.run(debug=True)
