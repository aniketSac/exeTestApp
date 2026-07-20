import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FormControlsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Form Controls Dashboard")
        self.root.configure(bg="#f5f5f5")
        
        # Approximate the 320px width from HTML
        self.root.geometry("380x600")
        self.root.resizable(False, False)

        # Style configurations for fonts and buttons
        self.title_font = ("Sans-serif", 9, "bold")
        self.element_font = ("Sans-serif", 10)
        
        # Configure a custom style map for radio buttons to match CSS active states
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('Custom.TRadiobutton', font=self.element_font, background='#eee', foreground='#555', padding=6)
        self.style.map('Custom.TRadiobutton',
            background=[('selected', '#4caf50')],
            foreground=[('selected', '#000')]
        )

        # Intercept Refresh Shortcuts like the JS Event Listener
        self.root.bind("<F5>", self.block_refresh)
        self.root.bind("<Control-r>", self.block_refresh)
        self.root.bind("<Command-r>", self.block_refresh) # For Mac compatibility

        # Build Container Widgets
        self.create_toggle_container()
        self.create_radio_group_one()
        self.create_radio_group_two()
        self.create_dropdown_container()

    def block_refresh(self, event):
        """ Replaces the native-modal HTML dialog error message """
        messagebox.showinfo("System Notification", "Keyboard Refresh Action Blocked.")
        return "break" # Prevents default system behavior

    def create_card_container(self):
        """ Helper method to generate the uniform white card styling (.container) """
        card = tk.Frame(self.root, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#e8e8e8")
        card.pack(fill="x", padx=30, pady=10)
        return card

    def create_toggle_container(self):
        container = self.create_card_container()
        
        # Toggle 1 Row
        row1 = tk.Frame(container, bg="white")
        row1.pack(fill="x", pady=5)
        
        lbl_spdt1 = tk.Label(row1, text="SPDT1", font=self.title_font, fg="#888", bg="white")
        lbl_spdt1.pack(side="left")
        
        self.toggle1_var = tk.BooleanVar(value=False)
        chk_1 = tk.Checkbutton(row1, variable=self.toggle1_var, bg="white", activebackground="white",
                               command=lambda: print(f"Toggle 1: {'ON' if self.toggle1_var.get() else 'OFF'}"))
        chk_1.pack(side="right")

        # Toggle 2 Row
        row2 = tk.Frame(container, bg="white")
        row2.pack(fill="x", pady=5)
        
        lbl_spdt2 = tk.Label(row2, text="SPDT2", font=self.title_font, fg="#888", bg="white")
        lbl_spdt2.pack(side="left")
        
        self.toggle2_var = tk.BooleanVar(value=False)
        chk_2 = tk.Checkbutton(row2, variable=self.toggle2_var, bg="white", activebackground="white",
                               command=lambda: print(f"Toggle 2: {'ON' if self.toggle2_var.get() else 'OFF'}"))
        chk_2.pack(side="right")

    def create_radio_group_one(self):
        container = self.create_card_container()
        
        lbl = tk.Label(container, text="RADIO GROUP ONE", font=self.title_font, fg="#888", bg="white")
        lbl.pack(anchor="w", pady=(0, 8))

        # Horizontal grouping bar (.radio-group background wrapper)
        wrapper = tk.Frame(container, bg="#eee", padx=4, pady=4)
        wrapper.pack(fill="x")

        self.radio1_var = tk.StringVar(value="G1 Option 1")
        options = [("Opt 1", "G1 Option 1"), ("Opt 2", "G1 Option 2"), 
                   ("Opt 3", "G1 Option 3"), ("Opt 4", "G1 Option 4")]

        for text, val in options:
            r = ttk.Radiobutton(wrapper, text=text, value=val, variable=self.radio1_var, 
                                style='Custom.TRadiobutton', 
                                command=lambda: print(f"Radio Group 1: {self.radio1_var.get()}"))
            r.pack(side="left", expand=True, fill="x")

    def create_radio_group_two(self):
        container = self.create_card_container()
        
        lbl = tk.Label(container, text="RADIO GROUP TWO", font=self.title_font, fg="#888", bg="white")
        lbl.pack(anchor="w", pady=(0, 8))

        wrapper = tk.Frame(container, bg="#eee", padx=4, pady=4)
        wrapper.pack(fill="x")

        self.radio2_var = tk.StringVar(value="G2 Option A")
        options = [("Opt A", "G2 Option A"), ("Opt B", "G2 Option B"), 
                   ("Opt C", "G2 Option C"), ("Opt D", "G2 Option D")]

        for text, val in options:
            r = ttk.Radiobutton(wrapper, text=text, value=val, variable=self.radio2_var, 
                                style='Custom.TRadiobutton',
                                command=lambda: print(f"Radio Group 2: {self.radio2_var.get()}"))
            r.pack(side="left", expand=True, fill="x")

    def create_dropdown_container(self):
        container = self.create_card_container()
        
        lbl = tk.Label(container, text="DROPDOWN MENU", font=self.title_font, fg="#888", bg="white")
        lbl.pack(anchor="w", pady=(0, 8))

        # Dynamically generate 0 to 63 binary string choices loop like the JavaScript setup
        dropdown_vals = []
        for i in range(64):
            binary_str = format(i, '06b')
            dropdown_vals.append(f"{binary_str} (Dec:{i})")

        self.dropdown_var = tk.StringVar()
        dropdown = ttk.Combobox(container, textvariable=self.dropdown_var, values=dropdown_vals, state="readonly")
        dropdown.pack(fill="x", ipady=4)
        dropdown.current(0) # Select first index by default
        
        # Trace dropdown adjustments
        dropdown.bind("<<ComboboxSelected>>", lambda e: print(f"Dropdown Selection: {self.dropdown_var.get().split(' ')[0]}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = FormControlsDashboard(root)
    root.mainloop()