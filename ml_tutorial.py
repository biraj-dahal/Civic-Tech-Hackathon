# -*- coding: utf-8 -*-
"""ml_tutorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f3Jkbg2coJqOOYJ4JVfNUi6-R2ONRxgP
"""

!pip install pytorch-lightning
!pip install transformers

import torch
import pytorch_lightning as pl
import torch.nn as nn
import csv
from torchmetrics import Accuracy
from torch.nn import functional as F
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from pytorch_lightning import Trainer

class Module(pl.LightningModule):
  def __init__(self):
    # define model
    super().__init__()
    self.layer1 = nn.Sequential(
        nn.Linear(28*28, 32), 
        nn.ReLU())

    self.layer2 = nn.Sequential(
        nn.Linear(32, 10), 
        nn.Sigmoid())
    
    self.model = nn.Sequential(
        self.layer1,
        self.layer2
    )

    # define metrics to evaluate
    self.accuracy = Accuracy(task="multiclass", num_classes=10)

  def forward(self, inputs):
    out = self.model(inputs)
    return out
    
  def training_step(self, batch, batch_idx):
    x, y = batch
    pred = self.forward(x)

    loss = F.cross_entropy(pred, y)

    return loss

  def validation_step(self, batch, batch_idx):
    x, y = batch
    pred = self.forward(x)

    acc = self.accuracy.update(pred, y)
    self.log("val_acc", self.accuracy)
    

  # dont worry about too much
  def configure_optimizers(self):
    optimizer = torch.optim.AdamW(
           self.model.parameters(),
           lr=0.0001,
           weight_decay=0.001,
       )
       
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
           optimizer=optimizer, T_max=3
       )
 
    return [optimizer], [lr_scheduler]

class MNISTData(Dataset):
  def __init__(self, split):

    if split=="train":
      with open("/content/sample_data/mnist_train_small.csv") as f:
        self.data = list(csv.reader(f))

    if split=="val":
      with open("/content/sample_data/mnist_test.csv") as f:
        self.data = list(csv.reader(f))

  def __getitem__(self, idx):
    entry = self.data[idx]
    label = torch.tensor(int(entry[0]))

    pixel_values = list(map(int, entry[1:]))
    pixels = torch.tensor(pixel_values).float()

    return pixels, label
  
  def __len__(self):
    return len(self.data)

model = Module()

dataset_train = MNISTData(split="train")
dataset_val = MNISTData(split="val")

dataloader_train = DataLoader(dataset_train, batch_size = 32)
dataloader_val = DataLoader(dataset_val, batch_size = 32)

# Initialize a trainer
trainer = Trainer(
    accelerator="auto",
    devices=1 if torch.cuda.is_available() else None, 
    max_epochs=1,
)

# Train the model ⚡
trainer.fit(
    model,
    train_dataloaders=dataloader_train,
    val_dataloaders=dataloader_val)

trainer.validate(dataloaders=dataloader_val)

"""Visualize an example"""

dataset_val = MNISTData(split="val")

pixel, label = dataset_val[0]

image = pixel.view(28,28)
from matplotlib import pyplot as plt
plt.imshow(image.numpy(), interpolation='nearest')
plt.show()

pred = model.forward(pixel)

predicted_class = torch.argmax(pred)
print(predicted_class)





"""**Using State-of-the-art Models**

These days, you would use a pre-trained model and fine-tune. 

Let's try that with OpenAI's CLIP model. 

CLIP was trained on 400 million pairs of image and text. 

It "understands" natural language. Hence, you can make it do object classification by just checking the scores for "this is an image of *object*", where *object* can be anything.

Let's try it.
"""

import torch
import torch.nn as nn
from PIL import Image
import requests
import matplotlib.pyplot as plt
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import pdb
from transformers import CLIPTokenizer

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

plt.imshow(image)

inputs = processor(text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)
print(probs)



"""### How do we adapt this model to detect numbers?


"""

## DATALOADER

