# Arachnida

### Created during a Cybersecurity Bootcamp at 42 Barcelona

This repository contains two Python scripts: **SPIDER** and **SCORPION**. 

## SPIDER

### Description
SPIDER is a web scraping tool designed to extract links and images from a given domain. It uses the `BeautifulSoup` library from `bs4` to parse the HTML content and extract the desired data.

### Usage
1. Ensure you have the required libraries installed:
  ```
  pip install bs4 requests
  ```

2. Run the script with the desired options:
  ```
  python spider.py [options]
  ```

### Options
- `-p`: Specify the folder where the images will be saved.
- `-l`: Specify the level of recursion.
- `-r`: Specify the number of images to retrieve.

---

## SCORPION

### Description
SCORPION is a tool designed to extract metadata from images using the `exifread` library. It can provide detailed metadata or a smaller, more concise version.

### Usage
1. Ensure you have the required library installed:
   ```
   pip install exifread
   ```
2. Run the script with the desired options:
   ```
   python scorpion.py [options] [image_paths]
   ```

### Options
- `-s`: Use this flag to get a smaller version of the metadata.

---

## Disclaimer
These scripts are provided for educational purposes only. Ensure you have the necessary permissions before scraping websites or extracting metadata from images.

