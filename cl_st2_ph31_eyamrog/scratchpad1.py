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
        title_tag = soup.find('h1', property='name')
        if title_tag:
            title = ' '.join(title_tag.get_text(' ', strip=True).split())
            text += f"Title: {title}\n\n"

        # Extract the 'Abstract'
        abstract_section = soup.find('section', property='abstract')
        if abstract_section:
            abstract_tag = abstract_section.find('h2', property='name')
            if abstract_tag:
                abstract = ' '.join(abstract_tag.get_text(' ', strip=True).split())
                text += f"\nAbstract: {abstract}\n\n"

            for section_h3 in abstract_section.find_all('section', recursive=False):
                section_h3_title_tag = section_h3.find('h3')
                if section_h3_title_tag:
                    section_h3_title = ' '.join(section_h3_title_tag.get_text(' ', strip=True).split())
                    text += f"\nSection: {section_h3_title}\n\n"

                # Extract paragraphs within each section
                paragraphs = section_h3.find_all('div', role='paragraph', recursive=False)
                for paragraph in paragraphs:
                    # Remove reference citations embedded in <span> tags
                    for ref_tag in paragraph.find_all('span', class_='dropBlock reference-citations'):
                        ref_tag.decompose()  # Completely removes the element

                    # Extract the paragraph text
                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                    text += f"{paragraph_text}\n"

        # Extract the 'article body'
        body_section = soup.find('section', property='articleBody')
        if body_section:
            body_section_core_container = body_section.find('div', class_='core-container')
            if body_section_core_container:
                # Extract sectioned content
                for section_h2 in body_section_core_container.find_all('section', recursive=False):
                    section_text = ''  # Reset for each section

                    # Extract section title (h2)
                    section_h2_title_tag = section_h2.find('h2')
                    if section_h2_title_tag:
                        section_h2_title = ' '.join(section_h2_title_tag.get_text(' ', strip=True).split())
                        section_text += f"\nSection: {section_h2_title}\n\n"
                    
                    # Extract h2 paragraphs, if there are any
                    paragraphs = section_h2.find_all('div', role='paragraph', recursive=False)
                    for paragraph in paragraphs:
                        # Remove reference citations embedded in <span> tags
                        for ref_tag in paragraph.find_all('span', class_='dropBlock reference-citations'):
                            ref_tag.decompose()  # Completely removes the element

                        # Extract the paragraph text
                        paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                        section_text += f"{paragraph_text}\n"

                    for section_h3 in section_h2.find_all('section'):
                        ## Extract subsection title (h3)
                        #section_h3_title_tag = section_h3.find('h3')
                        #if section_h3_title_tag:
                        #    section_h3_title = ' '.join(section_h3_title_tag.get_text(' ', strip=True).split())
                        #    section_text += f"\nSection: {section_h3_title}\n\n"

                        # Extract h3 paragraphs
                        paragraphs = section_h3.find_all('div', role='paragraph', recursive=False)
                        for paragraph in paragraphs:
                            # Remove reference citations embedded in <span> tags
                            for ref_tag in paragraph.find_all('span', class_='dropBlock reference-citations'):
                                ref_tag.decompose()  # Completely removes the element

                            # Extract the paragraph text
                            paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                            section_text += f"{paragraph_text}\n"

                        for section_h4 in section_h3.find_all('section'):
                            ## Extract subsection title (h4)
                            #section_h4_title_tag = section_h4.find('h4')
                            #if section_h4_title_tag:
                            #    section_h4_title = ' '.join(section_h4_title_tag.get_text(' ', strip=True).split())
                            #    section_text += f"\nSection: {section_h4_title}\n\n"

                            # Extract h4 paragraphs
                            paragraphs = section_h4.find_all('div', role='paragraph', recursive=False)
                            for paragraph in paragraphs:
                                # Remove reference citations embedded in <span> tags
                                for ref_tag in paragraph.find_all('span', class_='dropBlock reference-citations'):
                                    ref_tag.decompose()  # Completely removes the element

                                # Extract the paragraph text
                                paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                                section_text += f"{paragraph_text}\n"

                            for section_h5 in section_h4.find_all('section'):
                                ## Extract subsection title (h5)
                                #section_h5_title_tag = section_h5.find('h5')
                                #if section_h5_title_tag:
                                #    section_h5_title = ' '.join(section_h5_title_tag.get_text(' ', strip=True).split())
                                #    section_text += f"\nSection: {section_h5_title}\n\n"

                                # Extract h5 paragraphs
                                paragraphs = section_h5.find_all('div', role='paragraph', recursive=False)
                                for paragraph in paragraphs:
                                    # Remove reference citations embedded in <span> tags
                                    for ref_tag in paragraph.find_all('span', class_='dropBlock reference-citations'):
                                        ref_tag.decompose()  # Completely removes the element

                                    # Extract the paragraph text
                                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                                    section_text += f"{paragraph_text}\n"

                    text += section_text  # Append structured section text

        # Save text to a text file
        with open(txt_file, 'w', encoding='utf-8', newline='\n') as file:
            file.write(text)

        logging.info(f"Saved text for {article_id} to {txt_file}")