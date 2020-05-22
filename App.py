import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import math
import pymysql

connection = pymysql.connect(host="localhost",user="root",passwd="",database="bd" )
cursor = connection.cursor()

root = tk.Tk()

def_color= '#202020'
def_color2='#252525'

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading",background="#434343", foreground="white", relief="flat")
style.configure("Treeview", background="#353535", fieldbackground="#282828", foreground="white")

style.configure('TButton', font = ('Arial', 10, 'bold'))
style.configure('TMenubutton',font = ('Arial', 10, 'bold'))

style.configure('Header.Label', font=('Arial', 30, 'bold'), foreground ='#D3D3D3', background=def_color)
style.configure('Normal.Label', font=('Arial', 15), foreground ='#A8A8A8', background=def_color)

style.configure('TEntry', foreground="#D3D3D3", fieldbackground="#353535")
#style.configure('Header', font = ('Arial',30), 'bold')

def load_data(opt):
    
    cursor.execute(opt)
    rows = cursor.fetchall()
    return rows


class MainApplication(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()
     

    def switch_frame(self, frame_class, data=None):
        """Destroys current frame and replaces it with a new one."""
        print(data)
        self.create_frameR()
        new_frame = frame_class(self,data)
        if self.right_frame is not None:
            self.right_frame=None
        self.right_frame = new_frame

        self.right_frame.grid()

        

    def configure_gui(self):
        self.master.title('Bazy Danych')
        self.master.geometry('850x500')
        self.master.resizable(0, 0)
 
    def create_widgets(self):
        self.create_frameL()
        self.create_frameR()
        self.create_buttons()
 
    def create_frameL(self):
        self.left_frame = tk.Frame(width=150, height=500,background=def_color2)
        self.left_frame.grid_propagate(0)
        self.left_frame.grid(row=0, column=0)
        self.left_frame.columnconfigure(0,weight=1)

    def create_frameR(self):
        self.right_frame = tk.Frame(width=700, height=500, background=def_color)
        self.right_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=1)   
        self.right_frame.columnconfigure(0,weight=1)

    def create_buttons(self):
        self.create_left_frame_buttons()
        self.create_right_frame()       
 
    def create_left_frame_buttons(self):
        Button(self.left_frame,style = 'TButton', text="Albumy",    command=lambda:self.switch_frame(AlbumsPage))   .grid(row=0, sticky=N+S+E+W,padx=10, pady=(50,5))
        Button(self.left_frame,style = 'TButton', text="Wykonawcy", command=lambda:self.switch_frame(PerformerPage)).grid(row=1, sticky=N+S+E+W,padx=10, pady=5)
        Button(self.left_frame,style = 'TButton', text="Edycja", command=lambda:self.switch_frame(EditPage)).grid(row=2, sticky=N+S+E+W,padx=10, pady=5)
    def create_right_frame(self):
        self.switch_frame(StartPage)
    
    def clear_input(self):
        self.right_frame.destroy()
        self.right_frame = tk.Frame(width=700, height=500, background=def_color)
        self.right_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=1)   
        self.right_frame.columnconfigure(0,weight=1)

