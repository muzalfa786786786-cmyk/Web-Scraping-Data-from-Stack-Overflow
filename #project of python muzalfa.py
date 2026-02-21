import os
import requests
from bs4 import BeautifulSoup
try:
    company_url = "https://stackoverflow.com/jobs/companies"
    user_url = "https://stackoverflow.com/users"
    company_response = requests.get(company_url)
    company_response.raise_for_status()                                                                                       
    company_soup = BeautifulSoup(company_response.content, 'html.parser')                                                     
    images = [img.get('src') for img in company_soup.find_all('img')]                                                         
    headings = [heading.get_text() for heading in company_soup.find_all(class_='fs-body2 mb4')]                               
    items = [item.get_text() for item in company_soup.find_all(class_='d-flex gs12 gsx ff-row-wrap fs-body1')]                
    paragraphs = [para.get_text() for para in company_soup.find_all(class_='mt8 mb0 fs-body1 fc-black-700 v-truncate2')]      
    jobs = [job.get_text() for job in company_soup.find_all(class_='d-flex gs4 mt12 mb0 fw-wrap')]                            
    user_response = requests.get(user_url)
    user_response.raise_for_status()  
    user_soup = BeautifulSoup(user_response.content, 'html.parser')                                                             
    user_data = [data.get_text() for data in user_soup.find_all(class_='d-grid grid__4 lg:grid__3 md:grid__2 sm:grid__1 g12')]
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')            
    files_data = {
        'headings.txt': headings,
        'items.txt': items,
        'paragraphs.txt': paragraphs,
        'jobs.txt': jobs,
        'users.txt': user_data
    }
    for filename, data in files_data.items():
        with open(os.path.join(desktop_path, filename), 'w', encoding='utf-8') as file:
            file.write("\n".join(data))
        print(f"Data has been saved to '{os.path.join(desktop_path, filename)}'")
    images_dir = os.path.join(desktop_path, 'stackoverflow_images')
    os.makedirs(images_dir, exist_ok=True)
    for idx, img_url in enumerate(images):
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = 'https://stackoverflow.com' + img_url
        img_response = requests.get(img_url)
        img_response.raise_for_status()  
        img_filename = os.path.join(images_dir, f'image_{idx + 1}.jpg')
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Image has been saved to '{img_filename}'")
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
