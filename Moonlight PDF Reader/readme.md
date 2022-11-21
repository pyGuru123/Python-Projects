# Moonlight PDF Reader

Moonlight PDF Reader is a simple python tkinter based application to read pdfs with some of the advanced pdf features including :
* PDF Encryption
* PDF Decryption
* Page Extraction
* Image Extraction
* Text Extraction
* Page Rotation
* PDF Export to PNG, HTML, XML
* Split PDF 
* Merge PDF
* Watermarking PDF

![Alt text](app.png?raw=true "Moonlight PDF Reader")

Page zooming and navigation, opening recently opened files is also possible. Moonlight PDF Reader leverages the features of muPDF library which is available in python under pymupdf name

* ### Note : In case some feature is breaking like attribute is not there, replace the attribut with new attribute which can be found here [pymupdf snake_case update](https://pymupdf.readthedocs.io/en/latest/znames.html)

## How to Download

Download this project from here [Download Moonlight PDF Reader](https://downgit.github.io/#/home?url=https://github.com/pyGuru123/Python-Projects/tree/master/Moonlight%20PDF%20Reader)

## Requirements

PyMuPDF : Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyMuPDF.

```bash
pip install pymupdf
```

## Usage

Double click the application.pyw to open the GUI application, then either click the open file button or press Ctrl + O to open and read a new pdf file. Remember Moonlight displays an image of the pdf page so editing or highlighting text is not possible

List of shortcut commands
* Ctrl O : open new pdf file
* Ctrl + : zoom in
* Ctrl - : zoom out
* up, left arrow key : turn over previous page
* right, down arrow key : turn over the next page
* F11 : Fullscreen mode
* Esc : Leave fullscreen

Features

* Text Extraction : 
    Click save as text under Home after opening a pdf file to extract text from the currently opened page
* Page Extraction : 
    Click Extract page under tools to extract the current page and save as pdf
* Extract Images : 
    Click Extract Images under tools to extract all the images in the current page
* Rotate Images : 
    Click Rotate Images under tools to rotate the currently opened page or mark rotate all to rotate all the pages of the pdf and save as a new file. Rotation is only possible in 90 clockwise, 90 anticlockwise and turn up side down by 180
* Export PDF : 
    Click Export PDF under tools to export the current page to png / html / xml file
* Encrypt PDF : 
    Click Encrypt PDF under tools to encrypt the PDF by using AES 256 Encryption by entering a password and save as new PDF
* Decrypt PDF : 
    Click Decrypt PDF under tools to decrypt and remove the current password from the pdf and save as new PDF
* Split PDF : 
    Click Split PDF under tools to split the pdf from the entered vale of from page upto entered value of to page. Remember pages under split are zero based. So to split page 2-4 enter the value of from = 1 and value of to = 3
* Merge PDF : 
    Click Merge PDF under tools to merge the entered pages into a new selected pdf file. Remember page index here begins with zero too, also these pages will be inserted at the end of the selected PDF file
* Watermark PDF : 
    Click Watermark PDF under tools to watermark selected png or jpg file to the current pdf page. Enter the top left and bottom right coordinates of rectangle to insert the selected image inside the rectangle.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.