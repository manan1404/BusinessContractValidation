#scripts/text_comparison.py

from difflib import Differ

def compare_texts(text1, text2):
    """Compare two texts and return their differences."""
    if isinstance(text1, list):
        text1 = '\n'.join(text1)
    if isinstance(text2, list):
        text2 = '\n'.join(text2)

    diffs = list(Differ().compare(text1.splitlines(), text2.splitlines()))
    deviations = []
    page_num = 0  # Initialize page number
    for diff in diffs:
        if diff.startswith('- '):
            deviation = {
                'page': page_num,
                'text': diff[2:],  # Extract the deviating text
            }
            deviations.append(deviation)
        elif diff.startswith('? '):
            page_num += 1  # Increment page number when encountering a new page
    return deviations

def compare_headings_and_content(input_headings, template_headings, input_content, template_content):
    deviations = []

    # Extract only the heading texts from both lists of dictionaries
    input_heading_texts = [heading['text'] for heading in input_headings]
    template_heading_texts = [heading['text'] for heading in template_headings]

    # Find headings in input that are not in the template
    for input_heading in input_headings:
        if input_heading['text'] not in template_heading_texts:
            # If the heading text is not in the template, consider it a deviation
            deviations.append(input_heading)
        else:
            # Check if the content under this heading differs from the template
            input_heading_content = input_content[input_heading['text']]['content']
            template_heading_content = template_content[input_heading['text']]['content']
            if input_heading_content != template_heading_content:
                deviations.append({
                    'text': input_heading['text'],
                    'content': input_heading_content,
                    'page': input_heading['page']
                })

    return deviations

