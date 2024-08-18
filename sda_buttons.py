import tkinter as tk


def zeige_sda_buttons(root, sda_buttons_frame, back_button, quit_button, main_menu_frame, ida_buttons_frame):
    root.configure(bg='#00008b')  # Dunkleres Blau
    main_menu_frame.pack_forget()  # Verstecke Hauptmenü Frame
    ida_buttons_frame.pack_forget()  # Verstecke IDA Button Frame

    # Frame für SDA Buttons erstellen
    sda_buttons_frame.pack(fill=tk.BOTH, expand=True)

    # Lösche alle Widgets im SDA Frame
    for widget in sda_buttons_frame.winfo_children():
        widget.destroy()

    # Erstellen von Buttons im SDA Bereich
    sda_buttons_text = ['SDA Button 1', 'SDA Button 2']
    for text in sda_buttons_text:
        button = tk.Button(sda_buttons_frame, text=text, bg='gray', padx=20, pady=20)
        button.pack(side=tk.LEFT, padx=10, pady=10)

    # Zurück- und Beenden-Button am unteren Rand rechts anordnen
    back_button.pack(side=tk.RIGHT, anchor='se', padx=10, pady=10)
    quit_button.pack(side=tk.RIGHT, anchor='se', padx=10, pady=10)
