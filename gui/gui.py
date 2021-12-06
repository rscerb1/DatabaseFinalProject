from datetime import datetime, time
from time import sleep
from tkinter import filedialog as fd
import tkinter.messagebox, csv, os.path


from tkcalendar import DateEntry

import queryFunctions as qf

try:
    import tkinter as tk
    from tkinter import ttk, W
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
        for f in (MainMenu, CreateDistro, SearchDistros, EditDistro, DuplicateDistro, DeleteDistro, AddSpecies):
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
                                 command=lambda: controller.show_frame(DeleteDistro))
        deleteButton.pack(padx=10, pady=10)

        speciesButton = tk.Button(self, text='Add Species', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(AddSpecies))
        speciesButton.pack(padx=10, pady=10)


class CreateDistro(tk.Frame):
    
    menus = {
        'Date' : None,
        'regions' : None,
        'facilities' : None,
        'taxGroups' : None,
        'lifeStages' : None,
        'species' : None,
        'rec' : None,
        'type' : None
    }
    
    currentValue = {
        'Date' : None,
        'regions' : None,
        'facilities' : None,
        'taxGroups' : None,
        'lifeStages' : None,
        'species' : None,
        'rec' : None,
        'type' : None
    }
    
    dbLists = {
        'Date' : [],
        'regions' : [],
        'facilities' : [],
        'taxGroups' : [],
        'lifeStages' : ['Egg', 'Juvenile', 'Adult'],
        'species' : [],
        'type' : ['Transfer', 'Release']
    } 
    
    regionsFromDB = ['']

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        titleLabel = tk.Label(self, text='Create New Distribution', font=TITLE_FONT)
        titleLabel.grid(row=0, column=1, pady=10, columnspan=3)
        
        # Count
        countLabel = tk.Label(self, text='Count:', font=LARGE_FONT)
        countEntry = tk.Entry(self)
        countLabel.grid(row=1, column=1)
        countEntry.grid(row=1, column=2)
        
        # Date
        calLabel = tk.Label(self, text="Date:", font=LARGE_FONT)
        calEntry = DateEntry(self, width=16, background="grey", foreground="white", bd=2)
        calEntry.set_date(datetime.now())
        calLabel.grid(row=2, column=1)
        calEntry.grid(row=2, column=2)
        
        # Region Names
        self.dbLists['regions'] = qf.getRegions()
        self.addOM('regions', 3, 'Region')
        # self.currentValue['regions'].trace_variable('w', self.updateFaciliyList)
        
        # Facility Names
        self.dbLists['facilities'] = qf.getFacilities()
        self.addOM('facilities', 4, 'Facility Name')
        
        # Life Stages
        self.addOM('lifeStages', 5, 'Life Stage')
        
        # Taxonomic Groups
        self.dbLists['taxGroups'] = qf.getTaxGroups()
        self.addOM('taxGroups', 6, 'Taxonomic Group')
        # self.currentValue['taxGroups'].trace_variable('w', self.updateSpeciesList)

        # Species 
        self.dbLists['species'] = qf.getSpecies()
        self.addOM('species', 7, 'Species')
        
        # Life Stages
        self.addOM('type', 8, 'Distribution Type')
        
        rec = None
        recLabel = tk.Label(self, text='Recreational:',font=LARGE_FONT)
        recLabel.grid(row=9, column=1, columnspan=2)
        recButton = tk.Checkbutton(self,variable=rec, onvalue=1, offvalue=0)
        recButton.grid(row=9, column=2)
        
        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                               command= lambda: controller.show_frame(MainMenu))
        createButton = tk.Button(self, text='Create', font=LARGE_FONT,
                                command= lambda: controller.show_frame(MainMenu))
                
        cancelButton.grid(row=20,column=1)
        createButton.grid(row=20,column=3)
    
    def addOM(self, name, rowDD, label):
        newLabel = tk.Label(self, text=f'{label}:', font=LARGE_FONT)
        self.currentValue[name] = tk.StringVar(self)
        self.currentValue[name].set('Select..')
        self.menus[name] = tk.OptionMenu(self, self.currentValue[name], *self.dbLists[name])
        newLabel.grid(row=rowDD, column=1)
        self.menus[name].grid(row=rowDD, column=2, pady=5)
        self.menus[name].config(width = 14)

