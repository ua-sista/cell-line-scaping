from cell_LineScrape import from_soup
import time

#This program runs the user interface which allows users to search page by page, entry by entry the ATCC cell line database.

lst = from_soup()

def printHomeMenu(lst_, pgStr):
 
    sl = []
    prntStr = ("Page" + pgStr).center(80,"*")
    print (prntStr)
    pgInt = int(pgStr)

    if pgInt == 122:
        for i in range (0,1):
            print (str(i+1) +": "+lst_[10*(pgInt-1)+i]['Name'])
        print ('')    
        ask = input ("Press enter to select all, select page number by typing 'p' followed by the number (ex. p9), or type 'esc' to exit: ")
        print ('')
        print ('')
        firstEntry = 10*(pgInt-1)
        sl.append(ask)
        sl.append(pgStr)
        sl.append(pgInt)
        sl.append(firstEntry)
        return sl
    
    else: 
        for i in range (0,10):
            print (str(i+1) +": "+lst_[10*(pgInt-1)+i]['Name'])
        print ('')    
        ask = input ("Enter choices separated by spaces, select page number by typing 'p' followed by the number (ex. p9), press enter to select all, or type 'esc' to exit: ")
        print ('')
        print('')
        firstEntry = 10*(pgInt-1)
        sl.append(ask)
        sl.append(pgStr)
        sl.append(pgInt)
        sl.append(firstEntry)
        return sl
    
def main ():
    print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
    whereToGo = printHomeMenu(lst, '1')
    go = True
    while go:
        
        if whereToGo[0] == '':
            print ((' Return all on page ' + whereToGo[1] + ' ').center(80, '*'))
            if whereToGo[1] == '122':
                for i in range (0,1):
                    print ((' Entry '+ str(i+1) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                    print ('Name: '+lst[whereToGo[3]+i]['Name'])
                    print ('Organism: '+lst[whereToGo[3]+i]['Organism'])
                    print ('Tissue: '+lst[whereToGo[3]+i]['Tissue'])
                    print ('Cell Type: '+lst[whereToGo[3]+i]['Cell Type'])
                    print ('Disease: '+lst[whereToGo[3]+i]['Disease'])
                    print('')
                    
                print('')    
                ask = input("Press enter to return or type 'esc' to quit: ")
                print ('')
                print ('')
                print ('')
                if ask == '':
                    whereToGo = printHomeMenu(lst, whereToGo[1])
                elif ask == 'esc':
                    go = False
                    break
                else: 
                    print ((" Invalid entry ").center(80,"*"))
                    print ('')
                    go = False 
                    break
            else:        
                for i in range (0,10):
                    print ((' Entry '+ str(i+1) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                    print ('Name: '+lst[whereToGo[3]+i]['Name'])
                    print ('Organism: '+lst[whereToGo[3]+i]['Organism'])
                    print ('Tissue: '+lst[whereToGo[3]+i]['Tissue'])
                    print ('Cell Type: '+lst[whereToGo[3]+i]['Cell Type'])
                    print ('Disease: '+lst[whereToGo[3]+i]['Disease'])
                    print('')
                ask = input("Press enter to return or type 'esc' to quit: ")
                print ('')
                print ('')
                print ('')
                if ask == '':
                    whereToGo = printHomeMenu(lst, whereToGo[1])
                elif ask == 'esc':
                    go = False
                    break
                else: 
                    print ((" Invalid entry ").center(80,"*"))
                    print ('')
                    go = False   
                    break
                    
                
        elif 'p' in whereToGo[0]:
            x = whereToGo[0].replace('p','')
                
            if int(x)>122 or int(x)<1:
                print ((' Page number must be between 1 and 122 ').center(80,'*'))
                go = False
                                
            else:
                whereToGo = printHomeMenu (lst, x)
                
        elif whereToGo[0].replace(' ','').isdigit():
            if whereToGo[1] == "122":
            
                y = [int(i) for i in whereToGo[0].split(' ')]
                for i in range (len(y)):
                    if y[i] > 1 or y[i]<0:
                        print ((" Invalid entry ").center(80,"*"))
                        go = False
                        break     
                if go:        
                    #else:
                    print ((" Search of " + whereToGo[0] + " on page " + whereToGo[1] + ' ').center(80,"*")) 
                    print (('').center(80,'*'))
                    print ('')
                    for i in range (len(y)):
                        print ((' Entry '+ str(y[i]) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                        choose = y[i]-1
                        print ("Name: " + lst[whereToGo[3]+choose]["Name"])
                        print ("Organism: " + lst[whereToGo[3]+choose]["Organism"])
                        print ("Tissue: " + lst[whereToGo[3]+choose]["Tissue"])
                        print ("Cell Type: " + lst[whereToGo[3]+choose]["Cell Type"])
                        print ("Disease: " + lst[whereToGo[3]+choose]["Disease"])
                        print ('')
                    ask = input ("Press enter to return or type 'esc' to quit: ")    
                    print ('')
                    print ('')
                    print ('')
                    if ask == '':
                        whereToGo = printHomeMenu(lst, whereToGo[1])
                    elif ask == 'esc':
                        go = False   
                        break
                    else: 
                        print ((" Invalid entry ").center(80,"*"))
                        print ('')
                        go = False
                 
            else:    
                y = [int(i) for i in whereToGo[0].split(' ')]
                for i in range (len(y)):
                    if y[i] > 10 or y[i]<0:
                        print (("Invalid entry").center(80,"*"))
                        go = False
                        break     
                if go:        
                 
                    print ((" Search of " + whereToGo[0] + " on page " + whereToGo[1] + ' ').center(80,"*")) 
                    print (('').center(80,'*'))
                    print ('')
                    for i in range (len(y)):
                        print ((' Entry '+ str(y[i]) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                        choose = y[i]-1
                        print ("Name: " + lst[whereToGo[3]+choose]["Name"])
                        print ("Organism: " + lst[whereToGo[3]+choose]["Organism"])
                        print ("Tissue: " + lst[whereToGo[3]+choose]["Tissue"])
                        print ("Cell Type: " + lst[whereToGo[3]+choose]["Cell Type"])
                        print ("Disease: " + lst[whereToGo[3]+choose]["Disease"])
                        print ('')
                    ask = input ("Press enter to return or type 'esc' to quit: ")    
                    print ('')
                    print ('')
                    print ('') 
                    
                    if ask == '':
                        whereToGo = printHomeMenu(lst, whereToGo[1])
                    elif ask == 'esc':
                        go = False   
                        break
                    else: 
                        print ((" Invalid entry ").center(80,"*"))
                        print ('')
                        go = False
                
        elif whereToGo[0] == 'esc':
            go = False
            
        else:  
            print ((" Invalid entry ").center(80,"*"))
            print ('')
            go = False
                        
    
if __name__ == '__main__':
    main()        