
import requests
import re

# The URL of the (1st) web page with laptop products
# You may need to change the URL to that of some of the next product pages (due to product details formatting inconsistencies)
base_url = 'https://www.e-shop.gr/ypologistes-laptops-list?table=PER&category=%D6%CF%D1%C7%D4%CF%C9+%D5%D0%CF%CB%CF%C3%C9%D3%D4%C5%D3'
r = requests.get(base_url)
print('\n** Level 1 Scraping **')
print('\nBase URL:', r.url)
print('\nCollecting info...\n')

c = r.content
txt = c.decode('iso-8859-7') # Decode using the encoding used by the web site

# *** Level 1 Scraping ***
# Regex for collecting the item codes of laptop products
laptop_itemcodes = re.findall('(?<=\()PER\.\d+(?=\))', txt)

# Regex for collecting the titles of laptop products
laptop_titles = re.findall('(?<=<h2>).*(?=<\/h2>)', txt)

# Regex for collecting the discounts of laptop products
laptop_discounts = re.findall('(?<=ΕΚΠΤΩΣΗ&nbsp;)(\d+%)(?=<)', txt)

# Regex for collecting multiple product information for each product
# (Category, Category Value, Subcategory, Subcategory Value, Manufacturer, Manufacturer Value)
info_regx = '(?<=-info"><b>)(.*?)(<\/b>&nbsp;\s)(.*?)(&nbsp;&nbsp;&nbsp;\s<b>)(.*?)(<\/b>&nbsp;\s)(.*?)(&nbsp;&nbsp;&nbsp;\s<b>)(.*?)(<\/b>&nbsp;\s)(.*?)(?=\s<br><br>)'
info_regx_comp = re.compile(info_regx)

laptop_categories = []
laptop_inches = []
laptop_manufacturers = []

# Iterative loop for separating the matching regex groups
# Only the values - and not the title - of the product information will be kept (just 3 of all the groups that got matched)
for match in info_regx_comp.finditer(txt):
    # To print both the title and the values of the product information, uncomment the next line
    # print(match.group(1, 3, 5, 7, 9, 11))

    # Append values for Category, Subcategory (Inches) and Manufacturer - groups 3, 7 and 11 - to the according list
    laptop_categories.append(match.group(3))
    laptop_inches.append(match.group(7))
    laptop_manufacturers.append(match.group(11))

# Regex for collecting the URLs of the laptop pages (needed for level 2 scraping)
url_list = re.findall('(?<=<a href=\").*(?=\" class=\"web-title-link\"><h2>)', txt)

# *** Level 2 Scraping ***
cnt=1
laptop_cpus = []
laptop_displays = []
laptop_rams = []
laptop_storages = []
laptop_dvd_drives = []
laptop_gpus = []

# Regular expressions for all the information that is to be collected on level 2 scraping
cpu_regx = '(?<=<li><b>\sΕπεξεργαστής:<\/b>\s)([A-zΆ-ώ0-9#:.,+/\-\(\)\s]*)(?=\.<li><b>)'
display_regx ='(?<=<li><b>\sΟθόνη:<\/b>\s)([A-zΆ-ώ0-9#:.,+/\-\(\)\'\"\s]*)(?=\.<li><b>)'
memory_regx = '(?<=<li><b>\sΜνήμη:<\/b>\s)([A-zΆ-ώ0-9#:.,+/\-\(\)\s]*)(?=\.?<li><b>)'
storage_regx = '(?<=<li><b>\sΣκληρός\sΔίσκος:<\/b>\s)([A-zΆ-ώ0-9#:.,+/\-\(\)\s]*)(?=\.<li><b>)'
dvd_drive_regx = '(?<=<li><b>\sΟπτικός\sΔίσκος:<\/b>\s)([A-zΆ-ώ0-9#:.,+/\-\(\)\s]*)(?=\.<li><b>)'
gpu_regx = '(?<=<li><b>\sΚάρτα\sγραφικών:<\/b>\s)([A-zΆ-ώ0-9#:.,+/\-\(\)\s]*)(?=\.<li><b>)'

