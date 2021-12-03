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
        for f in (MainMenu, CreateDistro, SearchDistros, EditDistro, DuplicateDistro):
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

        editButton = tk.Button(self, text='Edit Distribution', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(EditDistro))
        editButton.pack(padx=10, pady=10)

        duplicateButton = tk.Button(self, text='Duplicate Distribution', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(DuplicateDistro))
        duplicateButton.pack(padx=10, pady=10)

        deleteButton = tk.Button(self, text='Delete Distribution', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(CreateDistro))
        deleteButton.pack(padx=10, pady=10)

        speciesButton = tk.Button(self, text='Add Species', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(SearchDistros))
        speciesButton.pack(padx=10, pady=10)


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

# class SearchResults(tk.Frame):
    
#     distros = []
    
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self,parent)
        
    
#     def addDistro(ID, Date, Facility, Count, Species):
            
        
#     def setDistros():
        
        

class SearchDistros(tk.Frame):
    
    dbLists = {
        'Date' : [],
        'regions' : [],
        'facilities' : [],
        'taxGroups' : [],
        'lifeStages' : ['Egg', 'Juvenile', 'Adult'],
        'species' : []
    }
    
    currentValue = {
        'Date' : None,
        'regions' : None,
        'facilities' : None,
        'taxGroups' : None,
        'lifeStages' : None,
        'species' : None
    }
    
    menus = {
        'Date' : None,
        'regions' : None,
        'facilities' : None,
        'taxGroups' : None,
        'lifeStages' : None,
        'species' : None
    }
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        titleLabel = tk.Label(self, text='Search Distribution Reports', font=TITLE_FONT)
        titleLabel.grid(row=0, column=1, pady=10, columnspan=5)

        # Fiscal Years
        self.dbLists['Date'] = qf.getYears()
        self.addOM('Date', 1, 'Year')
        
        # Region Names
        self.dbLists['regions'] = qf.getRegions()
        self.addOM('regions', 2, 'Region')
        self.currentValue['regions'].trace_variable('w', self.updateFaciliyList)
        
        # Facility Names
        self.dbLists['facilities'] = qf.getFacilities()
        self.addOM('facilities', 3, 'Facility Name')
        
        # Life Stages
        self.addOM('lifeStages', 4, 'Life Stage')
        
        # Taxonomic Groups
        self.dbLists['taxGroups'] = qf.getTaxGroups()
        self.addOM('taxGroups', 5, 'Taxonomic Group')
        self.currentValue['taxGroups'].trace_variable('w', self.updateSpeciesList)

        # Species 
        self.dbLists['species'] = qf.getSpecies()
        self.addOM('species', 6, 'Species')
        
        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                               command= lambda: controller.show_frame(MainMenu))
        
        clearButton = tk.Button(self, text='Clear Search', font=LARGE_FONT,
                               command= lambda: self.resetLists())
        
        searchButton = tk.Button(self, text='Search', font=LARGE_FONT,
                                command= lambda: self.getValues())
        
        cancelButton.grid(row=7, column=1)
        clearButton.grid(row=7, column=2, columnspan=2)
        searchButton.grid(row=7, column=5, pady=5)
    
    def addOM(self, name, rowDD, label):
        newLabel = tk.Label(self, text=f'{label}:', font=LARGE_FONT)
        self.currentValue[name] = tk.StringVar(self)
        self.currentValue[name].set('Any..')
        self.menus[name] = tk.OptionMenu(self, self.currentValue[name], *self.dbLists[name])
        newLabel.grid(row=rowDD, column=2)
        self.menus[name].grid(row=rowDD, column=3, pady=5)
    
    def resetLists(self):
        for key in self.currentValue:
            if(key != 'lifeStage'):
                self.currentValue[key].set('Any..')
        
    def getValues(self):
        for key in self.currentValue:
            value = self.currentValue[key].get()
            if(value != 'Any..'):
                print(f"{key} = {value}")

    def updateFaciliyList(self, *args):
        self.dbLists['facilities'] = qf.getFacilities(self.currentValue['regions'].get())
        self.menus['facilities']['menu'].delete(0, 'end')
        for facility in self.dbLists['facilities']:
            self.menus['facilities']['menu'].add_command(label=facility, command=tk._setit(self, facility))
            
    def updateSpeciesList(self, *args):
        self.dbLists['species'] = qf.getSpecies(self.currentValue['taxGroups'].get())
        self.menus['species']['menu'].delete(0, 'end')
        for species in self.dbLists['species']:
            self.menus['species']['menu'].add_command(label=species, command=tk._setit(self, species))
        
class EditDistro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        titleLabel = tk.Label(self, text='Edit Distribution', font=TITLE_FONT)
        titleLabel.grid(row=0, column=3, pady=10)

        # Date
        dateLabel = tk.Label(self, text='Date:', font=LARGE_FONT)
        dateEntry = tk.Entry(self)

        dateLabel.grid(row=1, column=1)
        dateEntry.grid(row=1, column=3)

        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(MainMenu))
        createButton = tk.Button(self, text='Create', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(MainMenu))

        cancelButton.grid(row=9, column=1, sticky='s')
        createButton.grid(row=9, column=4, sticky='s')


class DuplicateDistro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = tk.Label(self, text='Duplicate Distribution', font=TITLE_FONT)
        titleLabel.grid(row=0, column=3, pady=10)

        # Date
        distroIDLabel = tk.Label(self, text='Distribution ID:', font=LARGE_FONT)
        distroIDEntry = tk.Entry(self)

        distroIDLabel.grid(row=1, column=1)
        distroIDEntry.grid(row=1, column=3)

        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(MainMenu))
        createButton = tk.Button(self, text='Duplicate', font=LARGE_FONT,
                                 command=lambda: qf.distroExists(distroIDEntry.get()))

        cancelButton.grid(row=9, column=1, sticky='s')
        createButton.grid(row=9, column=4, sticky='s')

def main():
    app = ManageWindows()
    app.mainloop()

if (__name__ == '__main__'):
    main()