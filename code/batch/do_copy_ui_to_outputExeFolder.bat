set root=C:\Users\kristina\anaconda3

call %root%\Scripts\activate.bat %root%
call activate py39pa

p:
call cd D:\ALL_PROJECT\a_Factory\_ALI\py39pa
call copy /y ali.ui D:\ALL_PROJECT\a_Factory\_ALI\py39pa\output\ali

REM in neuer auto-py-to-exe werden folder copys im root abgelegt
call xcopy /y /I /E PaddleOCR   output\ali\PaddleOCR



cmd \k 