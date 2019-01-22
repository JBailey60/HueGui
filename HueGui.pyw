 #Graphical Interface to control Phillips Hue Lights
 #username: fQtHmWflCsBXEfznfFI-NLw0DI5nmxCO7Tzh-zlQ
 #ip-address: http://192.168.0.2


from tkinter import *
from phue import *

class Application(Frame):
    """A row of buttons to control your lights"""
    b = Bridge(ip='192.168.0.2', username='fQtHmWflCsBXEfznfFI-NLw0DI5nmxCO7Tzh-zlQ')
    lights = b.get_light_objects('id')
    onoff = True


    def __init__(self, master):
        """ Initialize the Frame. """
        super(Application, self).__init__(master) 
        master.columnconfigure(0, weight=1)   
        master.rowconfigure(0, weight = 1)
        self.grid(sticky="news")
        self.create_widgets()
        

    def create_widgets(self):
        for i in range(0,3):
           self.columnconfigure(i, weight=2)
        for i in range(0,4):
            self.rowconfigure(i, weight=2)

        
        
        self.bttn_white = Button(self, text = "Focus", bg="white", font="BOLD")
        self.bttn_white["command"] = self.bttn_Focus
        self.bttn_white.grid(rowspan=2, row = 0, column=0, sticky = ("N","S","E","W"))

        self.bttn_red = Button(self, text = "Red", bg="red", fg = "white", font="BOLD")
        self.bttn_red.grid(rowspan=2, row = 0, column=1, sticky = ("N","S","E","W"))

        self.bttn_green = Button(self, text = "Green", bg = "green", font="BOLD")
        self.bttn_green.grid(rowspan=2,row = 0, column=2, sticky = ("N","S","E","W"))

        self.bttn_low_bri = Button(self, text = "Bri -", bg = "grey", font="BOLD")
        self.bttn_low_bri["command"] = self.lower_bri
        self.bttn_low_bri.grid(row = 3, column=0, sticky = ("N","S","E","W"))

        self.bttn_next = Button(self, text = "Bri +", bg = "grey", font="BOLD")
        self.bttn_next["command"] = self.high_bri
        self.bttn_next.grid(row = 2, column=0, sticky = ("N","S","E","W"))

        self.bttn_off = Button(self, text = "On/Off", bg = "black", fg="white", font="BOLD")
        self.bttn_off.grid(rowspan=2, row = 2, column=1, sticky = ("N","S","E","W"))
        self.bttn_off["command"] = self.bttn_onoff

    def lower_bri(self):
        """Lowers Brightness of the lights"""
        for light in self.lights:
            bri = self.b.get_light(light,'bri')
            bri = bri - 50
            if bri < 0:
                bri = 1
            self.b.set_light(light,'bri',bri)


##        self.bttn_high_bri = Button(self, text = "To Dark", bg = "gray")
##        self.bttn_high_bri["command"] = self.high_bri
##        self.bttn_high_bri.grid(row = 1, column=1, sticky = ("N","S","E","W"))


    def high_bri(self):
        """Raises Brightness of the lights"""
        for light in self.lights:
            bri = self.b.get_light(light,'bri')
            bri = bri + 50 
            if bri > 255:
                bri = 255         
            self.b.set_light(light,'bri',bri)

##    def bttn_next_fun(self):
##        self.bttn_off = Button(self, text = "Off", bg = "black", fg="white", font="BOLD")
##        self.bttn_off["command"] = self.bttn_off_fun
##        self.bttn_off.grid(row = 1, column=1, sticky = ("N","S","E","W"))

    def bttn_onoff(self):
        if self.onoff == True:
            for light in self.lights:
                self.b.set_light(light,'on',False)
            self.onoff = False
        else:
            for light in self.lights:
                self.b.set_light(light,'on',True)
            self.onoff = True
    
    def bttn_Focus(self):
        self.b.run_scene('Living room', 'Concentrate',transition_time=30)





# main
root = Tk()
root.title("Hue Gui")
root.geometry("200x150")
#root.attributes('-fullscreen', True)
app = Application(root)
root.mainloop()
