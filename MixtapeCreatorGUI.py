try: 
    import tkinter as tk
    from tkinter import filedialog
    from PIL import ImageTk, Image
    import MixtapeCreatorApp

except Exception as e:
    print("Please install the required modules to execute the program: {}".format(e))
    exit()

##################################################################################################################

# This class represents all the attributes and methods needed to create and format the GUI

class MixtapeCreatorGUI:

    def __init__(self, window_dim, bg_colour, win_height_offset):
        self.window_dim = window_dim
        self.bg_colour = bg_colour
        self.win_height_offset = win_height_offset
        self.root = tk.Tk()
    
    def main(self):
        bg_canvas = self.set_initial_params()
        songs_list_path = EntryBox(0.233, 0.26, bg_canvas, 44, "white", 
        "Enter File Path to Songs List", ("Calibri", 11), tk.LEFT, True, "file")
        
        save_to_dir = EntryBox(0.233, 0.3, bg_canvas, 44, "white", 
        "Save To Directory...", ("Calibri", 11), tk.LEFT, True, "dir")
        
        mixtape_img = ImageTk.PhotoImage(self.load_mixtape_image())
        bg_canvas.create_image(353, 388, anchor = tk.CENTER, image = mixtape_img)

        mixtape_title = EntryBox(0.273, 0.43, bg_canvas, 32, "#e7e5cc", "Enter Mixtape Title", 
        ("Permanent Marker", 11), tk.CENTER, False, "none")

        state = tk.Label(bg_canvas, text = "Please fill all fields", bg = self.bg_colour, fg = "#9c9c9c", font = ("Calibri", 8))
        state.place(relx = 0.5, rely = 0.87, anchor = tk.CENTER)

        self.create_main_btns(self.root, bg_canvas, songs_list_path, save_to_dir, mixtape_title, state)
        self.root.mainloop()

    # This method sets the GUI window position to the center of the screen
    def set_window_position(self):
        position_right = int(self.root.winfo_screenwidth()/2 - self.window_dim/2)
        position_down = int(self.root.winfo_screenheight()/2 - self.window_dim/2) - self.win_height_offset
        self.root.geometry("{}x{}+{}+{}".format(self.window_dim, self.window_dim, position_right, position_down))

    # This method sets the title of the program and displays it on the GUI
    def set_gui_title(self, canvas_to_link):
        gui_header = tk.Label(canvas_to_link, text = "MIXTAPE CREATOR", 
            font = ("Lato", 30), bg = self.bg_colour, fg = "white")
        gui_header.place(relx = 0.5, rely = 0.15, anchor = tk.CENTER)

    # This method initializes the contents of the GUI
    def set_initial_params(self):
        # do not allow window to be resized
        self.root.resizable(False, False)
        # set GUI description
        self.root.title("Mixtape Creator - Version 2 (By Niphan Sethi)")
        # position window to open at center of screen
        self.set_window_position()
        # create a canvas and pack it to root (used as background of GUI)
        canvas = tk.Canvas(self.root, height = self.window_dim , width = self.window_dim, 
        bg = self.bg_colour, highlightcolor = "white")
        canvas.pack()
        # set and display title on canvas
        self.set_gui_title(canvas)
        return canvas
    
    def create_main_btns(self, root, link_to, songs_list_entry, dir_entry, title_entry, state):

        button_border = tk.Frame(link_to, width = 380, height = 30, bg = "#9c9c9c")
        button_border.place(relx = 0.233, rely = 0.775, anchor = tk.NW)

        start_btn = tk.Button(button_border, text = "Create Mixtape", font = ("Calibri", 9), padx = 49, 
        command = lambda : MixtapeCreatorApp.InputValidator.create_instance(songs_list_entry, dir_entry, title_entry).validate_input(root, state, songs_list_entry, dir_entry, title_entry))
        start_btn.place(relx = 0.998, rely = 0.1, anchor = tk.NE)

        reset_btn = tk.Button(button_border, text = "Reset Fields", font = ("Calibri", 9), padx = 57, 
        command = lambda : self.reset_all(songs_list_entry, dir_entry, title_entry, state))

        reset_btn.place(relx = 0.007, rely = 0.1, anchor = tk.NW)

    
    # This method loads the image of the mixtape onto the GUI
    @staticmethod
    def load_mixtape_image():
        load_img = Image.open("res/mixtape_image.png")
        load_img = load_img.resize((382, 250), Image.ANTIALIAS)
        return load_img
    
    # This method resets all of the entry boxes to the default text
    @staticmethod
    def reset_all(songs_list_entry, dir_entry, title_entry, state):
        songs_list_entry.set_default_text() 
        dir_entry.set_default_text()
        title_entry.set_default_text()
        # indicate to users to fill all fields before proceeding with mixtape creation
        state.configure(text = "Please fill all fields")

