import PyPDF4 as PDF_TK
import pikepdf as PDF_TK
import shutil
import zlib


def mergeTwoPdf(input_filename1, input_filename2, output_filename):
	# Open the files that have to be merged one by one
	pdf1File = open(input_filename1, 'rb')
	pdf2File = open(input_filename2, 'rb')
	 
	# Read the files that you have opened
	pdf1Reader = PDF_TK.PdfFileReader(pdf1File)
	pdf2Reader = PDF_TK.PdfFileReader(pdf2File)
	 
	# Create a new PdfFileWriter object which represents a blank PDF document
	pdfWriter = PDF_TK.PdfFileWriter()
	 
	# Loop through all the pagenumbers for the first document
	for pageNum in range(pdf1Reader.numPages):
	    pageObj = pdf1Reader.getPage(pageNum)
	    pdfWriter.addPage(pageObj)
	 
	# Loop through all the pagenumbers for the second document
	for pageNum in range(pdf2Reader.numPages):
	    pageObj = pdf2Reader.getPage(pageNum)
	    pdfWriter.addPage(pageObj)
	 
	# Now that you have copied all the pages in both the documents, write them into the a new document
	pdfOutputFile = open(output_filename, 'wb')
	pdfWriter.write(pdfOutputFile)
	 
	# Close all the files - Created as well as opened
	pdfOutputFile.close()
	pdf1File.close()
	pdf2File.close()



def extractPages(input_filename, page_num1, page_num2, output_filename):
	# extract pages in a doc from page_num1 to page_num2 and output it in a new doc

	pdf1File = open(input_filename, 'rb')
	pdf1Reader = PDF_TK.PdfFileReader(pdf1File)

	# Create a new PdfFileWriter object which represents a blank PDF document
	pdfWriter = PDF_TK.PdfFileWriter()

	for pageNum in range(page_num1, page_num2, 1):
	    pageObj = pdf1Reader.getPage(pageNum)
	    pdfWriter.addPage(pageObj)

	 
	pdfOutputFile = open(output_filename, 'wb')
	pdfWriter.write(pdfOutputFile)

	# Close all the files - Created as well as opened
	pdfOutputFile.close()
	pdf1File.close()



def compressPdf(doc_origin, doc_dest):
	assert(isinstance(doc_origin, str))
	pdf = PDF_TK.open(doc_origin, allow_overwriting_input=True)

	for page in pdf.pages:
		for im_key in page.images.keys():
			rawimage = page.images[im_key]
			pdfimage = PDF_TK.PdfImage(rawimage)
			pillowimage = pdfimage.as_pil_image()
			rawimage.write(zlib.compress(pillowimage.tobytes()), filter=PDF_TK.Name("/DCTDecode")) # FlateDecode

	pdf.save(doc_dest)




def removePages(input_filename, output_filename, page_ranges):
	"""Usage : 
		input_filename (str)
		output_filename (str)
		page_ranges (list of tuple): list of interval where pages are deleted
	"""

	assert(isinstance(input_filename, str))
	assert(isinstance(output_filename, str))
	assert(isinstance(page_ranges, list))
	assert(isinstance(page_ranges[0], list) or isinstance(page_ranges[0], tuple))

	shutil.copy2(input_filename, output_filename)
	
	pdf = PDF_TK.open(output_filename, allow_overwriting_input=True)

	page_ranges = sorted(page_ranges, key=lambda i:i[0], reverse=True)
	for (p0, p1) in page_ranges:
		del pdf.pages[p0:p1]

	pdf.save(output_filename)




def main():
	"""
	input_filename = './20-12-03-MDPI_Sensors.pdf'
	output_filename = './20-12-03-MDPI_Sensors_compressed.pdf'

	compressPdf(input_filename, output_filename)

	ranges = [(8,56), (100, 122)]
	removePages(input_filename, output_filename, page_ranges=ranges)

	"""
	pass


if __name__ == "__main__":
	main()