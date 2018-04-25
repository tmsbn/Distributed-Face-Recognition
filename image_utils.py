from os.path import join
from os import rename
import glob
from PIL import Image
from resizeimage import resizeimage

train_images_dir = join("images", "train")
train_image_files = glob.glob(join(train_images_dir, "*.jpg"))

bad_str_list = ['0001', '0002', '0003']

for train_image_file in train_image_files:

	with open(train_image_file, 'r+b') as f:
		with Image.open(f) as image:
			cover = resizeimage.resize_contain(image, [1000, 1000])
			cover.save(train_image_file, image.format)

	for bad_str in bad_str_list:
		new_name = train_image_file.replace(bad_str, '')
		if new_name != train_image_file:
			rename(train_image_file, new_name)
			print(new_name)

