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
    
    yearsFromDB = ['']
    regionsFromDB = ['']
    facilitiesFromDB = ['']
    taxGroupsFromDB = ['']
    lifeStagesFromDB = ['']
    speciesFromDB = ['']
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        titleLabel = tk.Label(self, text='Search Distribution Reports', font=TITLE_FONT)
        titleLabel.grid(row=0, column=1, pady=10, columnspan=5)

        # Fiscal Years
        yearLabel = tk.Label(self, text='Fiscal Year:', font=LARGE_FONT)
        yearList = tk.StringVar(self)
        yearList.set('Select...')
        yearMenu = tk.OptionMenu(self, yearList, *self.yearsFromDB)
        
        yearLabel.grid(row=1, column=2)
        yearMenu.grid(row=1, column=3, pady=5)
        
        # Region Names
        regionLabel = tk.Label(self, text='Facility Region:', font=LARGE_FONT)
        regionList = tk.StringVar(self)
        regionList.set('Select...')
        regionMenu = tk.OptionMenu(self, regionList, *self.regionsFromDB)
        
        regionLabel.grid(row=2, column=2)
        regionMenu.grid(row=2, column=3, pady=5)
        
        # Facility Names
        facilityLabel = tk.Label(self, text='Facility Name:', font=LARGE_FONT)
        facilityList = tk.StringVar(self)
        facilityList.set('Select...')
        facilityMenu = tk.OptionMenu(self, facilityList, *self.facilitiesFromDB)
        
        facilityLabel.grid(row=3, column=2)
        facilityMenu.grid(row=3, column=3, pady=5)
        
        # Taxonomic Groups
        taxGroupLabel = tk.Label(self, text='Taxonomic Group:', font=LARGE_FONT)
        taxGroupList = tk.StringVar(self)
        taxGroupList.set('Select...')
        taxGroupMenu = tk.OptionMenu(self, taxGroupList, *self.taxGroupsFromDB)
        
        taxGroupLabel.grid(row=4, column=2)
        taxGroupMenu.grid(row=4, column=3, pady=5)
        
        # Life Stage
        lifeStageLabel = tk.Label(self, text='Life Stage:', font=LARGE_FONT)
        lifeStageList = tk.StringVar(self)
        lifeStageList.set('Select...')
        lifeStageMenu = tk.OptionMenu(self, lifeStageList, *self.lifeStagesFromDB)
        
        lifeStageLabel.grid(row=5, column=2)
        lifeStageMenu.grid(row=5, column=3, pady=5)
        
        # Species 
        speciesLabel = tk.Label(self, text='Species:', font=LARGE_FONT)
        speciesList = tk.StringVar(self)
        speciesList.set('Select...')
        speciesMenu = tk.OptionMenu(self, speciesList, *self.lifeStagesFromDB)
        
        speciesLabel.grid(row=6, column=2)
        speciesMenu.grid(row=6, column=3, pady=5)
        
        # Search Button        
        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                               command= lambda: controller.show_frame(MainMenu))
        searchButton = tk.Button(self, text='Search', font=LARGE_FONT,
                                command= lambda: controller.show_frame(MainMenu))
        
        cancelButton.grid(row=7, column=1)
        searchButton.grid(row=7, column=5, pady=5)

def main():
    app = ManageWindows()
    app.mainloop()

if (__name__ == '__main__'):
    main()