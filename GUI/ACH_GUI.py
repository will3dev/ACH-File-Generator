import tkinter as tk
from tkinter import ttk
from GUI.windows import set_dpi_awareness
from GUI.FileCreate import FileCreate_Page
from GUI.HomePage import HomePage
from GUI.AddOriginator_Page import AddOriginator
from GUI.AddReceiver_Page import AddReceiver


set_dpi_awareness()

MAIN_BACKGROUND = "#000000"
FRAME_BACKGROUND = "#808080"
LIGHT_BACKGROUND = "#bfbfbf"
POP_COLOR = "#e00085"
WHITE_TEXT = "#ffffff"


class ACH_Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("BankProv ACH Generator")
        #self.resizable(False, False)

        # --Set Up Styles--
        style = ttk.Style(self)
        style.theme_use("clam")

        # --Frame Styles--
        style.configure("Page.TFrame", background=MAIN_BACKGROUND)
        style.configure("Function.TFrame", background=FRAME_BACKGROUND)

        # --Listbox--
        style.configure("Listbox.TListbox", font="Arial",)

        # --Labels--
        style.configure("Warning.TLabel", font="Arial 20", foreground=POP_COLOR, background=FRAME_BACKGROUND, weight="bold")
        style.configure("Header.TLabel", font="Arial 38", foreground=WHITE_TEXT, background=MAIN_BACKGROUND,)
        style.configure("Table.TLabel", font="Arial 28", foreground=WHITE_TEXT, background=FRAME_BACKGROUND,)
        style.configure("TableAlt.TLabel", font="Arial 28", foreground=WHITE_TEXT, background=MAIN_BACKGROUND)
        style.configure("FieldPop.TLabel", foreground=POP_COLOR, font="Arial 20")
        style.configure("Field.TLabel", font="Arial", foreground=WHITE_TEXT, background=FRAME_BACKGROUND)

        # --Buttons--
        style.configure("FieldCheck.TCheckbutton", font="Arial", foreground=WHITE_TEXT, background=FRAME_BACKGROUND)
        style.configure("ACHButton.TButton", background=LIGHT_BACKGROUND, font="Arial")
        style.configure("BigRadio.TRadiobutton", font="Arial 20", background=MAIN_BACKGROUND, foreground=WHITE_TEXT)

        # --Maps--
        style.map(
            "ACHButton.TButton",
            background=[("active", POP_COLOR), ("disabled", LIGHT_BACKGROUND)]
        )
        style.map('Dropdown.TCombobox', fieldbackground=[('readonly', WHITE_TEXT)])
        style.map('Dropdown.TCombobox', selectbackground=[('readonly', POP_COLOR)])
        style.map('Dropdown.TCombobox', selectforeground=[('readonly', WHITE_TEXT)])
        style.map('Dropdown.TCombobox', highlightcolor=[('pressed', POP_COLOR)])

        style.map("BigRadio.TRadiobutton", foreground=[("selected", POP_COLOR)])

        style.map("FieldCheck.TCheckbutton", foreground=[('selected', POP_COLOR)])
        style.map("FieldCheck.TCheckbutton", background=[('selected', WHITE_TEXT)])
        style.map("FieldCheck.TCheckbutton", highlightbackground=[('active', WHITE_TEXT)])
        style.map("FieldCheck.TCheckbutton", highlightcolor=[('active', POP_COLOR)])


        style.map('TListbox', selectforeground=[('readonly', WHITE_TEXT)])
        style.map('TListbox', selectbackground=[('readonly', POP_COLOR)])



        self["background"] = MAIN_BACKGROUND

        # --Main Frame--

        self.container = ttk.Frame(self, style="Page.TFrame")
        self.container.grid(row=1, column=2, sticky="NSEW")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.frames = dict()

        homepage_frame = HomePage(
            self.container, self,
            self.show_createfile,
            self.show_originator,
            self.show_receiver,
        )
        homepage_frame.grid(row=0, column=0, sticky="NSEW",)

        self.frames[HomePage] = homepage_frame

        self.show_frame(HomePage)

        # main_window_scroll = ttk.Scrollbar(self.container, orient="horizontal")
        # main_window_scroll.grid(column=0)


    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def show_createfile(self):
        filecreate_frame = FileCreate_Page(self.container, self, lambda: self.show_frame(HomePage), self.show_createfile)
        filecreate_frame.grid(column=0, row=0, sticky="NSEW")

        filecreate_frame.tkraise()

    def show_originator(self):
        originator_frame = AddOriginator(self.container, self, lambda: self.show_frame(HomePage), self.show_originator)
        originator_frame.grid(column=0, row=0, sticky="NSEW")

        originator_frame.tkraise()

    def show_receiver(self):
        receiver_frame = AddReceiver(self.container, self, lambda: self.show_frame(HomePage), self.show_receiver)
        receiver_frame.grid(column=0, row=0, sticky="NSEW")

        receiver_frame.tkraise()