class MNISTData(Dataset):
  def __init__(self, split):
    self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")

    if split=="train":
      with open("/content/sample_data/mnist_train_small.csv") as f:
        self.data = list(csv.reader(f))

    if split=="val":
      with open("/content/sample_data/mnist_test.csv") as f:
        self.data = list(csv.reader(f))

    labels = [
        "a photo of the number 0",
        "a photo of the number 1",
        "a photo of the number 2",
        "a photo of the number 3",
        "a photo of the number 4",
        "a photo of the number 5",
        "a photo of the number 6",
        "a photo of the number 7",
        "a photo of the number 8",
        "a photo of the number 9",
    ]

    self.text_inputs = self.tokenizer(labels, padding=True, return_tensors="pt")

  
  def __getitem__(self, idx):
    entry = self.data[idx]
    label = torch.tensor(int(entry[0]))

    pixel_values = list(map(int, entry[1:]))

    pixels = np.array(pixel_values)

    array_2d = pixels.reshape((28, 28))

    # add a third dimension to the array
    array_3d = np.expand_dims(array_2d, axis=2)

    # repeat the array 3 times along the new third dimension
    final_array = np.repeat(array_3d, 3, axis=2)

    num_img = Image.fromarray(final_array.astype(np.uint8))

    img_processed = self.processor(images=num_img, return_tensors="pt")
    pixel_values = img_processed['pixel_values']

    input_ids = self.text_inputs["input_ids"],
    attention_mask = self.text_inputs["attention_mask"],

    return input_ids, attention_mask, pixel_values, label
  
  def __len__(self):
    return len(self.data)


## MODEL
class our_clip_model(nn.Module):
  def __init__(self):
    super().__init__()
    self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

    self.model.eval()
    for p in self.model.parameters():
        p.requires_grad = False

    self.vision_linear = nn.Linear(512, 512)

    self.logit_scale = nn.Parameter(torch.ones([]) * 2.6592)

  def forward(self, input_ids, attention_mask, pixel_values):
    out = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                pixel_values=pixel_values,
                output_hidden_states=True,
            )
    text_embeds = out.text_embeds
    vision_embeds = out.image_embeds

    image_embeds = self.vision_linear(vision_embeds)

    image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)

    # cosine similarity
    logit_scale = self.logit_scale.exp()
    logits_per_text = torch.matmul(text_embeds, image_embeds.t()) * logit_scale
    logits_per_image = logits_per_text.T

    return logits_per_image

## TRAINER MODULE
class Module(pl.LightningModule):
  def __init__(self):
    # define model
    super().__init__()
    self.model = our_clip_model()
    # define metrics to evaluate
    self.accuracy = Accuracy(task="multiclass", num_classes=10)
  
  def training_step(self, batch, batch_idx):
    input_ids, attention_mask, pixel_values, label = batch
    # pdb.set_trace()
    pred = self.model.forward(input_ids[0][0], attention_mask[0][0], pixel_values.squeeze())

    loss = F.cross_entropy(pred, label)

    return loss

  def validation_step(self, batch, batch_idx):
    input_ids, attention_mask, pixel_values, label = batch
    # pdb.set_trace()
    pred = self.model.forward(input_ids[0][0], attention_mask[0][0], pixel_values.squeeze())

    acc = self.accuracy.update(pred, label)
    self.log("val_acc", self.accuracy)
    

  # dont worry about too much
  def configure_optimizers(self):
    optimizer = torch.optim.AdamW(
           self.model.parameters(),
           lr=0.0001,
           weight_decay=0.001,
       )
       
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
           optimizer=optimizer, T_max=3
       )
 
    return [optimizer], [lr_scheduler]

dataset_train = MNISTData(split="train")
dataset_val = MNISTData(split="val")

dataloader_train = DataLoader(dataset_train, batch_size = 32)
dataloader_val = DataLoader(dataset_val, batch_size = 32)

model = Module()

# Initialize a trainer
trainer = Trainer(
    accelerator="auto",
    devices=1 if torch.cuda.is_available() else None,  # limiting got iPython runs
    max_epochs=1,
)

# Train the model ⚡
trainer.fit(
    model,
    train_dataloaders=dataloader_train,
    val_dataloaders=dataloader_val)

trainer.validate(dataloaders=dataloader_val)

"""### Some other fun huggingface examples

Some other examples from Huggingface. Check them out for a lot of great examples such as as text-to-image, prompot guided image generation etc. 

Here are some references:
- Generative AI: https://huggingface.co/docs/diffusers/v0.13.0/en/index 
  - Stable Diffusion: https://huggingface.co/docs/diffusers/v0.13.0/en/api/pipelines/stable_diffusion_2 
  - Instruction-based image editing: https://huggingface.co/docs/diffusers/v0.13.0/en/api/pipelines/stable_diffusion/pix2pix 
- Transformer for vision, language, and audio: https://huggingface.co/docs/transformers/index 
  - CLIP: https://huggingface.co/docs/transformers/model_doc/clip 
  - GPT2: https://huggingface.co/docs/transformers/model_doc/gpt2
"""

from PIL import Image
import requests

from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)

"""GPT-2"""

from transformers import AutoTokenizer, GPT2Model
import torch

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs)

last_hidden_states = outputs.last_hidden_state