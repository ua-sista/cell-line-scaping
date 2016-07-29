from cell_line_scrape import get_soup, from_soup
import json 

# This file exports the cells into a json file titled cell_line_scrape.json

lst_ = []

urls = ['http://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx']#gets first url pages
for i in range (2,123): #completes url list for all 121 pages
    urls.append('https://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx?dsNav=Ro:'+str(i*10-10)+',Ns:P_Product_Name%7c101%7c1%7c')
for i in range (len(urls)):    
    soup = get_soup(urls[i])
    from_soup (soup, lst_)
    
with open ('cell_line_scrape.json', 'w') as f:
    json.dump(lst_, f)

    
#opens cell_line_scrape.json    
# with open('cell_line_scrape.json', 'r') as f:
     # load_json_file = json.load(f)
#load_json_file     
