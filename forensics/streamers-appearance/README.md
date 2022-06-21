# Streamers-appearance

## Description

We have been notified of a vehicle accident! As forensic investigators, we need to take a look at the report that was generated. However, the file looks broken to me. I bet the police department we got the report from is busy streaming on Instagram or TikTok right now. Here's where they messed up when creating the report....

The police department wants to know the unique identifier of the car. What are they talking about?

The flag format is `CTF{<unique-identifier>}`

## Solution

### TL;DR

The pdf file is manipulated. Some `stream` and `endstream` keywords are missing. Add those and the pdf will work again. The flag is the VIN highlighted within the report.

### Detailed version

The `file` command indicates that this file is a version 1.5 PDF document. We can verify this by looking for the header and the corresponding magic bytes.
```
$ xxd tamperd.pdf| head -n 1
00000000: 2550 4446 2d31 2e35 0a25 e2e3 cfd3 0a34 %PDF-1.5.%.....4
```
Based on [Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures), the hex signature of a PDF document is "25 50 44 46 2D". As we can see in the output above, this is valid in our case. So the usual manipulation of magic bytes is not the case here 

When you open the PDF file in a PDF viewer, you see a white screen. So the structure is messed up.

[This blogpost](https://resources.infosecinstitute.com/topic/pdf-file-format-basic-structure/) gives us a good overview of the basic structure of PDF documents.

```
 ---------------
|               |
|    Header     |
|               |
 ---------------
|               |
|               |
|               |
|     Body      |
|               |
|               |
|               |
 ---------------
| 'xref' Table  |
 ---------------
|    Trailer    |
 ---------------
```

We can see that each file contains a header, a body, an xref table and a trailer. The data resides in various objects that use specific types such as streams, dictionaries, arrays, and others. The description of the task suggests that the police department does a lot of *streaming*. Let's take a closer look at the file containing these types.

We use a text editor to view the file. In my case, it's neovim.

```
%PDF-1.5
%âãÏÓ
4 0 obj 
<<
/Filter /FlateDecode
/Length 882
>>
xµVÛrÓ0}÷Wì£ÄL]-«oÐ¦3íb`à!'ê [...]
endobj 
9 0 obj 
<<
/ColorSpace /DeviceRGB
/Subtype /Image
[...]
0000117325 00000 n 
0000117377 00000 n 
trailer

<<
/Info 19 0 R
/ID [<dc414c3458cffbbf0f200d6cc36854bf><b37a1fcea648cbf5f6e9376115e235a9>]
/Root 18 0 R
/Size 20
>>
startxref
117563
%%EOF
```
The above snippet shows us the PDF 1.5 header, an object (`obj`) including its end (`endobj`), the beginning of another object and the end of the PDF document which contains a reference to the beginning of the xref table (`startxref`) and the trailer (`trailer`).

Scrolling through the file, we see a pattern. We create an object (`obj`), have some additional information in it, and exit the object (`endobj`). However, some of the objects contain stream sections that are rounded off by `stream` and `endstream`. These keywords are usually arranged around these large pieces of data like
```
xµVÛrÓ0}÷Wì£ÄL]-«oÐ¦3íb`à!'ê [...]
```

Let's add the keywords `stream` and `endstream` around these chunks and check what happens. We can see two places where the chunks of data are not rounded by the keywords. If we add them and save the file, we can view the PDF document.

The task description asks for a unique identifier for a vehicle. A quick look on the Internet tells us that the so-called *VIN* or *vehicle identification number* is the unique identifier for each vehicle. In our case this is `5YJ3E1EA1JF0000`. Consequently, the license plate number is `CTF{5YJ3E1EA1JF0000}`.

