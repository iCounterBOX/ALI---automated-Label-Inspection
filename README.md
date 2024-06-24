**ALI – Automated Label Inspection**

![](Aspose.Words.9b933077-3ccf-4168-b0ce-d6846575f7b4.001.png)

**What is ALI?**

ALI stands for “ automated label inspection ”. ALI was designed for use in small series production (low to medium quantities). ALI supports the inspection and quality control of printed labels.

**Order templates / reference templates?**

In order for ALI to be able to "check", reference templates are needed (e.g. order templates, samples, etc. ) . These are "taught" in ALI in a similar way to the learning process for object detection. We use a so-called label image tool here (e.g. https://www.makesense.ai/ [) ](https://www.makesense.ai/).



![](Aspose.Words.9b933077-3ccf-4168-b0ce-d6846575f7b4.002.png)

This means that different reference templates can be stored in ALI. An ALI test then compares the stored reference document with the object that is compared to it during the test via webcam (USB cam) .
**



**


**OCR:**

Paddle-OCR is used ( [https://github.com/PaddlePaddle/PaddleOCR ](https://github.com/PaddlePaddle/PaddleOCR)).

See also [https://github.com/iCounterBOX/Paddle-OCR-on-Webcam ](https://github.com/iCounterBOX/Paddle-OCR-on-Webcam)...Here I describe in detail how PaddleOCR runs in the CUDA environment under WIN 10.

**Prerequisites :**

WIN10, CUDA 11.2 and cuDNN8​

available here as an .EXE . It comes with all Python dependencies and can be used immediately.

**YouTube:**

[**https://www.youtube.com/watch?v=cS_orV-vrYg**](https://www.youtube.com/watch?v=cS_orV-vrYg)

**Webcam :**

![](Aspose.Words.9b933077-3ccf-4168-b0ce-d6846575f7b4.003.png)  e.g. Angetube 60FPS 1080P Webcam – quite good webcam . In principle no special requirements for the webcam !!


**Set up** :

The PaddleOCR folders are stored in the directory structure. Unpack the ZIP with appropriate rights on the target system – that’s it.

**Special ALI folders:**

![](Aspose.Words.9b933077-3ccf-4168-b0ce-d6846575f7b4.004.png).. here are the images and labels “learned” via MakeSense

![](Aspose.Words.9b933077-3ccf-4168-b0ce-d6846575f7b4.005.png).. this is where the protocols are stored ( docx / word ). These can also be deleted or copied here, for example ...

