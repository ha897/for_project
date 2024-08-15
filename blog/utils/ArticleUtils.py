import random, os
from blog import cfg
def create_article_image(image):
    try:
        file_ext = image.filename.rsplit(".")[-1]
    except:
        return "default.png"
    else:
        if file_ext in cfg.ALLOW_EXTENTION_IMG:
            # random_name = "audio" + str(random.randint(1000,9999))+"."+file_ext
            img_random_name = "img" + str(random.randint(1000,9999))+"."+file_ext
            # file.save(str(cfg.FILES_DIR/"audio"/random_name))
            image.save(str(cfg.IMAGE_DIR/"article"/img_random_name))
            return img_random_name

def delete_article_image(article_image_name):
    if article_image_name.split(".")[0] != "default":
        os.remove(str(cfg.IMAGE_DIR/"article"/article_image_name))