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

        # Web Scraping - Begin

        # Extract the 'Title'
        title = soup.find('h1', property='name')
        if title:
            title_text = ' '.join(title.get_text(' ', strip=True).split())
            text += f"Title: {title_text}\n\n"

        # Extract the 'Abstract'
        abstract_section = soup.find('div', id='abstracts')
        if abstract_section:
            author_abstract_section = abstract_section.find('section', id='author-abstract')
            if author_abstract_section:
                author_abstract_h2_title = author_abstract_section.find('h2', property='name')
                if author_abstract_h2_title:
                    author_abstract_h2_title_text = ' '.join(author_abstract_h2_title.get_text(' ', strip=True).split())
                    text += f"\nAbstract: {author_abstract_h2_title_text}\n\n"
                for paragraph in author_abstract_section.find_all('div', role='paragraph', recursive=False):
                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                    text += f"{paragraph_text}\n"

        # Extract the 'body'
        body_section = soup.find('section', id='bodymatter')
        if body_section:
            body_core_container = body_section.find('div', class_='core-container')
            if body_core_container:
                # Extract sections
                for section_h2 in body_core_container.find_all('section', recursive=False):
                    # Extract section title
                    section_h2_title = section_h2.find('h2')
                    if section_h2_title:
                        section_h2_title_text = ' '.join(section_h2_title.get_text(' ', strip=True).split())
                        text += f"\nSection: {section_h2_title_text}\n\n"
                    # Extract section paragraphs
                    for paragraph in section_h2.find_all('div', role='paragraph', recursive=False):
                        paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                        text += f"{paragraph_text}\n"

                    # Extract subsections
                    for section_h3 in section_h2.find_all('section', recursive=False):
                        ## Extract subsection title
                        #section_h3_title = section_h3.find('h3')
                        #if section_h3_title:
                        #    section_h3_title_text = ' '.join(section_h3_title.get_text(' ', strip=True).split())
                        #    text += f"\nSubsection: {section_h3_title_text}\n\n"
                        # Extract subsection paragraphs
                        for paragraph in section_h3.find_all('div', role='paragraph', recursive=False):
                            paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                            text += f"{paragraph_text}\n"

                        # Extract subsubsections
                        for section_h4 in section_h3.find_all('section', recursive=False):
                            ## Extract subsubsection title
                            #section_h4_title = section_h4.find('h4')
                            #if section_h4_title:
                            #    section_h4_title_text = ' '.join(section_h4_title.get_text(' ', strip=True).split())
                            #    text += f"\nSubsubsection: {section_h4_title_text}\n\n"
                            # Extract subsubsection paragraphs
                            for paragraph in section_h4.find_all('div', role='paragraph', recursive=False):
                                paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                                text += f"{paragraph_text}\n"

                            # Extract subsubsubsections
                            for section_h5 in section_h4.find_all('section', recursive=False):
                                ## Extract subsubsubsection title
                                #section_h5_title = section_h5.find('h5')
                                #if section_h5_title:
                                #    section_h5_title_text = ' '.join(section_h5_title.get_text(' ', strip=True).split())
                                #    text += f"\nSubsubsubsection: {section_h5_title_text}\n\n"
                                # Extract subsubsubsection paragraphs
                                for paragraph in section_h5.find_all('div', role='paragraph', recursive=False):
                                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                                    text += f"{paragraph_text}\n"

        # Web Scraping - End

        # Save text to a text file
        with open(txt_file, 'w', encoding='utf-8', newline='\n') as file:
            file.write(text)

        logging.info(f"Saved text for {article_id} to {txt_file}")