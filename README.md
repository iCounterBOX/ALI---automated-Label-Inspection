**ALI – Automated Label Inspection**

Update: 26.06.24

@all\_user\_\* **ens**:inne\*nen\*ens:nen..ens

D:\ALL\_PROJECT\a\_Factory\ALI\py39pa

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.001.png)

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.002.png)

**What is ALI?**

ALI stands for “ automated label inspection ”. ALI was designed for use in small series production (low to medium quantities). ALI supports the inspection and quality control of printed labels.

Checking labels for complete correctness is certainly not one of the most exciting activities in the working world. In addition, such inspection tasks are time-consuming and tiring for people. This is how the USECASE from ALI (automated label inspection) came about. Designed for "pre-series tasks for small to medium quantities", ALI is intended to help with this type of quality assurance. 
Available on Github: <https://github.com/iCounterBOX/ALI---automated-Label-Inspection>

**Order templates / reference templates?**

In order for ALI to be able to "check", reference templates are needed (e.g. order templates, samples, etc. ) . These are "taught" in ALI in a similar way to the learning process for object detection. We use a so-called label image tool here (e.g. https://www.makesense.ai/ [) ](https://www.makesense.ai/).



![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.003.png)

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

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.004.png)  e.g. Angetube 60FPS 1080P Webcam – quite good webcam . In principle no special requirements for the webcam !!


**Code / run finally as EXE-File** :

Originally, the plan was to make ALI available here as an EXE file. The ZIP with the exe is 4 GB - much too big for github. The good news: ALI can be easily made into an exe with auto-py-to-exe. The code is now available here in the repository. My devel environment is Anaconda + Spyder ( py39 )

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.005.png)  this json is for the auto-py-to-exe

**Special ALI folders:**

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.006.png).. here are the images and labels “learned” via MakeSense

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.007.png).. this is where the protocols are stored ( docx / word ). These can also be deleted or copied here, for example ...




**The crucial Parts:**

Local path:

D:/ALL\_PROJECT/a\_Boc/pyQT5\_experimental/ai/py39pa

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.008.png)  is calling the auto-py-to-exe

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.009.png)  MUST copy some stuff into OUTPUT/EXE folder


![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.010.png) option for future setup! None of those keys is currently used!

As ALI is most times using an external camera ( Cam 1 ? ) we set 1 as default:

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.011.png)  user can change the cam to any nr user need..





Short introduction to MakeSense / <https://www.makesense.ai/>

Teach in Images/labes

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.012.png)   click Get Started

Open folder with your annotation-Images ( References, Bestellvorlagen, Patterns etc,..)

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.013.png)

DnD those into Makesense

` `![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.014.png)

Click  Object Detection

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.015.png)… load Labels from File.. ![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.016.png)

Select labels:

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.017.png)  …DnD to MakeSense 

Start Project:

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.018.png)

Now we have MakeSense open and se our Images:

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.019.png)

Learn HOW to use MakeSense: <https://www.youtube.com/watch?v=shLogkPDtBk>

Finally store your ANNOTATIONS in voc-Format

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.020.png)

You may have a look to your generated VOC annotation files: 

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.021.png)

Important ..however yo generate Image/annotation. Finally it MUST be located here:

![](Aspose.Words.0bd4351c-5a4d-475c-8921-ba72d331771d.022.png) That’s it .. ALI is gently processing those files J
