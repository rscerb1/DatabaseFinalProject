import queryFunctions as qf

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

LARGE_FONT = ('Verdana', 12)
TITLE_FONT = ('Verdana', 18)

class ManageWindows(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        # initialize Tk
        tk.Tk.__init__(self, *args, **kwargs)
        # app name
        tk.Tk.wm_title(self, "Database Access Tool")
        # make a window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # make dict of all the frame classes
        self.frames = {}
        for f in (MainMenu, CreateDistro, SearchDistros): # add every class that gets its own frame here
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class MainMenu(Page):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        
        createButton = tk.Button(self, text = 'Create New Distribution Report', font = LARGE_FONT,
                            command = lambda: controller.show_frame(CreateDistro))
        createButton.pack(padx=10, pady=10)
        
        searchButton = tk.Button(self, text = 'Search Distribution Report', font = LARGE_FONT,
                            command = lambda: controller.show_frame(SearchDistros))
        searchButton.pack(padx=10, pady=10)


class CreateDistro(tk.Frame):
    
    regionsFromDB = ['']

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        titleLabel = tk.Label(self, text='Create New Distribution', font=TITLE_FONT)
        titleLabel.grid(row=0, column=3, pady=10)

        # Date
        dateLabel = tk.Label(self, text='Date:', font=LARGE_FONT)
        dateEntry = tk.Entry(self)
        
        dateLabel.grid(row=1, column=1)
        dateEntry.grid(row=1, column=3)
        
        # Count
        countLabel = tk.Label(self, text='Count:', font=LARGE_FONT)
        countEntry = tk.Entry(self)
        
        countLabel.grid(row=2, column=1)
        countEntry.grid(row=2, column=3)
        
        # ITIS
        ITISLabel = tk.Label(self, text='Species ITIS:', font=LARGE_FONT)
        ITISEntry = tk.Entry(self)
        
        ITISLabel.grid(row=3, column=1)
        ITISEntry.grid(row=3, column=3)
        
        # Region
        regionLabel = tk.Label(self, text='Facility Region:', font=LARGE_FONT)
        regionList = tk.StringVar(self)
        regionList.set('Select...')
        regionMenu = tk.OptionMenu(self, regionList, *self.regionsFromDB)
        regionMenu.config(width=15)
        
        regionLabel.grid(row=4, column=1)
        regionMenu.grid(row=4, column=3)
        
        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                               command= lambda: controller.show_frame(MainMenu))
        createButton = tk.Button(self, text='Create', font=LARGE_FONT,
                                command= lambda: controller.show_frame(MainMenu))
                
        cancelButton.grid(row=9,column=1, sticky='s')
        createButton.grid(row=9,column=4, sticky='s')

class SearchDistros(tk.Frame):
    
    dbLists = {
        'years' : [],
        'regions' : [],
        'facilities' : [],
        'taxGroups' : [],
        'lifeStages' : ['Egg', 'Juvenile', 'Adult'],
        'species' : []
    }
    
    currentValue = {
        'years' : '',
        'regions' : '',
        'facilities' : '',
        'taxGroups' : '',
        'lifeStages' : '',
        'species' : ''
    }
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        titleLabel = tk.Label(self, text='Search Distribution Reports', font=TITLE_FONT)
        titleLabel.grid(row=0, column=1, pady=10, columnspan=5)

        # Fiscal Years
        self.dbLists['years'] = qf.getYears()
        self.addOM('years', 1)
        
        # Region Names
        self.dbLists['regions'] = qf.getRegions()
        self.addOM('regions', 2)
        
        # Facility Names
        self.dbLists['facilities'] = qf.getFacilities()
        self.addOM('facilities', 3)
        
        # Taxonomic Groups
        self.dbLists['taxGroups'] = qf.getTaxGroups()
        self.addOM('taxGroups', 4)
        
        # Life Stages
        self.addOM('lifeStages', 5)
        
        # Species 
        self.dbLists['species'] = qf.getSpecies()
        self.addOM('species', 6)
        
        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                               command= lambda: controller.show_frame(MainMenu))
        searchButton = tk.Button(self, text='Search', font=LARGE_FONT,
                                command= lambda: self.getValues())
        
        cancelButton.grid(row=7, column=1)
        searchButton.grid(row=7, column=5, pady=5)
    
    def addOM(self, name, rowDD):
        newLabel = tk.Label(self, text=f'{name}:', font=LARGE_FONT)
        self.currentValue[name] = tk.StringVar(self)
        self.currentValue[name].set('Any')
        newMenu = tk.OptionMenu(self, self.currentValue[name], *self.dbLists[name])
        newLabel.grid(row=rowDD, column=2)
        newMenu.grid(row=rowDD, column=3, pady=5)
        
    def getValues(self):
        for key in self.currentValue:
            print(self.currentValue[key].get())

def main():
    app = ManageWindows()
    app.mainloop()

if (__name__ == '__main__'):
    main()