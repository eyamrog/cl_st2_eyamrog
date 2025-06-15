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
        title = soup.find('h1', class_='c-article-title')
        if title:
            title_text = ' '.join(title.get_text(' ', strip=True).split())
            text += f"Title: {title_text}\n\n"

        # Extract the 'Abstract'
        abstract_section = soup.find('div', id='Abs1-section')
        if abstract_section:
            abstract_h2_title = abstract_section.find('h2', class_='c-article-section__title')
            if abstract_h2_title:
                abstract_h2_title_text = ' '.join(abstract_h2_title.get_text(' ', strip=True).split())
                text += f"\nAbstract: {abstract_h2_title_text}\n\n"
            abstract_content = abstract_section.find('div', class_='c-article-section__content')
            if abstract_content:
                for paragraph in abstract_content.find_all('p', recursive=False):
                    # Remove <sup> elements containing references
                    for sup_tag in paragraph.find_all('sup'):
                        sup_tag.decompose()
                    # Extract the paragraph text
                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                    text += f"{paragraph_text}\n"

        # Extract the 'main content'
        main_content = soup.find('div', class_='main-content')
        if main_content:
            for main_content_section in main_content.find_all('section', recursive=False):
                # Extract sections
                for section in main_content_section.find_all('div', class_='c-article-section', recursive=False):
                    # Extract section title
                    section_h2_title = section.find('h2')
                    if section_h2_title:
                        section_h2_title_text = ' '.join(section_h2_title.get_text(' ', strip=True).split())
                        text += f"\nSection: {section_h2_title_text}\n\n"
                    # Extract section content
                    section_content = section.find('div', class_='c-article-section__content')
                    if section_content:
                        for content in section_content.find_all(['h3', 'h4', 'h5', 'p'], recursive=False):
                            # Remove <sup> elements containing references
                            for sup_tag in content.find_all('sup'):
                                sup_tag.decompose()
                            # Extract the content text
                            content_text = ' '.join(content.get_text(' ', strip=True).split())
                            text += f"{content_text}\n"

        # Extract the 'u-mt-32'
        u_mt_32 = soup.find('div', class_='u-mt-32')
        if u_mt_32:
            data_availability_section = u_mt_32.find('section', attrs={'data-title': 'Data availability'})
            if data_availability_section:
                for section in data_availability_section.find_all('div', class_='c-article-section', recursive=False):
                    # Extract section title
                    section_h2_title = section.find('h2')
                    if section_h2_title:
                        section_h2_title_text = ' '.join(section_h2_title.get_text(' ', strip=True).split())
                        text += f"\nSection: {section_h2_title_text}\n\n"
                    # Extract section content
                    section_content = section.find('div', class_='c-article-section__content')
                    if section_content:
                        for content in section_content.find_all('p', recursive=False):
                            # Remove <sup> elements containing references
                            for sup_tag in content.find_all('sup'):
                                sup_tag.decompose()
                            # Extract the content text
                            content_text = ' '.join(content.get_text(' ', strip=True).split())
                            text += f"{content_text}\n"

            acknowledgements_section = u_mt_32.find('section', attrs={'data-title': 'Acknowledgements'})
            if acknowledgements_section:
                for section in acknowledgements_section.find_all('div', class_='c-article-section', recursive=False):
                    # Extract section title
                    section_h2_title = section.find('h2')
                    if section_h2_title:
                        section_h2_title_text = ' '.join(section_h2_title.get_text(' ', strip=True).split())
                        text += f"\nSection: {section_h2_title_text}\n\n"
                    # Extract section content
                    section_content = section.find('div', class_='c-article-section__content')
                    if section_content:
                        for content in section_content.find_all('p', recursive=False):
                            # Remove <sup> elements containing references
                            for sup_tag in content.find_all('sup'):
                                sup_tag.decompose()
                            # Extract the content text
                            content_text = ' '.join(content.get_text(' ', strip=True).split())
                            text += f"{content_text}\n"

        # Web Scraping - End

        # Save text to a text file
        with open(txt_file, 'w', encoding='utf-8', newline='\n') as file:
            file.write(text)

        logging.info(f"Saved text for {article_id} to {txt_file}")