# Usage

## Usage ASCII
$ python ascii_encode_msg.py -i"Images/lena.jpeg" -m"Lena ASCII Message Encode Test" <br/>
$ python ascii_decode_msg.py -i"lena-ASCII.png" <br/>

## Usage LSB
$ python lsb_encode_msg.py -i"Images/lena.jpeg" -m"Lena LSB Message Encode Test" -l0 <br/>
$ python lsb_decode_msg.py -i"lena-LSB_LEVEL_0.png" <br/>

## Usage Image Encoder
$ python image_encoder.py -f "Resized/lena-gray.jpeg-32x32.png" -t encode > lena-gray-encode.txt <br/>
$ python image_encoder.py -f "Resized/lena-gray.jpeg-32x32.png" -t decode <br/>
<i>image-recov.png dosyasını dışarı çıkartır.</i>

## Usage Image Resizer
$ python image_resizer.py -f"Images/lena-gray.jpeg" --size 32 <br/>
CONSOLE OUTPUT >> + Suc cess:  Resized/lena-gray.jpeg-32x32.png <br/>

## ASCII Encode Process
### Resize İşlemi
<p>$ python image_resizer.py -f"Images/lena-gray.jpeg" --size 32</p>
<p>CONSOLE OUTPUT >> + Success:  Resized/lena-gray.jpeg-32x32.png</p>

### Görüntüyü metin haline çevir. Image to Text
<p>$ python image_encoder.py -f "Resized/lena-gray.jpeg-32x32.png" -t encode > lena-gray-text.txt</p>

### Görüntü metnini şifrele
$ python ascii_encode_msg.py -i "Images/lena.jpeg" -m "@file:lena-gray-text.txt"

### Görüntü metnini şifrele
<p>$ python ascii_encode_msg.py -i "Images/lena.jpeg" -m "@file:lena-gray-text.txt"</p>

### Görüntü metnini çöz
<p>$ python ascii_decode_msg.py -i "lena-ASCII.png" > decoded-lena-gray-text.txt</p>

### Görüntü Metinin Görüntüye Dök
<p>$ python image_encoder.py -f decoded-lena-gray-text.txt -t decode</p>
