import tkinter as tk
from tkinter import filedialog, Text
from compress import compress
from decompress import decompress


class FileEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, bg="#1c1c1c")
        self.frame.pack(anchor="center", pady=20)
        self.root.title("Arithmetic Coding GUI")
        self.root.geometry("800x600")
        self.root.config(bg="#1c1c1c")

        self.compress_button = self.createButton(
            "Compress File", lambda: self.open_and_edit_file(True))
        self.decompress_button = self.createButton(
            "Decompress File", lambda: self.open_and_edit_file(False))

    def createButton(self, text, command):
        button = tk.Button(self.frame, text=text, command=command,
                           bg="#72b000", font=("Arial", 12, "bold"))
        button.pack(side="right", padx=10)
        return button

    def disableButton(self, button):
        button.config(state="disabled")
        button.pack_forget()

    def enableButton(self, button):
        button.config(state="normal")
        button.pack(side="right", padx=10)

    def open_and_edit_file(self, compressAction):
        file_types = [("Text files", "*.txt")
                      ] if compressAction else [("JSON files", "*.json")]
        inputFile = filedialog.askopenfilename(filetypes=file_types)

        if not inputFile:
            return

        with open(inputFile, "r") as file:
            content = file.read()

        action = "Compress" if compressAction else "Decompress"

        text_widget = Text(self.root, wrap="word", width=50,
                           height=15, font=("Arial", 14))
        text_widget.insert(tk.END, content)
        text_widget.config(state="disabled")
        text_widget.pack(pady=10)

        self.disableButton(self.compress_button)
        self.disableButton(self.decompress_button)

        def allowEdit():
            text_widget.config(state="normal")
            self.disableButton(proceed_button)
            self.disableButton(edit_button)
            self.disableButton(back_button)

            self.enableButton(save_button)
            self.enableButton(cancle_button)

        def doAction():
            if compressAction:
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if output_file:
                    compress(inputFile, output_file)
            else:
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                if output_file:
                    decompress(inputFile, output_file)
            finishAction()

        def finishAction():
            # Re-enable buttons and clear the text widget
            self.enableButton(self.compress_button)
            self.enableButton(self.decompress_button)
            text_widget.destroy()
            proceed_button.destroy()
            edit_button.destroy()
            back_button.destroy()

        def saveChanges():
            with open(inputFile, "w") as file:
                file.write(text_widget.get("1.0", tk.END)[:-1])
            finishChanges()

        def finishChanges():
            with open(inputFile, "r") as file:
                content = file.read()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state="disabled")
            self.enableButton(proceed_button)
            self.enableButton(edit_button)
            self.enableButton(back_button)

            self.disableButton(save_button)
            self.disableButton(cancle_button)

        proceed_button = self.createButton(action, doAction)
        edit_button = self.createButton("Edit file", allowEdit)
        back_button = self.createButton("Back", finishAction)
        save_button = self.createButton("Save Changes", saveChanges)
        cancle_button = self.createButton("Cancel", finishChanges)

        self.disableButton(save_button)
        self.disableButton(cancle_button)

    def run(self):
        self.root.mainloop()


# Main window setup
app = FileEditorApp()
app.run()
