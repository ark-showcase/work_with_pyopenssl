import easyocr

def extract_text(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image, detail=0)
    return result