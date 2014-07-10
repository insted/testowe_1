'''
Created on 18-02-2014

@author: Pawel Kramrzewski
'''
#!/usr/bin/python 
import struct 
import serial
import time
from datetime import datetime, timedelta 
from pylab import *
import matplotlib.pyplot as plt
import datetime as dt
import serial
from gi.repository import Gtk,GObject
from matplotlib.figure import Figure
import matplotlib.dates as md
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

ser = serial.Serial(
                        port="/dev/ttyUSB0",
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)
#f = open("dane.txt", 'r+')
file_date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M.txt")
f = open(file_date, "a")


class pomiar():
    def __init__(self):
        ser.open()
        p_start = ("7B4D080001EA457D")
        p_start_d = p_start.decode("hex")
        ser.write(p_start_d)
        p_dane = ser.read(64)
        p_sth = p_dane.encode("hex")    
        print(p_sth)
        p_sth = p_dane.encode("hex")
        p_t1 = p_sth.find("7b4d1800")   
        p_t2 = int(p_t1)    
        p_t3 = p_t2 + 12
        p_step = p_t2 + 36
        p_pomiar = p_sth[p_t3 : p_step]
        p_zera_pom = ('0'*24)
        if len(p_pomiar) != 24 or p_pomiar == p_zera_pom:
            print("dupa")
        #    self.p_temperatura = self.p_temperatura
        else:
            p_temp_h = p_pomiar[16:24]
            p_tem2 = str(p_temp_h.decode('hex'))
            self.p_temperatura = struct.unpack('<f', p_tem2)
 
            p_p1 = p_pomiar[8:16]
            p_p1_1 = p_p1.decode('hex')
            self.p_pomiar1 = struct.unpack('<f', p_p1_1)
   
            p_p2 = p_pomiar[0:8]
            p_p2_1 = p_p2.decode('hex')
            self.p_pomiar2 = struct.unpack('<f',p_p2_1)
    def temperatura(self):
        p_c_t = str(self.p_temperatura)
        p_z = p_c_t.replace('(' , ' \t' )
        p_z_1 = p_z.replace(',', ' ')
        p_z_2 = p_z_1.replace(')', ' \t')
        self.temperatura = p_z_2
        print self.temperatura
        return self.temperatura
        #temp = temperatura(p_temperatura)
    def woda(self):    
        p_c_p1 = str(self.p_pomiar1)
        p_c_p1_1 = p_c_p1.replace('(' , '\t ') 
        p_c_p1_2 = p_c_p1_1.replace( ',' , ' ')
        p_c_p1_3 = p_c_p1_2.replace(')', ' \t')
        self.woda = p_c_p1_3 
        print(self.woda)    
        return self.woda
        #water = woda(p_pomiar1)

    def amoniak(self):
        p_c_p2 = str(self.p_pomiar2)
        p_c_p2_1 = p_c_p2.replace('(' , ' \t ') 
        p_c_p2_2 = p_c_p2_1.replace( ',' , '')
        p_c_p2_3 = p_c_p2_2.replace(')', '')
        self.amoniak = p_c_p2_3
        print(self.amoniak)
        return self.amoniak
    # float & round 
    def amoniak_f(self):
        amoniak_f = round(float(self.amoniak),3)
        amoniak_s = str(amoniak_f)
        # return(amoniak_f)
        return(amoniak_s)
        print(amoniak_f)
    def woda_f(self):
        woda_f = round(float(self.woda),3)
        woda_s = str(woda_f)
        return(woda_s)
        #return(woda_f)
    def temperatur_f(self):
        temperatura_f = round(float(self.temperatura),3)
        temperatura_s = str(temperatura_f)
        return temperatura_s
        
