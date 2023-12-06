import tkinter as tk            # tkinter imported for GUI design
from tkinter import *
from PIL import Image
from PIL import ImageTk         # from PIL library GUI will be able to import images
from tkinter import filedialog  # with filedialog we can select file into GUI
import cv2                      # fundamental library for openCV
import numpy as np              # numpy imported for image processing row operations
import pytesseract              # pytesseract imported for reading contrast images and returning string from them


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR1\tesseract.exe'    # pytesseract engine imported
cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")                     # xml cascade file imported to read plates


def select_image():
    global panelA                           # panelA defined for original image place on to GUI
    path = filedialog.askopenfilename()
    select_image.path = path                # Image path taken and saved as function parameter for later use

    if len(path) > 0:
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)                  # Image has been open and became BGR to RGB

        scale_percent = 0.6
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)

        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # Original image size was too big for gui.
                                                                        # image resized
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        resized = Image.fromarray(resized)
        resized = ImageTk.PhotoImage(resized)                           # Image become array format for the later operations.

        if panelA is None:
            panelA = Label(image=resized)
            panelA.image = resized
            panelA.place(x=350, y=50)                                   # Original image reflected on to panelA

        else:
            panelA.configure(image=resized)                             # GUI can dynamically upload and analyze images
            panelA.image = resized


def detectLicencePlate():
    global panelB
    global panelC
    global read

    if len(select_image.path) > 0:
        image = cv2.imread(select_image.path)               # image uploaded
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      # image file become BGR to RGB
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)      # image became grayscale
        nplate = cascade.detectMultiScale(gray, 1.1, 4)
        # haarcascading technique were used to detect numberplate. It basically makes the image black and white then
        # detect the number plate with the help of contrast colors.

        for (x, y, w, h) in nplate:                         # we scan every coordinate and width height value in nplate
            a, b = (int(0.02 * image.shape[0]), int(0.025 * image.shape[1]))    # image reshaping parameters
            plate = image[y + a:y + h - a, x + b:x + w - b, :]  # detected plate reshaped and added into plate variable
            # IMAGE PROCESSING PART
            kernel = np.ones((1, 1), np.uint8)
            plate = cv2.dilate(plate, kernel, iterations=1)
            plate = cv2.erode(plate, kernel, iterations=1)       # Dilate and eroding processed on to image
            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY) # With thresholding image become black and white
            (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)

            read = pytesseract.image_to_string(plate)       # Pytesseract was used to Image to Text operation
            read = ''.join(e for e in read if e.isalnum())
            plate_text = "Plate Number: " + read
            T.delete("1.0", "end")
            T.insert(tk.CURRENT, plate_text)                # With string manipulation, text was written into GUI
            cv2.rectangle(image, (x, y), (x + w, y + h), (51, 51, 255), 2)
            cv2.rectangle(image, (x, y - 40), (x + w, y), (51, 51, 255), -1)
            cv2.putText(image, read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            # Cropped plate part was showed onto original image

            scale_percent = 0.6
            width = int(image.shape[1] * scale_percent)
            height = int(image.shape[0] * scale_percent)
            dim = (width, height)   # Processed image reshaped to fit in GUI

            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            resized = Image.fromarray(resized)
            resized = ImageTk.PhotoImage(resized)

            plate = Image.fromarray(plate)
            plate = ImageTk.PhotoImage(plate)

            if panelB is None:
                panelB = Label(image=resized)
                panelB.image = resized
                panelB.place(x=850, y=50)

            else:
                panelB.configure(image=resized)
                panelB.image = resized

            if panelC is None:
                panelC = Label(image=plate)
                panelC.image = plate
                panelC.place(x=520, y=390)

            else:
                panelC.configure(image=plate)
                panelC.image = plate

# GUI source code
root = Tk()
root.title("Plate Recognition")
canvas = tk.Canvas(root, width=1368, height=720, bg="#263D42")
canvas.pack()

T = Text(root, height=2, width=30)
T.place(x=50, y=230)

l = Label(root, text="Licence Plate Number")
l.config(font=("Courier", 11))
l.place(x=50, y=200)

l1 = Label(root, text="Original Image")
l1.config(font=("Courier", 11))
l1.place(x=500, y=25)

l2 = Label(root, text="Processed Image")
l2.config(font=("Courier", 11))
l2.place(x=1000, y=25)

l3 = Label(root, text="Detected Plate: ")
l3.config(font=("Courier", 11))
l3.place(x=350, y=400)

panelA = None
panelB = None
panelC = None

uploadImage = tk.Button(root, text="Upload Image", padx=15, pady=10, command=select_image)
uploadImage.place(x=50, y=50)

detectPlate = tk.Button(root, text="Detect Licence Plate", padx=15, pady=10, command=detectLicencePlate)
detectPlate.place(x=50, y=125)

root.mainloop()
