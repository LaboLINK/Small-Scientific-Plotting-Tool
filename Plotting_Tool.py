# In Plotting_Tool.py

#pip install pandas matplotlib numpy Pillow
#Python 3.11.0
import tkinter as tk
from tkinter import Toplevel, Entry, Label, Button
from tkinter import simpledialog
from tkinter import filedialog, ttk, colorchooser
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from Plotting_Tool_Config import create_config_window

global start_interval_entry, end_interval_entry
start_interval_entry = None
end_interval_entry = None

global start_interval, end_interval
start_interval = 0  # Standardwert für das Startintervall
end_interval = 0    # Standardwert für das Endintervall
# Globale Variablen für die Säulendiagramm Eingabefelder

global y_label_entry, title_entry

# Globale Variable für Linienstile
line_styles = {}

# Globale Variablen für die Diagrammgröße 900*600 = 150 DPI
DIAGRAM_WIDTH = 900 / 80  # Breite in Zoll
DIAGRAM_HEIGHT = 600 / 80  # Höhe in Zoll

# Globale Variablen für Schriftgrößen
global axis_font_size, title_font_size
axis_font_size = 16  # Standardgröße für Achsenbeschriftungen
title_font_size = 18  # Standardgröße für den Diagrammtitel

global show_data_points
show_data_points = False  # Standardmäßig sind Datenpunkte nicht sichtbar


# Globale Variable für die Position der Legende
global legend_position
legend_position = 'best'  # Automatische Positionierung

global SHOW_BAR_VALUES
SHOW_BAR_VALUES = False  # Setzen Sie auf False, wenn Sie die Werte nicht anzeigen möchten

global is_dialog_open
is_dialog_open = False

ROTATE_LABELS = True  # Setzen Sie dies auf False, um die Beschriftungen nicht zu drehen
AUTO_ADJUST_LABELS = True  # Setzen Sie dies auf False, um die automatische Anpassung zu deaktivieren
ROTATION_ANGLE = 45  # Winkel für die Rotation der Beschriftungen

def toggle_data_points():
    selected_items = tree.selection()
    for item in selected_items:
        axis_data = tree.item(item, 'values')[3]
        if 'X' in axis_data:
            new_axis_data = axis_data.replace('X', '')  # Entferne das 'X'
        else:
            new_axis_data = axis_data + 'X'  # Füge das 'X' hinzu
        tree.set(item, column='Select Axis', value=new_axis_data)

def reset_settings():
    """
    Setzt alle Einstellungen auf die Standardwerte zurück.
    """
    global start_interval, end_interval, df
    # Setzen Sie hier alle weiteren globalen Variablen zurück, die Sie haben
    start_interval = 0
    end_interval = 0
    df = None
    # Setzen Sie hier die Standardwerte für alle Tkinter-Elemente zurück
    title_entry.delete(0, tk.END)
    x_axis_entry.delete(0, tk.END)
    y_axis_entry.delete(0, tk.END)
    y_sec_axis_entry.delete(0, tk.END)
    # Aktualisieren Sie weitere Elemente nach Bedarf
    
def show_info():
    # Erstellen eines neuen Toplevel-Fensters
    info_window = tk.Toplevel(root)
    info_window.title("About")

    # Textinformationen
    info_label = tk.Label(info_window, text="Created by R.J\nProvided by LaboLINK\nVersion 1.00")
    info_label.pack()

    # Bild laden
    image_path = "C:/Users/OoUbu/OneDrive/Dokumente/VS_CODE/AddONs/htdocs/img/Lab.png"
    try:
        image = Image.open(image_path)

        # Bildgröße um die Hälfte reduzieren
        image = image.resize((int(image.width / 4), int(image.height / 4)), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image)

        # Label für das Bild
        image_label = tk.Label(info_window, image=photo)
        image_label.image = photo  # Referenz halten
        image_label.pack()
    except Exception as e:
        print(f"Fehler beim Laden des Bildes: {e}")

    # Schließen-Button
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack()