class StartPage(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.load_stuff()

    def load_stuff(self):
        x=Label(self.frame,style="Header.Label", text="Strona Startowa")
        x.grid(row=0, sticky=N)
        
class AlbumsPage(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.load_stuff()

    def load_stuff(self):
        Button(self.frame, style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=3, sticky=S, pady=30)
        
        rows=load_data('Select albumy.ida, albumy.nazwa, zespol.nazwa, albumy.data from albumy JOIN wydanie on ida=album_id JOIN zespol WHERE idz=wykonawca_id UNION SELECT albumy.ida, albumy.nazwa,CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname, albumy.data from albumy JOIN wydanie on ida=album_id JOIN muzyk WHERE idm=wykonawca_id')

        Label(self.frame, style="Header.Label", text="Albumy").grid(row=0, sticky=N)
        
        cols = ('Id', 'Nazwa', 'Wykonawca', 'Data wydania')
        self.listBox = Treeview(self.frame, columns=cols, show='headings', )


        self.listBox.column("Id",minwidth=0,width=50, stretch=NO)
        self.listBox.column("Data wydania",minwidth=0,width=100,stretch=NO)
        for col in cols:
           self.listBox.heading(col, text=col)  
        self.listBox.grid(row=0, sticky=N+S, pady=50)
    
        for (ida, nazwa, wykonawca, data) in rows:
           self.listBox.insert("", "end", values=(ida, nazwa, wykonawca, data))
        self.selected = []
        self.detail = Button(self.frame,style = 'TButton', text="Details",  command=lambda: self.master.switch_frame(AlbumDetails,self.listBox.item(self.listBox.selection())['values'][0])).grid(row=2)

class AlbumDetails(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.actual_id=str(data)

        self.load_stuff()

    def load_stuff(self):
        Button(self.frame, style = 'TButton', text="Return to start page", command=lambda: self.master.switch_frame(StartPage)).grid(row=3, sticky=S, pady=30)

        rows=load_data('SELECT utwor_album.numer, utwory.nazwa, utwory.dlugosc, utwory.ocena FROM utwory JOIN utwor_album ON idu=u_id JOIN albumy ON ida=a_id WHERE a_id='+self.actual_id+';')
        
        Label(self.frame, style="Header.Label", text="Szczegóły").grid(row=0, sticky=N)

        # create Treeview with 3 columns
        cols = ('Numer', 'Nazwa', 'Dlugosc', 'Ocena')
        self.listBox = Treeview(self.frame, columns=cols, show='headings')


        self.listBox.column("Numer",minwidth=0,width=50, stretch=NO)
        self.listBox.column("Dlugosc",minwidth=0,width=100,stretch=NO)
        self.listBox.column("Ocena",minwidth=0,width=50,stretch=NO)
        for col in cols:
           self.listBox.heading(col, text=col)  
        self.listBox.grid(row=0, sticky=N+S, pady=50)
    
        for (ida, nazwa, wykonawca, data) in rows:
           self.listBox.insert("", "end", values=(ida, nazwa, wykonawca, data))

        self.detail = Button(self.frame,style = 'TButton', text="Back",  command=lambda: self.master.switch_frame(AlbumsPage)).grid(row=2)

class PerformerPage(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.load_stuff()

    def load_stuff(self):
        Button(self.frame,style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=5, sticky=S, pady=30)
        
        op='SELECT zespol.idz, zespol.nazwa FROM zespol JOIN wydanie ON wykonawca_id=idz UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN wydanie ON wykonawca_id=idm'
        
        Label(self.frame, text="Wykonawcy", style="Header.Label").grid(row=0, sticky=N)
        # create Treeview with 3 columns
        
        self.load_list(op)

        z_albumem = tk.IntVar(value=1)
        bez_albumu = tk.IntVar()
  

        tk.Checkbutton(self.frame,background=def_color, text='Wykonawcy z albumami',font=("Arial",10),variable=z_albumem, onvalue=1, offvalue=0, command=self.print_selection(z_albumem,bez_albumu))  .grid(row=2,padx=10, pady=(10,5), sticky=E+W)
        tk.Checkbutton(self.frame,background=def_color, text='Wykonawcy bez albumów',font=("Arial",10),variable=bez_albumu, onvalue=1, offvalue=0, command=self.print_selection(z_albumem,bez_albumu)).grid(row=3,padx=10, pady=(5,10),sticky=E+W)
        
        self.detail = Button(self.frame,style = 'TButton', text="Pokaż",  command=lambda: self.print_selection(z_albumem,bez_albumu)).grid(row=4, padx=10, sticky=N) 
    
    def load_list(self,opt):

        if(opt!=''):
            rows=load_data(opt)
        else:
            rows=""

        cols = ('Id', 'Nazwa')
        self.listBox = Treeview(self.frame, columns=cols, show='headings')

        self.listBox.column("Id",minwidth=0,width=50, stretch=NO)

        for col in cols:
           self.listBox.heading(col, text=col)  
        self.listBox.grid(row=0, sticky=N+S, pady=50)
            
        for (ida, nazwa) in rows:
           self.listBox.insert("", "end", values=(ida, nazwa))

    def print_selection(self, z_albumem,bez_albumu):
        if (z_albumem.get() == 1) & (bez_albumu.get() == 0):
            op='SELECT zespol.idz, zespol.nazwa FROM zespol JOIN wydanie ON wykonawca_id=idz UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN wydanie ON wykonawca_id=idm'
        elif (z_albumem.get() == 0) & (bez_albumu.get() == 1):
            op='SELECT zespol.idz, zespol.nazwa FROM zespol WHERE idz NOT IN (SELECT wykonawca_id FROM wydanie) UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk WHERE idm NOT IN (SELECT wykonawca_id FROM wydanie)'
        elif (z_albumem.get() == 0) & (bez_albumu.get() == 0):
            op=''
        else:
            op='SELECT zespol.idz, zespol.nazwa FROM zespol UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk'
        
        self.load_list(op)

class EditPage(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   

        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)


        self.frame.grid_rowconfigure(10, weight=1)
        self.load_stuff()

    def load_stuff(self):
        Button(self.frame,style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=10, columnspan=4,pady=30, sticky=S)
        Label(self.frame, style="Header.Label", text="Edycja").grid(row=0, sticky=N,column=0,columnspan=4)
        
        self.OptionList = [
        "Opcje",
        "Zespół",
        "Utwór",
        "Album"
        ] 
        self.bottom = tk.Frame(self.frame,background=def_color)
        self.bottom.grid(row=1, rowspan=8, column=0, columnspan=4)
        self.option_choose = tk.StringVar(self)
        #self.option_choose.set("Opcje")

        OptionMenu(self.frame, self.option_choose, *self.OptionList,style='TMenubutton').grid(row=1,column=0,columnspan=2,sticky=E+W)

        self.ItemsList=[""]
        self.item_choose = tk.StringVar(self)
        self.item_choose.set("<--")
        
        self.opt2=OptionMenu(self.frame, self.item_choose, *self.ItemsList,style='TMenubutton')
        self.opt2.grid(row=1,column=2,columnspan=2,sticky=E+W)       
        self.option_choose.trace("w", self.callback)

    def callback(self,*args):
        for widget in self.bottom.winfo_children():
            widget.destroy()
        self.bottom.grid(row=1, rowspan=8, column=0, columnspan=4, pady=50)
        print(self.option_choose.get())
        self.opt2.grid_forget()
        op=""
        if(self.option_choose.get()=="Zespół"):
            op="SELECT idz,nazwa FROM zespol;"
        elif(self.option_choose.get()=="Utwór"):
            op="SELECT idu,nazwa FROM utwory;"
        elif(self.option_choose.get()=="Album"):
            op="SELECT ida,nazwa FROM albumy;"

        rows=load_data(op)
        self.ItemsList=[[]]
        
        for row in rows:
           self.ItemsList+=[[str(row[0]),row[1]]]
        self.item_choose = tk.StringVar(self)
        self.item_choose.set("Opcje")
        
        self.opt2=OptionMenu(self.frame, self.item_choose, *self.ItemsList,style='TMenubutton')
        self.opt2.grid(row=1,column=2,columnspan=2,sticky=E+W) 

        self.item_choose.trace("w", self.item)

    def item(self,*args):


        #zrób cos z tym przekazywaniem id bo jest zle!
        values = self.item_choose.get().split(",")
        self.idt= values[0].strip("(')")
        print(self.idt)
        print(self.option_choose.get())   
        
        op=""
        if(self.option_choose.get()=="Zespół"):
            op="SELECT * FROM zespol WHERE idz="+self.idt+";"
        elif(self.option_choose.get()=="Utwór"):
            op="SELECT * FROM utwory WHERE idu="+self.idt+";"
        elif(self.option_choose.get()=="Album"):
            op="SELECT * FROM albumy WHERE ida="+self.idt+";"

        

        Label(self.bottom,background=def_color, text="Edytujesz: "+str(load_data(op),)).grid(row=2,columnspan=4)
        Label(self.bottom,style="Normal.Label", text = 'Nazwa:').grid(row=3,column=0,sticky=E)
        self.NameInput=Entry(self.bottom)
        self.NameInput.grid(row=3,column=1,columnspan=3,sticky=E+W, padx=(25,0))
        
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=0, sticky='ew')

        if(self.option_choose.get()=="Album" or self.option_choose.get()=="Zespół"):
            Label(self.bottom,style="Normal.Label",text = 'Data (yyyy-mm-dd)').grid(row=4,column=0,sticky=E)
           
            self.rok1 = Entry(self.bottom, width=4)
            self.rok1.grid(row=4,column=1,columnspan=3,padx=(25,0),sticky=W)
            Label(self.bottom,style="Normal.Label", text='-').grid(row=4,column=1,columnspan=3,padx=(55,0),sticky=W)
            self.miesiac1 = Entry(self.bottom, width=2)
            self.miesiac1.grid(row=4,column=1,columnspan=3,padx=(70,0),sticky=W)
            Label(self.bottom,style="Normal.Label", text='-').grid(row=4,column=1,columnspan=3,padx=(90,0),sticky=W)
            self.dzien1 = Entry(self.bottom, width=2)
            self.dzien1.grid(row=4,column=1,columnspan=3,padx=(105,0),sticky=W)
    
        if(self.option_choose.get()=="Zespół"):
            Label(self.bottom, style="Normal.Label", text = 'Data rozwiazania (yyyy-mm-dd)').grid(row=5,column=0,sticky=E)
            self.rok2 = Entry(self.bottom, width=4)
            self.rok2.grid(row=5,column=1,columnspan=3,padx=(25,0),sticky=W)
            Label(self.bottom,style="Normal.Label", text='-').grid(row=5,column=1,columnspan=3,padx=(55,0),sticky=W)
            self.miesiac2 = Entry(self.bottom, width=2)
            self.miesiac2.grid(row=5,column=1,columnspan=3,padx=(70,0),sticky=W)
            Label(self.bottom, style="Normal.Label", text='-').grid(row=5,column=1,columnspan=3,padx=(90,0),sticky=W)
            self.dzien2 = Entry(self.bottom, width=2)
            self.dzien2.grid(row=5,column=1,columnspan=3,padx=(105,0),sticky=W)

        if(self.option_choose.get()=="Utwór"):
            Label(self.bottom,style="Normal.Label",text = 'Długość').grid(row=4,column=0,sticky=E)

            self.mm = Entry(self.bottom, width=4)
            self.mm.grid(row=4,column=1,columnspan=3,padx=(25,0),sticky=W)
            Label(self.bottom,style="Normal.Label", text='.').grid(row=4,column=1,columnspan=3,padx=(55,0),sticky=W)
            self.ss = Entry(self.bottom, width=2)
            self.ss.grid(row=4,column=1,columnspan=3,padx=(60,0),sticky=W)

        if(self.option_choose.get()=="Album" or self.option_choose.get()=="Utwór"):
            Label(self.bottom, style="Normal.Label", text = 'Ocena').grid(row=5,column=0,sticky=E)
            self.OcenaInput=Entry(self.bottom)
            self.OcenaInput.grid(row=5,column=1,columnspan=3,sticky=W, padx=(25,0))

        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes())
        buttonCommit.grid(row=8,column=0, columnspan=4, pady=15)
        
    def save_changes(self):
        print( self.idt)
        OK=True

        name=self.NameInput.get()

        if(not name):
            OK=False
        else:
            name="'"+name+"'"

        data=""
        data2=""
        czas=""

        if(self.option_choose.get()=="Album" or self.option_choose.get()=="Zespół"):
            if(not self.rok1.get() or not self.miesiac1.get() or int(self.miesiac1.get())<0 or int(self.miesiac1.get())>12 or not self.dzien1.get() or int(self.dzien1.get())<0 or int(self.dzien1.get())>31):
                OK=False
            else:
                data="('"+self.rok1.get()+"-"+self.miesiac1.get()+"-"+self.dzien1.get()+"')"
        if(self.option_choose.get()=="Zespół"):
            if(not self.rok2.get() or not self.miesiac2.get() or int(self.miesiac2.get())<0 or int(self.miesiac2.get())>12 or not self.dzien2.get() or int(self.dzien2.get())<0 or int(self.dzien2.get())>31):    
                data2="NULL"
            else:
                data2= "('"+self.rok2.get()+"-"+self.miesiac2.get()+"-"+self.dzien2.get()+"')"   
        
        if(self.option_choose.get()=="Utwór"):
            if(not self.mm.get() or not self.ss.get() or int(self.ss.get())<0 or int(self.ss.get())>59 or int(self.mm.get())<0):
                OK=False
            else:
                hou=str(math.floor(int(self.mm.get())/60)).zfill(2)
                min=str(int(self.mm.get())%60).zfill(2)
                
                czas="'"+str(hou)+":"+str(min)+":"+self.ss.get()+"'"  
        
        if(self.option_choose.get()=="Album" or self.option_choose.get()=="Utwór"): 
            ocena=self.OcenaInput.get()
            if(not ocena or int(ocena)>10 or int(ocena)<0):
                ocena="NULL"

        print(OK)

        if(OK):
            if(self.option_choose.get()=="Zespół"):  
                command="UPDATE zespol SET nazwa="+name+", data_utworzenia="+data+", data_rozwiazania="+data2+" WHERE idz="+self.idt+";"
            elif(self.option_choose.get()=="Utwór"):
                command="UPDATE utwory SET nazwa="+name+", dlugosc="+czas+", ocena="+ocena+" WHERE idu="+self.idt+";"
            elif(self.option_choose.get()=="Album"):
                command="UPDATE albumy SET nazwa="+name+", data="+data+", ocena="+ocena+" WHERE ida="+self.idt+";"

            print(command)
            cursor.execute(command)
            connection.commit()
            self.master.switch_frame(EditPage)


if __name__ == '__main__':
   
   main_app =  MainApplication(root)
   
   
  
   root.mainloop()
   connection.commit() 
   connection.close()