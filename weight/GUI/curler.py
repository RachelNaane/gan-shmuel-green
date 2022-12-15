import subprocess
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Curl Weight")
root.configure(background='black')

tk.Label(root, text = "Direction", bg="black", fg="white").grid(row=0, column=0, sticky="w")

direction_variable = tk.StringVar(root)
direction_variable.set("None")
direction_menu = tk.OptionMenu(root, direction_variable, "In", "Out", "None")
direction_menu.grid(row=0, column=1, sticky="w")

tk.Label(root, text = "Truck ID", bg="black", fg="white").grid(row=1, column=0, sticky="w")

truck_id_entry = tk.Entry(root, bg="white")
truck_id_entry.insert(0, "T-12345")
truck_id_entry.grid(row=1, column=1, sticky="w")

tk.Label(root, text = "Container ID", bg="black", fg="white").grid(row=2, column=0, sticky="w")

container_id_entry = tk.Entry(root, bg="white")
container_id_entry.insert(0, "C-00123,C-00124")
container_id_entry.grid(row=2, column=1, sticky="w")

tk.Label(root, text = "Weight", bg="black", fg="white").grid(row=3, column=0, sticky="w")

weight_entry = tk.Entry(root, bg="white")
weight_entry.insert(0, "9000")
weight_entry.grid(row=3, column=1, sticky="w")

tk.Label(root, text = "Unit", bg="black", fg="white").grid(row=4, column=0, sticky="w")

unit_variable = tk.StringVar(root)
unit_variable.set("Kg")
unit_menu = tk.OptionMenu(root, unit_variable, "Kg", "Lbs")
unit_menu.grid(row=4, column=1, sticky="w")

tk.Label(root, text = "Force", bg="black", fg="white").grid(row=5, column=0, sticky="w")

force_variable = tk.StringVar(root)
force_variable.set("True")
force_menu = tk.OptionMenu(root, force_variable, "True", "False")
force_menu.grid(row=5, column=1, sticky="w")

tk.Label(root, text = "Fruits", bg="black", fg="white").grid(row=6, column=0, sticky="w")

fruits_variable = tk.StringVar(root)
fruits_variable.set("Navel")
fruits_menu = tk.OptionMenu(root, fruits_variable, 'Navel', 'Blood', 'Mandarin' ,'Shamuti', 'Tangerine', 'Clementine', 'Grapefruit', 'Valencia',"Else")
fruits_menu.grid(row=6, column=1, sticky="w")

def print_data():

    data = {
        "Direction": direction_variable.get(),
        "Truck_ID": truck_id_entry.get(),
        "containers": container_id_entry.get(),
        "Weight": weight_entry.get(),
        "Unit": unit_variable.get(),
        "Force": force_variable.get(),
        "Fruits": fruits_variable.get()
    }


    command = f"curl -X POST -d 'direction={data['Direction']}&truck={data['Truck_ID']}&containers={data['containers']}&weight={data['Weight']}&unit={data['Unit']}&force={data['Force']}&produce={data['Fruits']}' http://localhost:5000/weight"
    subprocess.run(command, shell=True)

tk.Button(root, text="Send Data", command=print_data, bg="black", fg="white").grid(row=7, column=0, columnspan=2)

root.mainloop()