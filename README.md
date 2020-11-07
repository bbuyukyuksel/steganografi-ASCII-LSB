# Usage ASCII
$ python ascii_encode_msg.py -i"Images/lena.jpeg" -m"Lena ASCII Message Encode Test"
$ python ascii_decode_msg.py -i"lena-ASCII.png"

# Usage LSB
$ python lsb_encode_msg.py -i"Images/lena.jpeg" -m"Lena LSB Message Encode Test" -l0
$ python lsb_decode_msg.py -i"lena-LSB_LEVEL_0.png"

# Usage Image Encoder
$ python image_encoder.py -f "Resized/lena-gray.jpeg-32x32.png" -t encode > lena-gray-encode.txt
$ python image_encoder.py -f "Resized/lena-gray.jpeg-32x32.png" -t decode
  image-recov.png dosyasını dışarı çıkartır.

# Usage Image Resizer
$ python image_resizer.py -f"Images/lena-gray.jpeg" --size 32
CONSOLE OUTPUT >> + Suc cess:  Resized/lena-gray.jpeg-32x32.png

## ASCII Encode Process
- Resize İşlemi
$ python image_resizer.py -f"Images/lena-gray.jpeg" --size 32
CONSOLE OUTPUT >> + Success:  Resized/lena-gray.jpeg-32x32.png

- Görüntüyü metin haline çevir. Image to Text
$ python image_encoder.py -f "Resized/lena-gray.jpeg-32x32.png" -t encode > lena-gray-text.txt

- Görüntü metnini şifrele
$ python ascii_encode_msg.py -i "Images/lena.jpeg" -m "@file:lena-gray-text.txt"

- Görüntü metnini çöz
$ python ascii_decode_msg.py -i "lena-ASCII.png" > decoded-lena-gray-text.txt

- Görüntü Metinin Görüntüye Dök
$ python image_encoder.py -f decoded-lena-gray-text.txt -t decode