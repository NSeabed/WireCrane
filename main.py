from tkinter import *
from functions import calculate, calculate_total_length
from settings import *
from PIL import ImageTk

import serial
import time
import math
import socket
import webbrowser
import configparser
import os
import sys
import Pmw

#path = "C:\Users\pc_slooprijp\Documents\python"


boom_angle = 0

from tkinter import Tk, Label, Button, ttk

class MyFirstGUI:

    def __init__(self, master):

        # UDP settings
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005

        print("start of the program")
        self.com_button_press = False
        self.boom = 0
        self.wire = 0
        self.wire2 = 0
        self.load = 0

        # INTEGERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.integer_progress_show = StringVar()
        self.integer_progress_show.set("IDLE")

        self.integer_angle = IntVar()
        self.integer_angle.set(0)

        self.integer_cable_angle = IntVar()
        self.integer_cable_angle.set(0)

        self.integer_cable_length = IntVar()
        self.integer_cable_angle.set(0)

        self.integer_scan = IntVar()
        self.integer_scan.set(0)

        self.integer_scan_return = StringVar()
        self.integer_scan_return.set("#--")

        self.integer_UDP_IP = IntVar()
        self.integer_UDP_IP.set(0)

        self.integer_UDP_port = IntVar()
        self.integer_UDP_port.set(0)

        # settings window - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.entry_com_boom = StringVar()
        # self.entry_com_boom.set(" ")

        self.integer_entry_baud_boom = IntVar()
        self.integer_entry_baud_boom.set(0)

        self.entry_com_wire = StringVar()
        self.entry_com_wire.set(" ")

        self.integer_entry_baud_wire = IntVar()
        self.integer_entry_baud_wire.set(0)

        self.integer_error_com = StringVar()
        self.integer_error_com.set("")

        self.com = StringVar(root)
        self.com.set('COM3')

        # Window settings
        self.master = master
        master.title("WireCrane 2.0")
        master.geometry("800x600+800+600")

        # init - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if os.path.isfile('settings.ini') == False:
            self.write_ini(boom_port="com1", boom_baud="9600", wire_port="com2", wire_baud="9600", drum_min=595, drum_max=1000, cable=28, drum_width=150)

        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        print("d_drum_min: ", self.config['WIRE CALIBRATION']['d_drum_min'])
        print("config read")

        # menu bar - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="settings", command=self.settings_win)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_separator()
        helpmenu.add_command(label="Website", command=self.openweb)
        self.menubar.add_cascade(label="help", menu=helpmenu)

        # Row 0 - frame 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        w = Pmw.Group(master)
        w.grid(column=0, row=0, columnspan=15, rowspan=2, padx=3, pady=1)
        cw = Label(w.interior(), width=30, height=3)
        cw.grid(column=0, row=0, columnspan=15, rowspan=2, padx=8, pady=5)

        self.scan_button = Button(master, text="Start", command=self.scan)
        self.scan_button.grid(column=0, row=0, sticky=W+S, padx=8, pady=8)

        self.scan_ID = Label(master, text='Device ID:')
        self.scan_ID.grid(column=1, row=0, columnspan=2, sticky=W+S, pady=8)

        self.scan_return = Label(master, textvariable=str(self.integer_scan_return), width=5)
        self.scan_return.grid(column=2, row=0, sticky=E+S, pady=8)

        self.canvas = Canvas(master, width=400, height=150, bd=0, highlightthickness=0)
        self.canvas.configure(bg="white")
        self.canvas.grid(column=16, row=0, columnspan=10, rowspan=4, sticky=W+E+N+S, padx=5, pady=5)

        self.image = PhotoImage(file="crane.png")
        self.canvas.create_image(110, 50, image=self.image, anchor=NW)

        self.boom = self.canvas.create_line(200, 150, 360, 150, fill="black", width=3)
        self.wire = self.canvas.create_line(150, 49, 360, 150, fill="black", width=2)
        self.wire2 = self.canvas.create_line(360, 150, 360, 170, fill="black", width=2)
        self.load = self.canvas.create_line(355, 170, 365, 170, fill="black", width=2)

        self.open_com_button = Button(master, text="open com", command=self.open_com)
        self.open_com_button.grid(column=30, row=0, sticky=W, padx=5)

        self.entry_com_boom = Entry(master, width=7)

        # row 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.progress_show = Label(master, text="status: ")
        self.progress_show.grid(column=0, row=1, sticky=W+N, padx=5)

        self.progress_show = Label(master, textvariable=str(self.integer_progress_show))
        self.progress_show.grid(column=1, row=1, sticky=W+N)

        self.entry_box_error_message = Label(master, textvariable=str(self.integer_error_com), justify="left")
        self.entry_box_error_message.grid(column=2, row=1, sticky=W+N)

        # row 5 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        w = Pmw.Group(master)
        w.grid(column=0, row=2, columnspan=15, rowspan=2, padx=3, pady=3)
        cw = Label(w.interior(), width=30, height=2)
        cw.grid(column=0, row=2, columnspan=15, rowspan=2, padx=8, pady=20)

        # self.udp_ip_text = Label(master, text="ip address")
        # self.udp_ip_text.grid(column=0, row=2, sticky=W, padx=10, pady=3)

        # self.udp_ip = Entry(root, width=10)
        # self.udp_ip.insert(END, '127.0.0.1')
        # self.udp_ip.grid(column=1, row=2, sticky=W, columnspan=1, padx=10, pady=3)

        # row 6 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # self.udp_port_text = Label(master, text="port")
        # self.udp_port_text.grid(column=0, row=3, sticky=W, padx=10, pady=3)

        # self.udp_port = Entry(root, width=10)
        # self.udp_port.insert(END, '5005')
        # self.udp_port.grid(column=1, row=3, sticky=W, columnspan=1, padx=10, pady=3)

        # row 7
        # self.update_button = Button(master, text="Update", command=self.update)
        # self.update_button.grid(column=0, row=4, sticky=W, padx=5)

        # row 8
        self.send_udp = Button(master, text="send UDP", command=self.send_udp)
        self.send_udp.grid(column=0, row=5, sticky=W, padx=5)

        # row 9
        self.cable_test = Button(master, text="cable test", command=self.test_wire)
        self.cable_test.grid(column=0, row=6, sticky=W, padx=5)

        # row 16 - below picture - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # row 17
        self.angle = Label(master, text='angle')
        self.angle.grid(column=17, row=17)

        self.cable_angle = Label(master, text='cable angle')
        self.cable_angle.grid(column=18, row=17)

        self.cable_length = Label(master, text='cable length')
        self.cable_length.grid(column=19, row=17)

        # row 18
        self.entry_box_angle = Label(master, textvariable=str(self.integer_angle), justify="center", width=6)
        self.entry_box_angle.grid(column=17, row=18)

        self.entry_box_cable_length = Label(master, textvariable=str(self.integer_cable_length), justify="center", width=6)
        self.entry_box_cable_length.grid(column=18, row=18)

        self.entry_box_cable_angle = Label(master, textvariable=str(self.integer_cable_angle), justify="center", width=6)
        self.entry_box_cable_angle.grid(column=19, row=18)

        # row 19


        # set com  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


        # self.boomline = Canvas(root, width=800, height=800)
        # self.boomline.pack(side=BOTTOM)

    def write_ini(self, boom_port, boom_baud, wire_port, wire_baud, drum_min, drum_max, cable, drum_width):
        self.config = configparser.ConfigParser()
        self.config['COM PORTS'] = {'boom angle port': boom_port,
                                    'boom angle baud': boom_baud,
                                    'wire length port': wire_port,
                                    'wire length baud': wire_baud}

        self.config['WIRE CALIBRATION'] = {'D_drum_min': drum_min,
                                            'D_drum_max': drum_max,
                                            'D_cable': cable,
                                            'drum_width': drum_width}

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
            print("config file written")

    def openweb(self):
        webbrowser.open("https://www.seabed.nl/", new=1)

    def donothing(self):
        x = 0

