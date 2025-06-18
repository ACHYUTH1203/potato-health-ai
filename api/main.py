from fastapi import FastAPI,File,UploadFile
from uvicorn import run  
import numpy as np
from PIL import Image

from io import BytesIO
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



MODEL = tf.keras.models.load_model("C:/Users/achyu/Desktop/deeplearning/potato-disease/saved_models/model_v1.h5")




CLASS_NAMES = ["EARLY BLIGHT","LATE BLIGHT","HEALTHY"]
def read_file_as_image(data)->np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.get("/ping")
async def ping():
    return "Hello I AM THERE"

@app.post("/predict")
async def predict(file: UploadFile= File(...)):
    image = read_file_as_image(await file.read())
    img_batch =np.expand_dims(image,0)
    predictions = MODEL.predict(img_batch)
    
    predicted_class =CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class':predicted_class,
        'confidence':float(confidence)
    }

    

if __name__ == '__main__':
    run(app, host='localhost', port=8001)
