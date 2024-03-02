import io
import base64
from fastapi import FastAPI, UploadFile
from PIL import Image
from snapcrop.hough_line_corner_detector import HoughLineCornerDetector
from snapcrop.page_extractor import PageExtractor
from snapcrop.processors import FastDenoiser, OtsuThresholder, Resizer
from snapner.ner import generate_tags
from snapocr.predict import recognize
from snapbase.database import Database


app = FastAPI()

database = Database()


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

@app.get("/recentNotes")
async def recent_notes():
    recent_images = database.get_recent_images()
    recent_images_list = []
    for image in recent_images:
        image_dict = {
            "image_id": image[0],
            "image_path": image[1]
        }
        recent_images_list.append(image_dict)
    return recent_images_list

@app.get("/favoriteNotes")
async def favorite_notes():
    favorite_images = database.get_favorite_images()
    favorite_images_list = []
    for image in favorite_images:
        image_dict = {
            "image_id": image[0],
            "image_path": image[1]
        }
        favorite_images_list.append(image_dict)
    return favorite_images_list

@app.get("/searchNotes")
async def search_notes(tag: str):
    tags = tag.split(" ")
    searched_images = []
    for tag in tags:
        images = database.get_images(tag)
        for image in images:
            if image in searched_images:
                continue
            image_dict = {
                "image_id": image[0],
                "image_path": image[1]
            }
            searched_images.append(image_dict)
    return searched_images

@app.post("/uploadNote")
async def upload_note(image_file: UploadFile, tags: str):
    if image_file.filename.endswith(".jpg") or image_file.filename.endswith(".png") or image_file.filename.endswith(".jpeg"):
        img = Image.open(image_file.file)
        image_data = img.tobytes()
        image_id = database.insert_image(image_data, tags.split(" "))
        return {"image_id": image_id}
    return {"error": "File not supported"}