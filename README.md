

### guided-diffusion segmentation collage

Automatic segmentation and compositing of sets of videos. Utilises dichotomous image segmentation to remove humans from film shoots and frames a collage in three ways: green screen, human removal and diffused masking. Works with implemented methods of image diffusion with conditional guidance. Easily computes 1.5 frames per second on 4k videos with 3090 rtx gpus.

```
(download libraries)
! sudo chmod +x download_estimator.sh && ./download_estimator.sh
(compute masks from arbitrary video datasets)
! python3 man_1.py --video_dataset ./path/to/dataset
(organise datasets for collage)
! python3 man_2.py --estimated_folder ./path/to/dataset
! <guided diffusion over a film shoot>
(execute compositing methods)
! python3 man_3.py --estimated_folder ./path/to/dataset --fps 25 --composite_type green_background
! python3 man_3.py --estimated_folder ./path/to/dataset --fps 25 --composite_type mask_pil_with_frame
! python3 man_3.py --estimated_folder ./path/to/dataset --fps 25 --composite_type diffused_masking --second_dataset ./path/to/second/dataset
```

![output_image](https://github.com/luisarandas/guided-diffusion-segm-collage/assets/30077568/01d4b29b-9131-47c4-9f7f-5926a6f4e074)

https://github.com/luisarandas/guided-diffusion-segm-collage/assets/30077568/d1f61249-d665-4542-992d-b47b755f88fc




```
@article{interla23,
  title={Man lost in the convergence of time, Avebury (2022): Reconfiguring film through human figure removal and collage},
  author={Arandas, Luís and McDonough, Kate, Grierson, Mick and Carvalhais, Miguel},
  journal={Proceedings of Intermediartes'23},
  year={2023}
}
```

