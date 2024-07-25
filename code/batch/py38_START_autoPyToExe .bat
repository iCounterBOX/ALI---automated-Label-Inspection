set root=C:\Users\USERNAME\anaconda3

call %root%\Scripts\activate.bat %root%
call activate py39pa
p:
call cd D:\ALL_PROJECT\a_Factory\_ALI\py39pa
call pyrcc5 -o image_rc.py image.qrc
call auto-py-to-exe

cmd \k 