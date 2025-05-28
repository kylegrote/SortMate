#Created by Kyle Grote, 2025
#This program is free to use.
#it was created as piece of Kyle Grote's Portfolio

version = "1.1"


# <----------------------------------------------script setup------------------------------------------------->
import shutil
import threading

import time
import pdf2image
from PIL import Image, ImageTk
import pytesseract
import re
import os
from os import listdir
from os.path import isfile, join, exists
import pandas as pd
from pathlib import Path
# from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, BOTH, LEFT, RIGHT, VERTICAL, HORIZONTAL, Y, X




# <----------------------------------------------search term defaults------------------------------------------------->

try:
    dfSetup = pd.read_csv("PDF Mail Sorter Setup.csv")
except FileNotFoundError:
    data = {'mySourcePath': [""], 'tesseractPath': [""], "Created by Kyle Grote, 2025.":[""]}
    dfSetup = pd.DataFrame(data)
    dfSetup.to_csv("PDF Mail Sorter Setup.csv", index=False)

try:
    dfCategories = pd.read_csv("PDF Mail Sorter Category Filters.csv")
except FileNotFoundError:
    data = {'Category Name': ["Directory Name"], 'Category Filter Search Criteria': ["Keyword or phrase"], 'Destination Path': ["Destination Path(eg C:\My Documents)"]}
    dfCategories = pd.DataFrame(data)
    dfCategories.to_csv("PDF Mail Sorter Category Filters.csv", index=False)

try:
    dfItems = pd.read_csv("PDF Mailer Sorter Item Filters.csv")
except FileNotFoundError:
    data = {'Item Name': ["Item Name"], 'Item Filter Search Criteria': ["Keyword or Phrase"]}
    dfItems = pd.DataFrame(data)
    dfItems.to_csv("PDF Mailer Sorter Item Filters.csv", index=False)


mySourcePath = dfSetup["mySourcePath"][0]
tesseractPath = dfSetup["tesseractPath"][0]

import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = f'{tesseractPath}'
sourceFolder = mySourcePath


bg_color = "#FFFFFF"       # white
fg_color = "#000000"       # black
button_color = "#000000"   # not used
highlight_color = "#000000"  # black
fontType = "Inter Bold"





def createFolderIfNotExist(folderName:str):
    """Creates folder if it doesnt exist"""
    if os.path.isdir(folderName) == False:
        # directory exists?
        os.mkdir(folderName)
        write(f"destination directory was invalid. New Directory created: {folderName} ")


def moveFile(source, destination):
    try:
        shutil.move(source, destination)
    except shutil.Error:
        base, ext = os.path.splitext(source)
        copy_name = base + "_copy" + ext
        try:
            os.rename(source, copy_name)
        except PermissionError as e:
            writeWithIcon(f"skipping file: error: {e}", "img/warning.png", 8)
            return
        shutil.move(copy_name, destination)

def unique(listVar):
    return list(set(listVar))

