

"""
    luis arandas 14-08-2023

    $ python3 man_3.py --estimated_folder ./path/to/dataset --fps 25 --composite_type green_background
    $ python3 man_3.py --estimated_folder ./path/to/dataset --fps 25 --composite_type mask_pil_with_frame
    $ python3 man_3.py --estimated_folder ./path/to/dataset --fps 25 --composite_type diffused_masking --second_dataset ./path/to/second/dataset

    tests with (man-env.yml), utilises IS-Net library
"""

# ! python3 43/man_3.py --estimated_folder /home/luisarandas/Desktop/phdcodes/test_data/video_data_2/remove1 --fps 25 --composite_type green_background
# ! python3 43/man_3.py --estimated_folder /home/luisarandas/Desktop/phdcodes/test_data/video_data_2/remove1 --fps 25 --composite_type mask_pil_with_frame

import argparse
import random
from PIL import Image
import os
import subprocess
from tqdm import tqdm


def ensure_directory_exists(directory_path):
    """ creates the directory if it doesn't exist """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_random_color_image(size, idx):
    """Return an image of the specified size filled with a random color or white based on the index."""
    if idx % 2 == 0:  # For every second frame
        color = (255, 255, 255)  # white
    else:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return Image.new("RGB", size, color)


def composite_mask_with_green_background(frame_folder, mask_pil_folder, output_folder):
    ensure_directory_exists(output_folder)

    for idx, file in enumerate(tqdm(sorted(os.listdir(frame_folder)))):
        frame_path = os.path.join(frame_folder, file)
        frame = Image.open(frame_path)

        green_background = Image.new("RGB", frame.size, (0, 255, 0))
        
        mask_pil_file = file.replace(".jpg", "_mask_pil.png")
        mask_pil_path = os.path.join(mask_pil_folder, mask_pil_file)
        mask_pil = Image.open(mask_pil_path).convert("L")        
        composite = Image.composite(frame, green_background, mask_pil)        

        composite_file_name = f"frame{idx:05d}_masked.jpg"
        composite.save(os.path.join(output_folder, composite_file_name))


def composite_mask_pil_with_original_frame(frame_folder, mask_pil_folder, output_folder):
    ensure_directory_exists(output_folder)

    for idx, file in enumerate(tqdm(sorted(os.listdir(frame_folder)))):
        frame_path = os.path.join(frame_folder, file)
        frame = Image.open(frame_path)

        mask_pil_file = file.replace(".jpg", "_mask_pil.png")
        mask_pil_path = os.path.join(mask_pil_folder, mask_pil_file)

        mask_pil = Image.open(mask_pil_path).convert("L")
        #inverted_mask = ImageOps.invert(mask_pil)
        composite = Image.composite(Image.new("RGB", frame.size, (0, 0, 0)), frame, mask_pil)
        composite_file_name = f"frame{idx:05d}_masked.jpg"
        composite.save(os.path.join(output_folder, composite_file_name))

    

def composite_diffusion_with_original_frame(frame_folder, mask_pil_folder, second_dataset_folder, output_folder):
    ensure_directory_exists(output_folder)

    total_frames = len(os.listdir(frame_folder))
    second_dataset_files = os.listdir(second_dataset_folder)
    
    for idx, file in enumerate(tqdm(sorted(os.listdir(frame_folder)))):
        frame_path = os.path.join(frame_folder, file)
        frame = Image.open(frame_path)

        mask_pil_file = file.replace(".jpg", "_mask_pil.png")
        mask_pil_path = os.path.join(mask_pil_folder, mask_pil_file)
        mask_pil = Image.open(mask_pil_path).convert("L")
        
        second_image_path = os.path.join(second_dataset_folder, file) # Assuming the naming is the same for the second dataset
        
        if file in second_dataset_files:
            second_image = Image.open(second_image_path)
        else:
            second_image = get_random_color_image(frame.size, idx)

        composite = Image.composite(second_image, frame, mask_pil)
        composite_file_name = f"frame{idx:05d}_masked.jpg"
        composite.save(os.path.join(output_folder, composite_file_name))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform compositing based on given type")
    parser.add_argument("--estimated_folder", required=True, help="Path to the estimated folder containing the files")
    parser.add_argument("--composite_type", required=True, choices=["green_background", "mask_pil_with_frame", "diffused_masking"], help="Type of compositing to perform")
    parser.add_argument("--fps", required=True, help="fps")
    parser.add_argument("--second_dataset", help="Path to the second dataset folder (required for diffused_masking)")

    args = parser.parse_args()  

    # check if the composite type is "diffused_masking" and ensure that the second_dataset is provided.
    if args.composite_type == "diffused_masking" and args.second_dataset is None:
        parser.error("--second_dataset is required when using diffused_masking composite type")
    
    frame_folder = os.path.join(args.estimated_folder, "frames")
    mask_folder = os.path.join(args.estimated_folder, "masks")
    mask_pil_folder = os.path.join(args.estimated_folder, "mask_pils")
    
    if args.composite_type == "green_background":
        output_folder = os.path.join(args.estimated_folder, "composite_green")
        composite_mask_with_green_background(frame_folder, mask_pil_folder, output_folder)

    elif args.composite_type == "mask_pil_with_frame":
        output_folder = os.path.join(args.estimated_folder, "composite_mask_pil_frame")
        composite_mask_pil_with_original_frame(frame_folder, mask_pil_folder, output_folder)
    
    if args.composite_type == "diffused_masking":
        diffused_frames_folder = str(args.second_dataset)
        output_folder = os.path.join(args.estimated_folder, "composite_diffused_masking")
        composite_diffusion_with_original_frame(frame_folder, mask_pil_folder, diffused_frames_folder, output_folder)
    

    output_video_path = os.path.join(args.estimated_folder, f"{args.composite_type}.mp4")
    input_pattern = os.path.join(output_folder, "frame%05d_masked.jpg")
    command = ["/usr/bin/ffmpeg", "-framerate", args.fps, "-i", input_pattern, "-c:v", "libx264", "-pix_fmt", "yuv420p", output_video_path]

    subprocess.run(command)


