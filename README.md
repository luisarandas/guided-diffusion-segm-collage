# guided-diffusion-segm-collage
set of methods to diffuse sets of frames with sets of texts prompts after previous masking, using object segmentation. targeting reinterpretation of film shoots, implemented as video-to-video. 

We propose three methods to deal with the collage, with three diffusion characteristics so it stays different, here targeting moving image with raft. implements the paper

```
@bibliography
```


```
git clone xyz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

to run <br>

```
# python main.py "Hello, World!" 123

python3 main.py collage_1 <video_dir> <>
```