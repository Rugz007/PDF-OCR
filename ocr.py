import cv2 
import pytesseract
import numpy as np
import pdf2image

def convert_pdf_to_image(document, dpi):
    images = []
    images.extend(
                    list(
                        map(
                            lambda image: cv2.cvtColor(
                                np.asarray(image), code=cv2.COLOR_RGB2BGR
                            ),
                            pdf2image.convert_from_path(document, dpi=dpi,poppler_path=r'C:\Users\user\Desktop\My Things\assignment\poppler-0.68.0\bin'),
                        )
                    )
                )
    return images

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

images = convert_pdf_to_image('test.pdf', 300)
for img in images:
    custom_config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(img, config=custom_config))
    img = get_grayscale(img)
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(float(d['conf'][i])) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)