print('** Level 2 Scraping **')

print('\n~~ Sub-level URLs ~~\n')

# Iterative loop for printing the URL of each product page
# and collecting all the technical details that were selected for each product
for i in url_list:
    r = requests.get(i)
    c = r.content
    txt = c.decode('iso-8859-7')
    print('URL ' + str(cnt) + ':', r.url, '\n')
    print('Collecting info...\n')

    laptop_cpus.append(re.findall(cpu_regx, txt))
    laptop_displays.append(re.findall(display_regx, txt))
    laptop_rams.append(re.findall(memory_regx, txt))
    laptop_storages.append(re.findall(storage_regx, txt))
    laptop_dvd_drives.append(re.findall(dvd_drive_regx, txt))
    laptop_gpus.append(re.findall(gpu_regx, txt))

    cnt+=1

# If the length of any nested list is 0 (meaning it is empty)
# then the value None is appended to it
for x in laptop_dvd_drives:
    if len(x) == 0:
        x.append(None)

# List comprehension for all the nested lists
new_cpu = [x for l in laptop_cpus for x in l]
new_display = [x for l in laptop_displays for x in l]
new_rams = [x for l in laptop_rams for x in l]
new_storages = [x for l in laptop_storages for x in l]
new_dvd_drives = [x for l in laptop_dvd_drives for x in l]
new_gpus = [x for l in laptop_gpus for x in l]

# Entering all the lists in a single dictionary
dict = {
    'code' : laptop_itemcodes,
    'title' : laptop_titles,
    'discount' : laptop_discounts,
    'category' : laptop_categories,
    'inches' : laptop_inches,
    'manufacturer' : laptop_manufacturers,
    'cpu' : new_cpu,
    'display' : new_display,
    'memory' : new_rams,
    'storage' : new_storages,
    'dvd_drive' : new_dvd_drives,
    'gpu' : new_gpus
}

# Printing the entire dictionary
print('Final data dictionary:')
print(dict)

# Printing the collected information by category
# Level 1 scraped data
print("\nProduct Titles:")
print(dict.get('title'), '\n')
print("Product Codes:")
print(dict.get('code'), '\n')
print("Product Discounts:")
print(dict.get('discount'), '\n')
print("Product Categories:")
print(dict.get('category'), '\n')
print("Product Inches:")
print(dict.get('inches'), '\n')
print("Product Manufacturers:")
print(dict.get('manufacturer'), '\n')

# Level 2 scraped data
print("CPUs:")
print(dict.get('cpu'), '\n')
print("Displays:")
print(dict.get('display'), '\n')
print("RAMs:")
print(dict.get('memory'), '\n')
print("Storage Spaces:")
print(dict.get('storage'), '\n')
print("DVD Drives:")
print(dict.get('dvd_drive'), '\n')
print("GPUs:")
print(dict.get('gpu'), '\n')

# *** Exporting the data to a spreadsheet ***
import pandas
# pip install openpyxl
import os

# Inserting all dictionary data to a pandas dataframe
try:
    df = pandas.DataFrame(dict)
except Exception as e1:
    print(f'--> Error inserting dictionary data to dataframe: {e1}\n--> Try next product page URL to check if it works\n')

print('~~ Printing directory info ~~')

print('Current working directory: ', os.getcwd())

dirname = os.path.dirname(__file__)
print('Program directory: ', dirname)

# Variable for the full path of the excel file to be created
filename = os.path.join(dirname, 'laptop_data.xlsx')
print('Excel file directory:', filename)

# Exporting the dataframe to an excel file
try:
    df.to_excel(filename)
    print('\nExcel file created successfully!\n')
except Exception as e2:
    print(f'\n--> Error exporting dataframe to Excel file: {e2}\n')