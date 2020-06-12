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

style.configure('TCheckbutton', font=('Arial', 10),foreground ='#A8A8A8', background="#353535")
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
        Button(self.left_frame,style = 'TButton', text="Wykonawcy", command=lambda:self.switch_frame(PerformersPage)).grid(row=1, sticky=N+S+E+W,padx=10, pady=5)
        Button(self.left_frame,style = 'TButton', text="Utwory", command=lambda:self.switch_frame(PiecesPage)).grid(row=2, sticky=N+S+E+W,padx=10, pady=5)
        Button(self.left_frame,style = 'TButton', text="Edycja", command=lambda:self.switch_frame(EditPage)).grid(row=3, sticky=N+S+E+W,padx=10, pady=5)
       
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
        Label(self.frame,style="Header.Label", text="Strona Startowa").grid(row=0, sticky=N)
        
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
        Button(self.frame, style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=5, sticky=S, pady=30)
        
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
        
        Button(self.frame, style = 'TButton', text="Edycja",command=lambda: self.master.switch_frame(EditPage,['Album',self.listBox.item(self.listBox.selection())['values'][0]])).grid(row=3)
        Button(self.frame, style = 'TButton', text="Usuń",command=lambda: self.delete(self.listBox.item(self.listBox.selection())['values'][0])).grid(row=4)
    
    def delete(self, idd):
        op="DELETE FROM utwor_album WHERE a_id="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        op="DELETE FROM wydanie WHERE album_id="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        op="DELETE FROM albumy WHERE ida="+str(idd)+";"
        cursor.execute(op)
        connection.commit()
        self.load_stuff()

class AlbumDetails(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1) 
        self.frame.columnconfigure(0,weight=1)
        self.frame.columnconfigure(1,weight=1)
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
        self.listBox.grid(row=0, sticky=N+S, pady=50, column=0)
    
        for (ida, nazwa, wykonawca, data) in rows:
           self.listBox.insert("", "end", values=(ida, nazwa, wykonawca, data))
        ###


        self.detail = Button(self.frame,style = 'TButton', text="Back",  command=lambda: self.master.switch_frame(AlbumsPage)).grid(row=2)

