from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms

# Load the Keras model
# model_path = r"E:\\sam\\Cancer_Detection and Classification\\Cancer_Detection and Classification\\Cancer or Non-Cancer Models\\keras_model.h5"
# model_path = r"\\models\\inceptionV3\\keras_model.h5"
model_path = "./models/inceptionV3/keras_model.h5"
# model_path=r"E:\skin_cancer_detection_sam\models\inceptionV3\keras_model.h5"
model = load_model(model_path, compile=False)

# Load the labels for Keras model
# labels_path_keras = r"E:\\sam\\Cancer_Detection and Classification\\Cancer_Detection and Classification\\Cancer or Non-Cancer Models\\labels.txt"\
labels_path_keras = r"./models/inceptionV3/labels.txt"
# labels_path_keras=r"E:\skin_cancer_detection_sam\models\inceptionV3\labels.txt"
class_names_keras = open(labels_path_keras, "r").readlines()

# Load the PyTorch model
model_pytorch = models.resnet50(pretrained=False)
model_pytorch.fc = nn.Linear(in_features=2048, out_features=7)  # Adjust out_features based on your number of classes

# Load the saved weights for PyTorch model
# save_path_pytorch = "E:\\sam\\Cancer_Detection and Classification\\Cancer_Detection and Classification\\Cancer Types Classification Models\\method2_resnet50.pth"
save_path_pytorch = "./models/resnet_50/method2_resnet50.pth"
# save_path_pytorch=r"E:\skin_cancer_detection_sam\models\resnet_50\method2_resnet50.pth"
model_pytorch.load_state_dict(torch.load(save_path_pytorch, map_location=torch.device('cpu')))
model_pytorch.eval()  # Set the model to evaluation mode

# Define transformations for preprocessing the input image for PyTorch model
transform = transforms.Compose([
    transforms.Resize(384),
    transforms.CenterCrop(224),  # Adjust as needed based on your model's input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Path to the image
# image_path = "E:\sam\Cancer_Detection and Classification\Cancer_Detection and Classification\static\kalai_img.jpg"

class Model:    
    # Open and preprocess the image
    def __init__(self):
        pass

    def get_output(self, image_path):
        image = Image.open(image_path).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_tensor = transform(image).unsqueeze(0)  

        # Predict using the Keras model
        data_keras = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data_keras[0] = normalized_image_array
        prediction_keras = model.predict(data_keras)
        index_keras = np.argmax(prediction_keras)
        class_name_keras = class_names_keras[index_keras].strip()
        confidence_score_keras = prediction_keras[0][index_keras]

        # Predict using the PyTorch model
        with torch.no_grad():
            outputs_pytorch = model_pytorch(image_tensor)
            probabilities_pytorch = torch.softmax(outputs_pytorch, dim=1)

        confidence_scores_pytorch = probabilities_pytorch.squeeze().tolist()
        class_names_pytorch = ['Melanocytic nevi', 'Melanoma', 'Benign keratosis-like lesions', 
                            'Basal cell carcinoma', 'Actinic keratoses', 'Vascular lesions', 'Dermatofibroma']
        predicted_class_index_pytorch = confidence_scores_pytorch.index(max(confidence_scores_pytorch))
        predicted_class_pytorch = class_names_pytorch[predicted_class_index_pytorch]

        # Print predictions and confidence scores
        print("Keras Model Prediction:")
        print("Class:", class_name_keras)
        print("Confidence Score:", confidence_score_keras)
        if '0' in class_name_keras:
            print("\nPyTorch Model Prediction:")
            print("Predicted class:", predicted_class_pytorch)
        return {"class":class_name_keras, "score":confidence_score_keras, "predicted":predicted_class_pytorch}

# model__ = Model()
# model__.get_output("E:\sam\Cancer_Detection and Classification\Cancer_Detection and Classification\static\kalai_img.jpg")