class SearchDistros(tk.Frame):
    
    results = []
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
        # self.currentValue['regions'].trace_variable('w', self.updateFaciliyList)
        
        # Facility Names
        self.dbLists['facilities'] = qf.getFacilities()
        self.addOM('facilities', 3, 'Facility Name')
        
        # Life Stages
        self.addOM('lifeStages', 4, 'Life Stage')
        
        # Taxonomic Groups
        self.dbLists['taxGroups'] = qf.getTaxGroups()
        self.addOM('taxGroups', 5, 'Taxonomic Group')
        # self.currentValue['taxGroups'].trace_variable('w', self.updateSpeciesList)

        # Species 
        self.dbLists['species'] = qf.getSpecies()
        self.addOM('species', 6, 'Species')
        
        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                               command= lambda: controller.show_frame(MainMenu))
        
        clearButton = tk.Button(self, text='Clear Search', font=LARGE_FONT,
                               command= lambda: self.resetLists())
        
        searchButton = tk.Button(self, text='Search', font=LARGE_FONT,
                                command= lambda: self.openResults())
        
        cancelButton.grid(row=7, column=1)
        clearButton.grid(row=7, column=2, columnspan=2)
        searchButton.grid(row=7, column=5, pady=5)
        
    def openResults(self):
        resultWin = tk.Tk()
        resultWin.columnconfigure(1, weight=1)
        resultWin.columnconfigure(1, weight=1)
        
        self.results = self.getValues()
        for disNum, distro in enumerate(self.results):
            for i in range(0,5):
                self.addDistro(resultWin, distro[i], disNum+9, i+1)
        
        titleLabel = tk.Label(resultWin, text=f'{len(self.results)} Result(s) Found', font=TITLE_FONT)
        titleLabel.grid(row=1, column=1, pady=5, columnspan=5)
        titleSep = ttk.Separator(resultWin, orient='horizontal')
        titleSep.grid(row=2, column=1, columnspan=5, sticky=tk.EW)
        for i, colTitle in enumerate(['Date', 'Count', 'Facility', 'ID', 'Species ITIS']):
            label = tk.Label(resultWin, text=f'{colTitle}', font=LARGE_FONT)
            label.grid(row=3, column=i+1, padx=10)
        colSep = ttk.Separator(resultWin, orient='horizontal')
        colSep.grid(row=8, column=1, columnspan=5, sticky=tk.EW)
        
        exportButton = tk.Button(resultWin, text='Export to CSV', font=LARGE_FONT,
                           command= lambda: self.export())
        exportButton.grid(row=100, column=3, sticky=tk.S)
            
    def export(self):
        # get file path
        dir = fd.askdirectory()
        file = '/Distro-Report'
        # handle duplicate files
        count = 1
        while(os.path.exists(dir + file + '.csv')):
            file = f'/Distro-Report({count})'
            count += 1
        # write csv
        with open(dir+file+'.csv', 'w', newline='') as csvfile:
            distroWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            distroWriter.writerow(['Date', 'Count', 'Facility', 'Distribution ID', 'Species ITIS'])
            for distro in self.results:
                distroWriter.writerow(distro)
            # alter user of created file
            tkinter.messagebox.showinfo(title='Distrobution Exporter', message=f'File Created:\n{dir}{file}.csv')
    
    def addDistro(self, win, value, r, c):
        label = tk.Label(win, text=f'{value}', font=LARGE_FONT)
        label.grid(row=r, column=c, padx=10)
    
    def getValues(self):
        filters = []
        for key in self.currentValue:
            value = self.currentValue[key].get()
            if(value != 'Any..'):
                filters.append([key,value])
        return qf.getDistros(filters)
        
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
    dbLists = {
        'facilities': [],
        'ITIS': [],
        'transferFacility': []
    }

    currentValue = {
        'calendar': None,
        'count': None,
        'facilities': None,
        'ITIS': None,
        'latitude': None,
        'longitude': None,
        'length': None,
        'weight': None,
        'tagged': None,
        'transferFacility': None
    }

    labels = {
        'calendar': None,
        'count': None,
        'facilities': None,
        'ITIS': None,
        'latitude': None,
        'longitude': None,
        'length': None,
        'weight': None,
        'tagged': None,
        'transferFacility': None
    }
    entries = {
        'calendar': None,
        'count': None,
        'facilities': None,
        'ITIS': None,
        'latitude': None,
        'longitude': None,
        'length': None,
        'weight': None,
        'tagged': None,
        'transferFacility': None
    }

    distroVals = {
        'calendar': None,
        'count': None,
        'facilities': None,
        'ITIS': None
    }

    subVals = {
        'latitude': None,
        'longitude': None,
        'length': None,
        'weight': None,
        'tagged': None,
        'transferFacility': None
    }
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        titleLabel = tk.Label(self, text='Edit Distribution', font=TITLE_FONT)
        titleLabel.grid(row=0, column=3, pady=10)

        # Date
        distroLabel = tk.Label(self, text='Distribution:', font=LARGE_FONT)
        distroEntry = tk.Entry(self)

        distroLabel.grid(row=1, column=1)
        distroEntry.grid(row=1, column=3)

        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(MainMenu))
        getButton = tk.Button(self, text='Get', font=LARGE_FONT,
                                 command=lambda: [self.emptyFrame(), self.editDistro(distroEntry.get())])

        cancelButton.grid(row=20, column=1, sticky='s')
        getButton.grid(row=20, column=4, sticky='s')

    def emptyFrame(self):
        for i in self.labels:
            if self.labels[i] is not None:
                self.labels[i].destroy()
                self.labels[i] = None
        for i in self.currentValue:
            self.currentValue[i] = None
        for i in self.entries:
            if self.entries[i] is not None:
                self.entries[i].destroy()
                self.entries[i] = None

    def editDistro(self, d_id):
        details = qf.getSingleDistro(d_id)
        if len(details)==0:
            tkinter.messagebox.showerror("Distribution Error", "No Distribution Match")
        else:
            # Create a Label
            self.labels['calendar'] = tk.Label(self, text="Date:", font=LARGE_FONT)
            # Create a Calendar using DateEntry
            self.entries['calendar'] = DateEntry(self, width=16, background="grey", foreground="white", bd=2)
            self.entries['calendar'].set_date(details[0][0])
            self.labels['calendar'].grid(row=3, column=1)
            self.entries['calendar'].grid(row=3, column=3)

            # count
            self.labels['count'] = tk.Label(self, text='Count:', font=LARGE_FONT)
            self.entries['count'] = tk.Entry(self)
            self.entries['count'].insert(0, details[0][1])

            self.labels['count'].grid(row=4, column=1)
            self.entries['count'].grid(row=4, column=3)

            #facility name
            self.dbLists['facilities'] = qf.getFacilities()
            self.addOM('facilities', 5, 'Facility Name')
            self.currentValue['facilities'].set(details[0][2])

            self.dbLists['ITIS'] = qf.getITIS()
            self.addOM('ITIS', 6, 'ITIS')
            self.currentValue['ITIS'].set(details[0][4])


            if(qf.isReleased(d_id)):
                releasedResult = qf.getReleased(d_id)
                self.labels['latitude'] = tk.Label(self, text='Latitude:', font=LARGE_FONT)
                self.entries['latitude'] = tk.Entry(self)
                self.entries['latitude'].insert(0, releasedResult[0][1])

                self.labels['latitude'].grid(row=7, column=1)
                self.entries['latitude'].grid(row=7, column=3)


                self.labels['longitude'] = tk.Label(self, text='Longitude:', font=LARGE_FONT)
                self.entries['longitude'] = tk.Entry(self)
                self.entries['longitude'].insert(0, releasedResult[0][2])


                self.labels['longitude'].grid(row=8, column=1)
                self.entries['longitude'].grid(row=8, column=3)
                if releasedResult[0][3] is not None:
                    self.hatch(releasedResult[0][3])
            else:
                # facility name
                transferResult = qf.getTransfer(d_id)
                self.dbLists['transferFacility'] = qf.getFacilities()
                self.addOM('transferFacility', 7, 'Transfer Facility')
                self.currentValue['transferFacility'].set(transferResult[0][1])
                if transferResult[0][2] is not None:
                    self.hatch(transferResult[0][2])

            EditButton = tk.Button(self, text='Edit', font=LARGE_FONT,
                                     command=lambda: [self.getValues(), qf.editDistro(self.distroVals, self.subVals,
                                                                                      d_id), self.clearVals()])
            EditButton.grid(row=20, column=3, sticky='s')

    def clearVals(self):
        for i in self.distroVals:
            self.distroVals[i] = None
        for i in self.subVals:
            self.subVals[i] = None
    def getValues(self):
        self.distroVals['calendar'] = self.entries['calendar'].get_date()
        self.distroVals['count']= self.entries['count'].get()
        self.distroVals['facilities'] = self.currentValue['facilities'].get()
        self.distroVals['ITIS'] = self.currentValue['ITIS'].get()

        for i in self.subVals:
            if self.entries[i] is not None:
                if i=='transferFacility':
                    self.subVals[i] = self.currentValue[i].get()
                else:
                    self.subVals[i] = self.entries[i].get()
        for i in self.distroVals:
            print(self.distroVals[i])

        for i in self.subVals:
            print(self.subVals[i])

    def hatch(self, h_id):
        hatchResult = qf.getHatch(h_id)
        print(hatchResult)
        self.labels['length'] = tk.Label(self, text='Average Length:', font=LARGE_FONT)
        self.entries['length'] = tk.Entry(self)
        self.entries['length'].insert(0, hatchResult[0][0])

        self.labels['length'].grid(row=9, column=1)
        self.entries['length'].grid(row=9, column=3)

        self.labels['weight'] = tk.Label(self, text='Average Weight:', font=LARGE_FONT)
        self.entries['weight'] = tk.Entry(self)
        self.entries['weight'].insert(0, hatchResult[0][1])

        self.labels['weight'].grid(row=10, column=1)
        self.entries['weight'].grid(row=10, column=3)

        taggedResult = qf.getTagged(h_id)
        if(len(taggedResult)!=0):
            self.labels['tagged'] = tk.Label(self, text='Percent Tagged:', font=LARGE_FONT)
            self.entries['tagged'] = tk.Entry(self)
            self.entries['tagged'].insert(0, taggedResult[0][1])

            self.labels['tagged'].grid(row=11, column=1)
            self.entries['tagged'].grid(row=11, column=3)



    def addOM(self, name, rowDD, label):
        self.labels[name] = tk.Label(self, text=f'{label}:', font=LARGE_FONT)
        self.currentValue[name] = tk.StringVar(self)
        self.currentValue[name].set('Any..')
        self.entries[name] = tk.OptionMenu(self, self.currentValue[name], *self.dbLists[name])
        self.labels[name].grid(row=rowDD, column=1)
        self.entries[name].grid(row=rowDD, column=3, pady=5)


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
                                 command=lambda: qf.duplicateDistro(distroIDEntry.get()))

        cancelButton.grid(row=9, column=1, sticky='s')
        createButton.grid(row=9, column=4, sticky='s')