def open_database():
    print("Database-Funktion ausgelöst")

def open_config():
    create_config_window(root, update_config)

def update_diagram_size(width, height):
    global DIAGRAM_WIDTH, DIAGRAM_HEIGHT
    # ... Logik zur Aktualisierung der Diagrammgrößen ...

def update_font_size(axis_font, title_font):
    global axis_font_size, title_font_size
    # ... Logik zur Aktualisierung der Schriftgrößen ...

def open_config():

    create_config_window(root, update_diagram_size, update_font_size, update_legend_position)

def update_legend_position(position):
    global legend_position
    legend_position = position
    
def load_excel_file():
    global df, table_ranges  # Wir verwenden table_ranges statt table_starts
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        df = pd.read_excel(file_path)
        table_ranges = []
        find_table_ranges()  # Findet Start- und Endpunkte der Tabellen
        update_treeview()

def find_table_ranges():
    is_first_column = True
    start = 0
    for i, column in enumerate(df.columns):
        if pd.isna(df[column]).all():
            if not is_first_column:
                end = i - 1
                table_ranges.append((start, end))
                start = i + 1
                is_first_column = True
        else:
            if is_first_column:
                start = i
                is_first_column = False
    table_ranges.append((start, len(df.columns) - 1))  # Fügt die letzte Tabelle hinzu

def update_treeview():
    for i in tree.get_children():
        tree.delete(i)
    is_first_column = True
    skip_column = True
    index = 1

    for i, column in enumerate(df.columns):
        if pd.isna(df[column]).all():
            if not is_first_column:
                tree.insert('', 'end', values=('', '----', '', ''))
                index = 1
            is_first_column = True
            skip_column = True
        else:
            if is_first_column:
                table_starts.append(i)
                is_first_column = False
            if skip_column:
                skip_column = False
                continue
            tree.insert('', 'end', values=(index, column, '[Choose Color]', ''))
            index += 1

def plot_data():
    global title_font_size
    selected_items = tree.selection()
    if selected_items and df is not None:
        fig, ax1 = plt.subplots(figsize=(DIAGRAM_WIDTH, DIAGRAM_HEIGHT))

        use_secondary_axis = any('S' in tree.item(item)['values'][3] for item in selected_items)

        if use_secondary_axis:
            ax2 = ax1.twinx()

        for item in selected_items:
            column = tree.item(item)['values'][1]
            axis_choice = tree.item(item)['values'][3]
            color = tree.item(item)['values'][2]
            line_style = tree.item(item)['values'][4]  # Linienstil aus Treeview erhalten

            # Entscheiden, ob Linienstil gestrichelt sein soll
            if line_style == 'D':
                line_style = '--'
            else:
                line_style = '-'  # Standard-Linienstil

            for start, end in table_ranges:
                if df.columns.get_loc(column) >= start and df.columns.get_loc(column) <= end:
                    x_column = df.columns[start]
                    if 'S' in axis_choice:
                        ax = ax2 if use_secondary_axis else ax1
                    else:
                        ax = ax1
                    ax.plot(df[x_column], df[column], label=column, color=color, linestyle=line_style)  # Linienstil anwenden
                    if 'X' in axis_choice:
                        ax.scatter(df[x_column], df[column], color=color, marker='x')
                    break

 # Überprüfen, ob das title_entry Widget existiert und nicht leer ist
        if title_entry.winfo_exists():
            title = title_entry.get()
            if title:  # Wenn ein Titel vorhanden ist, verwenden Sie diesen
                plt.title(title, fontsize=title_font_size)
        # Legenden und Achsenbeschriftungen
        
    ax1.set_xlabel(x_axis_entry.get(), fontsize=axis_font_size)
    ax1.set_ylabel(y_axis_entry.get(), fontsize=axis_font_size)
    if use_secondary_axis:
        ax2.set_ylabel(y_sec_axis_entry.get(), fontsize=axis_font_size)
    plt.title(title_entry.get(), fontsize=title_font_size)

    # Legenden (mit Überprüfung auf 'none')
    if legend_position != 'none':
        lines, labels = ax1.get_legend_handles_labels()
        if use_secondary_axis:
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines + lines2, labels + labels2, loc=legend_position)
        else:
            ax1.legend(lines, labels, loc=legend_position)

    plt.show()

