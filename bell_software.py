import os
import customtkinter as ctk
from tkinter import StringVar

# corner radius, padx, pady and entry width settings for uniformaility
cr=10
px=10
py=10
entry_width=100

def main():
    # page settings
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    root.geometry("550x250")
    root.title("Bell's Inequality")
    root.resizable(False,False)
        
    # frame for buttons
    page_frame = ctk.CTkFrame(root, corner_radius=cr)
    page_frame.grid(row=0, column=0, padx=px, pady=py)
    
    # instruction label
    inst_lab = ctk.CTkLabel(page_frame, text="Select Your Procedure")
    inst_lab.grid(row=0, column=0, padx=px, pady=py)
    
    # button frame
    button_frame = ctk.CTkFrame(page_frame, corner_radius=cr)
    button_frame.grid(row=1, column=0)

    # launch epr fxn
    def launch_epr():
        os.system(f"python epr_state.py {time_var.get()} {coin_var.get()} {alpha_offset_var.get()} {beta_offset_var.get()}")
    
    # launch epr button
    epr_button = ctk.CTkButton(button_frame, text="EPR State", command=launch_epr)
    epr_button.grid(row=0, column=0, padx=px, pady=py)
    
    # launch beta sweep fxn
    def launch_beta():
        os.system(f"python beta_sweep.py {time_var.get()} {coin_var.get()} {alpha_offset_var.get()} {beta_offset_var.get()}")
    
    # launch beta sweep button
    beta_button = ctk.CTkButton(button_frame, text="Beta Sweep", command=launch_beta)
    beta_button.grid(row=1, column=0, padx=px, pady=py)
    
    # launch utility fxn
    def launch_utility():
        os.system(f"python utility.py {time_var.get()} {coin_var.get()} {alpha_offset_var.get()} {beta_offset_var.get()}")
    
    # launch beta sweep button
    util_button = ctk.CTkButton(button_frame, text="Utility", command=launch_utility)
    util_button.grid(row=2, column=0, padx=px, pady=py)
    
    # launch bell measurement fxn
    def launch_bell():
        os.system(f"python bell_measurement_page.py {time_var.get()} {coin_var.get()} {alpha_offset_var.get()} {beta_offset_var.get()}")
    
    # launch bell measurement button
    bell_button = ctk.CTkButton(button_frame, text="Bell Measurement", command=launch_bell)
    bell_button.grid(row=3, column=0, padx=px, pady=py)
    
    # settings frame
    set_frame = ctk.CTkFrame(root, corner_radius=cr)
    set_frame.grid(row=0, column=1, padx=px, pady=py)
    
    # run time, used whenever taking a measurement
    time_lab = ctk.CTkLabel(set_frame, text="Run Time (s):")
    time_lab.grid(row=0, column=0, padx=px, pady=py)
    time_var = StringVar()
    time_var.set("10")
    time_ent = ctk.CTkEntry(set_frame, textvariable=time_var, placeholder_text=time_var.get())
    time_ent.grid(row=0, column=1, padx=px, pady=py)

    # coincidence window, used whenever taking a measurement
    coin_lab = ctk.CTkLabel(set_frame, text="Coincidence Window (ns):")
    coin_lab.grid(row=1, column=0, padx=px, pady=py)
    coin_var = StringVar()
    coin_var.set("3")
    coin_ent = ctk.CTkEntry(set_frame, textvariable=coin_var, placeholder_text=coin_var.get())
    coin_ent.grid(row=1, column=1, padx=px, pady=py)
    
    # arm a polarizer offset, used in bell_measurement_page.py
    alpha_offset_lab = ctk.CTkLabel(set_frame, text="Alpha Offset (deg)")
    alpha_offset_lab.grid(row=2, column=0, padx=px, pady=py)
    alpha_offset_var = StringVar()
    alpha_offset_var.set("138")
    alpha_offset_ent = ctk.CTkEntry(set_frame, textvariable=alpha_offset_var, placeholder_text=alpha_offset_var.get())
    alpha_offset_ent.grid(row=2, column=1, padx=px, pady=py)
    
    # arm b polarizer offset, used in bell_measurement_page.py
    beta_offset_lab = ctk.CTkLabel(set_frame, text="Beta Offset (deg)")
    beta_offset_lab.grid(row=3, column=0, padx=px, pady=py)
    beta_offset_var = StringVar()
    beta_offset_var.set("0")
    beta_offset_ent = ctk.CTkEntry(set_frame, textvariable=beta_offset_var, placeholder_text=beta_offset_var.get())
    beta_offset_ent.grid(row=3, column=1, padx=px, pady=py)


    # create the page
    root.mainloop()


main()