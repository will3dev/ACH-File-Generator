import tkinter as tk
import os
from tkinter import ttk, filedialog
from conversion_codes import TransCodes
from conversion_codes import SEC_Codes
from Create_ACH import Create_ACH_File
from Database import *


class FileCreate_Page(ttk.Frame):
    def __init__(self, parent, controller, show_home, show_filecreate):
        super().__init__(parent)

        self.show_home = show_home
        self.show_filecreate = show_filecreate

        self["style"] = "Page.TFrame"

        filecreator_label = ttk.Label(self, text="generate ach file.", style="Header.TLabel")
        filecreator_label.grid(row=0, column=0, columnspan=2, sticky="EW")

        self.originator_frame = ttk.Frame(
           self, style="Page.TFrame"
        )
        self.originator_frame.grid(
            row=1, column=0, sticky="EW",
            padx=2, pady=2,
        )


        # --Set Up Originator--

        create_originator_table()
        self.existing_originators = [f"{company.get('name')}" for company in get_originators()]
        length = len(self.existing_originators)

        scrollbar = tk.Scrollbar(self.originator_frame, orient="vertical")
        self.originators = tk.StringVar(value=self.existing_originators)
        self.originators_list_box = tk.Listbox(
            self.originator_frame,
            listvariable=self.originators,
            height=10,
            selectmode="single",
            yscrollcommand=scrollbar.set,
            exportselection=0,
        )
        scrollbar.config(command=self.originators_list_box.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.originators_list_box.grid(row=0, column=0, rowspan=3, sticky="EW", padx=5, pady=5)
        self.selection = None
        self.originator_detail = {
            'sec': '',
            'discretionary': '',
            'effective_entry': '',
        }

        # --Additional transaction details--
        transaction_detail_frame = ttk.Frame(self, style="Function.TFrame")
        transaction_detail_frame.grid(column=1, row=1, columnspan=3, sticky="NSEW", padx=5, pady=5)

        transaction_label = ttk.Label(transaction_detail_frame, text="batch details.", style="Table.TLabel")
        transaction_label.grid(row=0, column=0, sticky="EW", pady=5)

        self.sec_val = tk.StringVar()
        self.effective_date_val = tk.StringVar()
        self.discretionary_data_val = tk.StringVar()

        sec_label = ttk.Label(transaction_detail_frame, text="Receiver Type Selection: ", style="Field.TLabel")
        sec_selection = ttk.Combobox(
            transaction_detail_frame,
            values=SEC_Codes.KEYS,
            state="readonly",
            textvariable=self.sec_val,
            style="Dropdown.TCombobox",
        )
        effective_date_label = ttk.Label(
            transaction_detail_frame,
            text="Effective Entry Date (MM/DD/YYYY): ",
            style="Field.TLabel", )
        effective_date = ttk.Entry(transaction_detail_frame, textvariable=self.effective_date_val)
        discretionary_data_label = ttk.Label(
            transaction_detail_frame,
            text="Descretionary Data: ",
            style="Field.TLabel", )
        discretionary_data_entry = ttk.Entry(transaction_detail_frame, textvariable=self.discretionary_data_val)

        sec_label.grid(row=1, column=0, sticky="EW", pady=2)
        sec_selection.grid(row=1, column=1, sticky="EW", pady=2)
        effective_date_label.grid(row=2, column=0, sticky="EW", pady=2)
        effective_date.grid(row=2, column=1, sticky="EW", pady=2)
        discretionary_data_label.grid(row=3, column=0, sticky="EW", pady=2)
        discretionary_data_entry.grid(row=3, column=1, sticky="EW", pady=2)


        # --Set up Receivers--
        create_receiver_table()
        self.receiver_frame = ttk.Frame(self, style="Function.TFrame" )
        self.receiver_frame.grid(columnspan=5, row=2, sticky="EW", padx=10, pady=10)

        self.receiver_names = list()

        self.originators_list_box.bind("<<ListboxSelect>>", self.handle_selection)

        # --Button Section--
        button_container = ttk.Frame(self, style="Page.TFrame")
        button_container.grid(column=0, row=4, columnspan=5, sticky="NSEW", padx=10,)
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(0, weight=2)
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(0, weight=2)
        button_container.columnconfigure(0, weight=1)

        back_button = ttk.Button(
            button_container,
            text="Back",
            command=self.back_homepage,
            cursor="hand2",
            style="ACHButton.TButton",
        )
        create_file_button = ttk.Button(
            button_container,
            text="Create ACH",
            command=self.create_ach_file,
            cursor="hand2",
            style="ACHButton.TButton",
        )
        back_button.grid(column=1, row=0, sticky="EW", padx=2, pady=10)
        create_file_button.grid(column=3, row=0, sticky="EW", padx=2, pady=10)

    def back_homepage(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.show_home()

    def process_receiver_information(self, receiver_list, originator_name):
        if len(receiver_list) > 0:
            receivers_detail_data = list()
            for receiver in receiver_list:
                name = receiver[0].get()
                amount = receiver[1].get()
                transcode = receiver[2].get()

                if name != '' and amount != '' and transcode != '':
                    receiver_detail = dict()
                    data = get_receiver_detail(originator_name, name)
                    for d in data:
                        receiver_detail.update(d)
                    receiver_detail['amt'] = amount
                    receiver_detail['transcode'] = transcode

                    receivers_detail_data.append(receiver_detail)
                else:
                    pass

        return receivers_detail_data

    def create_ach_file(self):
        if self.receiver_names:
            self.originator_detail['sec'] = self.sec_val.get()
            self.originator_detail['effective_entry'] = self.effective_date_val.get()
            self.originator_detail['discretionary'] = self.discretionary_data_val.get()

            entry_data = self.process_receiver_information(self.receiver_names, self.selection)

            data = [
                {'originator': self.originator_detail,
                 'entries': entry_data
                }
            ]

            print(data)

        else:
            print("Nothing available")

        caf = Create_ACH_File(data)
        file = caf.generate_file()

        file_path = filedialog.asksaveasfilename()
        filename = os.path.basename(file_path)

        try:
            with open(file_path, 'w') as f:
                f.write(file)
            print(f"<FILE SAVED: {filename}>")
        except (AttributeError, FileNotFoundError):
            print('Save operation cancelled')

        #saf = SaveACHFile(self.selection)
        #saf.save_file(file)

        self.reset_screen

    def handle_selection(self, event):
        for widget in self.receiver_frame.winfo_children():
            widget.destroy()

        curse_selection = self.originators_list_box.curselection()
        receiver_frame_label = ttk.Label(self.receiver_frame, text="select/configure receivers.", style="Table.TLabel")
        receiver_frame_label.grid(column=0, row=0, sticky="EW", padx=5, pady=5)

        for i in curse_selection:
            choice = i
            self.selection = self.originators_list_box.get(choice)
            self.originator_detail.update(get_originator_detail(self.selection))

            receivers_list = [orig.get("name") for orig in get_all_receivers(self.selection)]
            if len(receivers_list) > 0:
                count = 1
                for pos, val in enumerate(receivers_list):
                    self.receiver_names.append([])

                    # -- Receiver Select--
                    checkbox_selection = tk.StringVar()
                    checkbox = ttk.Checkbutton(
                        self.receiver_frame,
                        text=val,
                        variable=checkbox_selection,
                        onvalue=val,
                        offvalue="Off",
                        style="FieldCheck.TCheckbutton"
                    )
                    checkbox.grid(column=0, row=count, sticky="EW", padx=2, pady=5)

                    # --Amount Select--
                    amount_selection = tk.StringVar()
                    amount_label = ttk.Label(
                        self.receiver_frame,
                        text="Please Enter Amount:",
                        style="Field.TLabel"
                    )
                    amount_label.grid(column=1, row=count, sticky="EW", pady=5)

                    amount_selection_field = ttk.Entry(
                        self.receiver_frame,
                        text="Please enter amount <ex. $450.00>",
                        textvariable=amount_selection,
                    )
                    amount_selection_field.grid(column=2, row=count, sticky="EW", pady=5)

                    # --Transaction Type Selection--
                    transaction_type_selection = tk.StringVar()
                    transaction_type_label = ttk.Label(
                        self.receiver_frame,
                        text="Select Transaction Type",
                        style="Field.TLabel",
                    )
                    transaction_type_label.grid(column=3, row=count, sticky="EW", pady=5)

                    transaction_type_selection_field = ttk.Combobox(
                        self.receiver_frame,
                        values=TransCodes.KEYS,
                        textvariable=transaction_type_selection,
                        state="readonly",
                        style="Dropdown.TCombobox"
                    )
                    transaction_type_selection_field.grid(column=4, row=count, sticky="EW", pady=5)

                    self.receiver_names[pos].append(checkbox_selection)
                    self.receiver_names[pos].append(amount_selection)
                    self.receiver_names[pos].append(transaction_type_selection)

                    count += 1
            else:
                # --Warning for no receivers--
                no_receivers_label = ttk.Label(
                    self.receiver_frame,
                    text="NO ACTIVE RECEIVERS FOUND",
                    style="Warning.TLabel"
                )
                no_receivers_label.grid(column=0, row=1, padx=20, pady=20)

    @property
    def reset_screen(self):
        for widget in self.originator_frame.winfo_children():
            widget.destroy()

        self.show_filecreate()