##################################################################################################################

# This class represents the contents of an entry object. It contains all of the relevant attributes 
# and methods to position and style the entry box

class EntryBox:

    def __init__(self, x_pos, y_pos, link_to, box_width, box_colour, default_text, 
                text_font, text_anchor, include_browse, browse_type):
        self.relx_pos = x_pos
        self.rely_pos = y_pos
        self.link_to = link_to
        self.box_width = box_width
        self.box_colour = box_colour
        self.default_text = default_text
        self.text_font = text_font
        self.text_anchor = text_anchor
        # use the specified attributes to create an entry box
        self.create_user_entry()
        # use a flag variable to determine whether an entry object needs a corresponding browse button
        if include_browse:
            self.browse_button = BrowseButton(link_to, y_pos, self.user_entry, self, browse_type)

    # This method deletes the default text in the entry box (called when the entry box is 
    # clicked by the user)
    def enter_text(self, user_entry):
        # change the state of the entry box from DISABLED to NORMAL
        user_entry.configure(state = tk.NORMAL)
        # delete default text
        user_entry.delete(0, tk.END)

    # This method allows the user to enter text into the entry box when clicked
    def on_click(self, event):
        # if user has not entered any text into the entry box, delete default text and 
        # change state to NORMAL        
        if self.user_entry.cget("state") != tk.NORMAL:
            self.enter_text(self.user_entry)

    # This method is reponsible for setting the default text into the entry box
    def set_default_text(self):
        # delete all existing text (if any)
        self.user_entry.delete(0, tk.END)
        # insert default text
        self.user_entry.insert(0, self.default_text)
        # set state as DISABLED and set default text with required font parameters
        self.user_entry.configure(state = tk.DISABLED, font = self.text_font)

    # This method resets the entry box back to its default configuration
    def reset_user_entry(self, event):
        if len(self.user_entry.get()) == 0 and self.user_entry.cget("state") == tk.NORMAL:
            self.set_default_text()

    # This method is responsible for creating the entry box based on the specified attributes
    def create_user_entry(self):
        self.user_entry = tk.Entry(self.link_to, width = self.box_width, justify = self.text_anchor)
        self.user_entry.place(relx = self.relx_pos, rely = self.rely_pos)
        self.user_entry.configure(disabledbackground = self.box_colour, bg = self.box_colour, relief = tk.FLAT)
        self.set_default_text()
        # user can only type in entry box when it is clicked
        self.user_entry.bind("<Button>", self.on_click)
        # if user clicks away from entry box and entry box empty, reset to its default text
        self.user_entry.bind("<FocusOut>", self.reset_user_entry)

##################################################################################################################

# This class represents the corresponding browse button to an entry box (a user can browse 
# for the songs list text file and a directory to store the mixtape in)

class BrowseButton:

    def __init__(self, link_to, y_pos, display_on, user_entry_object, browse_type):
        self.link_to = link_to
        self.rely_pos = y_pos
        self.create_button(user_entry_object, display_on, browse_type)
    
    # This method creates the browse button according to the attributes specified
    def create_button(self, user_entry_object, user_entry, browse_type):
        self.browse_button = tk.Button(self.link_to, text = "Browse", 
                             font = ("Calibri", 9), padx = 7, pady = 0.4, 
                             command = self.determine_callback(user_entry_object, user_entry, browse_type))
        self.browse_button.place(relx = 0.69, rely = self.rely_pos)
    
    # This method determines whether a file path or directory path is needed for the corresponding entry box
    def determine_callback(self, user_entry_object, user_entry, browse_type):
        # prompt for file
        if browse_type == "file":
            return lambda : self.select_file(user_entry_object, user_entry)
        # prompt for directory
        else:
            return lambda : self.select_dir(user_entry_object, user_entry)
    
    # This method allows the user to browse for a text file path
    def select_file(self, user_entry_object, user_entry):
        filename = tk.filedialog.askopenfilename(initialdir = "/", title = "Select File", 
                   filetypes = [("Text Document", "*.txt")])
        # if a file has been selected, insert file path into entry box
        if filename:
            user_entry_object.enter_text(user_entry)
            user_entry.insert(0, filename)

    # This method allows the user to browse to a specific directory
    def select_dir(self, user_entry_object, user_entry):
        selected_directory = tk.filedialog.askdirectory()
        # if a directory has been selected, insert into entry box
        if selected_directory:
            user_entry_object.enter_text(user_entry)
            user_entry.insert(0, selected_directory)

##################################################################################################################

if __name__ == "__main__":
    # Execute program
    MixtapeCreatorGUI(700, "#263D42", 20).main()
