**ALI – Automated Label Inspection**

![](Aspose.Words.2abc5b30-61d2-4b07-af4f-68db8a666da2.001.png)

**What is ALI?**

ALI stands for “ automated label inspection ”. ALI was designed for use in small series production (low to medium quantities). ALI supports the inspection and quality control of printed labels.

Checking labels for complete correctness is certainly not one of the most exciting activities in the working world. In addition, such inspection tasks are time-consuming and tiring for people. This is how the USECASE from ALI (automated label inspection) came about. Designed for "pre-series tasks for small to medium quantities", ALI is intended to help with this type of quality assurance. 
Available on Github: <https://github.com/iCounterBOX/ALI---automated-Label-Inspection>

**Order templates / reference templates?**

In order for ALI to be able to "check", reference templates are needed (e.g. order templates, samples, etc. ) . These are "taught" in ALI in a similar way to the learning process for object detection. We use a so-called label image tool here (e.g. https://www.makesense.ai/ [) ](https://www.makesense.ai/).



![](Aspose.Words.2abc5b30-61d2-4b07-af4f-68db8a666da2.002.png)

This means that different reference templates can be stored in ALI. An ALI test then compares the stored reference document with the object that is compared to it during the test via webcam (USB cam) .

**OCR:**

Paddle-OCR:  ( [https://github.com/PaddlePaddle/PaddleOCR ](https://github.com/PaddlePaddle/PaddleOCR)).

See also [https://github.com/iCounterBOX/Paddle-OCR-on-Webcam ](https://github.com/iCounterBOX/Paddle-OCR-on-Webcam)...Here I describe in detail how PaddleOCR runs in the CUDA environment under WIN 10.

**Prerequisites :**

WIN10, CUDA 11.2 and cuDNN8​

available here as an .EXE . It comes with all Python dependencies and can be used immediately.

**YouTube:**

[**https://www.youtube.com/watch?v=cS_orV-vrYg**](https://www.youtube.com/watch?v=cS_orV-vrYg)

**Webcam :**

![](Aspose.Words.2abc5b30-61d2-4b07-af4f-68db8a666da2.003.png)  e.g. Angetube 60FPS 1080P Webcam – quite good webcam . In principle no special requirements for the webcam !!


**Code / run finally as EXE-File** :

Originally, the plan was to make ALI available here as an EXE file. The ZIP with the exe is 4 GB - much too big for github. The good news: ALI can be easily made into an exe with auto-py-to-exe. The code is now available here in the repository. My devel environment is Anaconda + Spyder ( py39 )

**Special ALI folders:**

![](Aspose.Words.2abc5b30-61d2-4b07-af4f-68db8a666da2.004.png).. here are the images and labels “learned” via MakeSense

![](Aspose.Words.2abc5b30-61d2-4b07-af4f-68db8a666da2.005.png).. this is where the protocols are stored ( docx / word ). These can also be deleted or copied here, for example ...


