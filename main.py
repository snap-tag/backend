from fastapi import FastAPI, UploadFile
from PIL import Image
from snapcrop.hough_line_corner_detector import HoughLineCornerDetector
from snapcrop.page_extractor import PageExtractor
from snapcrop.processors import FastDenoiser, OtsuThresholder, Resizer
from snapner.ner import generate_tags
from snapocr.predict import recognize
import io
import base64
import cv2



app = FastAPI()


page_extractor = PageExtractor(
        preprocessors = [
            Resizer(height = 1280, output_process = True), 
            FastDenoiser(strength = 9, output_process = True),
            OtsuThresholder(output_process = True)
        ],
        corner_detector = HoughLineCornerDetector(
            rho_acc = 1,
            theta_acc = 180,
            thresh = 100,
            output_process = True
        )
    )


@app.get("/")
def online():
    return {"I am": "online"}

@app.post("/snapservice")
async def snapservice(image_file: UploadFile):
    if image_file.filename.endswith(".jpg") or image_file.filename.endswith(".png") or image_file.filename.endswith(".jpeg"):
        img = Image.open(image_file.file)
        cropped_document = page_extractor(img)
        recognized_words = recognize(cropped_document)
        extracted_tags = generate_tags(recognized_words)

        # Convert cropped document to image readable format
        buffer = io.BytesIO()
        Image.fromarray(cropped_document).save(buffer, format="PNG")
        cropped_document_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Convert extracted tags to list of words
        return {"cropped_document": cropped_document_data, "extracted_tags": extracted_tags}
        
    return {"error": "File not supported"}