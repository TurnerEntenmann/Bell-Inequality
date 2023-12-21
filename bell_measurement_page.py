from re import S
import sys, os
import numpy as np
import pandas as pd
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import IntVar, StringVar, font
from tkinter import messagebox
from coincidence_timed_2 import get_counts


# corner radius, padx, pady, width
cr=10
px=7
py=5
w=40

# arguments passed from the main page
run_time = float(sys.argv[1]) # s
coincidence_window = float(sys.argv[2]) # ns
a_offset = float(sys.argv[3]) # deg
b_offset = float(sys.argv[4]) # deg


def main():
    # page settings
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    root.geometry("1100x600")
    root.title("Take the Bell Measurements")
    root.resizable(True,False)
    
    # bell frame
    bell_frame = ctk.CTkFrame(root, corner_radius=cr)
    bell_frame.grid(row=0, column=0, padx=px, pady=py, sticky="nsew")
    

    # table frame
    table_frame = ctk.CTkFrame(bell_frame, corner_radius=cr)
    table_frame.grid(row=0, column=0, padx=px, pady=py)
    
    # names of columns    
    ############################################################
    alpha_lab = ctk.CTkLabel(table_frame, text="alpha", width=w)
    alpha_lab.grid(row=0, column=0, padx=px, pady=py)
    
    alpha_off_lab = ctk.CTkLabel(table_frame, text="alpha with\noffset", width=w)
    alpha_off_lab.grid(row=0, column=2, padx=px, pady=py)
    
    beta_lab = ctk.CTkLabel(table_frame, text="beta", width=w)
    beta_lab.grid(row=0, column=1, padx=px, pady=py)
    
    beta_off_lab = ctk.CTkLabel(table_frame, text="beta with\noffset", width=w)
    beta_off_lab.grid(row=0, column=3, padx=px, pady=py)
    
    NA_lab = ctk.CTkLabel(table_frame, text="N_A", width=w)
    NA_lab.grid(row=0, column=4, padx=px, pady=py)
    NAs_lab = ctk.CTkLabel(table_frame, text="N_A/s", width=w)
    NAs_lab.grid(row=0, column=5, padx=px, pady=py)
    
    NB_lab = ctk.CTkLabel(table_frame, text="N_B", width=w)
    NB_lab.grid(row=0, column=6, padx=px, pady=py)
    NBs_lab = ctk.CTkLabel(table_frame, text="N_B/s", width=w)
    NBs_lab.grid(row=0, column=7, padx=px, pady=py)
    
    N_lab = ctk.CTkLabel(table_frame, text="N", width=w)
    N_lab.grid(row=0, column=8, padx=px, pady=py)
    Ns_lab = ctk.CTkLabel(table_frame, text="N/s", width=w)
    Ns_lab.grid(row=0, column=9, padx=px, pady=py)
    
    NC_lab = ctk.CTkLabel(table_frame, text="N_AC", width=w)
    NC_lab.grid(row=0, column=10, padx=px, pady=py)
    NCs_lab = ctk.CTkLabel(table_frame, text="N_AC/s", width=w)
    NCs_lab.grid(row=0, column=11, padx=px, pady=py)
    ############################################################


    # list of measurement lists
    # [[angle_a, angle_b, a, a/s, b, b/s, c, c/s, AC, AC/s], ...]
    blank_measurement = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    measurement_list = []
    for i in range(16):
        measurement_list.append(blank_measurement)

    # angle list for bell measurement
    angles_a = [-45, 0, 45, 90]
    angles_b = [-22.5, 22.5, 67.5, 112.5]

    # need this function so that each button has different params passed to it
    def make_button(a, b, idx):
        return lambda: measurement(a, b, idx)

    # default colors for buttons in dark mode
    fg_colors = ["#3a7ebf", "#1f538d"]
    hover_colors = ["#325882", "#14375e"]
    border_colors =  ["#3E454A", "#949A9F"]
    
    # fxn to populate rows
    def populate_rows():
        # what row we are on (labels are on row 0)
        row_idx = 1
        # iterate over the alpha angles
        for i in range(4):
            # iterate over the beta angles
            for j in range(4):
                # get and show alpha angle
                a_val = angles_a[i]
                a_lab = ctk.CTkLabel(table_frame, text=str(a_val), width=w)
                a_lab.grid(row=row_idx, column=0, padx=px, pady=0)
                
                # get and show beta angle
                b_val = angles_b[j]
                b_lab = ctk.CTkLabel(table_frame, text=str(b_val), width=w)
                b_lab.grid(row=row_idx, column=1, padx=px, pady=0)
                
                # get and show alpha with offset angle
                ao_val = (a_val - a_offset) % 360
                ao_lab = ctk.CTkLabel(table_frame, text=str(ao_val), width=w)
                ao_lab.grid(row=row_idx, column=2, padx=px, pady=0)
                
                # get and show beta with offset angle
                bo_val = (b_val - b_offset) % 360
                bo_lab = ctk.CTkLabel(table_frame, text=str(bo_val), width=w)
                bo_lab.grid(row=row_idx, column=3, padx=px, pady=0)
                
                # N_A
                Na_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Na_lab.grid(row=row_idx, column=4, padx=px, pady=0)
                Nas_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Nas_lab.grid(row=row_idx, column=5, padx=px, pady=0)
                
                # N_B
                Nb_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Nb_lab.grid(row=row_idx, column=6, padx=px, pady=0)
                Nbs_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Nbs_lab.grid(row=row_idx, column=7, padx=px, pady=0)
                
                # N
                N_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                N_lab.grid(row=row_idx, column=8, padx=px, pady=0)
                Ns_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Ns_lab.grid(row=row_idx, column=9, padx=px, pady=0)
                
                # N_AC
                Nac_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Nac_lab.grid(row=row_idx, column=10, padx=px, pady=0)
                Nacs_lab = ctk.CTkLabel(table_frame, text="-", width=w)
                Nacs_lab.grid(row=row_idx, column=11, padx=px, pady=0)

                # switch color every other row
                par = row_idx % 2
                
                # measurement button
                button = ctk.CTkButton(table_frame, text="Measure",
                                       fg_color=fg_colors[par], hover_color=hover_colors[par], border_color=border_colors[par],
                                       command=make_button(str(a_val), str(b_val), row_idx))
                button.grid(row=row_idx, column=12, padx=0, pady=0)

                # increment row number
                row_idx += 1
    
    # call the fxn and populate the table
    populate_rows()        

    # fxn to take measurement
    def measurement(angle_a, angle_b, idx):
        # get measurement
        a, a_s, b, b_s, c, c_s = get_counts(run_time, coincidence_window)
        
        # calc N_AC, N_AC/s
        N_AC = float((coincidence_window * 10**(-9)) * a * b)
        N_ACs = N_AC / 10
        
        # update measuremet list with values, idx is one more than the proper index because the rows start at 1
        measurement_list[idx-1] = [angle_a, angle_b, a, a_s, b, b_s, c, c_s, N_AC, N_ACs]

        # update labels
        # N_A
        Na_lab = ctk.CTkLabel(table_frame, text=str(a), width=w)
        Na_lab.grid(row=idx, column=4, padx=px, pady=0)
        Nas_lab = ctk.CTkLabel(table_frame, text=str(a_s), width=w)
        Nas_lab.grid(row=idx, column=5, padx=px, pady=0)
                
        # N_B
        Nb_lab = ctk.CTkLabel(table_frame, text=str(b), width=w)
        Nb_lab.grid(row=idx, column=6, padx=px, pady=0)
        Nbs_lab = ctk.CTkLabel(table_frame, text=str(b_s), width=w)
        Nbs_lab.grid(row=idx, column=7, padx=px, pady=0)
                
        # N
        N_lab = ctk.CTkLabel(table_frame, text=str(c), width=w)
        N_lab.grid(row=idx, column=8, padx=px, pady=0)
        Ns_lab = ctk.CTkLabel(table_frame, text=str(c_s), width=w)
        Ns_lab.grid(row=idx, column=9, padx=px, pady=0)
        
        # N_AC
        Nac_lab = ctk.CTkLabel(table_frame, text=str(N_AC), width=w)
        Nac_lab.grid(row=idx, column=10, padx=px, pady=0)
        Nacs_lab = ctk.CTkLabel(table_frame, text=str(N_ACs), width=w)
        Nacs_lab.grid(row=idx, column=11, padx=px, pady=0)


    # saving stuff frame
    save_frame = ctk.CTkFrame(bell_frame, corner_radius=cr)
    save_frame.grid(row=1, column=0, padx=px, pady=py, sticky="w")
        
    # input file name
    file_var = StringVar()
    file_var.set(os.path.join("C:\Bell_Data", "Bell_measurement_data.csv"))
    file_ent = ctk.CTkEntry(save_frame, textvariable=file_var,
                             placeholder_text=file_var.get(), width=500)
    file_ent.grid(row=0, column=0, padx=px, pady=py, sticky="e")

    # save data fxn and button
    def save_data():
        # angle_a, angle_b, a, a/s, b, b/s, c, c/s, AC, AC/s
        column_names = ["alpha", "beta", "N_A", "N_A/s", "N_B", "N_B/s", "coins", "coins/s", "N_AC", "N_AC/s"]
        try:
            save_df = pd.DataFrame(np.array(measurement_list), columns=column_names)
            save_df.to_csv(file_var.get())
            messagebox.showinfo("Save Success", f"Successfully saved data at\n{file_var.get()}")
        except Exception as e:
            CTkMessagebox(title=f"Error:\t{e}", message=f"Could not save data at\n{file_var.get()}")
            
    save_button = ctk.CTkButton(save_frame, text="Save Data", command=save_data, width=100)
    save_button.grid(row=0, column=1, padx=px, pady=py, sticky="w")


    # create the page
    root.mainloop()

main()