class wykres_1(Gtk.Window, pomiar):
    
    def __init__(self):    
        pomiar.__init__(self)
        Gtk.Window.__init__(self, title="Okno Pomiarowe")
        self.vpaned = Gtk.VPaned()     
        self.set_default_size(800,600)
        #self.move(200,100)     
        self.vbox = Gtk.VBox()
        self.box = Gtk.Box(spacing=6)
        self.set_border_width(20)
        
        self.button = Gtk.Button(label="Pomiar Amoniaku")
        self.button.connect("clicked", self.on_pomiar_clicked)
        self.box.pack_start(self.button, True, True, 5)
        
        self.button = Gtk.Button(label = "Pomiar Wody" )
        self.button.connect("clicked", self.on_pomiar_clicked)
        self.box.pack_start(self.button, True, True, 5)
        
        self.button = Gtk.Button(label = "Pomiar Temperatury" ) 
        self.button.connect("clicked", self.on_pomiar_clicked)
        self.box.pack_start(self.button,True, True, 5)  
        
        self.i = datetime.datetime.now()
        #self.i_strip = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        self.x = [date2num(self.i)] 
        print("Data teraz: ")
        print(self.x)
        
        self.f = plt.figure()
        self.f.autofmt_xdate()
        self.a = self.f.add_subplot(3,1,1)
        n1 = pomiar()
        self.amn_1 = n1.amoniak()
        self.wda_1 = n1.woda()
        self.tmp_1 = n1.temperatura()
        # print("Tutaj:",  z) 
        #print(type(z))
        #self.p = float(z)
        #print(self.p)
        self.a.plot_date(self.x, self.amn_1, tz=None,
                                color='green', linestyle = ':',
                                marker='o', markerfacecolor='blue', 
                                markersize=2)
           
        
        self.a.grid(True)
        #self.a.set_xlim(-3,22)
        self.a.set_ylim(-1,20)
        self.a.set_xlabel('Czas')
        self.a.set_ylabel('Amoniak [ppm]')
        self.b = self.f.add_subplot(312)
        self.b.plot_date(self.x,self.wda_1, tz=None,
                                color='green', linestyle = ':',
                                marker='o', markerfacecolor='blue', 
                                markersize=2)
        self.b.grid(True)
        self.b.set_xlabel('Czas')
        self.b.set_ylabel('Woda [ppm]')
        #self.a.set_animated(True)
        xfmt = md.DateFormatter('%m-%d-%H:%M:%S')    
        #print(xfmt)
        
        self.c = self.f.add_subplot(313)
        self.c.plot_date(self.x,self.tmp_1,tz=None,
                                color='green', linestyle = ':',
                                marker='o', markerfacecolor='blue', 
                                markersize=2)   
        self.c.grid(True)
        #self.a.set_xlim(-3,22)
        self.c.set_ylim(20,23)
        self.c.set_xlabel('Czas')
        self.c.set_ylabel(u'Temperatura [\u00B0C]')
        #self.c.set_xlim(0,self.x)
        plt.setp(self.c.xaxis.set_major_formatter(xfmt))
        #plt.setp(self.c.xaxis.get_majorticklabels(), rotation=30)
        plt.setp(self.a.xaxis.set_major_formatter(xfmt))
        # plt.setp(self.a.xaxis.get_majorticklabels(), rotation=30)
        plt.setp(self.b.xaxis.set_major_formatter(xfmt))
        #plt.setp(self.b.xaxis.set_major_locator(md.HourLocator()))
        plt.setp(self.a.xaxis.set_major_locator(MaxNLocator(4)))
        plt.setp(self.b.xaxis.set_major_locator(MaxNLocator(4)))
        plt.setp(self.c.xaxis.set_major_locator(MaxNLocator(4)))
        #self.c.relim()
#         relim()
        #self.c.autoscale_view()
        #plt.gcf()
        #plt.ion()
        # plt.setp(self.b.xaxis.get_majorticklabels(), rotation=30)
        
        #self.b.subplot_adjust(bottom = 0.5)
# Add canvas to vbox
        self.canvas = FigureCanvas(self.f)  # a Gtk.DrawingArea
        self.vbox.pack_start(self.canvas, True, True, 5)
       
