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
        title_tag = soup.find('h1', class_='c-article-title')
        if title_tag:
            title = ' '.join(title_tag.get_text(' ', strip=True).split())
            text += f"{title}\n"

        # Extract the 'article body'
        article_body_tag = soup.find('div', class_='c-article-body')
        if article_body_tag:
            for section in article_body_tag.find_all('section'):
                # Extract section title (h2)
                section_h2_title_tag = section.find('h2', class_='c-article-section__title')
                if section_h2_title_tag:
                    section_h2_title = ' '.join(section_h2_title_tag.get_text(' ', strip=True).split())
                    text += f"{section_h2_title}\n"

                # Extract subsection title (h3)
                section_h3_title_tag = section.find('h3', class_='c-article__sub-heading')
                if section_h3_title_tag:
                    section_h3_title = ' '.join(section_h3_title_tag.get_text(' ', strip=True).split())
                    text += f"{section_h3_title}\n"

                # Extract paragraphs
                for paragraph in section.find_all('p'):
                    # Remove <sup> elements containing references
                    for sup_tag in paragraph.find_all('sup'):
                        sup_tag.decompose()  # Completely removes the element

                    # Extract the paragraph text
                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                    text += f"{paragraph_text}\n"

        # Save text to a text file
        with open(txt_file, 'w', encoding='utf-8', newline='\n') as file:
            file.write(text)

        logging.info(f"Saved text for {article_id} to {txt_file}")