# The Analyzor

Author: k-gomez \
Points: tbd... (medium / hard)

## Description

I gave the USB stick to an malware analysis company. They analyzed some of the files and created an malware-analysis folder. However, it seems that some of the files are missing in the directory. I really need to find out more about the identified malware. Can you determine the name of the malware from Xcitium? This is the security vendor I use.

You need to use the file from challenge `Lost vacation`.

## Solution

### TL;DR

Reconstruct the files from the malware-analysis folder. Get the hash within the document: `02a7c7df31b0a93fc80b053e46dcfa1eeb82eff79c1c8d802db31f1d0db823fd`

Google the hash and find the vendor analysis results in VirusTotal. Xcitium *names* the file `Malware@#y5k2i037tivi`.


### Extended version

We have to work with the img from the `Lost vacation` challenge. Let's find something related to malware-analysis. We can take a look into the `Downloads` folder.
```
$ fls personal.img 7 
d/d 31096966:   a0
d/d 31096968:   a1
d/d 31096970:   a2
d/d 31096972:   a3
d/d 31096974:   a4
d/d 31096976:   a5
d/d 31096978:   a6
d/d 31096980:   a7
d/d 31096982:   a8
d/d 31096984:   a9
```

Here, we can see different folders containing different files. If we take a look into all directories, we find one additional folder within the `a4` folder.
```
$ fls personal.img 31096974 
r/r 31225605:   0
r/r 31225606:   1
r/r 31225607:   2
r/r 31225608:   3
r/r 31225609:   4
r/r 31225610:   5
r/r 31225611:   6
r/r 31225612:   7
r/r 31225613:   8
r/r 31225614:   9
d/d 31225617:   malware-analysis
```

We find a `malware-analysis` folder. This folder contains three deleted files.
```
$ fls personal.img 31225617 
r/r * 33776775: .~lock.results.doc#
r/r * 33776778: lu21604paeegu.tmp
r/r * 33776780: results.doc
```

Recover the `results.doc` file as we already did in the `Lost vacation` challenge.
```
$ icat -r personal.img 33776780 > res.doc 
```

We can open the file and find a malware-analysis report. The description indicates that the flag is the name of the malware from Xcitium. Let's look up the hash using VirusTotal. VirusTotal identifies the hash as malicious. Xcitium names the file `Malware@#y5k2i037tivi`.

The flag is: `DSC{Malware@#y5k2i037tivi}`
