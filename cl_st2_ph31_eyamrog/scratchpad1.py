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
        title = soup.find('h1', class_='citation__title')
        if title:
            title_text = ' '.join(title.get_text(' ', strip=True).split())
            text += f"Title: {title_text}\n\n"

        # Capture the 'article body'
        article_body = soup.find('div', class_='article__body')
        
        # Extract the 'Abstract'
        if article_body:
            abstract_section = article_body.find('section', class_='article-section__abstract')
            if abstract_section:
                h2_title = abstract_section.find('h2')
                if h2_title:
                    h2_title_text = ' '.join(h2_title.get_text(' ', strip=True).split())
                    text += f"\nAbstract: {h2_title_text}\n\n"
                abstract_content = abstract_section.find('div', class_='article-section__content en main')
                if abstract_content:
                    for paragraph in abstract_content.find_all('p', recursive=False):
                        paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                        text += f"{paragraph_text}\n"
                    for section in abstract_content.find_all('section', recursive=False):
                        h3_title = section.find('h3')
                        if h3_title:
                            h3_title_text = ' '.join(h3_title.get_text(' ', strip=True).split())
                            text += f"\nSection: {h3_title_text}\n\n"
                        for paragraph in section.find_all('p', recursive=False):
                            paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                            text += f"{paragraph_text}\n"

        # Extract the 'body'
        if article_body:
            body_section = article_body.find('section', class_='article-section article-section__full')
            if body_section:
                for h2_section in body_section.find_all('section', class_='article-section__content', recursive=False):
                    h2_title = h2_section.find('h2')
                    if h2_title:
                        h2_title_text = ' '.join(h2_title.get_text(' ', strip=True).split())
                        text += f"\nSection: {h2_title_text}\n\n"
                    for paragraph in h2_section.find_all('p', recursive=False):
                        paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                        text += f"{paragraph_text}\n"
                    for h3_section in h2_section.find_all('section', recursive=False):
                        #h3_title = h3_section.find('h3')
                        #if h3_title:
                        #    h3_title_text = ' '.join(h3_title.get_text(' ', strip=True).split())
                        #    text += f"\nSection: {h3_title_text}\n\n"
                        for paragraph in h3_section.find_all('p', recursive=False):
                            paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                            text += f"{paragraph_text}\n"
                        for h4_section in h3_section.find_all('section', recursive=False):
                            #h4_title = h4_section.find('h4')
                            #if h4_title:
                            #    h4_title_text = ' '.join(h4_title.get_text(' ', strip=True).split())
                            #    text += f"\nSection: {h4_title_text}\n\n"
                            for paragraph in h4_section.find_all('p', recursive=False):
                                paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                                text += f"{paragraph_text}\n"
                            for h5_section in h4_section.find_all('section', recursive=False):
                                #h5_title = h5_section.find('h5')
                                #if h5_title:
                                #    h5_title_text = ' '.join(h5_title.get_text(' ', strip=True).split())
                                #    text += f"\nSection: {h5_title_text}\n\n"
                                for paragraph in h5_section.find_all('p', recursive=False):
                                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                                    text += f"{paragraph_text}\n"

        # Extract the 'Acknowledgements'
        if body_section:
            for h2_section in body_section.find_all('div', class_='article-section__content', recursive=False):
                h2_title = h2_section.find('h2')
                if h2_title:
                    h2_title_text = ' '.join(h2_title.get_text(' ', strip=True).split())
                    text += f"\nSection: {h2_title_text}\n\n"
                for paragraph in h2_section.find_all('p', recursive=False):
                    paragraph_text = ' '.join(paragraph.get_text(' ', strip=True).split())
                    text += f"{paragraph_text}\n"

        # Web Scraping - End

        # Save text to a text file
        with open(txt_file, 'w', encoding='utf-8', newline='\n') as file:
            file.write(text)

        logging.info(f"Saved text for {article_id} to {txt_file}")