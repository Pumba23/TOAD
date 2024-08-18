import tkinter as tk


def zeige_ida_buttons(root, ida_buttons_frame, back_button, quit_button, main_menu_frame, sda_buttons_frame):
    root.configure(bg='#004d00')  # Dunkleres Grün
    main_menu_frame.pack_forget()  # Verstecke Hauptmenü Frame
    sda_buttons_frame.pack_forget()  # Verstecke SDA Button Frame

    # Frame für IDA Buttons erstellen
    ida_buttons_frame.pack(fill=tk.BOTH, expand=True)

    # Lösche alle Widgets im IDA Frame
    for widget in ida_buttons_frame.winfo_children():
        widget.destroy()

    # Erstellen von Buttons im IDA Bereich basierend auf einem Array
    buttons_text = ['Macro', 'Energy industries', 'Agriculture', 'Transport', 'Custom1', 'Custom2']
    for text in buttons_text:
        button = tk.Button(ida_buttons_frame, text=text, bg='gray', padx=20, pady=20)
        button.pack(side=tk.LEFT, padx=20, pady=100)

    # Zurück- und Beenden-Button am unteren Rand rechts anordnen
    back_button.pack(side=tk.RIGHT, anchor='se', padx=10, pady=10)
    quit_button.pack(side=tk.RIGHT, anchor='se', padx=10, pady=10)
