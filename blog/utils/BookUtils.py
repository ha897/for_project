
import stripe, os, random
from blog import cfg
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_stripe_product(title, description, price, category):

    product = stripe.Product.create(
        name=title,
        description=description,
        metadata={'category': category}

    )
    # إنشاء سعر للمنتج
    stripe_price = stripe.Price.create(
        product=product.id,
        unit_amount= price*100,
        currency='usd',
    )
    
    return product.id
def update_stripe_product(product_id, title, description, price, category):

    updated_product = stripe.Product.modify(
        product_id,
        name=title,
        description=description,
        metadata={'category': category}
    )

def create_file(file, allowed_ext, kind):
    file_ext = file.filename.rsplit(".")[-1]
    if file_ext in allowed_ext:
        # random_name = "audio" + str(random.randint(1000,9999))+"."+file_ext
        random_name = kind + str(random.randint(1000,9999))+"."+file_ext
        # file.save(str(cfg.FILES_DIR/"audio"/random_name))
        file.save(str(cfg.FILES_DIR/kind/random_name))
        return random_name

def create_image(image, allowed_ext, kind):
    try:
        file_ext = image.filename.rsplit(".")[-1]
    except:
        return "default.png"
    else:
        if file_ext in allowed_ext:
            # random_name = "audio" + str(random.randint(1000,9999))+"."+file_ext
            img_random_name = kind + str(random.randint(1000,9999))+"."+file_ext
            # file.save(str(cfg.FILES_DIR/"audio"/random_name))
            image.save(str(cfg.IMAGE_DIR/kind/img_random_name))
            return img_random_name

def delete_image(image, kind, book_cover):
    if book_cover.split(".")[0] != "default":
        os.remove(str(cfg.IMAGE_DIR/kind/book_cover))
        
def delete_file(file, kind, book_name):
    if book_name.split(".")[0] != "default":
        os.remove(str(cfg.FILES_DIR/kind/book_name))
