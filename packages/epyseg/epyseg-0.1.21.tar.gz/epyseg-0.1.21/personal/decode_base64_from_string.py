import pyperclip as clip
import base64

incr = 27





image_64_encode = clip.paste()
print(image_64_encode)

image_64_encode = image_64_encode.replace('<img src="data:image/png;base64, ','')
image_64_encode = image_64_encode.replace('" alt="select model">', '')
# image_64_encode = image_64_encode.replace('" />','')
image_64_encode = image_64_encode.replace('"/>','')

print(image_64_encode)

image_64_decode = base64.b64decode(image_64_encode)
image_result = open(str(incr) + '.png', 'wb')
image_result.write(image_64_decode)







