from PIL import Image, ImageFilter

before = Image.open("bridge.bmp")
after = before.filter(UmageFilter.BoxBlur(10))
after.save("out.bmp")
