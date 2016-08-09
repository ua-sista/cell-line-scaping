from cell_LineScrape import from_soup
import json 

# This file exports the cells into a json file titled cell_LineScrape.json
    
with open ('cell_LineScrape.json', 'w') as f:
    json.dump(from_soup(), f)

    
#opens cell_line_scrape.json    
# with open('cell_LineScrape.json', 'r') as f:
     # load_json_file = json.load(f)
#load_json_file     
