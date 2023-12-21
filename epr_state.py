# page to make epr state
import sys, subprocess, re, os, threading
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
from tkinter import IntVar, StringVar, DoubleVar, font
from CTkMessagebox import CTkMessagebox
from coincidence_timed_2 import get_counts

# corner radius, padx and pady
cr=5
px=7
py=3

# get run time from bell_software.py
run_time = sys.argv[1] # s
coincidence_window = sys.argv[2] # ns

def main():
    # needed to sort listts after appending when taking a new measurement
    global N00_list, N90_list, N45_list, N00_ab_list, N90_ab_list, progress_bar
    
    # page settings
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    root.geometry("1300x900")
    root.title("Create the EPR State")
    root.resizable(False,False)
    
    # epr_frame
    epr_frame = ctk.CTkFrame(root, corner_radius=cr)
    epr_frame.grid(row=0, column=0, padx=px, pady=py)

    # frame for equalizing N00, N9090
    eql_frame = ctk.CTkFrame(epr_frame, corner_radius=cr)
    eql_frame.grid(row=0, column=0, padx=px, pady=py)
    
    # label for equalizing N00, N9090
    eql_lab = ctk.CTkLabel(eql_frame, text="Equalize N(0,0) & N(90,90)")
    eql_lab.configure(font=(font.nametofont("TkDefaultFont"), 20))
    eql_lab.grid(row=0, column=0, padx=px, pady=py, columnspan=3)

    # N labels
    N00_lab = ctk.CTkLabel(eql_frame, text="N(0,0)", font=(font.nametofont("TkDefaultFont"), 15), justify="right")
    N00_lab.grid(row=1, column=0, padx=px, pady=py)
    N9090_lab = ctk.CTkLabel(eql_frame, text="N(90,90)", font=(font.nametofont("TkDefaultFont"), 15), justify="left")
    N9090_lab.grid(row=1, column=2, padx=px, pady=py)

    # tell the program if the user is taking 00 or 9090 data
    N_var = IntVar()
    N_button = ctk.CTkSwitch(eql_frame, text=None, variable=N_var, width=150, switch_width=150,
                             progress_color="transparent")
    N_button.grid(row=1, column=1, padx=px, pady=py)

    # tell the computer at what angle the arms are
    angle_lab = ctk.CTkLabel(eql_frame, text="Arm Angle", font=(font.nametofont("TkDefaultFont"), 18))
    angle_lab.grid(row=2, column=0, padx=px, pady=py)
    angle_var = StringVar()
    angle_var.set("7.0")
    angle_ent = ctk.CTkEntry(eql_frame, textvariable=angle_var,
                             placeholder_text=angle_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    angle_ent.grid(row=2, column=1, padx=px, pady=py)
    

    # fxn to draw N00 N9090 graph
    def draw_N00_graph():
        # make graph object and remove top and right spines
        N00_graph = Figure(figsize=(6, 4))
        N00_sub = N00_graph.add_subplot(111, xlabel=r"Arm Angle ($^{\circ}$)", ylabel="Coincidences / second")
        N00_sub.spines[["right", "top"]].set_visible(False)
        
        # plot angles as x, coins/s as y, 00 is black, 9090 is red
        N00_sub.plot([t[0] for t in N00_list], [t[-1] for t in N00_list], c="0", marker=".", markersize=15, linestyle=":", label="N(0,0)")
        N00_sub.plot([t[0] for t in N90_list], [t[-1] for t in N90_list], c="r", marker=".", markersize=15, linestyle=":", label="N(90,90)")
        
        # draw and place the graph and legend
        N00_sub.legend(frameon=False) 
        N00_graph.set_layout_engine("constrained")
        N00_canvas = FigureCanvasTkAgg(N00_graph, master=eql_frame)
        N00_canvas.draw()
        N00_canvas.get_tk_widget().grid(row=0, column=3, rowspan=4)
    
    # lists of angle, coincidences as [(angle, a, a/s, b, b/s, coin, coin/s), ...]
    N00_list = []
    N90_list = []
    
    # example of full sweep
    # N00_list = [(7.1, 0, 0, 0, 0, 1, 40), (7.2, 0, 0, 0, 0, 1, 85), (7.3, 0, 0, 0, 0, 1, 120), (7.4, 0, 0, 0, 0, 1, 135), (7.5, 0, 0, 0, 0, 1, 155), (7.6, 0, 0, 0, 0, 1, 140), (7.7, 0, 0, 0, 0, 1, 95)]
    # N90_list = [(7.1, 0, 0, 0, 0, 1, 30), (7.2, 0, 0, 0, 0, 1, 65), (7.3, 0, 0, 0, 0, 1, 115), (7.4, 0, 0, 0, 0, 1, 143), (7.5, 0, 0, 0, 0, 1, 160), (7.6, 0, 0, 0, 0, 1, 150), (7.7, 0, 0, 0, 0, 1, 100)]
    
    # draw blank graph when opening the page
    draw_N00_graph()

    # run coincidence_timed_2.py, update NXX_list depending on N_var
    def N00_measure():
        global N00_list, N90_list, run_time, coincidence_window, progress_bar            
        # run coincidence_timed_2.py and get count numbers, rates back
        # vals = (a, a/s, b, b/s, coins, coins/s)
        vals = get_counts(run_time, coincidence_window)
        # update the correct list
        if N_var.get() == 0:
            new = (float(angle_var.get()),) + vals
            N00_list.append(new)
            # sort by angle
            N00_list = sorted(N00_list, key=lambda t: t[0])
        else:
            new = (float(angle_var.get()),) + vals
            N90_list.append(new)
            # sort by angle
            N90_list = sorted(N90_list, key=lambda t: t[0])  
        
        # draw graph after taking measurment
        draw_N00_graph()
        
        # remind the user to update the angle value for the next measurement
        CTkMessagebox(title="Measurement Complete", message="Please be sure to update the angle value before the next measurement")

    # button to measure N00 or N9090
    N00_measure_button = ctk.CTkButton(eql_frame, text="Measure", command=N00_measure, width=100)
    N00_measure_button.grid(row=2, column=2, padx=px, pady=py)
    
    # save stuff frame
    save_frame = ctk.CTkFrame(eql_frame, corner_radius=cr)
    save_frame.grid(row=3, column=0, columnspan=3)

    # input file names
    # N00
    N00_file_var = StringVar()
    N00_file_var.set(os.path.join(r"C:\Bell_Data", "N00_equalize_data.csv"))
    N00_file_ent = ctk.CTkEntry(save_frame, textvariable=N00_file_var,
                             placeholder_text=N00_file_var.get(), width=500)
    N00_file_ent.grid(row=0, column=0, columnspan=2, padx=px, pady=py)
    
    # N9090
    N90_file_var = StringVar()
    N90_file_var.set(os.path.join(r"C:\Bell_Data", "N90_equalize_data.csv"))
    N90_file_ent = ctk.CTkEntry(save_frame, textvariable=N90_file_var,
                             placeholder_text=N00_file_var.get(), width=500)
    N90_file_ent.grid(row=1, column=0, columnspan=2, padx=px, pady=py)
    

    # fxn to save equalize data
    def N00_to_csv():
        column_names = ["angles", "a counts", "a rates", "b counts", "b rates", "coins", "coin rates"]
        save_df = pd.DataFrame(np.array(N00_list), columns=column_names)
        save_df.to_csv(N00_file_var.get())
        
    def N90_to_csv():
        column_names = ["angles", "a counts", "a rates", "b counts", "b rates", "coins", "coin rates"]
        save_df = pd.DataFrame(np.array(N90_list), columns=column_names)
        save_df.to_csv(N90_file_var.get())

    # buttons to save equalize data
    # N00
    N00_save_button = ctk.CTkButton(save_frame, text="Save N(0,0) Data", command=N00_to_csv, width=100)
    N00_save_button.grid(row=0, column=2, padx=px, pady=py)
    
    #N9090
    N90_save_button = ctk.CTkButton(save_frame, text="Save N(90, 90) Data", command=N90_to_csv, width=100)
    N90_save_button.grid(row=1, column=2, padx=px, pady=py)

    # end of equalizing sweep stuff
    # start of maximizing N4545 stuff

    # frame for maximizing N4545
    max_frame = ctk.CTkFrame(root, corner_radius=cr)
    max_frame.grid(row=1, column=0, padx=px, pady=py)

    # label for the maximization
    max_lab = ctk.CTkLabel(max_frame, text="Maximize N(45,45)")
    max_lab.configure(font=(font.nametofont("TkDefaultFont"), 20))
    max_lab.grid(row=0, column=0, padx=px, pady=py, columnspan=3)

    # entry for quatz plate angle
    qp_angle_lab = ctk.CTkLabel(max_frame, text="Quartz Plate Angle\n(about vertical)", font=(font.nametofont("TkDefaultFont"), 18))    
    qp_angle_lab.grid(row=1, column=0, padx=px, pady=py)
    qp_angle_var = StringVar()
    qp_angle_var.set("35")
    qp_angle_ent = ctk.CTkEntry(max_frame, textvariable=qp_angle_var,
                             placeholder_text=qp_angle_var.get(), width=75,
                             height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    qp_angle_ent.grid(row=1, column=1, padx=px, pady=py)

    # fxn to draw N4545 graph
    def draw_N45_graph():
        # make graph object and remove top and right spines
        N45_graph = Figure(figsize=(6, 4))
        N45_sub = N45_graph.add_subplot(111, xlabel=r"Quartz Plate Angle ($^{\circ}$)", ylabel="Coincidences / second")
        N45_sub.spines[["right", "top"]].set_visible(False)

         # plot angles as x, coins/s as y, 00 is black, 9090 is red
        N45_sub.plot([t[0] for t in N45_list], [t[-1] for t in N45_list], c="0", marker=".", markersize=15, linestyle=":", label="N(45,45)")

        # draw and place the graph and legend
        N45_sub.legend(frameon=False)
        N45_graph.set_layout_engine("constrained")
        N45_canvas = FigureCanvasTkAgg(N45_graph, master=max_frame)
        N45_canvas.draw()
        N45_canvas.get_tk_widget().grid(row=0, column=3, rowspan=4)


    # lits for angles and coincidences
    # (angle, a, a/s, b, b/s, coin, coin/s)    
    N45_list = []
    # example sweep
    # N45_list = [(0, 0, 0, 0, 0, 0, 130), (10, 0, 0, 0, 0, 0, 125), (15, 0, 0, 0, 0, 0, 80), (25, 0, 0, 0, 0, 0, 20), (33, 0, 0, 0, 0, 0, 80), (37, 0, 0, 0, 0, 0, 115), (39, 0, 0, 0, 0, 0, 120), (40, 0, 0, 0, 0, 0, 145), (41, 0, 0, 0, 0, 0, 143), (45, 0, 0, 0, 0, 0, 60), (55, 0, 0, 0, 0, 0, 0)]
    
    # draw_N45_graph needs N45_list to exist so it is called after N45_list = []
    draw_N45_graph()
    
    # run coincidence_timed_2.py, update N45_list
    def N45_measure():
        global N45_list
        # run coincidence_timed_2.py and get count numbers back
        # vals = (a, a/s, b, b/s, coins, coins/s)
        vals = get_counts(run_time, coincidence_window)
        # update list
        new = (float(qp_angle_var.get()),) + vals
        N45_list.append(new)

        # sort list 
        N45_list = sorted(N45_list, key=lambda t: t[0])
        
        # draw graph
        draw_N45_graph()

    # button to measure N4545
    N45_measure_button = ctk.CTkButton(max_frame, text="Measure", command=N45_measure, width=100)
    N45_measure_button.grid(row=1, column=2, padx=px, pady=py)

    # input file name
    N45_file_var = StringVar()
    N45_file_var.set(os.path.join(r"C:\Bell_Data", "maximize.csv"))
    N45_file_ent = ctk.CTkEntry(max_frame, textvariable=N45_file_var,
                             placeholder_text=N45_file_var.get(), width=500)
    N45_file_ent.grid(row=2, column=0, columnspan=2, padx=px, pady=py)

    # fxn & button to save data
    def N45_to_csv():
        column_names = ["angles", "a counts", "a rates", "b counts", "b rates", "coins", "coin rates"]
        # the np.array().T is to get the shape right
        save_df = pd.DataFrame(np.array(N45_list), columns=column_names)
        save_df.to_csv(N45_file_var.get())
    
    N45_save_button = ctk.CTkButton(max_frame, text="Save Data", command=N45_to_csv, width=100)
    N45_save_button.grid(row=2, column=2, padx=px, pady=py)
    
    
    # create the page
    root.mainloop()

main()
