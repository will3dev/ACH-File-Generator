import tkinter as tk
from tkinter import ttk
from conversion_codes import TransCodes as tc
from Database import *


class AddReceiver(ttk.Frame):
    def __init__(self, parent, controller, show_home, show_receiver):
        super().__init__(parent)

        self.column_total = 5

        self.show_home = show_home
        self.show_receiver = show_receiver
        self["style"] = "Page.TFrame"

        receiver_page_label = ttk.Label(self, text="manage receivers.", style="Header.TLabel")
        receiver_page_label.grid(row=0, column=0, sticky="EW", pady=2, padx=2)
        self.add_receiver_container = ttk.Frame(
            self,
            style="Page.TFrame",
        )
        self.add_receiver_container.grid(row=1, column=0, sticky="NSEW", columnspan=self.column_total, padx=10, pady=10,)
        self.add_receiver_container.columnconfigure(0, weight=1)
        self.add_receiver_container.columnconfigure(1, weight=1)
        self.add_receiver_container.columnconfigure(2, weight=1)
        self.add_receiver_container.columnconfigure(3, weight=1)
        self.add_receiver_container.columnconfigure(4, weight=1)

        # add column and row configure

        originator_selection_frame = ttk.Frame(self.add_receiver_container, style="Main.TFrame")
        originator_selection_frame.grid(column=0, row=0, columnspan=2, sticky="NSEW", padx=5, pady=5)

        create_originator_table()
        existing_originators = [f"{company.get('name')}" for company in get_originators()]

        self.originators = tk.StringVar(value=existing_originators)
        self.originators_list_box = tk.Listbox(
            originator_selection_frame,
            listvariable=self.originators,
            height=10,
            selectmode="single",
            exportselection=0,
        )
        self.originators_list_box.grid(row=0, column=0, columnspan=2, sticky="NSEW")

        self.originators_list_box.bind("<<ListboxSelect>>", self.handle_listbox_selection)

        # --Value Fields--
        self.form_count_val = tk.IntVar(value=0)

        self.radiobutton_selection = tk.StringVar()

        self.receiver_data = []

        # --Add/Edit Receiver Section--
        self.add_receiver_frame = ttk.Frame(self.add_receiver_container, style="Function.TFrame")
        self.add_receiver_frame.grid(row=1, column=0, columnspan=5, sticky="NSEW", padx=10, pady=10)


        # --Button Section--
        button_container = ttk.Frame(self.add_receiver_container, style="Function.TFrame",)
        button_container.grid(column=0, row=2, columnspan=5, sticky="EW", padx=10, pady=10)
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=1)
        button_container.columnconfigure(2, weight=2)
        button_container.columnconfigure(3, weight=2)
        button_container.columnconfigure(4, weight=2)

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
            command=self.save_receiver_data,
            cursor="hand2",
            style="ACHButton.TButton"
        )
        delete_button = ttk.Button(
            button_container,
            text="delete",
            command=self.delete_receivers,
            cursor="hand2",
            style="ACHButton.TButton",
        )

        back_button.grid(column=2, row=0, sticky="EW", padx=5, pady=5)
        delete_button.grid(column=3, row=0, sticky="EW", padx=5, pady=5)
        save_button.grid(column=4, row=0, stick="EW", padx=5, pady=5)

    def handle_listbox_selection(self, event):
        self.reset_receiver_manager

        # --Radio Button Options--
        add_edit_frame = ttk.Frame(self.add_receiver_container, style="Page.TFrame")
        add_edit_frame.grid(row=0, column=2, columnspan=3, sticky="EW", pady=5, padx=5)

        add_edit_label = ttk.Label(add_edit_frame, text="add or edit receivers.", style="TableAlt.TLabel")
        add_radiobutton = ttk.Radiobutton(
            add_edit_frame,
            text="Add New Receiver",
            variable=self.radiobutton_selection,
            value="Add",
            command=self.handle_add_receiver,
            style="BigRadio.TRadiobutton",
        )
        edit_radiobutton = ttk.Radiobutton(
            add_edit_frame,
            text="Edit Existing Receiver",
            variable=self.radiobutton_selection,
            value="Edit",
            command=self.handle_edit_receiver,
            style="BigRadio.TRadiobutton"
        )
        add_edit_label.grid(row=0, column=0, sticky="EW")
        add_radiobutton.grid(row=1, column=0, sticky="EW")
        edit_radiobutton.grid(row=2, column=0, sticky="EW")

        add_radiobutton.invoke()

    def handle_add_receiver(self):
        self.reset_receiver_manager

        # --Add Receiver Frame--
        add_receiver_frame_label = ttk.Label(self.add_receiver_frame, text="new receiver details. ", style="Table.TLabel")
        add_receiver_frame_label.grid(row=0, column=0, sticky="EW", padx=5, pady=10)

        form_count_label = ttk.Label(self.add_receiver_frame, text="Number of new Receivers to add: ", style="Field.TLabel")
        form_count_spinbox = tk.Spinbox(
            self.add_receiver_frame,
            from_=0,
            to=10,
            textvariable=self.form_count_val,
            wrap=False,
            command=self.create_new_receiver_form,
        )
        form_count_label.grid(row=1, column=0, sticky="EW", padx=5, pady=5)
        form_count_spinbox.grid(row=1, column=1, sticky="EW", padx=5, pady=5)

        self.receiver_form_frame = ttk.Frame(self.add_receiver_frame, style="Function.TFrame")
        self.receiver_form_frame.grid(row=2, column=0, columnspan=5, sticky="EW", padx=5, pady=5)


    def create_new_receiver_form(self):
        for widget in self.receiver_form_frame.winfo_children():
            widget.destroy()

        # scrollable_frame = ScrollableFrame(receiver_form_frame)

        count = self.form_count_val.get()

        for c in range(count):
            self.receiver_data.append([
                tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
            ])

            receiver_frame = ttk.Frame(self.receiver_form_frame, style="Function.TFrame" )
            receiver_frame.grid(row=c, column=0, columnspan=5, sticky="NSEW", padx=5, pady=5)

            receiver_name_label = ttk.Label(receiver_frame, text="Receiver Name: ", style="Field.TLabel")
            receivingID_label = ttk.Label(receiver_frame, text="Receivers Bank RTN: ", style="Field.TLabel")
            acct_label = ttk.Label(receiver_frame, text="Receivers Account Number: ", style="Field.TLabel")
            transcode_label = ttk.Label(receiver_frame, text="Default Account and Transaction Type: ", style="Field.TLabel")
            amount_label = ttk.Label(receiver_frame, text="Default Amount: ", style="Field.TLabel")

            receiver_name_entry = ttk.Entry(receiver_frame, textvariable=self.receiver_data[c][0])
            receivingID_entry = ttk.Entry(receiver_frame, textvariable=self.receiver_data[c][1])
            acct_entry = ttk.Entry(receiver_frame, textvariable=self.receiver_data[c][2])
            transcode_combobox = ttk.Combobox(
                receiver_frame,
                values=tc.KEYS,
                state="readonly",
                textvariable=self.receiver_data[c][3],
                style="Dropdown.TCombobox",
            )
            amount_entry = ttk.Entry(receiver_frame, textvariable=self.receiver_data[c][4])

            receiver_name_label.grid(row=0, column=0, pady=2, padx=2, sticky="EW")
            receiver_name_entry.grid(row=0, column=1, pady=2, padx=2, sticky="EW")
            receivingID_label.grid(row=0, column=2, pady=2, padx=2, sticky="EW")
            receivingID_entry.grid(row=0, column=3, pady=2, padx=2, sticky="EW")
            acct_label.grid(row=1, column=0, pady=2, padx=2, sticky="EW")
            acct_entry.grid(row=1, column=1, pady=2, padx=2, sticky="EW")
            transcode_label.grid(row=1, column=2, pady=2, padx=2, sticky="EW")
            transcode_combobox.grid(row=1, column=3, pady=2, padx=2, sticky="EW")
            amount_label.grid(row=2, column=0, pady=2, padx=2, sticky="EW")
            amount_entry.grid(row=2, column=1, pady=2, padx=2, sticky="EW")

        # scrollable_frame.grid(row=1, column=0, columnspan=5, sticky="EW")


    def handle_edit_receiver(self):
        # --Edit Receiver Frame--
        self.reset_receiver_manager

        edit_receiver_frame = ttk.Frame(self.add_receiver_frame, style="Function.TFrame")
        edit_receiver_frame.grid(row=1, column=0, columnspan=self.column_total, sticky="NSEW")
        edit_receiver_frame_label = ttk.Label(self.add_receiver_frame, text="update receiver info.", style="Table.TLabel")
        edit_receiver_frame_label.grid(row=0, column=0, sticky="NSEW", padx=5)

        # scrollable_frame = ScrollableFrame(edit_receiver_frame)

        selection = self.originators_list_box.get(self.originators_list_box.curselection())
        receivers_list = [val.get('name') for val in get_active_receivers(selection)]

        if len(receivers_list) > 0:
            receivers_list.sort()
            receivers_detail_list = [
                get_receiver_detail(selection, receiver)[0]
                for receiver in receivers_list
            ]

            for pos, receiver in enumerate(receivers_detail_list):
                name = receiver.get('name')
                receiverID = receiver.get('receivingID')
                acct = receiver.get('acct')
                transcode = receiver.get('transcode')
                amt = receiver.get('amt')

                self.receiver_data.append(
                    [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
                )

                receiver_frame = ttk.Frame(edit_receiver_frame, style="Function.TFrame" )
                receiver_frame.grid(row=pos+1, column=0, columnspan=5, sticky="NSEW", padx=5, pady=5)

                receiver_name_label = ttk.Label(receiver_frame, text="Receiver Name: ", style="Field.TLabel")
                receivingID_label = ttk.Label(receiver_frame, text="Receivers Bank RTN: ", style="Field.TLabel")
                acct_label = ttk.Label(receiver_frame, text="Receivers Account Number: ", style="Field.TLabel")
                transcode_label = ttk.Label(receiver_frame, text="Default Account and Transaction Type: ", style="Field.TLabel")
                amount_label = ttk.Label(receiver_frame, text="Default Amount: ", style="Field.TLabel")

                self.receiver_data[pos][0].set(name)
                self.receiver_data[pos][1].set(receiverID)
                self.receiver_data[pos][2].set(acct)
                self.receiver_data[pos][3].set(transcode)
                self.receiver_data[pos][4].set(amt)

                receiver_name_entry = ttk.Entry(receiver_frame, text=self.receiver_data[pos][0].get(), textvariable=self.receiver_data[pos][0])
                receivingID_entry = ttk.Entry(receiver_frame, text=self.receiver_data[pos][1].get(), textvariable=self.receiver_data[pos][1])
                acct_entry = ttk.Entry(receiver_frame, text=self.receiver_data[pos][2].get(), textvariable=self.receiver_data[pos][2])
                transcode_combobox = ttk.Combobox(
                    receiver_frame,
                    values=tc.KEYS,
                    state="readonly",
                    textvariable=self.receiver_data[pos][3],
                    style="Dropdown.TCombobox",
                )
                amount_entry = ttk.Entry(receiver_frame, text=self.receiver_data[pos][4].get(), textvariable=self.receiver_data[pos][4])
                delete_user_checkbutton = ttk.Checkbutton(
                    receiver_frame,
                    text="Delete Receiver",
                    variable=self.receiver_data[pos][5],
                    onvalue="Delete",
                    offvalue="Keep",
                    style="FieldCheck.TCheckbutton",
                )


                receiver_name_label.grid(row=0, column=0, pady=2, padx=2, sticky="EW")
                receiver_name_entry.grid(row=0, column=1, pady=2, padx=2, sticky="EW")
                receivingID_label.grid(row=0, column=2, pady=2, padx=2, sticky="EW")
                receivingID_entry.grid(row=0, column=3, pady=2, padx=2, sticky="EW")
                acct_label.grid(row=1, column=0, pady=2, padx=2, sticky="EW")
                acct_entry.grid(row=1, column=1, pady=2, padx=2, sticky="EW")
                transcode_label.grid(row=1, column=2, pady=2, padx=2, sticky="EW")
                transcode_combobox.grid(row=1, column=3, pady=2, padx=2, sticky="EW")
                amount_label.grid(row=2, column=0, pady=2, padx=2, sticky="EW")
                amount_entry.grid(row=2, column=1, pady=2, padx=2, sticky="EW")
                delete_user_checkbutton.grid(row=2, column=3, padx=2, pady=2, sticky="EW")

            # scrollable_frame.grid(row=0, columnspan=5, sticky="NSEW")

        else:
            no_receiver_data_label = ttk.Label(edit_receiver_frame, text="NO RECEIVER DATA AVAILABLE")
            no_receiver_data_label.grid(column=1, row=2, columnspan=3, sticky="EW", padx=10, pady=10)

    def save_receiver_data(self):
        if self.radiobutton_selection.get() == "Add":
            for receiver in self.receiver_data:
                name = receiver[0].get()
                ID = receiver[1].get()
                acct = receiver[2].get()
                transcode = receiver[3].get()
                amount = receiver[4].get()
                originator = self.originators_list_box.get(self.originators_list_box.curselection())

                new_receiver(originator, name, ID, acct, transcode, amount)

                print(f'<NEW DATA SAVED: {name}, {ID}, {acct}, {transcode}, {amount}>')

        elif self.radiobutton_selection.get() == "Edit":
            for receiver in self.receiver_data:
                name = receiver[0].get()
                ID = receiver[1].get()
                acct = receiver[2].get()
                transcode = receiver[3].get()
                amount = receiver[4].get()
                originator = self.originators_list_box.get(self.originators_list_box.curselection())

                update_receiver(originator, name, ID, acct, transcode, amount)

                print(f'<EDITED DATA SAVED: {name}, {ID}, {acct}, {transcode}, {amount}>')

        else:
            raise ValueError(f'<SAVE TYPE ERROR>')

        self.reset_screen

    def delete_receivers(self):
        for receiver in self.receiver_data:
            name = receiver[0].get()
            originator = self.originators_list_box.get(self.originators_list_box.curselection())

            inactivate_receiver(originator, name)

            print(f'<RECEIVER INACTIVATED: {name}>')

            self.reset_screen

    @property
    def reset_screen(self):
        for widget in self.add_receiver_container.winfo_children():
            widget.destroy()

        self.show_receiver()

    @property
    def reset_receiver_manager(self):
        for widget in self.add_receiver_frame.winfo_children():
            widget.destroy()

        self.receiver_data.clear()
        self.form_count_val.set(0)