# Create toolbar
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.vbox.pack_start(self.toolbar, False, False, 5)
        
        self.add(self.vpaned)
        self.vpaned.add(self.box)
        self.vpaned.add(self.vbox)
        self.show_all()
        self.s = GObject.timeout_add(6000,self.wykres)
        #GObject.idle_add(self.wykres)
    def on_pomiar_clicked(self,button):
        print("Dziala")
        stop = ("7B49080000EA4A7D")
        stop_d = stop.decode("hex")
        print(stop_d)
        ser.close()
        ser.open()
        ser.flushInput()
        ser.flushOutput()
        ser.write(stop_d)
        GObject.source_remove(self.s)
        self.destroy()

    def wykres(self):
        i_1 = datetime.datetime.now()
        #i_strip = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
            
        #print("Czas datetime" )
        #print(i_1)    
        x1 = [date2num(i_1)]    
        print("Czas teraz: ") 
        print(x1)   
        nowy_pomiar = pomiar()
        #print("Czas kiedys: " )
        print(self.x)
        amon_1 = nowy_pomiar.amoniak()
        tmp = nowy_pomiar.temperatura()
        wda = nowy_pomiar.woda()
        amoniak = ("Pomiar amoniaku: " + amon_1 + " \t " + "Woda: " + wda +
                    " \t " + "Temperatura celi: " + tmp )
        z = str(amoniak)
        self.set_title(z)
        self.a.plot_date(x1,amon_1,tz = None,
                                color='green', linestyle = '-',
                                marker='o', markerfacecolor='blue', 
                                markersize=3)
        self.b = self.f.add_subplot(312)
        self.b.plot_date(x1,wda, tz=None,
                                color='green', linestyle = ':',
                                marker='o', markerfacecolor='blue', 
                                markersize=3)
           
        
        self.b.grid(True)
       
        self.b.set_xlabel('Czas')
        self.b.set_ylabel('Woda [ppm]')
        self.c = self.f.add_subplot(313)
        
        self.c.plot_date(x1,tmp,tz=None,
                                color='green', linestyle = ':',
                                marker='o', markerfacecolor='blue', 
                                markersize=3 )
                                   
        self.c.grid(True)
        #self.a.set_xlim(-3,22)
        self.c.set_ylim(5,55)
        self.c.set_xlabel('Czas')
        self.c.set_ylabel(u'Temperatura [\u00B0C]')  
        self.a.set_xlim((i_1 - timedelta(minutes=8), i_1 + timedelta(seconds=15)) )   
        self.b.set_xlim((i_1 - timedelta(minutes=8), i_1 + timedelta(seconds=15)) )
        self.c.set_xlim((i_1 - timedelta(minutes=8), i_1 + timedelta(seconds=15)) ) 
        #self.a.xticks(x1,i_1,rotation=45)    
        # self.a.xaxis.set_minor_formatter(dates.DateFormatter('%d%a'))
        #self.a.setp(rotation=30)
        time.sleep(1)
        self.canvas.draw()   
        #self.show_all() 
        return True       
        #amon = amoniak(p_pomiar2) 

