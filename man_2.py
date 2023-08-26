

"""
    luis arandas 14-08-2023

    $ python3 man_2.py --estimated_folder ./path/to/dataset

    tests with (man-env.yml), utilises IS-Net library
"""

import argparse
import os
import shutil

def move_files(estimated_folder):

    all_files = os.listdir(estimated_folder)

    frame_files = [f for f in all_files if not "_mask" in f and f.endswith(".jpg")]
    mask_files = [f for f in all_files if "_mask.png" in f and not "_mask_pil.png" in f]
    mask_pil_files = [f for f in all_files if "_mask_pil.png" in f]

    frame_folder = os.path.join(estimated_folder, "frames")
    mask_folder = os.path.join(estimated_folder, "masks")
    mask_pil_folder = os.path.join(estimated_folder, "mask_pils")

    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    if not os.path.exists(mask_folder):
        os.makedirs(mask_folder)

    if not os.path.exists(mask_pil_folder):
        os.makedirs(mask_pil_folder)

    for f in frame_files:
        shutil.move(os.path.join(estimated_folder, f), os.path.join(frame_folder, f))

    for f in mask_files:
        shutil.move(os.path.join(estimated_folder, f), os.path.join(mask_folder, f))

    for f in mask_pil_files:
        shutil.move(os.path.join(estimated_folder, f), os.path.join(mask_pil_folder, f))

    print(f"number of frame files: {len(frame_files)}")
    print(f"number of mask files: {len(mask_files)}")
    print(f"number of mask_pil files: {len(mask_pil_files)}")

    if len(frame_files) == len(mask_files) == len(mask_pil_files):
        print("all sets have the same number of files!")
    else:
        print("the sets have different numbers of files.")



def main(args):
    folder_path = args.estimated_folder
    print("Moving raw frames and estimations to new paths!")
    move_files(folder_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="move estimated folder (see tam_1.py) files based on nomenclature")
    parser.add_argument("--estimated_folder", required=True, help="path to the estimated folder containing the files")
    args = parser.parse_args()
    main(args)
