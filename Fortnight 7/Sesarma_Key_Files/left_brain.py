# # # #
# Description: Handles the task AI's processing
# # # #
#modules_dir=r"C:\\Users\\katja\\OneDrive\\Documents\\Git Repos\\CS 195\\CS-195\\Fortnight 7\\Sesarma\\code\\modules\\"

#import sys
#sys.path.append(modules_dir)

from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
import tensorflow as tf
from datasets import load_dataset
import transformers as transformers
import torch as torch
import requests
import random

def HelloWorld():
    return random.choice(["Hello World","Hallo Welt","Привет, мир","안녕 세계"])

def Instantiate_Model():
    model_name = "facebook/blenderbot_small-90M"
    return TFAutoModelForSeq2SeqLM.from_pretrained(model_name)

def Instantiate_Tokenizer():
    model_name = "facebook/blenderbot_small-90M"
    return AutoTokenizer.from_pretrained(model_name)

def Run_BlenderBot(model, tokenizer, text_input="Hello BlenderBot"):
    inputs = tokenizer([text_input], return_tensors="tf")
    reply_ids = model.generate(input_ids=inputs["input_ids"],attention_mask=inputs["attention_mask"])
    decoded_reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
    return decoded_reply

def Run_Base_BlenderBot(text_input="Hello BlenderBot"):
    model_name = "facebook/blenderbot_small-90M"
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer([text_input], return_tensors="tf")
    reply_ids = model.generate(input_ids=inputs["input_ids"],attention_mask=inputs["attention_mask"])
    decoded_reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
    return decoded_reply

def Run_Base_Falcon(text_input="Hello Falcon Bot!"):
    print(text_input)
    model = "tiiuae/falcon-7b-instruct"

    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
    )
    sequences = pipeline(
        text_input,
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
    )
    for seq in sequences:
        print(f"Result: {seq['generated_text']}")
    return sequences[0]['generated_text']

def query(text,model_id="tiiuae/falcon-7b-instruct"):
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {INSERT_YOUR_HUGGING_FACE_KEY_HERE}"}
    payload = {"inputs": text}

    print(f"Querying...: {text}")
    response = requests.post(api_url, headers=headers, json=payload)
    print(response)
    return response.json()[0]["generated_text"][len(text) + 1 :]