class DeleteDistro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = tk.Label(self, text='Delete Distribution', font=TITLE_FONT)
        titleLabel.grid(row=0, column=3, pady=10)

        # Date
        distroIDLabel = tk.Label(self, text='Distribution ID:', font=LARGE_FONT)
        distroIDEntry = tk.Entry(self)

        distroIDLabel.grid(row=1, column=1)
        distroIDEntry.grid(row=1, column=3)

        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(MainMenu))
        deleteButton = tk.Button(self, text='Delete', font=LARGE_FONT,
                                 command=lambda: self.confirm(distroIDEntry.get()))

        cancelButton.grid(row=9, column=1, sticky='s')
        deleteButton.grid(row=9, column=4, sticky='s')

    def confirm(self, d_id):
        check = tkinter.messagebox.askyesno("Delete Distribution", "Are you sure you want to delete this distribution?")
        if check:
            qf.deleteDistro(d_id)

class AddSpecies(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = tk.Label(self, text='Add Species', font=TITLE_FONT)
        titleLabel.grid(row=0, column=3, pady=10)

        # Recreational
        recBool = tk.IntVar()
        recLabel = tk.Label(self, text='Recreational:', font=LARGE_FONT)
        recEntry = tk.Checkbutton(self,variable=recBool, onvalue=1, offvalue=0)

        recLabel.grid(row=1, column=1)
        recEntry.grid(row=1, column=3)

        # Aquatic
        aquaBool = tk.IntVar()
        aquaLabel = tk.Label(self, text='Aquatic:', font=LARGE_FONT)
        aquaEntry = tk.Checkbutton(self,variable=aquaBool, onvalue=1, offvalue=0)

        aquaLabel.grid(row=2, column=1)
        aquaEntry.grid(row=2, column=3)

        #ITIS NUMBER
        ITISLabel = tk.Label(self, text='Itis Number:', font=LARGE_FONT)
        ITISEntry = tk.Entry(self)

        ITISLabel.grid(row=3, column=1)
        ITISEntry.grid(row=3, column=3)
        #Taxonomic Group
        taxLabel = tk.Label(self, text='Taxonomic group:', font=LARGE_FONT)
        taxEntry = tk.Entry(self)

        taxLabel.grid(row=4,column=1)
        taxEntry.grid(row=4,column=3)

        # Name
        nameLabel = tk.Label(self, text='Name:', font=LARGE_FONT)
        nameEntry = tk.Entry(self)

        nameLabel.grid(row=5, column=1)
        nameEntry.grid(row=5, column=3)

        # Buttons
        cancelButton = tk.Button(self, text='Cancel', font=LARGE_FONT,
                                 command=lambda: controller.show_frame(MainMenu))

        createButton = tk.Button(self, text='Add', font=LARGE_FONT,
                                 command=lambda: qf.addSpecies(recBool.get(), aquaBool.get(), ITISEntry.get(),
                                                               taxEntry.get(), nameEntry.get()))
        cancelButton.grid(row=9, column=1, sticky='s')
        createButton.grid(row=9, column=4, sticky='s')
def main():
    app = ManageWindows()
    app.mainloop()

if (__name__ == '__main__'):
    main()