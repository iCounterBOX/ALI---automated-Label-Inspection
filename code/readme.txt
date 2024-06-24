
source:
https://github.com/iCounterBOX/ALI---automated-Label-Inspection/tree/main

Prerequisites :

******* WIN10, CUDA 11.2 and cuDNN8​   ********
See also https://github.com/iCounterBOX/Paddle-OCR-on-Webcam ...
Folder:  PaddleOCR is empty !! MUST be filled via github clone:  https://github.com/PaddlePaddle/PaddleOCR.git

What is ALI?

ALI stands for “ automated label inspection ”. ALI was designed for use in small series production 
(low to medium quantities). ALI supports the inspection and quality control of printed labels.
Order templates / reference templates?
In order for ALI to be able to "check", reference templates are needed (e.g. order templates, samples, etc. ) . These are "taught" in ALI in a similar way to the learning process for object detection. We use a so-called label image tool here (e.g. https://www.makesense.ai/ ) .
This means that different reference templates can be stored in ALI. 
An ALI test then compares the stored reference document with the object that is compared to it during the test via webcam (USB cam) . 

OCR:

Paddle-OCR is used ( https://github.com/PaddlePaddle/PaddleOCR ).
See also https://github.com/iCounterBOX/Paddle-OCR-on-Webcam ...
Here I describe in detail how PaddleOCR runs in the CUDA environment under WIN 10.

Prerequisites :

WIN10, CUDA 11.2 and cuDNN8​
See also https://github.com/iCounterBOX/Paddle-OCR-on-Webcam ...

YouTube:

https://www.youtube.com/watch?v=cS_orV-vrYg