def plot_data_interval():
    global df
    selected_items = tree.selection()
    if selected_items and df is not None:
        # Konvertiere Start- und Endintervall in Indizes
        try:
            start_value = float(start_interval_entry.get())
            end_value = float(end_interval_entry.get())
        except ValueError:
            print("Bitte gültige Zahlen für das Intervall eingeben")
            return

        # Finde die nächstgelegenen Indizes für Start- und Endwerte
        x_column = df.columns[table_ranges[0][0]]  # Annahme: x-Werte sind in der ersten Spalte jeder Tabelle
        start_idx = find_nearest_index(df[x_column], start_value)
        end_idx = find_nearest_index(df[x_column], end_value)

        # Überprüfen, ob das Intervall gültig ist
        if start_idx >= end_idx:
            print("Ungültiges Intervall: Start muss kleiner als Ende sein")
            return

        # Filtern der Daten nach dem angegebenen Intervall
        df_interval = df.iloc[start_idx:end_idx + 1]

        fig, ax1 = plt.subplots(figsize=(DIAGRAM_WIDTH, DIAGRAM_HEIGHT))

        use_secondary_axis = any(tree.item(item)['values'][3] == 'S' for item in selected_items)

        if use_secondary_axis:
            ax2 = ax1.twinx()

        for item in selected_items:
            column = tree.item(item)['values'][1]
            axis_choice = tree.item(item)['values'][3]
            color = tree.item(item)['values'][2]

            for start, end in table_ranges:
                if df.columns.get_loc(column) >= start and df.columns.get_loc(column) <= end:
                    if axis_choice == 'S' and use_secondary_axis:
                        ax2.plot(df_interval[x_column], df_interval[column], label=column, color=color)
                    else:
                        ax1.plot(df_interval[x_column], df_interval[column], label=column, color=color)
                    break

    ax1.set_xlabel(x_axis_entry.get(), fontsize=axis_font_size)
    ax1.set_ylabel(y_axis_entry.get(), fontsize=axis_font_size)
    if use_secondary_axis:
        ax2.set_ylabel(y_sec_axis_entry.get(), fontsize=axis_font_size)
    plt.title(title_entry.get(), fontsize=title_font_size)

    # Legenden (mit Überprüfung auf 'none')
    if legend_position != 'none':
        lines, labels = ax1.get_legend_handles_labels()
        if use_secondary_axis:
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines + lines2, labels + labels2, loc=legend_position)
        else:
            ax1.legend(lines, labels, loc=legend_position)

    plt.show()

def find_nearest_index(array, value):
    """
    Findet den Index des Wertes im 'array', der dem 'value' am nächsten ist.
    """
    array = pd.to_numeric(array, errors='coerce')
    idx = (np.abs(array - value)).idxmin()
    return idx

def create_color_style(color_hex):
    style_name = f"Treeview.Color.{color_hex}"
    style.map(style_name, foreground=[('!selected', color_hex)])
    return style_name

def set_color():
    selected_item = tree.selection()
    color = colorchooser.askcolor()[1]
    if selected_item and color:
        color_style = create_color_style(color)
        for item in selected_item:
            tree.item(item, values=(tree.item(item)['values'][0], tree.item(item)['values'][1], color, tree.item(item)['values'][3]))
            tree.tag_configure(color, foreground=color)
            tree.tag_bind(color, '<1>', lambda e: print(e.widget.item(e.widget.selection())))
            tree.set(item, column='Set Color', value=color)
            tree.item(item, tags=(color,))
            
