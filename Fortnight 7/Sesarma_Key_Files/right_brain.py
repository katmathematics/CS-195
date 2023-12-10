# # # #
# Description: Handles the emotion AI's processing
# # # #

import os
from os import listdir # Access the images
from os.path import isfile, join # Importing image file handling
import random # Assorted randomization functionality 
from transformers import pipeline

def Random_Emotion_From_Dir(path = "./static/icons"):
    #valid_file_endings = ["jpg","png","jpeg"]
    image_filenames = []
    for image in os.listdir(path):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            image_filenames.append(image)

    # print len(image_filenames)
    # print(image_filenames)
    return random.choice(image_filenames)

def Get_Images(path = "./static/icons"):
    image_filenames = []
    for image in os.listdir(path):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            image_filenames.append(image)
    return image_filenames

def Emotion(current_thought):
    icons = Get_Images()
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    model_outputs = classifier(current_thought)
    current_mood = max(model_outputs[0], key=lambda x:x['score'])
    if "?" in current_thought[-1] or current_mood == "confusion" or current_mood == "curiosity":
        for icon in icons:
            if "quizzical" in icon.lower():
                return icon
    elif current_mood == "approval" or current_mood == "excitement" or current_mood == "admiration" or current_mood == "joy" or current_mood == "amusement" or current_mood == "optimism":
        for icon in icons:
            if "happy" in icon.lower():
                return icon
    else:
        for icon in icons:
            if "neutral" in icon.lower():
                return icon

    return Random_Emotion_From_Dir()
