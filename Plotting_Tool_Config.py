#V1.03
# In Plotting_Tool_Config.py

import tkinter as tk
from tkinter import ttk  # Für das ComboBox-Widget

def create_config_window(parent, update_diagram_size_callback, update_font_size_callback, update_legend_position_callback):
    config_window = tk.Toplevel(parent)
    config_window.title("Configuration")
    config_window.geometry("350x300")

    # Frame für Diagrammgrößen
    diagram_size_frame = tk.Frame(config_window)
    diagram_size_frame.pack(pady=5)

    tk.Label(diagram_size_frame, text="Diagram Width:").grid(row=0, column=0)
    diagram_width_entry = tk.Entry(diagram_size_frame, width=5)
    diagram_width_entry.grid(row=0, column=1, padx=5)

    tk.Label(diagram_size_frame, text="Diagram Height:").grid(row=0, column=2)
    diagram_height_entry = tk.Entry(diagram_size_frame, width=5)
    diagram_height_entry.grid(row=0, column=3, padx=5)

    set_size_button = tk.Button(diagram_size_frame, text="Set Size",
        command=lambda: update_diagram_size_callback(diagram_width_entry.get(), 
                                                    diagram_height_entry.get()))
    set_size_button.grid(row=0, column=4, padx=5)

    # Frame für Schriftgrößen
    font_size_frame = tk.Frame(config_window)
    font_size_frame.pack(pady=5)

    tk.Label(font_size_frame, text="Axis Font Size:").grid(row=0, column=0)
    axis_font_size_entry = tk.Entry(font_size_frame, width=5)
    axis_font_size_entry.grid(row=0, column=1, padx=5)

    tk.Label(font_size_frame, text="Title Font Size:").grid(row=0, column=2)
    title_font_size_entry = tk.Entry(font_size_frame, width=5)
    title_font_size_entry.grid(row=0, column=3, padx=5)

    set_font_button = tk.Button(font_size_frame, text="Set Font",
        command=lambda: update_font_size_callback(axis_font_size_entry.get(),
                                                  title_font_size_entry.get()))
    set_font_button.grid(row=0, column=4, padx=5)

    legend_position_frame = tk.Frame(config_window)
    legend_position_frame.pack(pady=5, fill=tk.X)  # füllt den gesamten horizontalen Raum aus

    # Label für Legendenposition
    legend_position_label = tk.Label(legend_position_frame, text="Legend Position:")
    legend_position_label.pack(side=tk.LEFT, anchor='w')  # linksbündige Ausrichtung

 # Dropdown-Menü (ComboBox) für die Legendenposition
    legend_position_options = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center', 'none']
    legend_position_combobox = ttk.Combobox(legend_position_frame, values=legend_position_options, state="readonly", width=12)
    legend_position_combobox.set('best')  # Setzt den Standardwert
    legend_position_combobox.pack(side=tk.LEFT, anchor='w', padx=(5, 0))  # linksbündige Ausrichtung und ein wenig Abstand nach rechts
    
    # Callback für die Auswahl
    def legend_position_selected(event):
        selected_position = legend_position_combobox.get()
        update_legend_position_callback(selected_position)

    # Event-Bindung für die Auswahländerung
    legend_position_combobox.bind('<<ComboboxSelected>>', legend_position_selected)