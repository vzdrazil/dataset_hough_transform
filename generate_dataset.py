#!/usr/bin/env python3
"""Reproduce the synthetic line-image dataset (requires Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw
import random, csv, hashlib, json

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / 'images'
IMAGES.mkdir(parents=True, exist_ok=True)
SIZES = [('256x256',256,256),('512x512',512,512),('1024x1024',1024,1024),('FHD',1920,1080),('QHD',2560,1440),('4K',3840,2160)]
COUNTS = [10,50,100,500]
REPLICATES = 3
BASE_SEED = 20261013

def generate(w,h,n,rng):
    im = Image.new('L',(w,h),0)
    draw = ImageDraw.Draw(im)
    def perimeter_point(side):
        if side == 0: return (rng.randrange(w),0)
        if side == 1: return (w-1,rng.randrange(h))
        if side == 2: return (rng.randrange(w),h-1)
        return (0,rng.randrange(h))
    for _ in range(n):
        p1=perimeter_point(rng.randrange(4))
        p2=perimeter_point(rng.randrange(4))
        if p1 == p2:
            p2=((p2[0]+w//2)%w,(p2[1]+h//2)%h)
        draw.line([p1,p2],fill=255,width=1)
    return im

def main():
    rows=[]
    for label,w,h in SIZES:
        for count in COUNTS:
            for rep in range(1,REPLICATES+1):
                seed=BASE_SEED+w*101+h*103+count*107+rep*109
                im=generate(w,h,count,random.Random(seed))
                white=im.histogram()[255]
                filename=f'lines_{label}_{count:03d}_r{rep:02d}.png'
                path=IMAGES/filename
                im.save(path,optimize=True)
                rows.append({'filename':f'images/{filename}','width':w,'height':h,'resolution':label,'requested_lines':count,'replicate':rep,'seed':seed,'white_pixels':white,'white_fraction':f'{white/(w*h):.8f}','sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    with (ROOT/'metadata.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    config={'dataset_name':'Synthetic Binary Lines for Hough Transform CPU/GPU Benchmark','generator_seed':BASE_SEED,'resolutions':[{'label':label,'width':w,'height':h} for label,w,h in SIZES],'line_counts':COUNTS,'replicates_per_combination':REPLICATES,'image_format':'PNG grayscale 8-bit (L); pixel values exactly 0 or 255','line_width_pixels':1,'background':0,'foreground':255,'generation':'Random endpoints on image perimeter; deterministic per image seed.'}
    (ROOT/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Generated {len(rows)} images in {IMAGES}')

if __name__ == '__main__':
    main()
