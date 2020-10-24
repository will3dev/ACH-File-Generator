import tkinter as tk
from tkinter import ttk
from conversion_codes import ServiceClassCodes as SCC
from Database import *


class AddOriginator(ttk.Frame):
    def __init__(self, parent, controller, show_home, show_originator):
        super().__init__(parent)

        self["style"] = "Page.TFrame"

        self.show_originator = show_originator

        self.add_originator_container = ttk.Frame(
            self, style="Page.TFrame"
        )
        self.add_originator_container.grid(
            row=0, column=0, sticky="EW",
            padx=10, pady=10,
        )

        add_originator_label = ttk.Label(self.add_originator_container, text="add or edit originator.", style="Header.TLabel")
        add_originator_label.grid(row=0, column=0, padx=10, pady=10)

        add_edit_selection = tk.StringVar(value="Add")

        self.add_originator_selection = ttk.Radiobutton(
            self.add_originator_container,
            text="Add New Originator",
            variable=add_edit_selection,
            value="Add",
            command=self.handle_new_originator,
            style="BigRadio.TRadiobutton"
        )
        self.edit_originator_selection = ttk.Radiobutton(
            self.add_originator_container,
            text="Edit Existing Originator",
            variable=add_edit_selection,
            value="Edit",
            command=self.handle_edit_originator,
            style="BigRadio.TRadiobutton"
        )
        self.add_originator_selection.grid(row=1, column=0, pady=2)
        self.edit_originator_selection.grid(row=2, column=0, pady=2)

        # --Container to Manager Originators--
        self.originator_manager_container = ttk.Frame(self.add_originator_container, style="Page.TFrame")
        self.originator_manager_container.grid(row=3, column=0, columnspan=3, sticky="NSEW")

        # --Originator Data--
        self.originator_name_val = tk.StringVar()
        self.originator_ID_val = tk.StringVar()
        self.originator_acct_val = tk.StringVar()
        self.originator_scc_val = tk.StringVar()

        # --Button Section--
        button_container = ttk.Frame(self, style="Function.TFrame",)
        button_container.grid(column=0, row=2, columnspan=5, sticky="NSEW", padx=10)
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=2)
        button_container.columnconfigure(2, weight=2)
        button_container.columnconfigure(3, weight=2)
        button_container.columnconfigure(4, weight=1)

        back_button = ttk.Button(
            button_container,
            text="Back",
            command=show_home,
            cursor="hand2",
            style="ACHButton.TButton",
        )
        save_button = ttk.Button(
            button_container,
            text="Save",
            command=self.save_originator_data,
            cursor="hand2",
            style="ACHButton.TButton",
        )
        delete_button = ttk.Button(
            button_container,
            text="delete",
            command=self.delete_originator_data,
            cursor="hand2",
            style="ACHButton.TButton",
        )

        back_button.grid(column=1, row=0, sticky="EW", padx=5, pady=5)
        delete_button.grid(column=2, row=0, sticky="EW", padx=5, pady=5)

        save_button.grid(column=3, row=0, sticky="EW", padx=5, pady=5)


        self.add_originator_selection.invoke()

    def handle_new_originator(self):
        self.reset_originator_manager

        # --New Originator Form--s
        new_originator_frame = ttk.Frame(self.originator_manager_container, style="Function.TFrame")
        new_originator_frame.grid(row=0, column=0, columnspan=3, sticky="NSEW")

        new_originator_frame_label = ttk.Label(new_originator_frame, text="add originator. ", style="Table.TLabel")
        new_originator_frame_label.grid(row=0, column=0, pady=10)

        originator_name_label = ttk.Label(new_originator_frame, text="Originator Name: ", style="Field.TLabel")
        originator_name_label.grid(row=1, column=0, sticky="EW", pady=2)
        originator_name_entry = ttk.Entry(new_originator_frame, textvariable=self.originator_name_val)
        originator_name_entry.grid(row=1, column=1, sticky="EW", pady=2)

        originator_ID_label = ttk.Label(new_originator_frame, text="Originator TaxID: ", style="Field.TLabel")
        originator_ID_label.grid(row=2, column=0, sticky="EW", pady=2)
        originator_ID_entry = ttk.Entry(new_originator_frame, textvariable=self.originator_ID_val)
        originator_ID_entry.grid(row=2, column=1, sticky="EW", pady=2)

        originator_acct_label = ttk.Label(new_originator_frame, text="Account Number: ", style="Field.TLabel")
        originator_acct_label.grid(row=3, column=0, sticky="EW", pady=2)
        originator_acct_entry = ttk.Entry(new_originator_frame, textvariable=self.originator_acct_val)
        originator_acct_entry.grid(row=3, column=1, sticky="EW", pady=2)

        originator_scc_label = ttk.Label(new_originator_frame, text="Service Class Code: ", style="Field.TLabel")
        originator_scc_label.grid(row=4, column=0, sticky="EW", pady=2)
        originator_scc_entry = ttk.Combobox(
            new_originator_frame,
            values=SCC.KEYS,
            state="readonly",
            textvariable=self.originator_scc_val,
            style="Dropdown.TCombobox",
        )
        originator_scc_entry.grid(row=4, column=1, sticky="EW", pady=2)

    def handle_edit_originator(self):
        self.reset_originator_manager

        # --Edit Originator Form--
        self.edit_originator_frame = ttk.Frame(self.originator_manager_container, style="Function.TFrame")
        self.edit_originator_frame.grid(row=0, column=1, columnspan=3, sticky="NSEW")

        edit_originator_frame_label = ttk.Label(self.edit_originator_frame, text="edit originator. ", style="Table.TLabel")
        edit_originator_frame_label.grid(row=0, column=0, pady=10)

        create_originator_table()
        existing_originators = [f"{company.get('name')}" for company in get_originators()]

        originators = tk.StringVar(value=existing_originators)
        scrollbar = tk.Scrollbar(self.edit_originator_frame, orient="vertical")
        self.originators_list_box = tk.Listbox(
            self.edit_originator_frame,
            listvariable=originators,
            height=10,
            selectmode="single",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=self.originators_list_box.yview)
        scrollbar.grid(column=2, sticky="ns")
        self.originators_list_box.grid(row=1, column=0, columnspan=2, sticky="EW")

        self.originators_list_box.bind("<<ListboxSelect>>", self.handle_selection)

    def handle_selection(self, event):
        curse_selection = self.originators_list_box.curselection()

        for i in curse_selection:
            selection = self.originators_list_box.get(i)
            originator_details = get_originator_detail(selection)


            self.originator_name_val.set(originator_details.get('originator_name'))
            originator_name_label = ttk.Label(self.edit_originator_frame, text="Originator Name: ", style="Field.TLabel")
            originator_name_label.grid(row=2, column=0, sticky="EW", pady=2)
            originator_name_entry = tk.Entry(self.edit_originator_frame, text=self.originator_name_val.get(), textvariable=self.originator_name_val)
            originator_name_entry.grid(row=2, column=1, sticky="EW", pady=2)


            self.originator_ID_val.set(originator_details.get('originatorID'))
            originator_ID_label = ttk.Label(self.edit_originator_frame, text="Originator TaxID: ", style="Field.TLabel")
            originator_ID_label.grid(row=3, column=0, sticky="EW", pady=2)
            originator_ID_entry = tk.Entry(self.edit_originator_frame, text=self.originator_ID_val.get(), textvariable=self.originator_ID_val)
            originator_ID_entry.grid(row=3, column=1, sticky="EW", pady=2)

            self.originator_acct_val.set(originator_details.get('account'))
            originator_acct_label = ttk.Label(self.edit_originator_frame, text="Account Number: ", style="Field.TLabel")
            originator_acct_label.grid(row=4, column=0, sticky="EW", pady=2)
            originator_acct_entry = tk.Entry(self.edit_originator_frame, text=self.originator_acct_val.get(), textvariable=self.originator_acct_val)
            originator_acct_entry.grid(row=4, column=1, sticky="EW", pady=2)

            self.originator_scc_val.set(originator_details.get('serviceClass'))
            originator_scc_label = ttk.Label(self.edit_originator_frame, text="Service Class Code: ", style="Field.TLabel")
            originator_scc_label.grid(row=5, column=0, sticky="EW", pady=2)
            originator_scc_entry = ttk.Combobox(
                self.edit_originator_frame,
                values=SCC.KEYS,
                state="readonly",
                textvariable=self.originator_scc_val,
                style="Dropdown.TCombobox",
            )
            val = int(SCC.KEYS.index(originator_details.get('serviceClass')))
            originator_scc_entry.current(val)
            originator_scc_entry.grid(row=5, column=1, sticky="EW", pady=2)

        def handler(event):
            for widget in self.edit_originator_frame.winfo_children():
                widget.destroy()

        self.add_originator_selection.bind('<Button-1>', handler)

    def save_originator_data(self):
        name = self.originator_name_val.get()
        id = self.originator_ID_val.get()
        acct = self.originator_acct_val.get()
        scc = self.originator_scc_val.get()

        if name in [val.get('name') for val in get_originators()]:
            update_originator(
                name, id, acct, scc
            )
        else:
            new_originator(
                name, id, acct, scc
            )
        print(f'<DATA SAVED: {name}, {id}, {acct}, {scc}>')

        self.reset_screen

    def delete_originator_data(self):
        name = self.originator_name_val.get()
        id = self.originator_ID_val.get()
        acct = self.originator_acct_val.get()
        scc = self.originator_scc_val.get()

        delete_originator(name, id)

        print(f'<DATA DELETED: {name}, {id}, {acct}, {scc}>')

    @property
    def reset_screen(self):
        for widget in self.add_originator_container.winfo_children():
            widget.destroy()

        self.show_originator()

    @property
    def reset_originator_manager(self):
        for widget in self.originator_manager_container.winfo_children():
            widget.destroy()

        self.originator_name_val.set("")
        self.originator_ID_val.set("")
        self.originator_acct_val.set("")
        self.originator_scc_val.set("")









