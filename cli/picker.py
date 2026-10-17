from tkinter import Tk, filedialog


def pick_source_files():
    root = Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(
        title="Select Source Files"
    )

    root.destroy()

    return list(files)


def pick_output_folder():
    root = Tk()
    root.withdraw()

    folder = filedialog.askdirectory(
        title="Select Output Repository"
    )

    root.destroy()

    return folder