class PerformersPage(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.columnconfigure(0,weight=1)
        self.frame.columnconfigure(1,weight=1)
        
        self.load_stuff()

    def load_stuff(self):
        Button(self.frame,style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=7,columnspan=2, sticky=S, pady=30)
        
        op='SELECT zespol.idz, zespol.nazwa FROM zespol JOIN wydanie ON wykonawca_id=idz UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN wydanie ON wykonawca_id=idm'
        
        Label(self.frame, text="Wykonawcy", style="Header.Label").grid(row=0,columnspan=2, sticky=N)
        # create Treeview with 3 columns
        
        self.load_list(op)

        z_albumem = tk.IntVar(value=1)
        bez_albumu = tk.IntVar()
        uczestniczacy = tk.IntVar()

        Checkbutton(self.frame, text='Wykonawcy z albumami (przypisanymi do nich)',style='TCheckbutton',variable=z_albumem, onvalue=1, offvalue=0, command=self.print_selection(z_albumem,bez_albumu, uczestniczacy))  .grid(row=1,column=1,padx=10,stick=NW)
        Checkbutton(self.frame,text='Wykonawcy bez albumów (przypisanymi do nich)',style='TCheckbutton',variable=bez_albumu, onvalue=1, offvalue=0, command=self.print_selection(z_albumem,bez_albumu, uczestniczacy)) .grid(row=2,column=1,padx=10,stick=NW)
        Checkbutton(self.frame,text='Muzycy uczestniczący',style='TCheckbutton',variable=uczestniczacy, onvalue=1, offvalue=0, command=self.print_selection(z_albumem,bez_albumu,uczestniczacy)) .grid(row=3,column=1,padx=10,stick=NW)

        self.detail = Button(self.frame,style = 'TButton', text="Pokaż",  command=lambda: self.print_selection(z_albumem,bez_albumu, uczestniczacy)).grid(row=5, padx=10,column=1, sticky=N) 
        Button(self.frame, style = 'TButton', text="Edycja",command=lambda:self.master.switch_frame(EditPage,['Wykonawca',self.listBox.item(self.listBox.selection())['values'][0]])).grid(row=6)
        Button(self.frame,style = 'TButton', text="Details",  command=lambda: self.master.switch_frame(PerformerDetails,self.listBox.item(self.listBox.selection())['values'][0])).grid(row=5)
        Button(self.frame, style = 'TButton', text="Usuń",command=lambda: self.delete(self.listBox.item(self.listBox.selection())['values'][0])).grid(row=4)
    
    def delete(self, idd):
        op="DELETE FROM wykonawca WHERE idw="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        op="DELETE FROM zespol WHERE idz="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        op="DELETE FROM muzyk WHERE idm="+str(idd)+";"
        cursor.execute(op)
        connection.commit()
        
        self.load_stuff()

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
        self.listBox.grid(row=0, rowspan=5, sticky=N+S, pady=50)
            
        for (ida, nazwa) in rows:
           self.listBox.insert("", "end", values=(ida, nazwa))

    # do wymiany
    def print_selection(self, z_albumem,bez_albumu,uczestniczacy):
        if (z_albumem.get() == 1) & (bez_albumu.get() == 0) & (uczestniczacy.get() == 0):
            op='SELECT zespol.idz, zespol.nazwa FROM zespol JOIN wydanie ON wykonawca_id=idz UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN wydanie ON wykonawca_id=idm'
        elif (z_albumem.get() == 0) & (bez_albumu.get() == 1) & (uczestniczacy.get() == 0):
            op='SELECT zespol.idz, zespol.nazwa FROM zespol WHERE idz NOT IN (SELECT wykonawca_id FROM wydanie) UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk WHERE idm NOT IN (SELECT wykonawca_id FROM wydanie)'
        elif (z_albumem.get() == 1) & (bez_albumu.get() == 0) & (uczestniczacy.get() == 1):
            op='SELECT zespol.idz, zespol.nazwa FROM zespol JOIN wydanie ON wykonawca_id=idz UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN wydanie ON wykonawca_id=idm UNION SELECT DISTINCT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN nalezy on idm=nalezy.m_id JOIN zespol on idz=nalezy.z_id JOIN wydanie on idz=wydanie.wykonawca_id JOIN albumy on ida=wydanie.album_id WHERE (nalezy.do IS NULL OR nalezy.do>albumy.data) AND (idm IN (SELECT wykonawca_id FROM wydanie) OR idz IN (SELECT wykonawca_id FROM wydanie))'
        elif (z_albumem.get() == 0) & (bez_albumu.get() == 0) & (uczestniczacy.get() == 1):
            op='SELECT DISTINCT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk JOIN nalezy on idm=nalezy.m_id JOIN zespol on idz=nalezy.z_id JOIN wydanie on idz=wydanie.wykonawca_id JOIN albumy on ida=wydanie.album_id WHERE (nalezy.do IS NULL OR nalezy.do>albumy.data) AND (idm IN (SELECT wykonawca_id FROM wydanie) OR idz IN (SELECT wykonawca_id FROM wydanie))'
        elif (z_albumem.get() == 0) & (bez_albumu.get() == 0) & (uczestniczacy.get() == 0):
            op=''
        else:
            op='SELECT zespol.idz, zespol.nazwa FROM zespol UNION SELECT muzyk.idm, CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM muzyk'
        
        self.load_list(op)

class PerformerDetails(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(8, weight=1)
        self.frame.columnconfigure(0,weight=1)
        
        self.frame.columnconfigure(1,weight=1)

        self.actual_id=str(data)

        if(load_data('SELECT * FROM muzyk WHERE idm='+self.actual_id+';')==()):
            rows_1=load_data('SELECT idz, nazwa, data_utworzenia,data_rozwiazania FROM zespol WHERE idz='+self.actual_id+';')
            cols_1 = ('Id', 'Nazwa','Data_utworzenia', 'Data_rozwiazania')
            
            rows_2=load_data('SELECT ida,albumy.nazwa FROM albumy JOIN wydanie on album_id=ida JOIN zespol on wykonawca_id=idz WHERE idz='+self.actual_id+';')
            cols_2 = ('Id', 'Nazwa')
            
            rows_3=load_data('SELECT idu,utwory.nazwa FROM utwory JOIN utwor_album ON u_id=idu JOIN wydanie on album_id=a_id JOIN zespol on wykonawca_id=idz where idz='+self.actual_id+';')
            cols_3 = ('Id', 'Nazwa')

            rows_4=load_data('SELECT imie, nazwisko, nalezy.od, nalezy.do FROM muzyk JOIN nalezy ON idm=m_id WHERE z_id='+self.actual_id+';')
            cols_4 = ('Imie','Nazwisko', 'Od','Do')
        
            self.load_mus(2,rows_1,cols_1,rows_2,cols_2,rows_3,cols_3,rows_4,cols_4)
        
        else:
            rows_1=load_data('SELECT idm, imie, nazwisko, data_ur,data_sm,rola FROM muzyk WHERE idm='+self.actual_id+';')
            cols_1 = ('Id', 'Imie', 'Nazwisko','Data_ur', 'Data_sm','Rola')

            rows_2=load_data('SELECT ida,nazwa FROM albumy JOIN wydanie on album_id=ida JOIN muzyk on wykonawca_id=idm WHERE idm='+self.actual_id+';')
            cols_2 = ('Id', 'Nazwa')

            rows_3=load_data('SELECT idu,nazwa FROM utwory JOIN utwor_album ON u_id=idu JOIN wydanie on album_id=a_id JOIN muzyk on wykonawca_id=idm where idm='+self.actual_id+';')
            cols_3 = ('Id', 'Nazwa')

            cols_4 = ('Nazwa', 'Od','Do')
            rows_4=load_data('SELECT zespol.nazwa, nalezy.od, nalezy.do FROM muzyk JOIN nalezy on m_id=idm JOIN zespol on z_id=idz WHERE idm='+self.actual_id+';')

            self.load_mus(1,rows_1,cols_1,rows_2,cols_2,rows_3,cols_3,rows_4,cols_4)

    def load_mus(self,mode,r1,c1,r2,c2,r3,c3,r4,c4):
        Button(self.frame,style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=9, columnspan=4,pady=30, sticky=S)

        Label(self.frame, style="Header.Label", text="Szczegóły").grid(row=0,columnspan=4, sticky=N)

        da = Treeview(self.frame, columns=c1, show='headings')
        for col in c1:
           da.heading(col, text=col)  
        da.column("Id",minwidth=0,width=50, stretch=NO)

        if(mode==1):
            da.column("Data_ur",minwidth=0,width=75, stretch=NO)
            da.column("Data_sm",minwidth=0,width=75, stretch=NO)
            da.column("Rola",minwidth=0, width=100,stretch=NO)

            for (ida, imie, nazwisko,d1,d2,r) in r1:
               da.insert("", "end", values=(ida, imie, nazwisko,d1,d2,r))
        elif(mode==2):
            da.column("Data_utworzenia",minwidth=0,width=75, stretch=NO)
            da.column("Data_rozwiazania",minwidth=0,width=75, stretch=NO)
            for (idz, nazwa,d1,d2) in r1:
               da.insert("", "end", values=(idz,nazwa,d1,d2))
        da.grid(row=1,columnspan=2, sticky=N+S+E+W)

        listAl = Treeview(self.frame, columns=c2, show='headings')
        listAl.column("Id",minwidth=0,width=50, stretch=FALSE)

        for col in c2:
           listAl.heading(col, text=col)  

        for (ida, nazwa) in r2:
           listAl.insert("", "end", values=(ida, nazwa))

        Label(self.frame, style="Normal.Label", text="Albumy").grid(row=3, sticky=S)   
        listAl.grid(row=4, sticky=N)
        
        #6
        xx = Treeview(self.frame, columns=c3, show='headings')
        xx.column("Id",minwidth=0,width=50, stretch=TRUE)

        for col in c3:
           xx.heading(col, text=col)

        Label(self.frame, style="Normal.Label", text="Utwory").grid(row=3,column=1, sticky=S)
        xx.grid(row=4,column=1, sticky=N)

        for (ida, nazwa) in r3:
           xx.insert("", "end", values=(ida, nazwa))

        if(mode==1):
            da = Treeview(self.frame, columns=c4, show='headings')

            for col in c4:
               da.heading(col, text=col) 
            da.column("Od",minwidth=0,width=75, stretch=NO)
            da.column("Do",minwidth=0,width=75, stretch=NO)

            for (nazwa,d1,d2) in r4:
               da.insert("", "end", values=(nazwa,d1,d2))
            Label(self.frame, style="Normal.Label", text="Zespoły").grid(row=7,columnspan=3, sticky=S)
            
        elif(mode==2):
            da = Treeview(self.frame, columns=c4, show='headings')

            for col in c4:
                da.heading(col, text=col) 
            da.column("Od",minwidth=0,width=75, stretch=NO)
            da.column("Do",minwidth=0,width=75, stretch=NO) 
            for (imie,nazwisko,d1,d2) in r4:
               da.insert("", "end", values=(imie,nazwisko,d1,d2))
            Label(self.frame, style="Normal.Label", text="Członkowie").grid(row=7,columnspan=3, sticky=S)
        da.grid(row=8,columnspan=3, sticky=N+S+E+W)

class PiecesPage(tk.Frame):
    def __init__(self, master,data=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(width=700, height=500, background=def_color)
        self.frame.grid_propagate(0)
        self.frame.grid(row=0, column=1)   
        self.frame.columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.load_stuff()

    def load_stuff(self):
        Button(self.frame, style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=6, sticky=S, pady=30)
        
        rows=load_data('SELECT utwory.*, utwor_album.numer, albumy.nazwa, zespol.nazwa FROM utwory JOIN utwor_album ON u_id=idu JOIN albumy on a_id=ida JOIN wydanie on ida=album_id JOIN zespol WHERE idz=wykonawca_id UNION SELECT utwory.*, utwor_album.numer, albumy.nazwa,CONCAT(muzyk.imie," ",muzyk.nazwisko) fullname FROM utwory JOIN utwor_album ON u_id=idu JOIN albumy on a_id=ida JOIN wydanie on ida=album_id JOIN muzyk WHERE idm=wykonawca_id')

        Label(self.frame, style="Header.Label", text="Utwory").grid(row=0, sticky=N)
        
        cols = ('Id', 'Nazwa', 'Czas', 'Ocena','Nr','Album','Wykonawca')
        self.listBox = Treeview(self.frame, columns=cols, show='headings', )


        self.listBox.column("Id",minwidth=0,width=50, stretch=NO)
        self.listBox.column("Ocena",minwidth=0,width=45,stretch=NO)
        self.listBox.column("Czas",minwidth=0,width=45, stretch=NO)
        self.listBox.column("Nr",minwidth=0,width=30, stretch=NO)
        self.listBox.column("Album",minwidth=0,width=100, stretch=NO)
        self.listBox.column("Wykonawca",minwidth=0,width=100, stretch=NO)
        for col in cols:
           self.listBox.heading(col, text=col)  
        self.listBox.grid(row=0, sticky=N+S, pady=50)
    
        for (Id, Nazwa, Długość, Ocena,Nr,Album,Wykonawca) in rows:
           self.listBox.insert("", "end", values=(Id, Nazwa, Długość, Ocena,Nr,Album,Wykonawca))
        self.selected = []

        Button(self.frame, style = 'TButton', text="Edycja",command=lambda: self.master.switch_frame(EditPage,['Utwór',self.listBox.item(self.listBox.selection())['values'][0]])).grid(row=3)
        Button(self.frame, style = 'TButton', text="Usuń",command=lambda: self.delete(self.listBox.item(self.listBox.selection())['values'][0])).grid(row=4)
    
    def delete(self, idd):
        op="DELETE FROM utwor_album WHERE u_id="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        op="DELETE FROM utwory WHERE idu="+str(idd)+";"
        cursor.execute(op)
        connection.commit()
        self.load_stuff()

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

        # Create a frame for the self.CANV with non-zero row&column weights
        self.Fr = tk.Frame( self.frame)
        self.Fr.grid(row=2, column=0,columnspan=4, pady=(5, 0), sticky='nesw')
        self.Fr.grid_rowconfigure(0, weight=1)
        self.Fr.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.Fr.grid_propagate(False)
        # Add a self.CANV in that frame
        self.CANV = tk.Canvas(self.Fr, bg=def_color)
        self.CANV.grid(row=0, column=0,columnspan=4, sticky="news")
        # Link a scrollbar to the self.CANV
        vsb = tk.Scrollbar(self.Fr, orient="vertical", command=self.CANV.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.CANV.configure(yscrollcommand=vsb.set)
        # Create a frame to contain the buttons
        self.bottom = tk.Frame(self.CANV, bg=def_color)
        self.CANV.create_window((0, 0), window=self.bottom, anchor='center')
    
        self.bottom.update_idletasks()
        self.CANV.config(scrollregion=self.CANV.bbox("all"))
        self.Fr.config(width=700, height=300)
        
        #self.bottom = tk.Frame(self.frame,background=def_color)
        #self.bottom.grid(row=2, rowspan=8, column=0, columnspan=4)

        self.option_choose = tk.StringVar(self)
        self.ido=-1

        Button(self.frame, style = 'TButton', text="Return to start page",command=lambda: self.master.switch_frame(StartPage)).grid(row=100, columnspan=4,pady=30, sticky=S)
        Label(self.frame, style="Header.Label", text="Edycja").grid(row=0, sticky=N,column=0,columnspan=4)

        if(data is None):
            self.load_stuff()
        else:
            self.actual_id=str(data[1])
            self.option_choose.set(data[0])

            print("ID: "+self.actual_id)
            self.ido=int(self.actual_id)
            print("NAZWA: "+self.option_choose.get())

            if(self.option_choose.get()=="Wykonawca"):
                opt="SELECT * FROM muzyk WHERE idm="+self.actual_id+";"
                cursor.execute(opt)

                if not cursor.rowcount:
                    self.option_choose.set("Zespół")
                else:
                    self.option_choose.set("Muzyk")

            self.item()
        
    def load_stuff(self):
        
        
        self.OptionList = [
        "Opcje",
        "Zespół",
        "Muzyk",
        "Utwór",
        "Album"
        ] 
       

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
        self.bottom = tk.Frame(self.CANV, bg=def_color)
        self.bottom.grid(sticky="news",columnspan=10)
        self.CANV.create_window((0, 0), window=self.bottom, anchor='nw')
        # Add 9-by-5 buttons to the frame
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
  
        # Set the self.CANV scrolling region
        self.bottom.update_idletasks()
        self.CANV.config(scrollregion=self.CANV.bbox("all"))
        self.Fr.config(width=700, height=300)

        print(self.option_choose.get())
        self.opt2.grid_forget()
        op=""
        if(self.option_choose.get()=="Zespół"):
            op="SELECT idz,nazwa FROM zespol;"
        elif(self.option_choose.get()=="Muzyk"):
            op="SELECT idm, nazwisko FROM muzyk;"
        elif(self.option_choose.get()=="Utwór"):
            op="SELECT idu,nazwa FROM utwory;"
        elif(self.option_choose.get()=="Album"):
            op="SELECT ida,nazwa FROM albumy;"

        orows=load_data(op)
        self.OList={-1:"---",-2:"Dodaj"}
            
        for (ida, nazwa) in orows:
            self.OList[ida]=nazwa
            
        print(self.OList)

        self.opt_choose = tk.StringVar(self)
        
        self.opt=OptionMenu(self.frame, self.opt_choose, *self.OList.values(),style='TMenubutton', command=lambda _:self.change_option1(self.opt_choose))
        self.opt.grid(row=1,column=2,columnspan=2,sticky=E+W)        
    
    def change_option1(self, arg):

        print('     args:', arg)
        print('var.get():', self.opt_choose.get() )
        self.ido = list(self.OList.keys())[list(self.OList.values()).index(self.opt_choose.get())]
        self.actual_id=str(self.ido)
        print("Act_id ", self.actual_id)
        self.item()

    def album_edit(self):

        #---------- NAZWA ----------
        Label(self.bottom,style="Normal.Label", text = 'Nazwa:').grid(row=3,column=0,sticky=E)
        self.NameInput=Entry(self.bottom)
        self.NameInput.grid(row=3,column=1,columnspan=3,sticky=E+W, padx=(25,0),pady=10)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=3, sticky='sew')
        
        #---------- DATA WYDANIA ----------
        Label(self.bottom,style="Normal.Label",text = 'Data (yyyy-mm-dd)').grid(row=4,column=0,sticky=E,pady=10)
        self.rok1 = Entry(self.bottom, width=4)
        self.rok1.grid(row=4,column=1,columnspan=3,padx=(25,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='-').grid(row=4,column=1,columnspan=3,padx=(55,0),sticky=W)
        self.miesiac1 = Entry(self.bottom, width=2)
        self.miesiac1.grid(row=4,column=1,columnspan=3,padx=(70,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='-').grid(row=4,column=1,columnspan=3,padx=(90,0),sticky=W)
        self.dzien1 = Entry(self.bottom, width=2)
        self.dzien1.grid(row=4,column=1,columnspan=3,padx=(105,0),sticky=W)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=4, sticky='sew')

        #---------- OCENA ----------
        Label(self.bottom, style="Normal.Label", text = 'Ocena').grid(row=5,column=0,sticky=E,pady=10)
        self.OcenaInput=Entry(self.bottom)
        self.OcenaInput.grid(row=5,column=1,columnspan=3,sticky=W, padx=(25,0))
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=5, sticky='sew')

        #---------- PRZYPISANIE DO ZESPOŁU ----------
        Button(self.bottom, style = 'TButton', text="Przypisz do zespołu",command=lambda: self.multichoice_album()).grid(row=6, columnspan=4,pady=30, sticky=S)
        
        #---------- WYPEŁNIENIE PÓL (jeśli edytujemy) ----------
        if(int(self.idt)>0):
            self.NameInput.insert(END, load_data("SELECT nazwa from albumy WHERE ida="+self.idt+";")[0][0])       
            self.rok1.insert(END, load_data("SELECT YEAR(data) from albumy WHERE ida="+self.idt+";")[0][0])
            self.miesiac1.insert(END, load_data("SELECT MONTH(data) from albumy WHERE ida="+self.idt+";")[0][0])
            self.dzien1.insert(END, load_data("SELECT DAY(data) from albumy WHERE ida="+self.idt+";")[0][0])

            if(load_data("SELECT ocena FROM albumy WHERE ida="+self.idt+";")[0][0] is None):
                self.OcenaInput.insert(END, "")
            else:
                self.OcenaInput.insert(END, load_data("SELECT ocena FROM albumy WHERE ida="+self.idt+";")[0][0])


        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes())
        buttonCommit.grid(row=100,column=0, columnspan=4, pady=15) 

    def multichoice_album(self):
        for widget in self.bottom.winfo_children():
            widget.destroy()
        self.bottom = tk.Frame(self.CANV, bg=def_color)
        self.bottom.grid(sticky="news",columnspan=10)
        self.CANV.create_window((0, 0), window=self.bottom, anchor='nw')
        # Add 9-by-5 buttons to the frame
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
  
        # Set the self.CANV scrolling region
        self.bottom.update_idletasks()
        self.CANV.config(scrollregion=self.CANV.bbox("all"))
        self.Fr.config(width=700, height=300)

        col=['Id',"Nazwa"]
        self.assigned = Treeview(self.bottom, columns=col, show='headings')
        self.assigned.column("Id",minwidth=0,width=50, stretch=TRUE)

        for c in col:
           self.assigned.heading(c, text=c)

        Label(self.bottom, style="Normal.Label", text = 'Aktualni wykonawcy').grid(row=1,columnspan=4,sticky=E+W,pady=10) 
        self.assigned.grid(row=2,columnspan=4)

        r=load_data('SELECT idz,nazwa FROM zespol JOIN wydanie ON wykonawca_id=idz where album_id='+self.actual_id+';')
        for (ida, nazwa) in r:
           self.assigned.insert("", "end", values=(ida, nazwa))
         
        self.idze=-1
        self.r=2
        self.choosen=[]
        self.x('a',self.r)
        Button(self.bottom, style = 'TButton', text="Usuń",command=lambda: self.delete_wydanie(self.assigned.item(self.assigned.selection())['values'][0])).grid(row=2,column=4,padx=10) 
        Button(self.bottom,style = 'TButton',text="+",command=lambda: self.x('a',self.r)).grid(row=2,column=5,padx=10,sticky=E+S) 
        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes_assign())
        buttonCommit.grid(row=1,column=0, columnspan=4, pady=15, sticky=E+W) 
    
    def multichoice_piece(self):
        for widget in self.bottom.winfo_children():
            widget.destroy()
        self.bottom = tk.Frame(self.CANV, bg=def_color)
        self.bottom.grid(sticky="news",columnspan=10)
        self.CANV.create_window((0, 0), window=self.bottom, anchor='nw')
        # Add 9-by-5 buttons to the frame
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
  
        # Set the self.CANV scrolling region
        self.bottom.update_idletasks()
        self.CANV.config(scrollregion=self.CANV.bbox("all"))
        self.Fr.config(width=700, height=300)

        col=['Id',"Nazwa"]
        self.assigned = Treeview(self.bottom, columns=col, show='headings')
        self.assigned.column("Id",minwidth=0,width=50, stretch=TRUE)

        for c in col:
           self.assigned.heading(c, text=c)

        Label(self.bottom, style="Normal.Label", text = 'Aktualne albumy').grid(row=1,columnspan=4,sticky=E+W,pady=10) 
        self.assigned.grid(row=2,columnspan=4)

        r=load_data('SELECT ida,nazwa FROM albumy JOIN utwor_album on a_id=ida where u_id='+self.actual_id+';')
        for (ida, nazwa) in r:
           self.assigned.insert("", "end", values=(ida, nazwa))
         
        self.idze=-1
        self.r=2
        self.choosen=[]
        self.x('u',self.r)
        Button(self.bottom, style = 'TButton', text="Usuń",command=lambda: self.delete_utworalbum(self.assigned.item(self.assigned.selection())['values'][0])).grid(row=2,column=4,padx=10) 
        Button(self.bottom,style = 'TButton',text="+",command=lambda: self.x('u',self.r)).grid(row=2,column=5,padx=10,sticky=E+S) 
        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes_assign_piece())
        buttonCommit.grid(row=1,column=0, columnspan=4, pady=15, sticky=E+W) 

    def save_changes_assign(self):

        print(self.choosen)
            
        for ids in self.choosen:
            command="INSERT INTO wydanie(wydanie.album_id,wydanie.wykonawca_id) VALUES("+str(self.idt)+","+str(ids)+");"
            print(command)
            cursor.execute(command) 
            connection.commit()
        self.multichoice_album()

    def save_changes_assign_piece(self):
        print(self.choosen)

        numbers=self.get_frame_inputs(self.bottom)
        print(numbers)
        for i in range(len(self.choosen)):
            
            if(numbers[i]!=''):
                command="INSERT INTO utwor_album(a_id,u_id,numer) VALUES("+ str(self.choosen[i])+ ","+ str(self.idt) +"," + str(numbers[i]) +");"
                print(command)
                cursor.execute(command) 
                connection.commit()
        self.multichoice_piece()
        

    def piece_edit(self):

        #---------- NAZWA ----------
        Label(self.bottom,style="Normal.Label", text = 'Nazwa:').grid(row=3,column=0,sticky=E)
        self.NameInput=Entry(self.bottom)
        self.NameInput.grid(row=3,column=1,columnspan=3,sticky=E+W, padx=(25,0),pady=10)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=3, sticky='sew')

        #---------- DŁUGOŚĆ ----------
        Label(self.bottom,style="Normal.Label",text = 'Długość').grid(row=4,column=0,sticky=E,pady=10)
        self.mm = Entry(self.bottom, width=4)
        self.mm.grid(row=4,column=1,columnspan=3,padx=(25,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='.').grid(row=4,column=1,columnspan=3,padx=(55,0),sticky=W)
        self.ss = Entry(self.bottom, width=2)
        self.ss.grid(row=4,column=1,columnspan=3,padx=(60,0),sticky=W)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=4, sticky='sew')

        #---------- OCENA ----------
        Label(self.bottom, style="Normal.Label", text = 'Ocena').grid(row=5,column=0,sticky=E,pady=10)
        self.OcenaInput=Entry(self.bottom)    
        self.OcenaInput.grid(row=5,column=1,columnspan=3,sticky=W, padx=(25,0))
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=5, sticky='sew')

        #---------- PRZYPISANIE DO ALBUMU ----------
        Button(self.bottom, style = 'TButton', text="Przypisz do albumu",command=lambda: self.multichoice_piece()).grid(row=6, columnspan=4,pady=30, sticky=S)
        
        #---------- WYPEŁNIENIE PÓL (jeśli edytujemy) ----------
        if(int(self.idt)>0):
            self.NameInput.insert(END, load_data("SELECT nazwa from utwory WHERE idu="+self.idt+";")[0][0])
            self.mm.insert(END, load_data("SELECT MINUTE(dlugosc) FROM utwory WHERE idu="+self.idt+";")[0][0])
            self.ss.insert(END, load_data("SELECT SECOND(dlugosc) FROM utwory WHERE idu="+self.idt+";")[0][0])

            if(load_data("SELECT ocena FROM utwory WHERE idu="+self.idt+";")[0][0] is None):
                self.OcenaInput.insert(END, "")
            else:
                self.OcenaInput.insert(END, load_data("SELECT ocena FROM utwory WHERE idu="+self.idt+";")[0][0])
        
        
        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes())
        buttonCommit.grid(row=10,column=0, columnspan=4, pady=15)
   
    def performer_edit_m(self):
        print("XSXSXS: ",self.idt)
        
        #---------- IMIE ----------
        Label(self.bottom,style="Normal.Label", text = 'Imię:').grid(row=3,column=0,sticky=E)
        self.NameInputM=Entry(self.bottom)
        self.NameInputM.grid(row=3,column=1,columnspan=3,sticky=E+W, padx=(25,0),pady=10)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=3, sticky='sew')
    
        #---------- NAZWISKO ----------
        Label(self.bottom,style="Normal.Label", text = 'Nazwisko:').grid(row=4,column=0,sticky=E)
        self.SurnameInputM=Entry(self.bottom)
        self.SurnameInputM.grid(row=4,column=1,columnspan=3,sticky=E+W, padx=(25,0),pady=10)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=3, sticky='sew')
        
        #---------- DATA URODZENIA ----------
        Label(self.bottom,style="Normal.Label",text = 'Data ur (yyyy-mm-dd)').grid(row=5,column=0,sticky=E,pady=10)
        self.rok1 = Entry(self.bottom, width=4)
        self.rok1.grid(row=5,column=1,columnspan=3,padx=(25,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='-').grid(row=5,column=1,columnspan=3,padx=(55,0),sticky=W)
        self.miesiac1 = Entry(self.bottom, width=2)
        self.miesiac1.grid(row=5,column=1,columnspan=3,padx=(70,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='-').grid(row=5,column=1,columnspan=3,padx=(90,0),sticky=W)
        self.dzien1 = Entry(self.bottom, width=2)
        self.dzien1.grid(row=5,column=1,columnspan=3,padx=(105,0),sticky=W)    
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=5, sticky='sew')
        
        #---------- DATA ŚMIERCI ----------
        Label(self.bottom,style="Normal.Label",text = 'Data śm (yyyy-mm-dd)').grid(row=6,column=0,sticky=E,pady=10)
        self.rok2 = Entry(self.bottom, width=4)
        self.rok2.grid(row=6,column=1,columnspan=3,padx=(25,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='-').grid(row=6,column=1,columnspan=3,padx=(55,0),sticky=W)
        self.miesiac2 = Entry(self.bottom, width=2)
        self.miesiac2.grid(row=6,column=1,columnspan=3,padx=(70,0),sticky=W)
        Label(self.bottom,style="Normal.Label", text='-').grid(row=6,column=1,columnspan=3,padx=(90,0),sticky=W)
        self.dzien2 = Entry(self.bottom, width=2)
        self.dzien2.grid(row=6,column=1,columnspan=3,padx=(105,0),sticky=W)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=6, sticky='sew')
        
        #---------- ROLA ----------
        Label(self.bottom,style="Normal.Label", text = 'Rola:').grid(row=7,column=0,sticky=E)
        self.RoleInput=Entry(self.bottom)
        self.RoleInput.grid(row=7,column=1,columnspan=3,sticky=E+W, padx=(25,0),pady=10)
    

        #---------- WYPEŁNIENIE PÓL (jeśli edytujemy) ----------
        if(int(self.idt)>0):
            self.NameInputM.insert(END, load_data("SELECT imie FROM muzyk WHERE idm="+self.idt+";")[0][0])
            self.SurnameInputM.insert(END, load_data("SELECT nazwisko FROM muzyk WHERE idm="+self.idt+";")[0][0])
            self.rok1.insert(END, load_data("SELECT YEAR(data_ur) from muzyk WHERE idm="+self.idt+";")[0][0])
            self.miesiac1.insert(END, load_data("SELECT MONTH(data_ur) from muzyk WHERE idm="+self.idt+";")[0][0])
            self.dzien1.insert(END, load_data("SELECT DAY(data_ur) from muzyk WHERE idm="+self.idt+";")[0][0])
            

            if(load_data("SELECT data_sm FROM muzyk WHERE idm="+self.idt+";")[0][0] is None):
                self.rok2.insert(END, "")
                self.miesiac2.insert(END, "")
                self.dzien2.insert(END, "")
            else:
                self.rok2.insert(END, load_data("SELECT YEAR(data_sm) from muzyk WHERE idm="+self.idt+";")[0][0])
                self.miesiac2.insert(END, load_data("SELECT MONTH(data_sm) from muzyk WHERE idm="+self.idt+";")[0][0])
                self.dzien2.insert(END, load_data("SELECT DAY(data_sm) from muzyk WHERE idm="+self.idt+";")[0][0])

            self.RoleInput.insert(END,load_data("SELECT rola FROM muzyk WHERE idm="+self.idt+";"))

        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes())
        buttonCommit.grid(row=10,column=0, columnspan=4, pady=15)

    def performer_edit_b(self): 
        Label(self.bottom,style="Normal.Label", text = 'Nazwa:').grid(row=3,column=0,sticky=E)
        self.NameInput=Entry(self.bottom)
        self.NameInput.grid(row=3,column=1,columnspan=3,sticky=E+W, padx=(25,0),pady=10)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=3, sticky='sew')
        
        Label(self.bottom,style="Normal.Label",text = 'Data (yyyy-mm-dd)').grid(row=4,column=0,sticky=E,pady=10)
        self.rok1 = Entry(self.bottom, width=4)
        self.rok1.grid(row=4,column=1,columnspan=3,padx=(25,0),sticky=W)
        
        Label(self.bottom,style="Normal.Label", text='-').grid(row=4,column=1,columnspan=3,padx=(55,0),sticky=W)
        self.miesiac1 = Entry(self.bottom, width=2)
        self.miesiac1.grid(row=4,column=1,columnspan=3,padx=(70,0),sticky=W)
        
        Label(self.bottom,style="Normal.Label", text='-').grid(row=4,column=1,columnspan=3,padx=(90,0),sticky=W)
        self.dzien1 = Entry(self.bottom, width=2)
        self.dzien1.grid(row=4,column=1,columnspan=3,padx=(105,0),sticky=W)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=4, sticky='sew')
        
        

        Label(self.bottom, style="Normal.Label", text = 'Data rozwiazania (yyyy-mm-dd)').grid(row=5,column=0,sticky=E,pady=10)
        self.rok2 = Entry(self.bottom, width=4)
        
        self.rok2.grid(row=5,column=1,columnspan=3,padx=(25,0),sticky=W)
        
        Label(self.bottom,style="Normal.Label", text='-').grid(row=5,column=1,columnspan=3,padx=(55,0),sticky=W)
        self.miesiac2 = Entry(self.bottom, width=2)
        
        self.miesiac2.grid(row=5,column=1,columnspan=3,padx=(70,0),sticky=W)
        
        Label(self.bottom, style="Normal.Label", text='-').grid(row=5,column=1,columnspan=3,padx=(90,0),sticky=W)
        self.dzien2 = Entry(self.bottom, width=2)
        
        self.dzien2.grid(row=5,column=1,columnspan=3,padx=(105,0),sticky=W)
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=5, sticky='sew')
        
        #---------- WYPEŁNIENIE PÓL (jeśli edytujemy) ----------
        if(int(self.idt)>0):
            self.NameInput.insert(END, load_data("SELECT nazwa FROM zespol WHERE idz="+self.idt+";")[0][0])
            self.rok1.insert(END, load_data("SELECT YEAR(data_utworzenia) FROM zespol WHERE idz="+self.idt+";"))
            self.miesiac1.insert(END, load_data("SELECT MONTH(data_utworzenia) FROM zespol WHERE idz="+self.idt+";"))
            self.dzien1.insert(END, load_data("SELECT DAY(data_utworzenia) FROM zespol WHERE idz="+self.idt+";"))

            if(load_data("SELECT data_rozwiazania FROM zespol WHERE idz="+self.idt+";")[0][0] is None):
                self.rok2.insert(END, "")
                self.miesiac2.insert(END, "")
                self.dzien2.insert(END, "")
            else:
                self.rok2.insert(END, load_data("SELECT YEAR(data_rozwiazania) from zespol WHERE idz="+self.idt+";")[0][0])
                self.miesiac2.insert(END, load_data("SELECT MONTH(data_rozwiazania) from zespol WHERE idz="+self.idt+";")[0][0])
                self.dzien2.insert(END, load_data("SELECT DAY(data_rozwiazania) from zespol WHERE idz="+self.idt+";")[0][0])    

        buttonCommit=Button(self.bottom,style = 'TButton',text="Commit", command=lambda: self.save_changes())
        buttonCommit.grid(row=10,column=0, columnspan=4, pady=15)
        
    def item(self,*args):
        print("=>", end="")
        print(self.option_choose.get())

        if(self.ido!=-1):
            self.idt= str(self.ido)
        else:
            self.idt= str(self.actual_id)

        for widget in self.bottom.winfo_children():
            widget.destroy()
        self.bottom = tk.Frame(self.CANV, bg=def_color)
        self.bottom.grid(sticky="news",columnspan=10)
        self.CANV.create_window((0, 0), window=self.bottom, anchor='nw')
        # Add 9-by-5 buttons to the frame
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
  
        # Set the self.CANV scrolling region
        self.bottom.update_idletasks()
        self.CANV.config(scrollregion=self.CANV.bbox("all"))
        self.Fr.config(width=700, height=300)


        if(self.option_choose.get()=="Zespół"):
            self.performer_edit_b()
        elif(self.option_choose.get()=="Muzyk"):
            self.performer_edit_m()
        elif(self.option_choose.get()=="Utwór"):
            self.piece_edit()
        elif(self.option_choose.get()=="Album"):
            self.album_edit()

    def delete_wydanie(self, idd):
        op="DELETE FROM wydanie WHERE wykonawca_id="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        self.multichoice_album()
    def delete_utworalbum(self, idd):
        op="DELETE FROM utwor_album WHERE a_id="+str(idd)+";"
        cursor.execute(op)
        connection.commit()

        self.multichoice_piece()

    def get_frame_inputs(self,frame):
        inputs = [frame.children[x].get() for x in frame.children if 'entry' in x]
        return inputs

    #drop menu chooser function
    def x(self,op,r):
        if(op=='a'):
            z_op="SELECT idz,nazwa FROM zespol;"
        elif(op=='u'):
            z_op="SELECT ida,nazwa FROM albumy;"

        zrows=load_data(z_op)
        self.ZList={-1:"---"}
        
        for (ida, nazwa) in zrows:
            self.ZList[ida]=nazwa
        
        self.itemz_choose = tk.StringVar(self)
        self.optZ=OptionMenu(self.bottom, self.itemz_choose, *self.ZList.values(),style='TMenubutton', command=lambda _:self.change_option(op,self.itemz_choose))
        self.optZ.grid(row=r,column=4,sticky=W+S, padx=50)
        
        if(op=='u'):
            self.nr = Entry(self.bottom, width=4)
            self.nr.grid(row=r,column=4,padx=10, sticky=W+S)
        
        self.r+=1
        Separator(self.bottom, orient=HORIZONTAL).grid(column=0,columnspan=4, row=r, sticky='sew')
        self.bottom.update_idletasks()
        self.CANV.config(scrollregion=self.CANV.bbox("all"))
        self.Fr.config(width=700, height=300)

    def change_option(self,op, arg):

        print('     args:', arg)
        print('var.get():', self.itemz_choose.get() )

        self.idze = list(self.ZList.keys())[list(self.ZList.values()).index(self.itemz_choose.get())]
        
        self.choosen.append(self.idze)

    def save_changes(self):
        print( self.idt)

        OK=True

        

     
        name=""
        
        if(self.option_choose.get()!="Muzyk"):
            name=self.NameInput.get()
            if(not name):
                OK=False
            else:
                name="'"+name+"'"
        else:
            name=self.NameInputM.get()    
            if(not name):
                name="NULL"
            else:
                name="'"+name+"'"

            sname = self.SurnameInputM.get()
            if(not sname):
                OK=False
            else:
                sname="'"+sname+"'"

            rola= self.RoleInput.get()
            if(not rola):
                OK=False
            else:
                rola="'"+rola+"'"

        data=""
        data2=""
        czas=""

        if(self.option_choose.get()=="Album" or self.option_choose.get()=="Zespół" or self.option_choose.get()=="Muzyk"):
            if(not self.rok1.get() or not self.miesiac1.get() or int(self.miesiac1.get())<0 or int(self.miesiac1.get())>12 or not self.dzien1.get() or int(self.dzien1.get())<0 or int(self.dzien1.get())>31):
                OK=False
            else:
                data="('"+self.rok1.get()+"-"+self.miesiac1.get()+"-"+self.dzien1.get()+"')"
        if(self.option_choose.get()=="Zespół" or self.option_choose.get()=="Muzyk"):
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
        print("IDO: ", self.ido)
        
        if(OK):
            if(self.ido>0):
                if(self.option_choose.get()=="Zespół" or self.option_choose.get()=="Muzyk"):
                    checkifband="SELECT * FROM zespol WHERE idz="+self.idt+";"
                    cursor.execute(checkifband)

                    if not cursor.rowcount:
                        command="UPDATE muzyk SET imie="+name+", nazwisko="+sname+", data_ur="+data+", data_sm="+data2+", rola="+rola+" WHERE idm="+self.idt+";"
                    else:
                        command="UPDATE zespol SET nazwa="+name+", data_utworzenia="+data+", data_rozwiazania="+data2+" WHERE idz="+self.idt+";"
                elif(self.option_choose.get()=="Utwór"):
                    command="UPDATE utwory SET nazwa="+name+", dlugosc="+czas+", ocena="+ocena+" WHERE idu="+self.idt+";"
                elif(self.option_choose.get()=="Album"):
                    command="UPDATE albumy SET nazwa="+name+", data="+data+", ocena="+ocena+" WHERE ida="+self.idt+";"
            elif(self.ido==-2):
                if(self.option_choose.get()=="Zespół"):  
                    command="INSERT INTO wykonawca VALUES ();"
                    cursor.execute(command)
                    connection.commit()
                    command="SET @last_id = LAST_INSERT_ID();"
                    cursor.execute(command)
                    command="INSERT INTO zespol(zespol.idz, zespol.nazwa,zespol.data_utworzenia,zespol.data_rozwiazania) VALUES (@last_id," + name + "," + data + "," + data2 + ");"
                elif(self.option_choose.get()=="Muzyk"):  
                    command="INSERT INTO wykonawca VALUES ();"
                    cursor.execute(command)
                    connection.commit()
                    command="SET @last_id = LAST_INSERT_ID();"
                    cursor.execute(command)
                    command="INSERT INTO muzyk(idm,imie,nazwisko,data_ur,data_sm,rola) VALUES (@last_id," + name + "," +sname +","+ data + "," + data2 + ","+rola+");"
                elif(self.option_choose.get()=="Utwór"):
                    command="INSERT INTO utwory(utwory.nazwa,  utwory.dlugosc, utwory.ocena) VALUES("+name+","+ czas+","+ocena +");" 
                elif(self.option_choose.get()=="Album"):
                    command="INSERT INTO albumy(albumy.nazwa, albumy.data, albumy.ocena) VALUES ("+name+","+data+","+ocena+");"
            print(command)
            cursor.execute(command)
            connection.commit()
            self.master.switch_frame(EditPage)
     

if __name__ == '__main__':
   
   main_app =  MainApplication(root)
   
   root.mainloop()
   connection.commit() 
   connection.close()