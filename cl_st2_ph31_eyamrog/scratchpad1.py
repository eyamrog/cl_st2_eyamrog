def extract_text(df, path):
    """Extracts text from HTML files and saves as text files."""

    for article_id in df['ID']:
        html_file = os.path.join(path, f"{article_id}.html")
        txt_file = os.path.join(path, f"{article_id}.txt")

        # Check if the HTML file exists
        if not os.path.exists(html_file):
            logging.error(f"Skipping {html_file}: File not found")
            continue

        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'lxml')

        # Initialise text variable
        text = ''

        # Extract the 'Title'
        title_tag = soup.find('span', class_='article-title')
        if title_tag:
            title = ' '.join(title_tag.get_text(' ', strip=True).split())
            text += f"Title: {title}\n\n"

        # Extract 'article sections'
        for section in soup.find_all('div', class_='articleSection'): # Finds all 'div.articleSection' elements (both top-level and nested).
            if not section.find_parent('div', class_='articleSection'): # Keeps only the top-level sections because it filters out nested ones by checking if the 'div.articleSection' has a parent that is also 'div.articleSection'
                
                # Extract section title
                section_title_tag = section.find('div', class_='tl-main-part title')
                if section_title_tag:
                    section_title = ' '.join(section_title_tag.get_text(' ', strip=True).split())
                    text += f"\nSection: {section_title}\n\n"

                # Extract paragraphs (only from top-level sections)
                for paragraph in section.find_all('p'):
                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                    text += f"{paragraph_text}\n"

                # Extract subsections
                for subsection in section.find_all('div', recursive=False):
                    #label_tag = subsection.find('span', class_='label')
                    #if label_tag:
                    #    label_text = ' '.join(label_tag.get_text(' ', strip=True).split())
                    #    text += f"\nSection: {label_text} "
                    #subsection_tag = subsection.find('span', class_='tl-lowest-section')
                    #if subsection_tag:
                    #    subsection_title = ' '.join(subsection_tag.get_text(' ', strip=True).split())
                    #    text += f"{subsection_title}\n\n"
                    for paragraph in subsection.find_all('p'):
                        paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                        text += f"{paragraph_text}\n"

        # Save text to a text file
        with open(txt_file, 'w', encoding='utf-8', newline='\n') as file:
            file.write(text)

        logging.info(f"Saved text for {article_id} to {txt_file}")