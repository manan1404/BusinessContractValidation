#scripts/pdf_highlighting.py
import fitz
import re

def extract_text_and_highlight_locations(pdf_path, search_text):
    highlights = {}
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = []
        words = page.get_text("words")
        for word in words:
            if search_text in word[4]:
                text_instances.append((word[:4]))
        highlights[page_num] = text_instances
    doc.close()
    return highlights


def highlight_pdf(input_pdf, output_pdf, deviations):
    doc = fitz.open(input_pdf)

    for dev in deviations:
        page_num = dev['page']
        page = doc.load_page(page_num)

        # Highlight heading
        heading_instances = page.search_for(dev['text'])
        for inst in heading_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.set_colors(stroke=(1, 1, 0))  # Yellow color for highlights
            highlight.update()

        # Highlight content under the heading if it exists and differs from the template
        if 'content' in dev and dev['content']:
            content_instances = page.search_for(dev['content'])
            for inst in content_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(1, 1, 0))  # Yellow color for highlights
                highlight.update()

    doc.save(output_pdf)


def extract_headings_and_content(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    content_by_heading = {}
    current_heading = None
    current_content = ""
    current_page = None

    heading_pattern = re.compile(r"^\d+(\.\d+)*\.")  # Pattern to match headings like 1., 1.1., 2., 2.1., etc.

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4].strip()  # The text of the block is at index 4
            if heading_pattern.match(text):
                if current_heading:
                    content_by_heading[current_heading] = {"content": current_content.strip(), "page": current_page}
                current_heading = text
                current_content = ""
                current_page = page_num
                headings.append({"text": current_heading, "page": page_num})
            elif current_heading:
                current_content += text + " "

    if current_heading:
        content_by_heading[current_heading] = {"content": current_content.strip(), "page": current_page}

    doc.close()
    return headings, content_by_heading
