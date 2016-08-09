import sqlite3, os
from cell_LineScrape import from_soup

# This file creates the cells table in the sqlite3 database cell.db. If the table already exists, this file does nothing.  
# The columns are name, organism, tissue, cell type, and disease

conn = sqlite3.connect('cell.db')
c = conn.cursor()

lst_ = from_soup ()
try:
    c.execute ('CREATE TABLE cells (name, organism, tissue, type, disease)')
    
    conn.commit()
    
    for i in range (len(lst_)):
        args = []         
            
        args.append(lst_[i]['Name'])
        args.append(lst_[i]['Organism'])
        args.append(lst_[i]['Tissue'])
        args.append(lst_[i]['Cell Type'])
        args.append(lst_[i]['Disease'])
            
        c.execute('INSERT INTO cells (name, organism, tissue, type, disease) VALUES (?, ?, ?, ?, ?);', args)
        conn.commit()
except:
    pass
    
conn.close()