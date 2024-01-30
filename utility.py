import sys, os
import numpy as np
import pandas as pd
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar, filedialog, font
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
    root.geometry("1400x600")
    root.title("Take the Bell Measurements")
    root.resizable(True,False)
    
    var_frame = ctk.CTkFrame(root, corner_radius=cr)
    var_frame.grid(row=0, column=0, padx=px, pady=py, sticky="nsew")
    
    
    arm_frame = ctk.CTkFrame(var_frame, corner_radius=cr)
    arm_frame.grid(row=0, column=0, padx=px, pady=py, sticky="nsew")    
    arm_lab = ctk.CTkLabel(arm_frame, text="Arm Angle", font=(font.nametofont("TkDefaultFont"), 18))
    arm_lab.grid(row=0, column=0, padx=px, pady=py, sticky="w")
    arm_var = StringVar()
    arm_var.set("7.7")
    arm_ent = ctk.CTkEntry(arm_frame, textvariable=arm_var,
                             placeholder_text=arm_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    arm_ent.grid(row=0, column=1, padx=px, pady=py, sticky="e")

    
    ta_frame = ctk.CTkFrame(var_frame, corner_radius=cr)
    ta_frame.grid(row=1, column=0, padx=px, pady=py, sticky="nsew")    
    ta_lab = ctk.CTkLabel(ta_frame, text="Polarizer A Angle on Dial", font=(font.nametofont("TkDefaultFont"), 18))
    ta_lab.grid(row=0, column=0, padx=px, pady=py, sticky="w")
    ta_var = StringVar()
    ta_var.set(str(a_offset))
    ta_ent = ctk.CTkEntry(ta_frame, textvariable=ta_var,
                             placeholder_text=ta_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    ta_ent.grid(row=0, column=1, padx=px, pady=py, sticky="e")
    
    tb_frame = ctk.CTkFrame(var_frame, corner_radius=cr)
    tb_frame.grid(row=2, column=0, padx=px, pady=py, sticky="nsew")    
    tb_lab = ctk.CTkLabel(tb_frame, text="Polarizer B Angle on Dial", font=(font.nametofont("TkDefaultFont"), 18))
    tb_lab.grid(row=0, column=0, padx=px, pady=py, sticky="w")
    tb_var = StringVar()
    tb_var.set(str(b_offset))
    tb_ent = ctk.CTkEntry(tb_frame, textvariable=tb_var,
                             placeholder_text=tb_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    tb_ent.grid(row=0, column=1, padx=px, pady=py, sticky="e")
    
    
    l2_frame = ctk.CTkFrame(var_frame, corner_radius=cr)
    l2_frame.grid(row=3, column=0, padx=px, pady=py, sticky="nsew")    
    l2_lab = ctk.CTkLabel(l2_frame, text="lambda / 2 Angle", font=(font.nametofont("TkDefaultFont"), 18))
    l2_lab.grid(row=0, column=0, padx=px, pady=py, sticky="w")
    l2_var = StringVar()
    l2_var.set(str(262))
    l2_ent = ctk.CTkEntry(l2_frame, textvariable=l2_var,
                             placeholder_text=l2_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    l2_ent.grid(row=0, column=1, padx=px, pady=py, sticky="e")
    
    qp_frame = ctk.CTkFrame(var_frame, corner_radius=cr)
    qp_frame.grid(row=4, column=0, padx=px, pady=py, sticky="nsew")    
    qp_lab = ctk.CTkLabel(qp_frame, text="Quartz Plate Angle", font=(font.nametofont("TkDefaultFont"), 18))
    qp_lab.grid(row=0, column=0, padx=px, pady=py, sticky="w")
    qp_var = StringVar()
    qp_var.set(str(268))
    qp_ent = ctk.CTkEntry(qp_frame, textvariable=qp_var,
                             placeholder_text=qp_var.get(),
                             width=75, height=65, font=(font.nametofont("TkDefaultFont"), 23),
                             fg_color="white", text_color="black", justify="center")
    qp_ent.grid(row=0, column=1, padx=px, pady=py, sticky="e")

    
    
    # table frame
    table_frame = ctk.CTkFrame(root, corner_radius=cr)
    table_frame.grid(row=0, column=1, padx=px, pady=py)
    
    # names of columns    
    ############################################################
    arm_ang_lab = ctk.CTkLabel(table_frame, text="arm angle", width=w)
    arm_ang_lab.grid(row=0, column=0, padx=px, pady=py)
    
    alpha_lab = ctk.CTkLabel(table_frame, text="alpha", width=w)
    alpha_lab.grid(row=0, column=1, padx=px, pady=py)
    
    alpha_off_lab = ctk.CTkLabel(table_frame, text="alpha with\noffset", width=w)
    alpha_off_lab.grid(row=0, column=3, padx=px, pady=py)
    
    beta_lab = ctk.CTkLabel(table_frame, text="beta", width=w)
    beta_lab.grid(row=0, column=2, padx=px, pady=py)
    
    beta_off_lab = ctk.CTkLabel(table_frame, text="beta with\noffset", width=w)
    beta_off_lab.grid(row=0, column=4, padx=px, pady=py)
    
    lambda_lab = ctk.CTkLabel(table_frame, text="lambda/2 angle", width=w)
    lambda_lab.grid(row=0, column=5, padx=px, pady=py)
    
    quartz_lab = ctk.CTkLabel(table_frame, text="quartz plate angle", width=w)
    quartz_lab.grid(row=0, column=6, padx=px, pady=py)
    
    NA_lab = ctk.CTkLabel(table_frame, text="N_A", width=w)
    NA_lab.grid(row=0, column=7, padx=px, pady=py)
    NAs_lab = ctk.CTkLabel(table_frame, text="N_A/s", width=w)
    NAs_lab.grid(row=0, column=8, padx=px, pady=py)
    
    NB_lab = ctk.CTkLabel(table_frame, text="N_B", width=w)
    NB_lab.grid(row=0, column=9, padx=px, pady=py)
    NBs_lab = ctk.CTkLabel(table_frame, text="N_B/s", width=w)
    NBs_lab.grid(row=0, column=10, padx=px, pady=py)
    
    N_lab = ctk.CTkLabel(table_frame, text="N", width=w)
    N_lab.grid(row=0, column=11, padx=px, pady=py)
    Ns_lab = ctk.CTkLabel(table_frame, text="N/s", width=w)
    Ns_lab.grid(row=0, column=12, padx=px, pady=py)
    
    NC_lab = ctk.CTkLabel(table_frame, text="N_AC", width=w)
    NC_lab.grid(row=0, column=13, padx=px, pady=py)
    NCs_lab = ctk.CTkLabel(table_frame, text="N_AC/s", width=w)
    NCs_lab.grid(row=0, column=14, padx=px, pady=py)
    ############################################################
    
    # store measurements
    # [[arm angle, alpha, polarizer a, beta, polarizer b, lambda/2, qp, a, a_s, b, b_s, c, c_s, N_AC, N_ACs], ... , [...]]
    measurement_list = []
    
    def measure():
        idx = len(measurement_list)
        # get input params
        arm_val = arm_ent.get()
        pol_a_val = ta_ent.get()
        alpha = (a_offset - float(pol_a_val)) % 360
        pol_b_val = tb_ent.get()
        beta = (b_offset - float(pol_b_val)) % 360
        l2_val = l2_ent.get()
        qp_val = qp_ent.get()
        
        # get measurement
        a, a_s, b, b_s, c, c_s = get_counts(run_time, coincidence_window)
        
        # calc N_AC, N_AC/s
        N_AC = float((coincidence_window * 10**(-9)) * a * b)
        N_ACs = N_AC / 10
        
        # update measuremet list with values, idx is one more than the proper index because the rows start at 1
        measurement_list.append([arm_val, alpha, pol_a_val, beta, pol_b_val, l2_val, qp_val, a, a_s, b, b_s, c, c_s, N_AC, N_ACs])

        # update labels
        # arm angle
        arm_angle = ctk.CTkLabel(table_frame, text=str(arm_val), width=w)
        arm_angle.grid(row=idx+1, column=0, padx=px, pady=0)
        
        # alpha
        alpha_lab = ctk.CTkLabel(table_frame, text=str(alpha), width=w)
        alpha_lab.grid(row=idx+1, column=1, padx=px, pady=0)
        
        # alpha with offset
        alpha_off_lab = ctk.CTkLabel(table_frame, text=str(pol_a_val), width=w)
        alpha_off_lab.grid(row=idx+1, column=2, padx=px, pady=0)
        
        # beta
        beta_lab = ctk.CTkLabel(table_frame, text=str(beta), width=w)
        beta_lab.grid(row=idx+1, column=3, padx=px, pady=0)
        
        # beta with offset
        alpha_off_lab = ctk.CTkLabel(table_frame, text=str(pol_b_val), width=w)
        alpha_off_lab.grid(row=idx+1, column=4, padx=px, pady=0)
        
        # lambda/2
        lam_lab = ctk.CTkLabel(table_frame, text=str(l2_val), width=w)
        lam_lab.grid(row=idx+1, column=5, padx=px, pady=0)
        
        # quartz plate
        q_lab = ctk.CTkLabel(table_frame, text=str(qp_val), width=w)
        q_lab.grid(row=idx+1, column=6, padx=px, pady=0)
        
        # N_A
        Na_lab = ctk.CTkLabel(table_frame, text=str(a), width=w)
        Na_lab.grid(row=idx+1, column=7, padx=px, pady=0)
        Nas_lab = ctk.CTkLabel(table_frame, text=str(a_s), width=w)
        Nas_lab.grid(row=idx+1, column=8, padx=px, pady=0)
                
        # N_B
        Nb_lab = ctk.CTkLabel(table_frame, text=str(b), width=w)
        Nb_lab.grid(row=idx+1, column=9, padx=px, pady=0)
        Nbs_lab = ctk.CTkLabel(table_frame, text=str(b_s), width=w)
        Nbs_lab.grid(row=idx+1, column=10, padx=px, pady=0)
                
        # N
        N_lab = ctk.CTkLabel(table_frame, text=str(c), width=w)
        N_lab.grid(row=idx+1, column=11, padx=px, pady=0)
        Ns_lab = ctk.CTkLabel(table_frame, text=str(c_s), width=w)
        Ns_lab.grid(row=idx+1, column=12, padx=px, pady=0)
        
        # N_AC
        Nac_lab = ctk.CTkLabel(table_frame, text=str(N_AC), width=w)
        Nac_lab.grid(row=idx+1, column=13, padx=px, pady=0)
        Nacs_lab = ctk.CTkLabel(table_frame, text=str(N_ACs), width=w)
        Nacs_lab.grid(row=idx+1, column=14, padx=px, pady=0)
    
    
    # button to measure 
    measure_button = ctk.CTkButton(root, text="Measure", command=measure, width=100, height=65)
    measure_button.grid(row=1, column=0, padx=px, pady=py, sticky="w")
    
    # save to csv
    def data_to_csv():
        try:
            # [arm_val, alpha, pol_a_val, beta, pol_b_val, l2_val, qp_val, a, a_s, b, b_s, c, c_s, N_AC, N_ACs]
            column_names = ["arm_angle", "alpha", "alpha dial", "beta", "beta dial", "lambda/2", "quartz", "NA", "NA/s", "NB", "NB/s", "coins", "coins/s", "N_AC", "N_AC/s"]
            save_df = pd.DataFrame(np.array(measurement_list), columns=column_names)
            file_path = filedialog.asksaveasfilename(initialdir="C:\Bell_Data", filetypes=[("csv file", ".csv")], defaultextension=".csv")
            if file_path:
                save_df.to_csv(file_path)
        except Exception as e:
            CTkMessagebox(title=f"Error", message=e)

    # buttons to save data
    save_button = ctk.CTkButton(root, text="Save Data", command=data_to_csv, width=200, height=75)
    save_button.grid(row=1, column=1, padx=px, pady=py)
    
    root.mainloop()    
    
main()