class MyWindow(Gtk.Window, pomiar):

    def __init__(self):
        #pomiar.__init__(self)
        Gtk.Window.__init__(self, title="Axetris ver. 0.15")
    
        self.vpaned = Gtk.VPaned()
        nowy_pomiar = pomiar()
        self.amon_1 = nowy_pomiar.amoniak()
        self.tmp = nowy_pomiar.temperatura()
        self.wda = nowy_pomiar.woda()
        self.amon_1_f = nowy_pomiar.amoniak_f()
        self.tmp_f = nowy_pomiar.temperatur_f()
        self.wda_f = nowy_pomiar.woda_f()
        #print(wda)
        #print(type(wda))
        self.box = Gtk.Box(spacing=8)
        #self.add(self.box)
        
        self.set_border_width(20)
        self.button = Gtk.Button(label="Rozpocznij pomiar")
        self.button.connect("clicked", self.on_pomiar_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button(label="Edycja parametrow")
        self.button.connect("clicked", self.on_parametry_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button(label="Zatrzymanie pomiaru")
        self.button.connect("clicked", self.on_stop_clicked)
        self.box.pack_start(self.button, True, True, 0)
        
        #dodanie listy 
        self.liststore1 = Gtk.ListStore(str, str)
        self.liststore1.append([u"Pomiar temperatury [\u00B0C]", self.tmp_f])
        self.liststore1.append(["Pomiar amoniaku [ppm]", self.amon_1_f ])
        self.liststore1.append(["Pomiar wody [ppm]", self.wda_f])
    
    
        self.treeview_1 = Gtk.TreeView(model=self.liststore1)

        renderer_text_1 = Gtk.CellRendererText()
        column_text_1 = Gtk.TreeViewColumn("", renderer_text_1, text=0)
        self.treeview_1.append_column(column_text_1)

        renderer_editabletext_1 = Gtk.CellRendererText()
        renderer_editabletext_1.set_property("editable", False)

        column_editabletext_1 = Gtk.TreeViewColumn("Wyniki Pomiarowe",
                            renderer_editabletext_1, text=1) 
        self.treeview_1.append_column(column_editabletext_1)

        #renderer_editabletext_1.connect("edited", self.pomiary)
        #renderer_editabletext_1.connect("edited", self.text_edited)
        self.add(self.vpaned)
        
        self.vpaned.add(self.box)
        self.vpaned.add(self.treeview_1)
        #self.show_all() 
        
        self.p = GObject.timeout_add(6000,self.pomiar_1)
        self.vpaned.show_all()
        self.show_all()
        #return True
    def on_pomiar_clicked(self, widget):
        wykres_1()
 
    def on_parametry_clicked(self, widget):
        self.answerwin = Gtk.Window()
        self.answerwin.set_title("Parametry")
        self.answerwin.set_border_width(10)
        self.answerwin.move(200,300)    
        # Lista 
        print("Dziala")
        ping = ("7B50080010001D7D")
        ping_d = ping.decode("hex")
        print(ping_d)
        ser.open()
        ser.flushInput()
        ser.flushOutput()
        ser.write(ping_d)
        #ser.write(ver_d)
        dane = ser.read(80)
        sth = dane.encode('hex')
        print(dane)
        print(sth)
        print("Ilosc znakow ", len(sth))
# Gas 1 offset 
        print(len(sth))
        self.gas_1_off = sth[12:20]
        print(self.gas_1_off)
        gas_1_off_th = self.gas_1_off.decode('hex')
        gas_1_offset = struct.unpack('<f',gas_1_off_th)
        print("Offset pierwszefgo gazu ", gas_1_offset)
        gas_1_offset_str = str(gas_1_offset)
        gas_1_offset_str_1 = gas_1_offset_str.replace('(', "")
        gas_1_offset_str_2 = gas_1_offset_str_1.replace(",", "")
        gas_1_offset_str_3 = gas_1_offset_str_2.replace(")", "")
        float_gas_1_offset = float(gas_1_offset_str_3)
        print(type(float_gas_1_offset))
        t1 = float_gas_1_offset
# Gas 1 span 
        self.gas_1_spn = sth[20:28]
        print(self.gas_1_spn)
        gas_1_span_th = self.gas_1_spn.decode('hex')
        gas_1_span = struct.unpack('<f', gas_1_span_th)
        print("Gas span: " , gas_1_span)
        gas_1_span_str = str(gas_1_span)
        gas_1_span_str_1 = gas_1_span_str.replace("(", "")
        gas_1_span_str_2 = gas_1_span_str_1.replace(",","")
        gas_1_span_str_3 = gas_1_span_str_2.replace(")", "")
        float_gas_1_span = float(gas_1_span_str_3)
        t2 = float_gas_1_span
# Alarm koncetracji 1 gas 
        self.alrm_1 = sth[28:36]
        print(self.alrm_1)
        alrm_1_th = self.alrm_1.decode('hex')
        alrm_1_alr = struct.unpack('<f', alrm_1_th)
        print("Alarm koncetracji: ", alrm_1_alr)
        print(alrm_1_alr)
        alrm_1_alr_str = str(alrm_1_alr)
        alrm_1_alr_str_1 = alrm_1_alr_str.replace("(", "")
        alrm_1_alr_str_2 = alrm_1_alr_str_1.replace(",", "")
        alrm_1_alr_str_3 = alrm_1_alr_str_2.replace(")", "")
        float_alrm_1_alr = float(alrm_1_alr_str_3)
        t3 = float_alrm_1_alr
# Ostrzezenie koncetracji 1 gas
        self.warn_1 = sth[36:44]
        warn_1_th = self.warn_1.decode('hex')
        warning_1 = struct.unpack("<f", warn_1_th)
        print(self.warn_1)
        print("Przekroczenie zakresu", warning_1)
        warning_1_str = str(warning_1)
        warning_1_str_1 = warning_1_str.replace("(", "")
        warning_1_str_2 = warning_1_str_1.replace(",", "")
        warning_1_str_3 = warning_1_str_2.replace(")", "")
        float_warning_1 = float(warning_1_str_3)
        t4 = float_warning_1
# Analog output min koncentracji
        self.anlg_out_min = sth[44:52]
        anlg_out_min_th = self.anlg_out_min.decode('hex')
        analog_out_min = struct.unpack('<f', anlg_out_min_th)
        print(self.anlg_out_min)
        print("Wyjscie analogowe minimalna koncentracja: ", analog_out_min)
        anlg_out_min_str = str(analog_out_min)
        anlg_out_min_str_1 = anlg_out_min_str.replace("(", "")
        anlg_out_min_str_2 = anlg_out_min_str_1.replace(",", "")
        anlg_out_min_str_3 = anlg_out_min_str_2.replace(")", "")
        float_anlg_out_min = float(anlg_out_min_str_3)
        t5 = float_anlg_out_min
# Analog output max koncentracji 
        self.anlg_out_max = sth[52:60]
        anlg_out_max_th = self.anlg_out_max.decode('hex')
        analog_out_max = struct.unpack('<f', anlg_out_max_th)
        print(self.anlg_out_max)
        print("Wyjscie analogowe maksymalna koncentracja: ", analog_out_max )
        analog_out_max_str = str(analog_out_max)
        analog_out_max_str_1 = analog_out_max_str.replace("(", "")
        analog_out_max_str_2 = analog_out_max_str_1.replace(",", "")
        analog_out_max_str_3 = analog_out_max_str_2.replace(")", "")
        float_analog_out_max = float(analog_out_max_str_3)
        t6 = float_analog_out_max
# Analog output offset 
        self.anlg_offset = sth[60:68]
        anlg_offset_th = self.anlg_offset.decode('hex')
        analog_offset = struct.unpack('<f', anlg_offset_th)
        print(self.anlg_offset)
        print("Offset wyjscia analogowego: ", analog_offset )
        analog_offset_str = str(analog_offset)
        analog_offset_str_1 = analog_offset_str.replace("(", "")
        analog_offset_str_2 = analog_offset_str_1.replace(",", "")
        analog_offset_str_3 = analog_offset_str_2.replace(")","")
        float_analog_offset = float(analog_offset_str_3)
        t7 = float_analog_offset
# Analog output span
        self.anlg_span = sth[68:76]
        anlg_span_th = self.anlg_span.decode('hex')
        analog_span = struct.unpack('<f', anlg_span_th)
        print(self.anlg_span)
        print("Span wyjscia analogowego: ", analog_span)
        analog_span_str = str(analog_span)
        analog_span_str_1 = analog_span_str.replace("(", "")
        analog_span_str_2 = analog_span_str_1.replace(",", "")
        analog_span_str_3 = analog_span_str_2.replace(")", "")
        float_analog_span = float(analog_span_str_3)
        t8 = float_analog_span
# Czas integracji
        self.int_t = sth[76:84]
        int_t_th = self.int_t.decode("hex")
        integration_time = struct.unpack('<f', int_t_th)
        print(self.int_t)
        print("Czas integracji: ", integration_time)
        integration_time_str = str(integration_time)
        integration_time_str_1 = integration_time_str.replace("(","")
        integration_time_str_2 = integration_time_str_1.replace(",", "")
        integration_time_str_3 = integration_time_str_2.replace(")", "")
        float_integration_time = float(integration_time_str_3)
        t9 = float_integration_time
# Gas 2 offset 
        self.gas_2_off = sth[84:92]
        gas_2_off_th = self.gas_2_off.decode('hex')
        gas_2_offset = struct.unpack('<f', gas_2_off_th)
        print(self.gas_2_off)
        print("Gas 2 offset: ", gas_2_offset)
        gas_2_offset_str = str(gas_2_offset)
        gas_2_offset_str_1 = gas_2_offset_str.replace("(", "")
        gas_2_offset_str_2 = gas_2_offset_str_1.replace(",", "")
        gas_2_offset_str_3 = gas_2_offset_str_2.replace(")", "")
        float_gas_2_offset = float(gas_2_offset_str_3)
        t10 = float_gas_2_offset
# Gas 2 span 
        self.gas_2_spn = sth[92:100]
        gas_2_spn_th = self.gas_2_spn.decode('hex')
        gas_2_span = struct.unpack('<f', gas_2_spn_th)
        print(self.gas_2_spn)
        print("Gas 2 span", gas_2_span)
        gas_2_span_str = str(gas_2_span)
        gas_2_span_str_1 = gas_2_span_str.replace("(","")
        gas_2_span_str_2 = gas_2_span_str_1.replace(",", "")
        gas_2_span_str_3 = gas_2_span_str_2.replace(")","")
        float_gas_2_span = float(gas_2_span_str_3)
        t11 = float_gas_2_span
#Tworzenie listy
        self.liststore = Gtk.ListStore(str, float)
        self.liststore.append(["Offset NH3", t1])
        self.liststore.append(["Span NH3", t2 ])
        self.liststore.append(["Alarm Koncentracji", t3])
        self.liststore.append(["Ostrzezenie koncentracji", t4])
        self.liststore.append(["Min. wyjscia analogowego",t5])
        self.liststore.append(["Max wyjscia analogowego",t6])
        self.liststore.append(["Offset wyjscia pradowego", t7])
        self.liststore.append(["Span wyjscia pradowego", t8])
        self.liststore.append(["Czas integracji", t9])
        self.liststore.append(["Offset H20", t10])
        self.liststore.append(["Span H20", t11])
        
        self.treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        self.treeview.append_column(column_text)

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)

        column_editabletext = Gtk.TreeViewColumn("Editable Text",
            renderer_editabletext, text=1)
        self.treeview.append_column(column_editabletext)

        renderer_editabletext.connect("edited", self.text_edited)
        
        #float(text)
        self.answerwin.add(self.treeview)
        self.answerwin.show_all()    
    def text_edited(self, widget, path, flt):
        self.liststore[path][1] = float(flt)
        model, treeiter = self.treeview.get_selection().get_selected()
        start = ("7B43500000EA")
        end = ("007D")
        zera = ('0'*56)
        if model[treeiter][0] == "Offset NH3": 
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_offset = val_str.encode('hex')
            
            wynik = (start + new_offset + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max+ self.anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end)                  
            wynik_decoded = wynik.decode('hex')      
            ser.write(wynik_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
                
        if model[treeiter][0] == "Span NH3":
            val1 = float(flt)
            val_1_str = struct.pack('<f', val1)
            new_span = val_1_str.encode('hex')
            wynik_1 = (start + self.gas_1_off + new_span + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max+ self.anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_1_decoded = wynik_1.decode('hex')
            ser.write(wynik_1_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        if model[treeiter][0] == "Alarm Koncentracji":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_alrm_1 = val_str.encode('hex')
            wynik_2 = (start + self.gas_1_off + self.gas_1_spn + new_alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max+ self.anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_2_decoded = wynik_2.decode('hex')
            ser.write(wynik_2_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)  
        elif model[treeiter][0] == "Ostrzezenie koncentracji":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_warn_1 = val_str.encode("hex")
            wynik_3 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + new_warn_1 + self.anlg_out_min 
                     + self.anlg_out_max+ self.anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_3_decoded = wynik_3.decode('hex')
            ser.write(wynik_3_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        elif model[treeiter][0] == "Min. wyjscia analogowego":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_anlg_out_min = val_str.encode("hex")
            wynik_4 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + new_anlg_out_min 
                     + self.anlg_out_max+ self.anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_4_decoded = wynik_4.decode('hex')
            ser.write(wynik_4_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)    
        elif model[treeiter][0] == "Max wyjscia analogowego":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_anlg_out_max = val_str.encode("hex")
            wynik_5 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + new_anlg_out_max + self.anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_5_decoded = wynik_5.decode('hex')
            ser.write(wynik_5_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)    
        elif model[treeiter][0] == "Offset wyjscia pradowego":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_anlg_offset = val_str.encode("hex")
            wynik_6 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max + new_anlg_offset+ self.anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_6_decoded = wynik_6.decode('hex')
            ser.write(wynik_6_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        elif model[treeiter][0] == "Span wyjscia pradowego":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_anlg_span = val_str.encode("hex")
            wynik_7 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max + self.anlg_offset + new_anlg_span + self.int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_7_decoded = wynik_7.decode('hex')
            ser.write(wynik_7_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        elif model[treeiter][0] == "Czas integracji":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_int_t = val_str.encode("hex")
            wynik_8 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max + self.anlg_offset + self.anlg_span + new_int_t + self.gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_8_decoded = wynik_8.decode('hex')
            ser.write(wynik_8_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        elif model[treeiter][0] == "Offset H20":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_gas_2_off= val_str.encode("hex")
            wynik_9 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max + self.anlg_offset + self.anlg_span + self.int_t + new_gas_2_off + 
                     self.gas_2_spn + zera + end )
            wynik_9_decoded = wynik_9.decode('hex')
            ser.write(wynik_9_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        elif model[treeiter][0] == "Span H20":
            val = float(flt)
            val_str = struct.pack('<f', val)
            new_gas_2_spn = val_str.encode("hex")
            wynik_10 = (start + self.gas_1_off + self.gas_1_spn + self.alrm_1 + self.warn_1 + self.anlg_out_min 
                     + self.anlg_out_max + self.anlg_offset + self.anlg_span + self.int_t + self.gas_2_off + 
                     new_gas_2_spn + zera + end )
            wynik_10_decoded = wynik_10.decode('hex')
            ser.write(wynik_10_decoded)
            ser.read(14)
            self.answerwin.destroy()
            self.on_parametry_clicked(widget)
        else:
            print "You selected", model[treeiter][0]
            print(text)
  
    def on_stop_clicked(self, widget):
        GObject.source_remove(self.p)
        ser.open()
        stop = ("7B49080000EA4A7D")
        stop_d = stop.decode("hex")
        print(stop_d)
        ser.write(stop_d)
        ser.close()   
        print("Kolejna opcja ")    
    def pomiar_1(self):
        
        self.vpaned.remove(self.treeview_1)
        
        nowy_pomiar = pomiar()
        self.amon_1 = nowy_pomiar.amoniak()
        self.tmp = nowy_pomiar.temperatura()
        self.wda = nowy_pomiar.woda()
        self.amon_1_f = nowy_pomiar.amoniak_f()
        self.tmp_f = nowy_pomiar.temperatur_f()
        self.wda_f = nowy_pomiar.woda_f()
        print("Zmienna amoniak:")
        print(type(self.amon_1_f))
        print(self.amon_1_f)
        print("Woda: ")
        print(self.wda_f)
        print("Temperatura")
        print(self.tmp_f)
        
        
        
        self.box = Gtk.Box(spacing=8)
        
        self.set_border_width(20)
        self.button = Gtk.Button(label="Rozpocznij pomiar")
        self.button.connect("clicked", self.on_pomiar_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button(label="Edycja parametrow")
        self.button.connect("clicked", self.on_parametry_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button(label="Zatrzymanie pomiaru")
        self.button.connect("clicked", self.on_stop_clicked)
        self.box.pack_start(self.button, True, True, 0)
        
        #dodanie listy 
        self.liststore1 = Gtk.ListStore(str, str)
        self.liststore1.append([u"Pomiar temperatury [\u00B0C]", self.tmp_f])
        self.liststore1.append(["Pomiar amoniaku [ppm]", self.amon_1_f ])
        self.liststore1.append(["Pomiar wody [ppm]", self.wda_f])
    
    
        self.treeview_1 = Gtk.TreeView(model=self.liststore1)

        renderer_text_1 = Gtk.CellRendererText()
        column_text_1 = Gtk.TreeViewColumn("", renderer_text_1, text=0)
        self.treeview_1.append_column(column_text_1)

        renderer_editabletext_1 = Gtk.CellRendererText()
        renderer_editabletext_1.set_property("editable", False)

        column_editabletext_1 = Gtk.TreeViewColumn("Wyniki Pomiarowe",
                            renderer_editabletext_1, text=1) 
        self.treeview_1.append_column(column_editabletext_1)
    
        self.vpaned.add(self.treeview_1)
        self.show_all() 
        
        self.queue_draw()
       
     
        return True   

if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
        