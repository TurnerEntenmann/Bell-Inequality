import sys, os
import numpy as np
import pandas as pd
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import StringVar, font, filedialog
from coincidence_timed_2 import get_counts


# corner radius, padx, pady, width
cr=10
px=7
py=5
w=40

# arguments passed from the main page
run_time = float(sys.argv[1]) # s
coincidence_window = float(sys.argv[2]) # ns
alpha_offset = float(sys.argv[3])
beta_offset = float(sys.argv[4])


def main():
    # needed to sort listts after appending when taking a new measurement
    global data_list
    
    # page settings
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    root.geometry("1000x400")
    root.title("Beta Sweep")
    root.resizable(True,False)
    
    # update the dial label when changing the beta label
    def update_label(event):
        # avoid error when non-number angle_var
        try:
            new_angle = (beta_offset - float(angle_var.get())) % 360
            number_lab.configure(text=str(round(new_angle, 1)))
        except:
            pass
    
    # frame for beta sweep
    beta_frame = ctk.CTkFrame(root, corner_radius=cr)
    beta_frame.grid(row=0, column=0, padx=px, pady=py)
    
    # frame for measurement
    m_frame = ctk.CTkFrame(beta_frame, corner_radius=cr)
    m_frame.grid(row=1, column=0, padx=px, pady=py)

    # tell the user where to put alpha
    alpha_lab = ctk.CTkLabel(beta_frame, text=f"Set alpha to\n{np.round(alpha_offset,2)}\non the dial", font=(font.nametofont("TkDefaultFont"), 18))
    alpha_lab.grid(row=0, column=0, padx=px, pady=py)
    
    # tell the computer at what angle the user wants to measure
    angle_lab = ctk.CTkLabel(m_frame, text="Beta", font=(font.nametofont("TkDefaultFont"), 18))
    angle_lab.grid(row=0, column=0, padx=px, pady=py, sticky="w")
    angle_var = StringVar()
    angle_var.set("0")
    angle_ent = ctk.CTkEntry(m_frame, textvariable=angle_var,
                             placeholder_text=angle_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    angle_ent.grid(row=1, column=0, padx=px, pady=py)
    angle_ent.bind("<KeyRelease>", update_label)
    
    # tell the user what angle to put the dial
    dial_lab = ctk.CTkLabel(m_frame, text="Dial", font=(font.nametofont("TkDefaultFont"), 18))
    dial_lab.grid(row=0, column=2, padx=px, pady=py)
    
    arrow_lab = ctk.CTkLabel(m_frame, text="--->", font=(font.nametofont("TkDefaultFont"), 18))
    arrow_lab.grid(row=1, column=1, padx=px, pady=py)

    number_lab = ctk.CTkLabel(m_frame, text=str((0 - beta_offset) % 360),
                              width=75, height=65, fg_color="white", text_color="black",
                              font=(font.nametofont("TkDefaultFont"), 18))
    number_lab.grid(row=1, column=2, padx=px, pady=py)


    
    # fxn to draw graph
    def draw_graph():
        # make graph object and remove top and right spines
        graph = Figure(figsize=(6, 4))
        sub = graph.add_subplot(111, xlabel=r"$\beta$ ($^{\circ}$)", ylabel="Coincidences / second")
        sub.spines[["right", "top"]].set_visible(False)
        
        # plot angles as x, coins/s as y
        sub.plot([t[0] for t in data_list], [t[-1] for t in data_list], c="0", marker=".", markersize=15, linestyle=":", label=r"N(0,$\beta$)")
        
        # draw and place the graph and legend
        sub.legend(frameon=False) 
        graph.set_layout_engine("constrained")
        N00_canvas = FigureCanvasTkAgg(graph, master=root)
        N00_canvas.draw()
        N00_canvas.get_tk_widget().grid(row=0, column=1)

    # lists of angle, coincidences as [(angle, a, a/s, b, b/s, coin, coin/s), ...]
    data_list = []
    draw_graph()

    # run coincidence_timed_2.py, update data_list
    def measure():
        global data_list
        # run coincidence_timed_2.py and get count numbers, rates back
        # vals = (a, a/s, b, b/s, coins, coins/s)
        vals = get_counts(run_time, coincidence_window)
        
        # update the data list
        new = (float(angle_var.get()),) + vals
        data_list.append(new)
        
        # sort by angle
        data_list = sorted(data_list, key=lambda t: t[0])
        
        # draw graph after taking measurment
        draw_graph()
        
        # remind the user to update the angle value for the next measurement
        CTkMessagebox(title="Measurement Complete", message="Please be sure to update the angle value before the next measurement")

    # button to measure 
    measure_button = ctk.CTkButton(m_frame, text="Measure", command=measure, width=100, height=65)
    measure_button.grid(row=1, column=3, padx=px, pady=py, sticky="e")

    # frame for save stuff
    save_frame = ctk.CTkFrame(beta_frame, corner_radius=cr)
    save_frame.grid(row=2, column=0, padx=px, pady=py)

    # save to csv
    def data_to_csv():
        try:
            column_names = ["beta", "a counts", "a rates", "b counts", "b rates", "coins", "coin rates"]
            save_df = pd.DataFrame(np.array(data_list), columns=column_names)
            file_path = filedialog.asksaveasfilename(initialdir="C:\Bell_Data", filetypes=[("csv file", ".csv")], defaultextension=".csv")
            if file_path:
                save_df.to_csv(file_path)
        except Exception as e:
            CTkMessagebox(title=f"Error", message=e)

    # buttons to save data
    save_button = ctk.CTkButton(save_frame, text="Save Data", command=data_to_csv, width=200, height=75)
    save_button.grid(row=0, column=2, padx=px, pady=py)






    root.mainloop()
    
main()