def unique_preserve_order(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def updatefileCountLabel():
    try:
        fileList = os.listdir(sourceFolder)
        fileCount = len(fileList)
        runDescriptionLabel.config(text=f"{fileCount} files found in directory")
    except FileNotFoundError:
        runDescriptionLabel.config(text=f"Please set up source folder in \nGetting Started page")
    except TypeError:
        runDescriptionLabel.config(text=f"Please set up source folder in \nGetting Started page")
    root.after(5000, updatefileCountLabel)


def selectSourceFolder():
    global sourceFolder
    folder_selected = filedialog.askdirectory(title="Select a Folder")
    if folder_selected:
        sourceFolderLoc = folder_selected
        buttons["start_entry_2"].delete(0, 'end')
        buttons["start_entry_2"].insert(0, sourceFolderLoc)
        updatefileCountLabel()
        dfSetup.loc[0,"mySourcePath"] = sourceFolderLoc
        dfSetup.to_csv("PDF Mail Sorter Setup.csv", index = False)

        global mySourcePath
        global sourceFolder
        global tesseractPath

        mySourcePath = dfSetup["mySourcePath"][0]
        tesseractPath = dfSetup["tesseractPath"][0]
        sourceFolder = mySourcePath

        updatefileCountLabel()
        root.update()

def selectTesserectFolder():
    global tesseractPath
    folder_selected = filedialog.askopenfilename(title='Select "tesserect.exe" file', filetypes=[("EXE files", "*.exe"), ("All files", "*.*")])
    if folder_selected:
        tesseractLoc = folder_selected
        buttons["start_entry_1"].delete(0, 'end')
        buttons["start_entry_1"].insert(0, tesseractLoc)
        dfSetup.loc[0,"tesseractPath"] = tesseractLoc
        dfSetup.to_csv("PDF Mail Sorter Setup.csv", index = False)
        pytesseract.pytesseract.tesseract_cmd = f'{tesseractLoc}'

        global mySourcePath
        global sourceFolder
        global tesseractPath

        mySourcePath = dfSetup["mySourcePath"][0]
        tesseractPath = dfSetup["tesseractPath"][0]
        sourceFolder = mySourcePath
        root.update()


def write(text):
    label = tk.Label(frames["runFrame"], text=f"{text}", bg=bg_color, fg=fg_color, font=(fontType, 11))
    label.pack(anchor="w")  # side="top" is the default, so no need to specify it
    root.update()
    # frames["runFrame"].yview_scroll(400, "units")

runLines = 0
def writeWithIcon(text, iconPath, indent):
    frame = tk.Frame(frames["runFrame"], bg=bg_color)
    frame.pack(anchor="w", pady=2)

    indentText = ""
    for n in range(0,indent):
        indentText = indentText+" "

    text_label = tk.Label(frame, text=indentText, bg=bg_color, fg=fg_color, font=(fontType, 11))
    text_label.pack(side="left")

    img = Image.open(iconPath).resize((20, 20), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    icon_label = tk.Label(frame, image=tk_img, bg=bg_color)
    icon_label.image = tk_img  # Keep a reference
    icon_label.pack(side="left")

    text_label = tk.Label(frame, text=f"  {text}", bg=bg_color, fg=fg_color, font=(fontType, 11))
    text_label.pack(side="left")


    frames["runFrame"].update_idletasks()
    global runLines
    runLines += 1
    homeFrame.update_idletasks()
    homeFrame.configure(height=300 + (runLines * 34))
    updateScrollbarheight()
    # if runLines > 70:
    #     mainCanvas.yview_moveto(1.0)
    root.update()

pdfSelected = ""
def clickLink(pdf):
    global pdfSelected
    pdfSelected = pdf
    openPDFPreview()

def writeLink(pdf):
    link = tk.Label(frames["runFrame"], text=pdf, bg=bg_color, fg="#0070C5", cursor="hand2", font=(fontType, 11, "underline"))
    link.pack()
    link.bind("<Button-1>", lambda e: clickLink(pdf))



def emoji(path):
    """Returns a Tk-compatible image from the emoji path"""
    img = Image.open(path).resize((20, 20), Image.LANCZOS)
    return ImageTk.PhotoImage(img)




def openPDFPreview():
    global pdfPreviewIMGDict

    if not pdfPreviewIMGDict:
        return  # Nothing to preview

    global pdfSelected
    for pdf in pdfPreviewIMGDict["file"]:
        if pdf == pdfSelected:
            indexWherePDFIsLocatedInDict = pdfPreviewIMGDict["file"].index(pdf)


    previewWin = tk.Toplevel(root)
    previewWin.title("PDF Preview")
    previewWin.minsize(width=900, height=600)
    previewWin.configure(bg=bg_color)

    # Scrollable canvas
    canvas = tk.Canvas(previewWin, bg=bg_color, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(previewWin, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")

    previewWin.grid_rowconfigure(0, weight=1)
    previewWin.grid_columnconfigure(0, weight=1)

    canvas.configure(yscrollcommand=scrollbar.set)

    previewFrame = tk.Frame(canvas, bg=bg_color)
    canvas.create_window((0, 0), window=previewFrame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    previewFrame.bind("<Configure>", on_frame_configure)

    def on_close():
        bindMousewheelOnRoot()
        previewWin.destroy()
    def on_focus_out():
        bindMousewheelOnRoot()

    previewWin.protocol("WM_DELETE_WINDOW", on_close)
    # previewWin.bind("<FocusOut>", on_focus_out)

    # Header
    if os.path.exists(f"{mySourcePath}/{pdfPreviewIMGDict["file"][indexWherePDFIsLocatedInDict]}"):
        header = tk.Label(previewFrame, text=pdfPreviewIMGDict["file"][indexWherePDFIsLocatedInDict],
                          bg="#FFFFFF", fg="#000000", font=("Inter SemiBold", 22))
        header.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="n")

        # manually sort prompt
        def on_ok():
            manSortDestinationFolder = filedialog.askdirectory(title=f"manually sort {pdfPreviewIMGDict["file"][indexWherePDFIsLocatedInDict]}")
            createFolderIfNotExist(manSortDestinationFolder)
            moveFile(mySourcePath + "/" + pdfPreviewIMGDict["file"][indexWherePDFIsLocatedInDict], manSortDestinationFolder)
            previewWin.destroy()

            manSortSuccessful.config(text=f"Manual Save Successful", fg="#000000")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#1A1A1A")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#333333")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#4D4D4D")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#666666")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#808080")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#999999")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#B3B3B3")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#CCCCCC")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#E6E6E6")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#F2F2F2")
            time.sleep(.1)
            root.update()
            manSortSuccessful.config(fg="#000000", text="")
            root.update()

            bindMousewheelOnRoot()


        images["preview_manSort_1"] = PhotoImage(file="assets/manSortButton.png")
        buttons["manSort"] = Button(previewFrame,
                                      image=images["preview_manSort_1"],
                                      borderwidth=0,
                                      highlightthickness=0,
                                      command=on_ok,
                                      relief="flat"
                                      )
        buttons["manSort"].grid(row=2, column=0,columnspan=3, sticky="n")

        previewFrame.grid_columnconfigure(0, weight=1)
        previewFrame.grid_columnconfigure(1, weight=1)

        # Image Frame
        image_frame = tk.Frame(previewFrame, bg=bg_color)
        image_frame.grid(row=10, column=0, padx=10, sticky="n")

        for img in pdfPreviewIMGDict["images"][indexWherePDFIsLocatedInDict]:
            img.thumbnail((400, 570))
            tk_img = ImageTk.PhotoImage(img)
            img_label = tk.Label(image_frame, image=tk_img, bg=bg_color)
            img_label.image = tk_img
            img_label.pack(pady=5)

        # Text Frame
        text_frame = tk.Frame(previewFrame, bg=bg_color)
        text_frame.grid(row=10, column=1, columnspan=2, padx=10, sticky="n")

        text_label = tk.Label(text_frame, text="📝 Translated Text:", bg=bg_color,
                              fg=highlight_color, font=(fontType, 14, "bold"))
        text_label.pack(anchor="w", pady=(0, 5))


        text_content = pdfPreviewIMGDict["text"][indexWherePDFIsLocatedInDict]
        text_box = tk.Label(text_frame, text=text_content, wraplength=400,
                            bg=bg_color, fg=fg_color, justify="left",
                            font=(fontType, 11), anchor="nw")
        text_box.pack(anchor="w")


    else:
        header = tk.Label(previewFrame, text="File has been moved or no longer exists",
                          bg=bg_color, fg=highlight_color, font=(fontType, 16, "bold"))
        header.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="n")

    def _on_preview_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    bind_mousewheel_scrolling(canvas, _on_preview_mousewheel)




def bind_mousewheel_scrolling(canvas_widget, scroll_func):
    def _on_enter(event):
        canvas_widget.bind_all("<MouseWheel>", scroll_func)
        canvas_widget.bind_all("<Button-4>", scroll_func)
        canvas_widget.bind_all("<Button-5>", scroll_func)

    def _on_leave(event):
        canvas_widget.unbind_all("<MouseWheel>")
        canvas_widget.unbind_all("<Button-4>")
        canvas_widget.unbind_all("<Button-5>")

    canvas_widget.bind("<Enter>", _on_enter)
    canvas_widget.bind("<Leave>", _on_leave)


def checkIfStringIsValid(string):
    if any(c.isalpha() for c in string):
        return True

    if any(c.isdigit() for c in string):
        return True
    return False

def checkForValidInputs(listOfEntries, errorLocation):
    xLine = 1
    errorsOnxLines = []
    saveError = False
    for entryInput in listOfEntries:
        entryInput = entryInput.get()
        errorMessage = "Expected Input to contain at least 1 number or letter"
        if checkIfStringIsValid(entryInput) == False:
            saveError = True
            errorsOnxLines.append(xLine)
        xLine += 1
    if saveError == True:
        if len(errorsOnxLines) > 3:
            errorInvalidDirSettingsLabel.config(
                text=f"Save Error: Failed to Save: \n{errorMessage} \n{errorLocation} line(s) \n{errorsOnxLines}")
        else:
            errorInvalidDirSettingsLabel.config(
                text=f"Save Error: Failed to Save: \n{errorMessage} \n{errorLocation} line(s) {errorsOnxLines}")
    return saveError


def saveChangesSettings():
    #check if directory input is valid
    xLine = 1
    errorsOnxLines = []
    saveError = False
    global errorInvalidDirSettingsLabel
    for dir in categoryEntriesAndButtons["categoryDirectoryEntries"]:
        dir = dir.get()
        if checkIfStringIsValid(dir) == False:
            saveError = True
            errorsOnxLines.append(xLine)
        if os.path.isdir(dir) == False:
            saveError=True
            errorsOnxLines.append(xLine)
        if saveError == True:
            if len(errorsOnxLines) >3:
                errorInvalidDirSettingsLabel.config(text=f"Save Error: Failed to Save: \nDirectory Path Invalid on line(s) \n{errorsOnxLines}")
            else:
                errorInvalidDirSettingsLabel.config(
                    text=f"Save Error: Failed to Save: \nDirectory Path Invalid on line(s) {errorsOnxLines}")
        xLine += 1




    checkSaveError = checkForValidInputs(categoryEntriesAndButtons["categoryEntries"], "Directory")
    if checkSaveError == True:
        saveError = True

    checkSaveError = checkForValidInputs(categoryEntriesAndButtons["categoryKeywordEntries"], "Directory")
    if checkSaveError == True:
        saveError = True

    checkSaveError = checkForValidInputs(itemEntriesAndButtons["itemNames"], "Item")
    if checkSaveError == True:
        saveError = True

    checkSaveError = checkForValidInputs(itemEntriesAndButtons["itemKeywords"], "Item")
    if checkSaveError == True:
        saveError = True


    if saveError == False:
        catDict = {"Category Name":[],"Category Filter Search Criteria":[], "Destination Path":[]}
        for input in categoryEntriesAndButtons["categoryEntries"]:
            catDict["Category Name"].append(input.get())
        for input in categoryEntriesAndButtons["categoryKeywordEntries"]:
            catDict["Category Filter Search Criteria"].append(input.get())
        for input in categoryEntriesAndButtons["categoryDirectoryEntries"]:
            catDict["Destination Path"].append(input.get())

        df = pd.DataFrame(catDict)
        df.to_csv("PDF Mail Sorter Category Filters.csv", index=False)

        itemDict = {"Item Name":[],"Item Filter Search Criteria":[]}
        for input in itemEntriesAndButtons["itemNames"]:
            itemNameInput = input.get().replace("/", "_").replace('\\', '_').replace(":", "_").replace("*", "_")
            itemNameInput.replace("?", "_").replace("'", "_").replace('"', "_").replace("<", "_").replace(">", "_")
            itemNameInput.replace("|", "_").replace(".", "_").replace('"', "_").replace(',', "_")
            itemDict["Item Name"].append(itemNameInput)
        for input in itemEntriesAndButtons["itemKeywords"]:
            itemDict["Item Filter Search Criteria"].append(input.get())


        df = pd.DataFrame(itemDict)
        df.to_csv("PDF Mailer Sorter Item Filters.csv", index=False)

        global dfCategories
        global dfItems
        dfCategories = pd.read_csv("PDF Mail Sorter Category Filters.csv")
        dfItems = pd.read_csv("PDF Mailer Sorter Item Filters.csv")

    if saveError == False:
        errorInvalidDirSettingsLabel.config(text=f"Save Successful", fg="#000000")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#1A1A1A")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#333333")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#4D4D4D")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#666666")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#808080")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#999999")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#B3B3B3")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#CCCCCC")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#E6E6E6")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#F2F2F2")
        time.sleep(.1)
        root.update()
        errorInvalidDirSettingsLabel.config(fg="#000000", text="")
        root.update()





def start_run_thread():
    thread = threading.Thread(target=run)
    thread.start()



pdfPreviewIMGDict= {"file":[], "text":[], "images":[]}
def run():
    timeStart = time.time()
    files = [f for f in listdir(mySourcePath) if isfile(join(mySourcePath, f))]
    buttons["runButton"].destroy()
    for pdf in files:
        printText = False
        try: #check if the pdf file is an image or pdf
            checkIfFileIsImage = Image.open(f"{mySourcePath}/{pdf}")
            isImageFile = True
            checkIfFileIsImage.close()
        except:
            isImageFile = False
        if ".pdf" in pdf or isImageFile == True:
            writeWithIcon(f"processing file: {pdf}", "img/document.png", 0)
            fileSize = os.path.getsize(f"{mySourcePath}/{pdf}")
            fileSize = fileSize/1000000
            if fileSize > 5: # if file bigger than 5mb give file size warning
                writeWithIcon(f"Large File: {round(fileSize, 1)}mb: File may take longer to process", "img/warning.png", 4)
            writeWithIcon(f"converting to image...", "img/picture.png", 4)
            try:
                imagespdf = pdf2image.convert_from_path(f"{mySourcePath}/{pdf}")
            except:
                # writeWithIcon(f"skipping file: error converting to image: {pdf}", "img/warning.png", 8)
                # continue
                imagespdf = [Image.open(f"{mySourcePath}/{pdf}")]

            # Extract text from each image
            writeWithIcon("Reading text from images...", "img/glass.png", 8)
            text = ''
            fulltext = ''
            for image in imagespdf:
                text += pytesseract.image_to_string(image)
                #check all orientations
                image90 = image.rotate(90)
                fulltext += pytesseract.image_to_string(image90)
                image180 = image.rotate(180)
                fulltext += pytesseract.image_to_string(image180)
                image270 = image.rotate(270)
                fulltext += pytesseract.image_to_string(image270)


            # Search for a specific string in the extracted text
            writeWithIcon("Sorting file...", "img/folder.png", 12)
            TEMPdestinationFolder = mySourcePath

            # search for a category term
            catIndex = 0
            for cat in dfCategories["Category Filter Search Criteria"]:
                fileFiltered = False

                if cat.lower() in text.lower() or cat.lower() in fulltext.lower():
                    writeWithIcon(f"{dfCategories["Category Name"][catIndex]} file...", "img/folder.png", 16)

                    # search for an item term
                    itemIndex = 0
                    for item in dfItems["Item Filter Search Criteria"]:
                        try:
                            item.lower()
                        except:
                            continue
                        if item.lower() in text.lower() or item.lower() in fulltext.lower():
                            writeWithIcon(f"{dfItems["Item Name"][itemIndex]} file...", "img/folder.png", 20)
                            TEMPdestinationFolder = dfCategories["Destination Path"][catIndex] + "/" + \
                                                    dfItems["Item Name"][itemIndex]
                            createFolderIfNotExist(TEMPdestinationFolder)
                            if isImageFile == True:
                                imagespdf[0].close()
                            moveFile(mySourcePath + "/" + pdf, TEMPdestinationFolder)
                            updatefileCountLabel()
                            fileFiltered = True
                            printText = False
                            break
                        else:
                            printText = True
                        itemIndex = itemIndex + 1

                else:
                    printText = True
                if fileFiltered == True:  # checks to see if loops need to be stopped
                    break
                catIndex = catIndex + 1










            else:
                writeWithIcon(f"skipping file: no match", "img/warning.png", 16)
                printText = True

            if printText == True:
                global pdfPreviewIMGDict
                pdfPreviewIMGDict["file"].append(pdf)
                pdfPreviewIMGDict["text"].append(f"{text}\n\nChecking Text on different orientations...\n\n{fulltext}")
                pdfPreviewIMGDict["images"].append(imagespdf)
                writeLink(pdf)








        else:
            writeWithIcon(f"skipping file: wrong file type: {pdf}\nPlease use pdf file type", "img/warning.png", 0)

    timeEnd = time.time()
    timeDiff = round(timeEnd - timeStart, 2)
    null = writeWithIcon(f"Process completed in {timeDiff} seconds.", "img/brain.png", 0)

    # Recreate Run Button
    buttons["runButton"] = Button(homeFrame,
        image=images["home_button_1"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: start_run_thread(),
        relief="flat"
    )
    buttons["runButton"].place(
        x=17.0,
        y=180.0,
        width=164.0,
        height=27.0
    )
    updatefileCountLabel()






# <------------------------------------------TK windows and scrollbar--------------------------------------------------->
root = Tk()

root.geometry("800x600")
root.configure(bg ="#FFFFFF")
root.title(f"SortMate v{version}")

mainFrame = tk.Frame(root, bg="#FFFFFF")
mainFrame.pack(fill=BOTH, expand=1)

mainCanvas = tk.Canvas(mainFrame, bg="#FFFFFF")
mainCanvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = tk.Scrollbar(mainFrame, orient=VERTICAL, command=mainCanvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

mainCanvas.configure(yscrollcommand=scrollbar.set)
mainCanvas.bind('<Configure>', lambda e: mainCanvas.configure(scrollregion=mainCanvas.bbox("all")))

frameForContent = tk.Frame(mainCanvas, bg="#FFFFFF")

mainCanvas.create_window((0,0), window=frameForContent, anchor="nw")

# Mouse wheel scroll support
def _on_mousewheel(event):
    if event.num == 5 or event.delta < 0:
        mainCanvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta > 0:
        mainCanvas.yview_scroll(-1, "units")

# Cross-platform mousewheel bindings
mainCanvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/macOS
mainCanvas.bind_all("<Button-4>", _on_mousewheel)  # Linux
mainCanvas.bind_all("<Button-5>", _on_mousewheel)

# make a Frame that goes into frameForContent, this Frame holds your content,
# for all basic purposes, treat your frameForContent as root


def bindMousewheelOnRoot():
    mainCanvas.configure(yscrollcommand=scrollbar.set)
    mainCanvas.bind('<Configure>', lambda e: mainCanvas.configure(scrollregion=mainCanvas.bbox("all")))
    mainCanvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/macOS
    mainCanvas.bind_all("<Button-4>", _on_mousewheel)
    mainCanvas.bind_all("<Button-5>", _on_mousewheel)

def updateScrollbarheight():
    frameForContent.update_idletasks()  # Redraw the frame
    mainCanvas.configure(scrollregion=mainCanvas.bbox("all"))  #  Recalculate scroll region

def onFocusInRoot():
    bindMousewheelOnRoot()

# root.bind("<FocusIn>", onFocusInRoot)



images = {}
frames = {}
buttons = {}


# <------------------------------------------Home page--------------------------------------------------->


# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


# def relative_to_assetsHomePage(path: str) -> Path:
#     ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")
#     return ASSETS_PATH / Path(path)





homeFrame =  tk.Frame(frameForContent,height = 600,width = 2200, bg="#FFFFFF")
homeFrame.grid(row=0, column=0, sticky="nsew")

manSortSuccessful = tk.Label(
    homeFrame,
    anchor="nw",
    text=f"",
    bg="#FFFFFF",
    fg="#454545",
    font=("Inter", 12 * -1)
)

manSortSuccessful.place(
    x=573,
    y=39
)

tk.Label(
    homeFrame,
    anchor="nw",
    text="File Sorting",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter Bold", 22 * -1)
).place(
    x=17,
    y=9
)


images["home_link_1"] = PhotoImage(
    file="assets/homeButtonHighlight.png")
button_1 = Button(homeFrame,
                  image=images["home_link_1"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: homeFrame.tkraise(),
                  relief="flat"
                  )
button_1.place(
    x=17.0,
    y=58.0,
    width=164.0,
    height=36.0
)

images["home_link_2"] = PhotoImage(
    file="assets/startButton.png")
button_2 = Button(homeFrame,
                  image=images["home_link_2"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: startFrame.tkraise(),
                  relief="flat"
                  )
button_2.place(
    x=17.0,
    y=98.0,
    width=164.0,
    height=36.0
)

images["home_link_3"] = PhotoImage(
    file="assets/settingsButton.png")
button_3 = Button(homeFrame,
                  image=images["home_link_3"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: settingsFrame.tkraise(),
                  relief="flat"
                  )
button_3.place(
    x=17.0,
    y=139.0,
    width=164.0,
    height=36.0
)


tk.Label(
    homeFrame,
    anchor="nw",
    text="SortMate",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=56
)

tk.Label(
    homeFrame,
    anchor="nw",
    text="File Sorting PDF Scans Made Easy",
    bg="#FFFFFF",
    fg="#454545",
    font=("Inter", 12 * -1, "italic")
).place(
    x=232,
    y=81
)


images["home_button_1"] = PhotoImage(
    file="assets/button_1.png")
buttons["runButton"] = Button(homeFrame,
    image=images["home_button_1"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: start_run_thread(),
    relief="flat"
)
buttons["runButton"].place(
    x=17.0,
    y=180.0,
    width=164.0,
    height=27.0
)


runDescriptionLabel = tk.Label(
    homeFrame,
    anchor="nw",
    text=f"",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter Bold", 9 * -1, "italic")
)
runDescriptionLabel.place(
    x=32,
    y=211
)
updatefileCountLabel()

tk.Label(
    anchor="nw",
    text="Created by Kyle Grote, 2025. \nThis Program is free to use",
    bg="#FFFFFF",
    fg="#454545",
    font=("Inter", 10 * -1)
).place(
    x=17,
    y=550)


frames["runFrame"] =  tk.Frame(homeFrame,height = 99999,width = 2000, bg="#FFFFFF")
frames["runFrame"].place(x = 233, y = 116)






# <------------------------------------------getting started page--------------------------------------------------->
# def relative_to_assetsCreatedStartedPage(path: str) -> Path:
#     ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")
#     return ASSETS_PATH / Path(path)

startFrame =  tk.Frame(frameForContent,height = 1150,width = 800, bg="#FFFFFF")
startFrame.grid(row=0, column=0, sticky="nsew")


tk.Label(
    startFrame,
    anchor="nw",
    text="File Sorting",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter Bold", 22 * -1)
).place(
    x=17,
    y=9
)


images["start_link_1"] = PhotoImage(
    file="assets/homeButton.png")
button_1 = Button(startFrame,
                  image=images["start_link_1"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: homeFrame.tkraise(),
                  relief="flat"
                  )
button_1.place(
    x=17.0,
    y=58.0,
    width=164.0,
    height=36.0
)

images["C.r.e.a.t.e.d. .b.y. .K.y.l.e. .G.r.o.t.e.,. .2.0.2.5."] = PhotoImage(
    file="assets/startButtonHighlight.png")
button_2 = Button(startFrame,
                  image=images["C.r.e.a.t.e.d. .b.y. .K.y.l.e. .G.r.o.t.e.,. .2.0.2.5."],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: startFrame.tkraise(),
                  relief="flat"
                  )
button_2.place(
    x=17.0,
    y=98.0,
    width=164.0,
    height=36.0
)

images["start_link_3"] = PhotoImage(
    file="assets/settingsButton.png")
button_3 = Button(startFrame,
                  image=images["start_link_3"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: settingsFrame.tkraise(),
                  relief="flat"
                  )
button_3.place(
    x=17.0,
    y=139.0,
    width=164.0,
    height=36.0
)


tk.Label(
    startFrame,
    anchor="nw",
    text="SortMate",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=56
)


tk.Label(
    startFrame,
    anchor="nw",
    text='This program automatically organizes scanned PDF documents by reading their text and \nsorting them using custom filters. It looks for keywords that match categories like \n"Personal" or "Business," then moves each file into specific folders based on \ntype or sender (e.g., Bank of America, Utility Bills). It’s a simple way to \nkeep your digital documents neat—no manual sorting needed.',
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=81
)


tk.Label(
    startFrame,
    anchor="nw",
    text="Step 1: Install Tesseract OCR",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=193
)


tk.Label(
    startFrame,
    anchor="nw",
    text="To enable text recognition from scanned PDFs, you must first install Tesseract OCR:\n1. Download the installer from: 👉 https://github.com/UB-Mannheim/tesseract/wiki\n2. Run the installer and complete the installation.\n3. During setup, make note of the installation path to “tesseract.exe”, enter it below",
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=227
)


images["start_tesserectButton_1"] = PhotoImage(
    file="assets/button_2.png")
button_2 = Button(startFrame,
                  image=images["start_tesserectButton_1"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: selectTesserectFolder(),
                  relief="flat"
                  )
button_2.place(
    x=232.0,
    y=305.0,
    width=126.0,
    height=26.0
)
buttons["start_entry_1"] = tk.Entry(startFrame,
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
buttons["start_entry_1"].place(
    x=367.0,
    y=305.0,
    width=398.0,
    height=24.0
)
buttons["start_entry_1"].insert(0, tesseractPath)



tk.Label(
    startFrame,
    anchor="nw",
    text="Step 2: Select Source Folder",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=355
)


tk.Label(
    startFrame,
    anchor="nw",
    text="To choose the folder containing your scanned PDF documents:\n1. Click the Browse button to open a folder selection window.\n2. Select the folder containing your PDFs and confirm",
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=389
)

buttons["start_entry_2"] = Entry(
    startFrame,
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
buttons["start_entry_2"].place(
    x=367.0,
    y=446.0,
    width=398.0,
    height=24.0
)
buttons["start_entry_2"].insert(0, sourceFolder)


images["start_sourceButton_8"] = PhotoImage(file="assets/button_3.png")
button_3 = Button(startFrame,
                  image=images["start_sourceButton_8"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: selectSourceFolder(),
                  relief="flat"
)
button_3.place(
    x=232.0,
    y=446.0,
    width=125.23170471191406,
    height=26.0
)

tk.Label(
    startFrame,
    anchor="nw",
    text="Step 3: Set Up Sorting Directories",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=496
)


tk.Label(
    startFrame,
    anchor="nw",
    text='After launching the program:\n1. Go to the Settings section.\n2. For each sorting destination:\n    • Name the category (e.g., "Personal", "Business", "Receipts").\n    • Select the folder path where matching documents should be saved.\n    • Enter keyword that should trigger sorting into this folder.\n      • Example: If you enter keywords like your business name, UBI number, or \n        Business Legal Name, any document containing those terms will go into the \n        Business folder.',
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=530
)


tk.Label(
    startFrame,
    anchor="nw",
    text="Step 4: Configure Item Filters",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=692
)


tk.Label(
    startFrame,
    anchor="nw",
    text="Fine-tune your sorting with Item Filters:\n1. Navigate to the Settings > Item Filters section.\n2. Add specific keywords to look for within documents.\n3. When a document matches an item keyword:\n    • The program will automatically move it into a subfolder named after that keyword.\n    • If the subfolder doesn’t exist, it will be created.",
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=726
)


tk.Label(
    startFrame,
    anchor="nw",
    text="Step 5: Start Sorting",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=843
)


tk.Label(
    startFrame,
    anchor="nw",
    text="Once setup is complete:\n • Click the Run button.\n • The program will scan all PDFs in the source folder, extract text using OCR, and move \n    them into the appropriate destination folders based on your filters.",
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=877
)

tk.Label(
    startFrame,
    anchor="nw",
    text="Pro Tips",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=951
)


tk.Label(
    startFrame,
    anchor="nw",
    text=' • You can update directory names, paths, and keywords anytime.\n • Works best with cleanly scanned PDFs (300 DPI recommended).\n • No need to worry if your PDFs are sideways or upside down — the program uses OCR \n    that can read text in any orientation!\n • Make sure Tesseract is accessible via system PATH or configure its path in the \n    program settings if needed.\n • Keywords are not case sensitive. The keyword "business" will find documents with \n   "business", "BUSINESS", and "bUsInEsS" in them and sort them the same way. \n \n ',
    bg="#FFFFFF",
    fg="#454545",
    justify="left",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=983
)




# #<----------------------------------------load settings page--------------------------------------------------------->



# def relative_to_assetsSettingsPage(path: str) -> Path:
#     ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame2")
#     return ASSETS_PATH / Path(path)


settingsFrame =  tk.Frame(frameForContent,height = 600,width = 800, bg="#FFFFFF")
# settingsFrame.grid_propagate(True)
settingsFrame.grid(row=0, column=0, sticky="nsew")


tk.Label(
    settingsFrame,
    anchor="nw",
    text="File Sorting",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter Bold", 22 * -1)
).place(
    x=17,
    y=9
)


images["settings_link_1"] = PhotoImage(
    file="assets/homeButton.png")
button_1 = Button(settingsFrame,
                  image=images["settings_link_1"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: homeFrame.tkraise(),
                  relief="flat"
                  )
button_1.place(
    x=17.0,
    y=58.0,
    width=164.0,
    height=36.0
)

images["settings_link_2"] = PhotoImage(
    file="assets/startButton.png")
button_2 = Button(settingsFrame,
                  image=images["settings_link_2"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: startFrame.tkraise(),
                  relief="flat"
                  )
button_2.place(
    x=17.0,
    y=98.0,
    width=164.0,
    height=36.0
)

images["settings_link_3"] = PhotoImage(
    file="assets/settingsButtonHighlight.png")
button_3 = Button(settingsFrame,
                  image=images["settings_link_3"],
                  borderwidth=0,
                  highlightthickness=0,
                  command=lambda: settingsFrame.tkraise(),
                  relief="flat"
                  )
button_3.place(
    x=17.0,
    y=139.0,
    width=164.0,
    height=36.0
)


tk.Label(
    settingsFrame,
    anchor="nw",
    text="SortMate",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=56
)

tk.Label(
    settingsFrame,
    anchor="nw",
    text="File Sorting PDF Scans Made Easy",
    bg="#FFFFFF",
    fg="#454545",
    font=("Inter", 12 * -1, "italic")
).place(
    x=232,
    y=81
)

tk.Label(
    settingsFrame,
    anchor="nw",
    text="Sorting Directories",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
).place(
    x=232,
    y=105
)

tk.Label(
    settingsFrame,
    anchor="nw",
    text="Directory Name",
    bg="#FFFFFF",
    fg="#444444",
    font=("Inter", 12 * -1)
).place(
    x=232,
    y=139
)

tk.Label(
    settingsFrame,
    anchor="nw",
    text="Keyword",
    bg="#FFFFFF",
    fg="#444444",
    font=("Inter", 12 * -1)
).place(
    x=358,
    y=139
)

tk.Label(
    settingsFrame,
    anchor="nw",
    text="Directory Path",
    bg="#FFFFFF",
    fg="#444444",
    font=("Inter", 12 * -1)
).place(
    x=484,
    y=139
)

images["settings_addNewButton_1"] = PhotoImage(file="assets/addNewButton.png")
addNewButton = Button(settingsFrame,
    image=images["settings_addNewButton_1"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: createNewCategoryInputLine("", "", ""),
    relief="flat"
)

class selectDirectoryButton(Button):
    def __init__(self):
        super().__init__(settingsFrame,
            image=images["settings_button_2"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.selectDirectory(),
            relief="flat"
        )

    def selectDirectory(self):
        folder_selected = filedialog.askdirectory(title="Select a Folder")
        if folder_selected:
            for x in categoryEntriesAndButtons["categoryBrowseButtons"]:
                if x == self:
                    indx = categoryEntriesAndButtons["categoryBrowseButtons"].index(self)
                    categoryEntriesAndButtons["categoryDirectoryEntries"][indx].delete(0, 'end')
                    categoryEntriesAndButtons["categoryDirectoryEntries"][indx].insert(0, folder_selected)

                    root.update()


class deleteButton(Button):
    def __init__(self, categoryOrItem):
        super().__init__(settingsFrame,
            image=images["settings_DeleteButton_1"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.deleteInputRow(),
            relief="flat"
        )
        self.type = categoryOrItem.lower()

    def deleteInputRow(self):
        global settingsInputLines
        global settingsInputLinesItems
        if self.type == "category":
            for x in categoryEntriesAndButtons["deleteButtons"]:
                if self == x:
                    indx = categoryEntriesAndButtons["deleteButtons"].index(self)
                    catEntry = categoryEntriesAndButtons["categoryEntries"][indx]
                    catKeyWord = categoryEntriesAndButtons["categoryKeywordEntries"][indx]
                    catBrowseBut = categoryEntriesAndButtons["categoryBrowseButtons"][indx]
                    catDirEntry = categoryEntriesAndButtons["categoryDirectoryEntries"][indx]

                    self.destroy()
                    categoryEntriesAndButtons["categoryEntries"][indx].destroy()
                    categoryEntriesAndButtons["categoryKeywordEntries"][indx].destroy()
                    categoryEntriesAndButtons["categoryBrowseButtons"][indx].destroy()
                    categoryEntriesAndButtons["categoryDirectoryEntries"][indx].destroy()



                    categoryEntriesAndButtons["deleteButtons"].remove(self)
                    categoryEntriesAndButtons["categoryEntries"].remove(catEntry)
                    categoryEntriesAndButtons["categoryKeywordEntries"].remove(catKeyWord)
                    categoryEntriesAndButtons["categoryBrowseButtons"].remove(catBrowseBut)
                    categoryEntriesAndButtons["categoryDirectoryEntries"].remove(catDirEntry)

                    settingsInputLines -= 1
                    realignInputLines()
        if self.type == "item":
            for x in itemEntriesAndButtons["deleteButtons"]:
                if self == x:
                    indx = itemEntriesAndButtons["deleteButtons"].index(self)
                    itemEntry = itemEntriesAndButtons["itemNames"][indx]
                    itemKeyWord = itemEntriesAndButtons["itemKeywords"][indx]


                    self.destroy()
                    itemEntriesAndButtons["itemNames"][indx].destroy()
                    itemEntriesAndButtons["itemKeywords"][indx].destroy()


                    itemEntriesAndButtons["deleteButtons"].remove(self)
                    itemEntriesAndButtons["itemNames"].remove(itemEntry)
                    itemEntriesAndButtons["itemKeywords"].remove(itemKeyWord)

                    settingsInputLinesItems -= 1
                    realignInputLines()


images["settings_DeleteButton_1"] = PhotoImage(file="assets/deleteIcon.png")
images["settings_button_2"] = PhotoImage(file="assets/frame2button_2.png")
settingsInputLines = 0
settingsInputLinesItems = 0
categoryEntriesAndButtons = {"index":[],"deleteButtons":[],"categoryEntries":[],"categoryKeywordEntries":[],"categoryBrowseButtons":[],"categoryDirectoryEntries":[]}
def realignInputLines():
    lines = 0
    for element in categoryEntriesAndButtons["categoryDirectoryEntries"]:
        element.place(
            x=566.0,
            y=166.0 + (lines * 30)
        )
        lines += 1
    lines = 0
    for element in categoryEntriesAndButtons["categoryBrowseButtons"]:
        element.place(
            x=486.0,
            y=166.0 + (lines * 30)
        )
        lines += 1
    lines = 0
    for element in categoryEntriesAndButtons["categoryKeywordEntries"]:
        element.place(
            x=358.0,
            y=166.0 + (lines * 30)
        )
        lines += 1
    lines = 0
    for element in categoryEntriesAndButtons["categoryEntries"]:
        element.place(
            x=232.0,
            y=166.0 + (lines * 30)
        )
        lines += 1
    lines = 0
    for element in categoryEntriesAndButtons["deleteButtons"]:
        element.place(
            x=212.0,
            y=166.0 + (lines * 30)
        )
        lines += 1
    addNewButton.place(
        x=232.0,
        y=166.0+(lines*30)
    )

    itemHeaderLabel.place(
        x=232.0,
        y=166 + (lines * 30) + 50
    )
    itemLabel1.place(
        x=232.0,
        y=166 + (lines * 30) + 50 + 39
    )
    itemLabel2.place(
        x=486.0,
        y=166 + (lines * 30) + 50 + 39
    )

    itemLines = 0
    for element in itemEntriesAndButtons["deleteButtons"]:
        element.place(
            x=212.0,
            y=166 + (lines * 30) + 50 + 39 + 27 + (itemLines * 30)
        )
        itemLines += 1

    itemLines = 0
    for element in itemEntriesAndButtons["itemNames"]:
        element.place(
            x=232.0,
            y=166 + (lines * 30) + 50 + 39 + 27 + (itemLines * 30)
        )
        itemLines += 1

    itemLines = 0
    for element in itemEntriesAndButtons["itemKeywords"]:
        element.place(
            x=486.0,
            y=166 + (lines * 30) + 50 + 39 + 27 + (itemLines * 30)
        )
        itemLines += 1
    addNewButtonItems.place(
        x=232.0,
        y=166 + (lines * 30) + 50 + 39 + 27 + (itemLines * 30)
    )

    root.update()




def createNewCategoryInputLine(textFill1="",textFill2="",textFill3="" ):
    global settingsInputLines
    categoryIndex = categoryEntriesAndButtons["index"].append(len(categoryEntriesAndButtons["index"]))


    deleteButton1 = deleteButton(categoryOrItem="category")
    deleteButton1.place(
        x=212.0,
        y=166.0+(settingsInputLines*30),
        width=16.0,
        height=18.0
    )
    categoryEntriesAndButtons["deleteButtons"].append(deleteButton1)

    entry_1 = Entry(settingsFrame,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.insert(0, textFill1)

    entry_1.place(
        x=232.0,
        y=166.0+(settingsInputLines*30),
        width=112.0,
        height=24.0
    )
    categoryEntriesAndButtons["categoryEntries"].append(entry_1)


    entry_2 = Entry(settingsFrame,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=358.0,
        y=166.0+(settingsInputLines*30),
        width=112.0,
        height=24.0
    )
    entry_2.insert(0, textFill2)
    categoryEntriesAndButtons["categoryKeywordEntries"].append(entry_2)



    entry_3 = Entry(settingsFrame,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("inter", 9 * -1)
    )
    entry_3.place(
        x=566.0,
        y=166.0+(settingsInputLines*30),
        width=210.0,
        height=24.0
    )
    entry_3.insert(0, textFill3)
    categoryEntriesAndButtons["categoryDirectoryEntries"].append(entry_3)


    browseButton = selectDirectoryButton()
    browseButton.place(
        x=486.0,
        y=166.0+(settingsInputLines*30),
        width=80.0,
        height=26.0
    )
    categoryEntriesAndButtons["categoryBrowseButtons"].append(browseButton)



    settingsInputLines += 1
    addNewButton.place(
        x=232.0,
        y=166.0+(settingsInputLines*30),
        width=192,
        height=27.0
    )
    try:
        realignInputLines()
    except:
        pass

    settingsFrame.update_idletasks()
    settingsFrame.configure(height=166.0+(settingsInputLines*30)+50+39+27+(settingsInputLinesItems*30)+60)
    updateScrollbarheight()

for index in range(0, len(dfCategories["Category Name"])):
    createNewCategoryInputLine(dfCategories.loc[index,"Category Name"], dfCategories.loc[index,"Category Filter Search Criteria"], dfCategories.loc[index,"Destination Path"],)




images["settings_button_1"] = PhotoImage(
    file="assets/frame2button_1.png")
button_1 = Button(settingsFrame,
    image=images["settings_button_1"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: saveChangesSettings(),
    relief="flat"
)
button_1.place(
    x=573.0,
    y=12.0,
    width=192.0,
    height=27.0
)

errorInvalidDirSettingsLabel = tk.Label(
    settingsFrame,
    anchor="nw",
    text=f"",
    bg="#FFFFFF",
    fg="#454545",
    font=("Inter", 12 * -1)
)

errorInvalidDirSettingsLabel.place(
    x=573,
    y=39
)



itemHeaderLabel = tk.Label(
    settingsFrame,
    anchor="nw",
    text="Item Filters",
    bg="#FFFFFF",
    fg="#000000",
    font=("Inter SemiBold", 22 * -1)
)

itemHeaderLabel.place(
    x=232,
    y=166+(settingsInputLines*30)+50
)

itemLabel1 = tk.Label(
    settingsFrame,
    anchor="nw",
    text="Item Name",
    bg="#FFFFFF",
    fg="#444444",
    font=("Inter", 12 * -1)
)
itemLabel1.place(
    x=232,
    y=166+(settingsInputLines*30)+50+39
)

itemLabel2 = tk.Label(
    settingsFrame,
    anchor="nw",
    text="Keyword",
    bg="#FFFFFF",
    fg="#444444",
    font=("Inter", 12 * -1)
)
itemLabel2.place(
    x=486,
    y=166+(settingsInputLines*30)+50+39
)




addNewButtonItems = Button(settingsFrame,
    image=images["settings_addNewButton_1"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: createNewItemInputLine("", ""),
    relief="flat"
)


itemEntriesAndButtons = {"deleteButtons":[],"itemNames":[],"itemKeywords":[]}
def createNewItemInputLine(textFill1="",textFill2=""):
    global settingsInputLines
    global settingsInputLinesItems

    deleteButton2 = deleteButton(categoryOrItem="item")
    deleteButton2.place(
        x=212.0,
        y=166+(settingsInputLines*30)+50+39+27+(settingsInputLinesItems*30),
        width=16.0,
        height=18.0
    )
    itemEntriesAndButtons["deleteButtons"].append(deleteButton2)

    entry_1 = Entry(settingsFrame,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.insert(0, textFill1)

    entry_1.place(
        x=232.0,
        y=166.0+(settingsInputLines*30)+50+39+27+(settingsInputLinesItems*30),
        width=200.0,
        height=24.0
    )
    itemEntriesAndButtons["itemNames"].append(entry_1)


    entry_2 = Entry(settingsFrame,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=486.0,
        y=166.0+(settingsInputLines*30)+50+39+27+(settingsInputLinesItems*30),
        width=200.0,
        height=24.0
    )
    entry_2.insert(0, textFill2)
    itemEntriesAndButtons["itemKeywords"].append(entry_2)



    settingsInputLinesItems += 1
    addNewButtonItems.place(
        x=232.0,
        y=166.0+(settingsInputLines*30)+50+39+27+(settingsInputLinesItems*30),
        width=192,
        height=27.0
    )
    settingsFrame.update_idletasks()
    settingsFrame.configure(height=166.0+(settingsInputLines*30)+50+39+27+(settingsInputLinesItems*30)+60)
    updateScrollbarheight()



for index in range(0, len(dfItems["Item Name"])):
    createNewItemInputLine(dfItems.loc[index,"Item Name"], dfItems.loc[index,"Item Filter Search Criteria"])





#<-----------------------------------------start up code and mainloop------------------------------------------------------------------->
if dfSetup["tesseractPath"][0] == "":
    startFrame.tkraise()
else:
    homeFrame.tkraise()


root.resizable(True, True)
root.mainloop()

