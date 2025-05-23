from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://cris.utec.edu.pe/es/persons/?page=1"

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

os.makedirs("profile_images", exist_ok=True)

def download_image(img_url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.90 Safari/537.36",
        "Referer": BASE_URL
    }
    try:
        response = requests.get(img_url, headers=headers)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def get_education_info(soup):
    for h in soup.find_all("h3", class_="subheader"):
        if h.get_text() == "Educación":
            container = h.parent
            return [div.text.strip().split(",")[0].split(' ')[0] for div in container.find_all("div", class_="rendering")]
    return []


def scrape_person_page(url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Name
    name_tag = soup.find(class_="header person-details")
    name = name_tag.find("h1").text.strip() if name_tag else "N/A"
    print("==========================\n",name,"\n==========================\n")

    # Profile image
    profile = soup.find(class_="profile").find(class_="meta")
    img_url = None
    if profile:
        img_tag = profile.find("img")
        if img_tag and img_tag.get("src"):
            img_url = urljoin(url, img_tag["src"])
            #download_image(img_url, f"profile_images/{name.replace(' ', '_')}.jpg")

    # Email
    email_tag = soup.find(class_="email")
    try:
        email = email_tag.get_text(strip=True) if email_tag else "N/A"
    except Exception as e:
        email = None

    try:
        citas = soup.find("ul", class_="metrics-list").find_all(class_="value")[0].text
    except:
        citas = None

    try:
        h_index = soup.find("ul", class_="metrics-list").find_all("div", class_="value")[-1].text
    except:
        h_index = None

    # Research areas
    research_areas = []
    ul = soup.find("ul", class_="relations keywords")
    if ul:
        research_areas = [li.get_text(strip=True) for li in ul.find_all("li")]

    # Department
    dept_tag = soup.find(class_="link department")
    if not dept_tag:
        dept_tag = soup.find(class_="link primary")
    department = dept_tag.get_text(strip=True) if dept_tag else "N/A"

    orgs = [x.text.strip() for x in soup.find_all("a", class_="link researchgroup")]
    orgs2 = [x.text.strip() for x in soup.find_all("a", class_="link center")]

    edu = get_education_info(soup)

    print("Name", name)
    print("Email", email)
    print("Department", department)
    print("Research", "; ".join(orgs + orgs2))
    print("Image URL", img_url)
    print("ResearchAreas", "; ".join(research_areas))
    print("H-index", h_index)
    print("Citas", citas)
    print("Edu", "; ".join(edu))

    return {
        "Name": name,
        "Email": email,
        "Department": department,
        "Research": "; ".join(orgs + orgs2),
        "Education": edu,
        "Image URL": img_url,
        "ResearchAreas": "; ".join(research_areas),
        "H-index": h_index,
        "Citas": citas
    }

def main():
    driver.get(BASE_URL)
    time.sleep(2)

    persons = driver.find_elements(By.CLASS_NAME, "link.person")
    links = [a.get_attribute("href") for a in persons if a.get_attribute("href")]

    results = []
    for link in links:
        print(f"Scraping {link}")
        data = scrape_person_page(link)
        results.append(data)

    keys = ["Name", "Email", "Department", "Research", "Education", "Image URL", "ResearchAreas", "H-index", "Citas"]
    with open("persons_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print("Data saved to persons_data.csv")
    driver.quit()

if __name__ == "__main__":
    main()