#    def open_com(self):
#            if self.com_button_press == False:
#                try:
#                    self.ser_boom = serial.Serial(self.config['COM PORTS']['boom angle port'], int(self.config['COM PORTS']['boom angle baud']), timeout=0, parity=serial.PARITY_NONE, rtscts=1)
#                except OSError as err:
#                    self.integer_progress_show.set("OS error: {0}".format(err))
#                    print("button press: ", self.com_button_press)
#                    return

#                print("boom com: ", self.config['COM PORTS']['boom angle port'])
#                print("boom baud: ", self.config['COM PORTS']['boom angle baud'])
#                self.ser_cable = serial.Serial(self.config['COM PORTS']['wire length port'], self.config['COM PORTS']['wire length baud'], timeout=0, parity=serial.PARITY_EVEN, stopbits=1, bytesize=7)
#                print("boom com: ", self.config['COM PORTS']['wire length port'])
#                print("boom baud: ", self.config['COM PORTS']['wire length baud'])
#                self.open_com_button.config(relief=SUNKEN)
#                self.com_button_press = True
#                print("com opened")
#            elif self.com_button_press == True:
#                self.ser_boom.close()
#                self.ser_cable.close()
#                self.open_com_button.config(relief=RAISED)
#                self.com_button_press = False
#                print("com closed")

    def open_com(self):
        try:
            self.ser_boom = serial.Serial(self.config['COM PORTS']['boom angle port'], int(self.config['COM PORTS']['boom angle baud']), timeout=0, parity=serial.PARITY_NONE, rtscts=1)
        except OSError:
            print("error opening com port")
            self.integer_progress_show.set("error opening")
            self.integer_error_com.set(self.config['COM PORTS']['boom angle port'])
            return

        print("boom com: ", self.config['COM PORTS']['boom angle port'])
        print("boom baud: ", self.config['COM PORTS']['boom angle baud'])
        self.ser_cable = serial.Serial(self.config['COM PORTS']['wire length port'], self.config['COM PORTS']['wire length baud'], timeout=0, parity=serial.PARITY_EVEN, stopbits=1, bytesize=7)
        print("boom com: ", self.config['COM PORTS']['wire length port'])
        print("boom baud: ", self.config['COM PORTS']['wire length baud'])
        self.open_com_button.config(relief=SUNKEN)
        self.com_button_press = True
        print("com opened")
        self.integer_error_com.set("")

    def send_udp(self):
        # print("UDP target IP:", self.UDP_IP)
        # print("UDP target port:", self.UDP_PORT)
        # print("message:", self.MESSAGE)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes("Hoi", "utf-8"), (self.udp_ip.get(), int(self.udp_port.get())))

    # 86 6c  00 1b 00

    def test_wire(self):
        packet1 = bytearray()
        packet1.append(0x04)
        packet1.append(0x31)
        packet1.append(0x31)
        packet1.append(0x3A)
        packet1.append(0x39)
        packet1.append(0x05)
        self.ser_cable.write(packet1)
        time.sleep(0.1)
        d = self.ser_cable.readline()
        s = d.decode()
        cable = int(s[4:10])
        print(cable)

    def update(self):

        # set information about the process
        self.integer_progress_show.set("updating")
        self.integer_error_com.set("")

        # boom angle get data
        self.ser_boom.write("#0%d\r\n".encode() % self.ID)

        time.sleep(0.1)
        boom_angle_read = self.ser_boom.readline()

        # cable length get data
        # ceate a package for requesting data: EOT 1 1 : 9 ENQ
        packet1 = bytearray()
        packet1.append(0x04)
        packet1.append(0x31)
        packet1.append(0x31)
        packet1.append(0x3A)
        packet1.append(0x39)
        packet1.append(0x05)
        self.ser_cable.write(packet1)
        time.sleep(0.1)
        cable_length_read = self.ser_cable.readline()

        # boom angle proses data
        # calculate the actual angle of the boom
        # calculate cable angle and cable length
        boom_angle_read_string = boom_angle_read.decode()
        angle = (float(boom_angle_read_string[43:49]) * 1.25 + 59.8)
        calculated_angle = calculate(angle)

        # show angle, cable angle and cable length in the GUI
        self.integer_cable_angle.set(round(calculated_angle[1], 2))
        self.integer_cable_length.set(round(calculated_angle[0], 2))
        self.integer_angle.set(round(angle, 2))

        # calculate x and y end points of the boom (not good yet)
        angle_in_radians = angle * math.pi / 180
        line_length = 100
        center_x = 3
        center_y = 1
        end_x = center_x * line_length * math.sin(angle_in_radians)
        end_y = center_y * line_length * math.cos(angle_in_radians)

        # extract the cable length from the received string
        cable_length_read_string = cable_length_read.decode()
        print("cable length str", cable_length_read_string)
        cable_length_read_int = int(cable_length_read_string[4:10])

        # draw crane interactive boom and cable
        self.canvas.delete(self.boom, self.wire, self.wire2, self.load)
        self.boom = self.canvas.create_line(200, 150, end_x, end_y, fill="black", width=3)  # boom
        self.wire = self.canvas.create_line(150, 49, end_x, end_y, width=2) # wire from the back of the crane to the boom
        self.wire2 = self.canvas.create_line(end_x, end_y, end_x, cable_length_read_int - 117100, fill="black", width=2)    # wire from the boom to the load
        self.load = self.canvas.create_line(end_x-5, cable_length_read_int - 117100, end_x+5, cable_length_read_int - 117100, fill="black", width=2)    # load

        # sent the angle over UDP to read it in in qinsy (format: $DATA,DATA,DATA)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes("$", "utf-8"), (self.udp_ip.get(), int(self.udp_port.get())))
        sock.sendto(bytes(str(angle), "utf-8"), (str(self.udp_ip.get()), int(self.udp_port.get())))

        # update the GUI
        root.update()
        # self.update_button.after(100, self.update)
        # time.sleep(0.1)
        self.update()

    def scan(self):
        # update progress information
        self.integer_progress_show.set("scanning")

        # call the open com function
        self.open_com()

        # start scanning device id's
        for self.ID in range(0, 11):
            # write #01 to #10 over serial
            self.ser_boom.write("#0%d\r\n".encode() % self.ID)
            self.integer_scan_return.set(self.ID)
            # read serial and write to buf
            buf = self.ser_boom.readline()
            check = buf.decode()

            # if ckeck is not empty, it means we got data, so the device id is correct.
            if check != "":
                self.ID = self.ID - 1
                self.integer_scan_return.set("#0%d" % self.ID)
                self.update()
                break

            # if id 10 is reached, no device is found. I use 10 as limit for now
            if self.ID == 10:
                self.integer_progress_show.set("no device found!")
                self.integer_error_com.set("")
                root.update()
                # take a nap for a second ;)
                time.sleep(1)
                self.integer_scan_return.set("#--")
                root.update()
            root.update()
            time.sleep(0.1)

    # create a settings window
    def settings_win(self):  # new window definition
        # read ini file
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        print("config read")

        # window settings
        setwin = Toplevel(root)
        setwin.title("settings")
        setwin.geometry("800x450+850+650")

        tabs = ttk.Notebook(setwin)

        # window stuff
        # Row 1 frame 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        w = Pmw.Group(setwin, tag_text='com port settings')
        w.grid(column=0, row=1, columnspan=10, rowspan=6, padx=3, pady=3)
        cw = Label(w.interior(), width=40, height=8)
        cw.grid(column=0, row=1, columnspan=10, rowspan=6, padx=8, pady=8)

        w = Pmw.Group(setwin, tag_text='UDP settings')
        w.grid(column=11, row=1, columnspan=10, rowspan=6, padx=3, pady=3)
        cw = Label(w.interior(), width=25, height=8)
        cw.grid(column=11, row=1, columnspan=10, rowspan=6, padx=8, pady=8)

        # Row 2 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text4 = Label(setwin, text="boom angle")
        text4.grid(column=0, row=2, columnspan=4, sticky=W+S, padx=8, pady=8)

        # Row 3 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text2 = Label(setwin, text="port")
        text2.grid(column=0, row=3, sticky=W, padx=8)

        self.entry_com_boom = Entry(setwin, width=7)
        self.entry_com_boom.insert(0, self.config['COM PORTS']['boom angle port'])
        self.entry_com_boom.grid(column=1, row=3, sticky=W)

        text3 = Label(setwin, text="baud rate")
        text3.grid(column=2, row=3, sticky=W)

        self.entry_baud_boom = Entry(setwin, width=7)
        self.entry_baud_boom.insert(0, self.config['COM PORTS']['boom angle baud'])
        self.entry_baud_boom.grid(column=3, row=3, sticky=W)

        self.udp_ip_text = Label(setwin, text="ip address")
        self.udp_ip_text.grid(column=11, row=3, sticky=W, padx=10, pady=3)

        self.udp_ip = Entry(setwin, width=10)
        self.udp_ip.insert(END, '127.0.0.1')
        self.udp_ip.grid(column=12, row=3, sticky=W, columnspan=1, padx=10, pady=3)

        # Row 3 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text4 = Label(setwin, text="wire length")
        text4.grid(column=0, row=4, columnspan=4, sticky=W, padx=8, pady=8)

        self.udp_port_text = Label(setwin, text="port")
        self.udp_port_text.grid(column=11, row=4, sticky=W, padx=10, pady=3)

        self.udp_port = Entry(setwin, width=10)
        self.udp_port.insert(END, '5005')
        self.udp_port.grid(column=12, row=4, sticky=W, columnspan=1, padx=10, pady=3)

        # Row 4 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text5 = Label(setwin, text="port")
        text5.grid(column=0, row=5, sticky=W, padx=8)

        self.entry_com_wire = Entry(setwin, width=7)
        self.entry_com_wire.insert(0, self.config['COM PORTS']['wire length port'])
        self.entry_com_wire.grid(column=1, row=5, sticky=W, pady=5)

        text6 = Label(setwin, text="baud rate")
        text6.grid(column=2, row=5, sticky=W, pady=5)

        self.entry_baud_wire = Entry(setwin, width=7)
        self.entry_baud_wire.insert(0, self.config['COM PORTS']['wire length baud'])
        self.entry_baud_wire.grid(column=3, row=5, sticky=W, pady=5)

        # Row 6 - frame 2 - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        w = Pmw.Group(setwin, tag_text='wire crane calibration settings')
        w.grid(column=0, row=7, columnspan=10, rowspan=8, padx=3, pady=3)
        cw = Label(w.interior(), width=40, height=11)
        cw.grid(column=0, row=7, columnspan=10, rowspan=8, padx=8, pady=8)

        # Row 7 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text8 = Label(setwin, text="min diameter drum")
        text8.grid(column=0, row=9, columnspan=3, padx=8, pady=8, sticky=W)

        self.entry_drum_min = Entry(setwin, width=7)
        self.entry_drum_min.insert(0, self.config['WIRE CALIBRATION']['d_drum_min'])
        self.entry_drum_min.grid(column=2, row=9, columnspan=1, padx=8, pady=8)

        # Row 8 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text9 = Label(setwin, text="max diameter drum")
        text9.grid(column=0, row=10, columnspan=3, padx=8, pady=8, sticky=W)

        self.entry_drum_max = Entry(setwin, width=7)
        self.entry_drum_max.insert(0, self.config['WIRE CALIBRATION']['d_drum_max'])
        self.entry_drum_max.grid(column=2, row=10, columnspan=1, padx=5, pady=5)

        # Row 9 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text10 = Label(setwin, text="cable")
        text10.grid(column=0, row=11, padx=8, pady=8, sticky=W)

        self.entry_cable = Entry(setwin, width=7)
        self.entry_cable.insert(0, self.config['WIRE CALIBRATION']['d_cable'])
        self.entry_cable.grid(column=2, row=11, padx=5, pady=5)

        # Row 10 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        text11 = Label(setwin, text="drum width")
        text11.grid(column=0, row=12, columnspan=2, padx=8, pady=8, sticky=W)

        self.entry_drum_width = Entry(setwin, width=7)
        self.entry_drum_width.insert(0, self.config['WIRE CALIBRATION']['drum_width'])
        self.entry_drum_width.grid(column=2, row=12, padx=5, pady=5)

        # last Row - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.calc_button = Button(setwin, text="calculate", command=lambda: calculate_total_length(
            D_drum_min=int(self.config['WIRE CALIBRATION']['d_drum_min']),
            D_drum_max=int(self.config['WIRE CALIBRATION']['d_drum_max']),
            D_cable=int(self.config['WIRE CALIBRATION']['d_cable']),
            drum_width=int(self.config['WIRE CALIBRATION']['drum_width'])))
        self.calc_button.grid(column=0, row=20, sticky=W, padx=5)

        self.save_button = Button(setwin, text="save", command=(
            lambda: self.write_ini(str(self.entry_com_boom.get()), str(self.entry_baud_boom.get()),
                                   str(self.entry_com_wire.get()), str(self.entry_baud_wire.get()),
                                   str(self.entry_drum_min.get()), str(self.entry_drum_max.get()),
                                   str(self.entry_cable.get()), str(self.entry_drum_width.get()))))
        self.save_button.grid(column=1, row=20, sticky=W, padx=5)

        self.quit_button = Button(setwin, text="close", command=setwin.destroy)
        self.quit_button.grid(column=2, row=20, sticky=W, padx=5)

        # self.config['WIRE CALIBRATION']['d_drum_min']

# self.udp_port = Entry(root)
# self.udp_port.insert(END, '5005')
# self.udp_port.grid(column=1, row=4, columnspan=2)

root = Tk()
my_gui = MyFirstGUI(root)
# C:\Users\pc_slooprijp\PycharmProjects\wirecrane
root.iconbitmap(r'C:\Users\pc_slooprijp\PycharmProjects\wirecrane\logo.ico')
root.mainloop()