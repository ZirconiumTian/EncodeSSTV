import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
from pysstv.color import *
import image

inputFilePath = None
outputFilePath = None

def askFileInput():
	global inputFilePath
	inputFilePath = filedialog.askopenfilename(
		title='Open file',
		filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")]
	)

def startTranslate():
	global inputFilePath, outputFilePath
	if not inputFilePath:
		messagebox.showerror("Error", "Please select a file to input first.")
		return
	outputFilePath = filedialog.asksaveasfilename(
		title='Save as',
		defaultextension=".mp3",
		filetypes=[("MP3 file", "*.mp3")]
	)
	if not outputFilePath:
		return 
	translateMode = modeCombobox.get()
	try:
		image = Image.open(inputFilePath)
		if image.mode != 'RGB':
			image = image.convert('RGB')
		image = image.resize((320, 256))
		sstv_class = {
			'Martin 1': MartinM1,
			'Martin 2': MartinM2,
			'PD90': PD90,
			'PD120': PD120,
			'PD180': PD180,
			'PD240': PD240,
			'PD290': PD290,
			'ScottieDX': ScottieDX,
			'Scottie 1': ScottieS1,
			'Scottie 2': ScottieS2,
			'Robot 36': Robot36
		}.get(translateMode)
		
		if not sstv_class:
			raise ValueError("Invalid encoding format.")
		
		sstv = sstv_class(image, 44100, 16)
		sstv.write_wav(outputFilePath)
		messagebox.showinfo("Success", "Encode completed!")
		
	except Exception as e:
		messagebox.showerror("Error", f"Error encoding: {str(e)}")
	finally:
		inputFilePath = None
		outputFilePath = None

root = tk.Tk()
root.title('EncodeSSTV')
root.geometry('320x220')
root.resizable(False, False)
root.maxsize(320, 220)
root.minsize(320, 220)

photo = tk.PhotoImage(data=image.imageLogo)
imgLabel = tk.Label(root, image=photo)
imgLabel.pack(side='top', pady=0)

modeLabel = tk.Label(root, text='Encode Format: ')
modeLabel.place(x=5, y=110)
modeVar = tk.StringVar()
modeCombobox = ttk.Combobox(
	root,
	textvariable=modeVar,
	values=[
		'Martin 1',
		'Martin 2',
		'ScottieDX',
		'Scottie 1',
		'Scottie 2',
		'PD90',
		'PD120', 'PD180',
		'PD240', 'PD290',
		'Robot 36'
	],
	state='readonly',
	width=25
)
modeCombobox.current(0)
modeCombobox.place(x=115, y=110)

buttonInput = tk.Button(root, text='Select Picture', command=askFileInput, width=15)
buttonOutput = tk.Button(root, text='Start Encoding', command=startTranslate, width=15)
buttonInput.place(x=5, y=140)
buttonOutput.place(x=125, y=140)

supportLabel = tk.Label(root, text='Support me on Bilibili @ZirconiumTian')
supportLabel.place(x=5, y=195)

root.mainloop()