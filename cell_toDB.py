import sqlite3, os
from cell_line_scrape import get_soup, from_soup

# This file creates the cells table in the sqlite3 database cell.db 
# The column names are generic, atcc, organism, tissue, type, and disease
# Once this file is ran, 'sqlite3 cell.db' can be ran from windows powershell
#The table can be searched by 'select var from cells' where var is equal to any of the column names


lst_ = []

urls = ['http://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx']#gets first url pages
for i in range (2,123): #completes url list for all 121 pages
    urls.append('https://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx?dsNav=Ro:'+str(i*10-10)+',Ns:P_Product_Name%7c101%7c1%7c')
for i in range (len(urls)):    
    soup = get_soup(urls[i])
    from_soup (soup, lst_)

conn = sqlite3.connect('cell.db')
c = conn.cursor()

# new = not os.path.exists('cell.db')

# if new:
try:
    c.execute ('CREATE TABLE cells (generic, atcc, organism, tissue, type, disease)')
    
    conn.commit()
    
    for i in range (len(lst_)):
        args = [lst_[i]['GenName'], lst_[i]['ATCCName'], lst_[i]['Organism'], lst_[i]['Tissue'], lst_[i]['Cell Type'], lst_[i]['Disease']]
        c.execute('INSERT INTO cells (generic, atcc, organism, tissue, type, disease) VALUES (?, ?, ?, ?, ?, ?);', args)
        conn.commit()
except:
    pass
    
#c.execute('SELECT * FROM cells').fetchall() #check to see if database has been populated
conn.close()