## تعليمات التنصيب
#### تعليمات التنصيب علي windows
- قم بادخال الاوامر التالية في ال cmd
```
in website's root directory (on the same level as run.py) run the following commands:

python -m venv .venv

.venv\Scripts\activate

python.exe -m pip install --upgrade pip setuptools

pip install -r requirements.txt

python run.py
```

#### لاستخدام خاصية stripe cli
مدرج بالمشروع stripe cli client تحت strip\stripe.exe
اذا كنت تستخدم نظام تشغيل مختلف عن windows x64 فقم بالتالي
- قم بزيارة https://github.com/stripe/stripe-cli/releases/tag/v1.21.2
- قم بتحميل stripe cli بالصيغة المناسبة
- انقل stripe.exe ل stripe\
- قم بإدخال الاوامر التالية في ال cmd
```
in website's root directory run the following commands:

cd stripe

stripe login

<Press Enter> # a web page will open to ask for permission to access your account information

stripe listen --forward-to 127.0.0.1:5000/webhook

كما موضح بالصورة المرفقة
<Copy the webhook sign in secret>

<Edit .env file copy the secret key to STRIPE_ENDPOINT_SECRET>

<rerun the flask server>
```
