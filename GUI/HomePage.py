import tkinter as tk
from tkinter import ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, controller, show_file, show_originator, show_receiver):
        super().__init__(parent)

        self["style"] = "Page.TFrame"

        options_label = ttk.Label(self, text="get started.", style="Header.TLabel")
        options_label.grid(row=0, column=0, padx=30, pady=30, sticky="EW")

        menu_frame = ttk.Frame(self, style="Function.TFrame",)
        menu_frame.grid(row=1, column=0, pady=(0, 50))

        # --Buttons--
        self.originator_page_button = ttk.Button(
            menu_frame,
            text="Originator Create/Edit",
            command=show_originator,
            style="ACHButton.TButton",
        )
        self.receiver_page_button = ttk.Button(
            menu_frame,
            text="Receiver Create/Edit",
            command=show_receiver,
            style="ACHButton.TButton",
        )
        self.file_page_button = ttk.Button(
            menu_frame,
            text="ACH File Create",
            command=show_file,
            style="ACHButton.TButton",
        )

        self.originator_page_button.grid(column=0, row=2, sticky="EW", padx=5, pady=5)
        self.receiver_page_button.grid(column=0, row=3, sticky="EW", padx=5, pady=5)
        self.file_page_button.grid(column=0, row=4, sticky="EW", padx=5, pady=5)
