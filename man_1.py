

"""
    luis arandas 14-08-2023

    $ python3 man_1.py --video_dataset ./path/to/dataset

    tests with (man-env.yml), utilises IS-Net library
"""

import sys
import argparse
import torch
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
import numpy as np
import os
import subprocess


sys.path.append("./libs/DIS/IS-Net")
import data_loader_cache as isnet_data_loader_cache
import models as isnet_models


class GOSNormalize(object):
    # normalize image using torch.transforms
    def __init__(self, mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]):
        self.mean = mean
        self.std = std
    def __call__(self,image):
        image = isnet_data_loader_cache.normalize(image,self.mean,self.std)
        return image
    

class ISNetInterface:
    def __init__(self, model_path="models/", restore_model="isnet-general-use.pth", device="cuda"):
        self.hypar = {
            "model_path": model_path,
            "restore_model": restore_model,
            "interm_sup": False,
            "model_digit": "full",
            "seed": 0,
            "cache_size": [1024, 1024],
            "input_size": [1024, 1024],
            "crop_size": [1024, 1024],
            "model": isnet_models.ISNetDIS()
        }
        self.valid_extensions = ['.jpg', '.png', '.jpeg']
        self.device = device
        self.net = self.build_model()
        self.transform = transforms.Compose([GOSNormalize([0.5,0.5,0.5],[1.0,1.0,1.0])])

    def load_image(self, im_path):
        im = isnet_data_loader_cache.im_reader(im_path)
        im, im_shp = isnet_data_loader_cache.im_preprocess(im, self.hypar["cache_size"])
        im = torch.divide(im, 255.0)
        shape = torch.from_numpy(np.array(im_shp))
        return self.transform(im).unsqueeze(0), shape.unsqueeze(0) # make a batch of image, shape

    def build_model(self):
        net = self.hypar["model"]
        # convert to half precision
        if self.hypar["model_digit"] == "half":
            net.half()
            for layer in net.modules():
                if isinstance(layer, torch.nn.BatchNorm2d):
                    layer.float()

        net.to(self.device)
        if self.hypar["restore_model"]:
            net.load_state_dict(torch.load(self.hypar["model_path"] + "/" + self.hypar["restore_model"], map_location=self.device))
            net.to(self.device)
        net.eval()
        return net

    def predict(self, im_path):
        self.net.eval()
        inputs_val, shapes_val = self.load_image(im_path)
        if self.hypar["model_digit"] == "full":
            inputs_val = inputs_val.type(torch.FloatTensor)
        else:
            inputs_val = inputs_val.type(torch.HalfTensor)

        inputs_val_v = torch.autograd.Variable(inputs_val, requires_grad=False).to(self.device)
        ds_val = self.net(inputs_val_v)[0]
        pred_val = ds_val[0][0, :, :, :]
        pred_val = torch.squeeze(torch.nn.functional.upsample(torch.unsqueeze(pred_val, 0), (shapes_val[0][0], shapes_val[0][1]), mode='bilinear'))
        ma = torch.max(pred_val)
        mi = torch.min(pred_val)
        pred_val = (pred_val - mi) / (ma - mi)
        if self.device == 'cuda': torch.cuda.empty_cache()
        return (pred_val.detach().cpu().numpy() * 255).astype(np.uint8)

    def inference(self, image: Image):
        #image_tensor, orig_size = self.load_image(image_path) 
        image_path = image
        mask = self.predict(image_path)
        pil_mask = Image.fromarray(mask).convert('L')
        im_rgb = Image.open(image_path).convert("RGB")
        im_rgba = im_rgb.copy()
        im_rgba.putalpha(pil_mask)
        return [im_rgba, pil_mask]
    
    def process_frames(self, video_path):
        frames_directory = self.extract_frames(video_path)
        frame_files = sorted([f for f in os.listdir(frames_directory) if any(f.endswith(ext) for ext in self.valid_extensions)])
        for frame_file in tqdm(frame_files, desc="Processing frames", unit="frame"):
            print("Creating masks for ->", os.path.join(frames_directory, frame_file))
            frame_path = os.path.join(frames_directory, frame_file)
            mask1, mask2 = self.inference(frame_path)
            mask1.save(os.path.join(frames_directory, frame_file.replace(".jpg", "_mask.png")))
            mask2.save(os.path.join(frames_directory, frame_file.replace(".jpg", "_mask_pil.png")))
    
    def process_path(self, path):
        if os.path.isfile(path):
            self.process_frames(path)
        elif os.path.isdir(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):  # Ensure it's a file
                    self.process_frames(file_path)
        else:
            print(f"Path {path} does not exist or is neither a file nor a directory.")

    @staticmethod
    def extract_frames(video_path):
        video_directory = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        frames_directory = os.path.join(video_directory, video_name)
        os.makedirs(frames_directory, exist_ok=True)        
        cmd = ['ffmpeg', '-i', video_path, os.path.join(frames_directory, 'frame%05d.jpg')]
        subprocess.run(cmd)
        return frames_directory





def main(args):

    dataset_path = args.video_dataset
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    isnet = ISNetInterface(device=device)
    isnet.process_path(dataset_path)

    print("finished processing frames.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='load a custom dataset.')
    parser.add_argument('-d', '--video_dataset', type=str, required=True, help='path to the dataset.')
    args = parser.parse_args()
    main(args)

    