# Lost vacation

Author: k-gomez \
Points: tbd... (medium)

## Description

Our USB stick looks broken. I am sure that we downloaded something odd that tampered the stick. Sadly, some content from our vacation folders is missing. I am pretty sure that I miss-spelled the folder names too. Can you find the flag?

## Generation of the USB stick

Generate random directories and files:
```
for a in {0..9}
do
    for f in {0..9}
    do
        mkdir -p ./a$a
        head -c 100000 /dev/urandom > ./a$a/$f
    done
done
```

1. Create multiple directories
```
mkdir -p Documents/personal
mkdir -p Documents/work
mkdir -p Documents/projects
mkdir -p Documents/development
mkdir -p Pictures/vaccation2016
mkdir -p Pictures/vaccation2020
mkdir -p Pictures/vaccation2022
mkdir -p Pictures/cars
mkdir -p Pictures/houses
mkdir Downloads             # generate random directories here
```
2. Upload random files from the internet to the directories
3. The vaccation2022 folder should contain one picture of a city with the flag printed on it. This picture is delete it afterwards
4. Create the img
```
lsblk   # determine location of the USB stick
sudo dd if=/dev/sda1 | gzip > out.img.gz
```

## Solution

### TL;DR 

Recover the picture within the vaccation2022 folder and look at it.

### Extended version

First, we need to download the file from the DSC website. The `file` command indicates that this is a gzip compressed file. Let's decompress it using `gzip` and the following command. The `-dk` option makes sure to keep the compressed file. Just in case :-)
```
$ gzip -dk personal.img.gz
```

The result is an img file that looks like a FAT file. The description references an USB stick. Commonly, the FAT format is used for USB sticks.
```
$ file personal.img
personal.img: DOS/MBR boot sector, code offset 0x58+2, OEM-ID "mkfs.fat", sectors/cluster 8, Media descriptor 0xf8, sectors/track 62, heads 124, sectors 7831552 (volumes > 32 MB), FAT (32 bit), sectors/FAT 7640, reserved 0x1, serial number 0xf6eeb1f8, label: "personal   "
```

Let's take a look at the file using `fls`.
```
$ fls personal.img 
r/r 3:  personal    (Volume Label Entry)
d/d 5:  Documents
d/d 7:  Downloads
d/d 9:  Pictures
v/v 125059843:  $MBR
v/v 125059844:  $FAT1
v/v 125059845:  $FAT2
V/V 125059846:  $OrphanFiles
```

We can see multiple folders. I would assume that content for vaccations is within the Pictures folder. Let's take a look.
```
$ fls personal.img 9 
d/d 31418374:   vaccation2016
d/d 31418376:   vaccation2020
d/d 31418378:   vaccation2022
d/d 31418380:   cars
d/d 31418382:   houses
```

Nice, we can see a vaccation2022 folder. Let's look into it.
```
$ fls personal.img 31418378 
r/r 32687496:   rathaus-hdr-2-4228067506.jpeg
r/r 32687501:   Marienplatz-Munich-Germany-1-950130474.jpeg
r/r * 32687504: th-3446069388.jpeg
```

We can see three files. One of them is deleted. It's filename is `th-3446069388.jpeg`. Recover it using the following command.
```
$ icat -r personal.img 32687504 > th.jpeg 
```

The flag is within the image.

Flag is: `DSC{y3s_y0u_f0und_wh3r3_we_w3nt_t0}`