def set_dashed_lines():
    selected_items = tree.selection()
    for item in selected_items:
        tree.set(item, column='Line Style', value='D')
        column_name = tree.item(item)['values'][1]
        line_styles[column_name] = '--'  # Speichert den Stil als gestrichelte Linie

def select_pri_y():
    selected_items = tree.selection()
    for item in selected_items:
        tree.set(item, column='Select Axis', value='P')  # Setzt 'P' für die primäre Y-Achse

def select_sec_y():
    selected_items = tree.selection()
    for item in selected_items:
        tree.set(item, column='Select Axis', value='S')  # Setzt 'S' für die sekundäre Y-Achse
        
def update_plot_interval():
    global start_interval, end_interval
    try:
        start_interval = int(start_interval_entry.get())
        end_interval = int(end_interval_entry.get())
        plot_data_interval()  # Ruft die Funktion auf, um das Diagramm mit dem Intervall zu zeichnen
        print(f"Intervall gesetzt: {start_interval} bis {end_interval}")
    except ValueError:
        print("Bitte geben Sie gültige Intervallwerte ein")

def open_advanced_window():
    global start_interval_entry, end_interval_entry
    advanced_window = tk.Toplevel()
    advanced_window.title("Advanced Options")
    advanced_window.geometry("200x200")

    # Frame für den Statistics-Button mit linksbündiger Ausrichtung
    stats_button_frame = tk.Frame(advanced_window)
    stats_button_frame.pack(anchor='w')

    # Button für Statistiken
    stats_button = tk.Button(stats_button_frame, text="Statistics", command=show_statistics, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    stats_button.pack(side=tk.LEFT, anchor='w')

    # Button für Column Plot
    column_plot_button = tk.Button(stats_button_frame, text="Column Plot", command=open_label_dialog, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    column_plot_button.pack(side=tk.LEFT, anchor='w')

    # Frame für die MAX- und MIN-Buttons
    max_min_button_frame = tk.Frame(advanced_window)
    max_min_button_frame.pack(anchor='w')
    
    # Button für MAX-Wert
    max_button = tk.Button(max_min_button_frame, text="MAX", command=show_max_values, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    max_button.pack(side=tk.LEFT, anchor='w')

    # Button für MIN-Wert
    min_button = tk.Button(max_min_button_frame, text="MIN", command=show_min_values, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    min_button.pack(side=tk.LEFT, anchor='w')

    # Frame für die Intervalleingabe
    interval_frame = tk.Frame(advanced_window)
    interval_frame.pack(anchor='w')

    # Eingabefelder und Set-Button für das Intervall
    start_interval_entry = tk.Entry(interval_frame, width=5)
    end_interval_entry = tk.Entry(interval_frame, width=5)
    start_interval_entry.pack(side=tk.LEFT, anchor='w')
    tk.Label(interval_frame, text="-").pack(side=tk.LEFT, anchor='w')
    end_interval_entry.pack(side=tk.LEFT, anchor='w')
    set_button = tk.Button(interval_frame, text="Set Interval", command=plot_data_interval)
    set_button.pack(side=tk.LEFT, anchor='w')

def show_statistics():
    selected_items = tree.selection()
    if selected_items and df is not None:
        stats_window = tk.Toplevel()
        stats_window.title("Statistics")

        # Stil für Treeview-Widget definieren
        stats_style = ttk.Style()
        stats_style.configure("Stats.Treeview", justify='center')

        # Treeview-Widget mit dem definierten Stil erstellen
        stats_tree = ttk.Treeview(stats_window, style="Stats.Treeview", columns=('Column Name', 'Mean', 'Std Dev', 'Variance'), show='headings')
        stats_tree.heading('Column Name', text='Column Name')
        stats_tree.heading('Mean', text='Mean')
        stats_tree.heading('Std Dev', text='Standard Deviation')
        stats_tree.heading('Variance', text='Variance')

        # Spalten mittig ausrichten
        for col in ['Column Name', 'Mean', 'Std Dev', 'Variance']:
            stats_tree.column(col, anchor='center')

        for item in selected_items:
            column = tree.item(item)['values'][1]
            mean_val = df[column].mean()
            std_val = df[column].std()
            var_val = df[column].var()
            stats_tree.insert('', 'end', values=(column, mean_val, std_val, var_val))

        stats_tree.pack(expand=True, fill='both')
        
def show_max_values():
    show_extreme_values("Max")

def show_min_values():
    show_extreme_values("Min")

def show_extreme_values(extreme_type):
    selected_items = tree.selection()
    if selected_items and df is not None:
        extreme_window = tk.Toplevel()
        extreme_window.title(f"{extreme_type} Values")

        # Stil für Treeview-Widget definieren
        extreme_style = ttk.Style()
        extreme_style.configure("Extreme.Treeview", justify='center')

        # Treeview-Widget mit dem definierten Stil erstellen
        extreme_tree = ttk.Treeview(extreme_window, style="Extreme.Treeview", columns=('Column Name', f'{extreme_type} Value', 'X Value'), show='headings')
        extreme_tree.heading('Column Name', text='Column Name')
        extreme_tree.heading(f'{extreme_type} Value', text=f'{extreme_type} Value')
        extreme_tree.heading('X Value', text='X Value')

        # Spalten mittig ausrichten
        for col in ['Column Name', f'{extreme_type} Value', 'X Value']:
            extreme_tree.column(col, anchor='center')

        for item in selected_items:
            column = tree.item(item)['values'][1]
            # Finde die korrespondierende Zeitachse für die ausgewählte Spalte
            for start, end in table_ranges:
                if df.columns.get_loc(column) >= start and df.columns.get_loc(column) <= end:
                    x_column = df.columns[start]
                    if extreme_type == "Max":
                        extreme_value = df[column].max()
                        x_value = df[x_column][df[column].idxmax()]
                    else:
                        extreme_value = df[column].min()
                        x_value = df[x_column][df[column].idxmin()]

                    extreme_tree.insert('', 'end', values=(column, extreme_value, x_value))
                    break

        extreme_tree.pack(expand=True, fill='both')


def open_label_dialog():
    global is_dialog_open
    is_dialog_open = True
    global y_label_entry, title_entry

    dialog = Toplevel()
    dialog.title("Add Labels")
    dialog.geometry("300x150")

    Label(dialog, text="Do you need chart labels?").pack(pady=10)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    y_label_entry = Entry(dialog)
    title_entry = Entry(dialog)

    def on_yes():
        Label(dialog, text="Y-axis Label:").pack()
        y_label_entry.pack()

        Label(dialog, text="Chart Title:").pack()
        title_entry.pack()

        Button(dialog, text="Plot", command=lambda: plot_and_close(dialog, True)).pack()

    def on_no():
        plot_and_close(dialog, False)

    Button(button_frame, text="Yes", command=on_yes).pack(side=tk.LEFT, padx=10)
    Button(button_frame, text="No", command=on_no).pack(side=tk.RIGHT, padx=10)

def plot_and_close(dialog, use_labels):
    global is_dialog_open
    is_dialog_open = False
    if use_labels:
        y_label = y_label_entry.get()
        title = title_entry.get()
    else:
        y_label = None
        title = None
    dialog.destroy()
    plot_column_data_statistics(y_label, title)
    
    selected_column_names = []

def plot_column_data_statistics(y_label, title):
    global legend_position, SHOW_BAR_VALUES

    selected_items = tree.selection()
    if selected_items and df is not None:
        # Berechnen von Mittelwert, Standardabweichung und Varianz
        stats = {'Mean': [], 'Std Dev': [], 'Variance': []}
        column_names = [tree.item(item)['values'][1] for item in selected_items]

        for item in selected_items:
            column = tree.item(item)['values'][1]
            stats['Mean'].append(df[column].mean())
            stats['Std Dev'].append(df[column].std())
            stats['Variance'].append(df[column].var())

        # Erstellen des Säulendiagramms mit spezifischer Größe
        fig, ax1 = plt.subplots(figsize=(900/80, 600/80))

        # Sekundärachse für die Varianz
        ax2 = ax1.twinx()

        colors = ['blue', 'red', 'green']
        x = np.arange(len(column_names))  # X-Werte für die Balkendiagrammplatzierung
        width = 0.2  # Breite der Balken

        # Zeichnen der Balken für Mittelwert und Standardabweichung
        bars = []
        for i, (stat, color) in enumerate(zip(['Mean', 'Std Dev'], colors[:2])):
            values = stats[stat]
            bar = ax1.bar(x + i * width, values, width, label=stat, color=color)
            bars.append(bar)

            # Annotiere die Balken mit Werten, falls SHOW_BAR_VALUES True ist
            if SHOW_BAR_VALUES:
                for rect in bar:
                    height = rect.get_height()
                    ax1.annotate(f'{height:.2f}',
                                 xy=(rect.get_x() + rect.get_width() / 2, height),
                                 xytext=(0, 3),  # 3 Punkte vertikaler Abstand
                                 textcoords="offset points",
                                 ha='center', va='bottom')

        # Zeichnen der Varianz-Balken auf der Sekundärachse
        variance_bar = ax2.bar(x + 2 * width, stats['Variance'], width, label='Variance', color=colors[2])
        bars.append(variance_bar)

        # Annotiere die Varianzbalken, falls SHOW_BAR_VALUES True ist
        if SHOW_BAR_VALUES:
            for rect in variance_bar:
                height = rect.get_height()
                ax2.annotate(f'{height:.2f}',
                             xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, 3),  # 3 Punkte vertikaler Abstand
                             textcoords="offset points",
                             ha='center', va='bottom')

        # Anpassungen an den Achsen
        ax1.set_xticks(x + width)
        ax1.set_xticklabels(column_names, rotation=ROTATION_ANGLE, ha="right")
        ax1.set_ylabel("Mittelwert/Standardabweichung", fontsize=16)
        ax2.set_ylabel("Varianz", fontsize=16)
        if y_label:
            ax1.set_ylabel(y_label, fontsize=16)
        if title:
            plt.title(title, fontsize=18)

        # Erstellen der kombinierten Legende unter Berücksichtigung der Konfigurationsdatei
        lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        
        # Verwenden Sie die globale Variable für die Legendenposition
        ax1.legend(lines, labels, loc=legend_position)

        if AUTO_ADJUST_LABELS:
            plt.tight_layout()

        plt.show()

        
        
root = tk.Tk()
root.title("Scientific Data Plotting Tool")


# Laden Sie Ihr eigenes Icon
icon_path = r"C:\Users\OoUbu\OneDrive\Dokumente\VS_CODE\AddONs\htdocs\img\Lab.ico"
root.iconbitmap(icon_path)

df = None
table_starts = []

tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)

style = ttk.Style()
style.configure("Bold.Treeview", font=('Helvetica', 10, 'bold'))

tree = ttk.Treeview(tree_frame, columns=('Index', 'Column Name', 'Set Color', 'Select Axis', 'Line Style'), show='headings', yscrollcommand=scrollbar.set, style="Bold.Treeview")
tree.heading('Index', text='Index')
tree.heading('Column Name', text='Column Name')
tree.heading('Set Color', text='Set Color')
tree.heading('Select Axis', text='Select Axis')
tree.heading('Line Style', text='Line Style')
# Konfigurieren Sie die Breite und Ausrichtung für jede Spalte
tree.column('Index', width=50)
tree.column('Column Name', width=150)
tree.column('Set Color', width=120)
tree.column('Line Style', width=60)
tree.column('Select Axis', width=60)  # Spaltenbreite angepasst

# Spalte 'Column Name' linksbündig ausrichten
tree.column('Column Name', anchor='w')  

# Die restlichen Spalten mittig ausrichten
tree.column('Index', anchor='center')
tree.column('Set Color', anchor='center')
tree.column('Select Axis', anchor='center')

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

BUTTON_WIDTH = 11  # Breite in Zeichen
BUTTON_HEIGHT = 1  # Höhe in Zeilen

# Erstellen Sie ein Frame für die Buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Button für das Umschalten der Datenpunkte-Anzeige
data_points_button = tk.Button(button_frame, text="Data Points", command=toggle_data_points, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
data_points_button.pack(side=tk.LEFT)

# Verschieben Sie die Buttons in das neue Frame und ordnen Sie sie nebeneinander an
color_button = tk.Button(button_frame, text="Set Color", command=set_color, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
color_button.pack(side=tk.LEFT)

dashed_line_button = tk.Button(button_frame, text="Dashed Lines", command=set_dashed_lines, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
dashed_line_button.pack(side=tk.LEFT)

pri_y_button = tk.Button(button_frame, text="Primary Axis", command=select_pri_y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
pri_y_button.pack(side=tk.LEFT)

sec_y_button = tk.Button(button_frame, text="Secondary Axis", command=select_sec_y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
sec_y_button.pack(side=tk.LEFT)

advanced_button = tk.Button(button_frame, text="Advanced", command=open_advanced_window, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
advanced_button.pack(side=tk.LEFT)

entry_width = 70  # Definieren Sie die Breite der Eingabefelder

title_label = tk.Label(root, text="Title:")
title_label.pack()

title_entry = tk.Entry(root, width=entry_width)
title_entry.pack()

x_axis_label = tk.Label(root, text="X-Axis Label:")
x_axis_label.pack()

x_axis_entry = tk.Entry(root, width=entry_width)
x_axis_entry.pack()

y_axis_label = tk.Label(root, text="Primary Y-Axis Label:")
y_axis_label.pack()

y_axis_entry = tk.Entry(root, width=entry_width)
y_axis_entry.pack()

y_sec_axis_label = tk.Label(root, text="Secondary Y-Axis Label:")
y_sec_axis_label.pack()

y_sec_axis_entry = tk.Entry(root, width=entry_width)
y_sec_axis_entry.pack()

# Erstellen eines Frames für die Plot- und Reset-Buttons
plot_reset_frame = tk.Frame(root)
plot_reset_frame.pack()

# Erstellen des Plot Data Buttons im neuen Frame
plot_button = tk.Button(plot_reset_frame, text="Plot Data", command=plot_data, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
plot_button.pack(side=tk.LEFT)

# Erstellen des Reset-Buttons im neuen Frame
reset_button = tk.Button(plot_reset_frame, text="Reset Settings", command=reset_settings, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
reset_button.pack(side=tk.LEFT)

# Erstellen der Menüleiste
menu_bar = tk.Menu(root)

# Erstellen des File-Menüs
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=load_excel_file)
menu_bar.add_cascade(label="File", menu=file_menu)

# Erstellen des Database-Menüs
database_menu = tk.Menu(menu_bar, tearoff=0)
database_menu.add_command(label="Open Database", command=open_database)
menu_bar.add_cascade(label="Database", menu=database_menu)

# Erstellen des Config-Menüs
config_menu = tk.Menu(menu_bar, tearoff=0)
config_menu.add_command(label="Open Config", command=open_config)
menu_bar.add_cascade(label="Config", menu=config_menu)

# Erstellen des Info-Menüs
info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="About", command=show_info)
menu_bar.add_cascade(label="Info", menu=info_menu)

# Hinzufügen der Menüleiste zum Hauptfenster
root.config(menu=menu_bar)

root.mainloop()