# ماشین‌حساب NOVA با KivyMD

یک ماشین‌حساب تیره و مدرن با عملیات جمع، تفریق، ضرب، تقسیم، درصد، تغییر علامت و پاک‌کردن ورودی.

## ساختار پروژه

```text
KivyMD_Dark_Calculator/
├── main.py
├── requirements.txt
├── buildozer.spec
├── README_FA.md
├── .gitignore
└── assets/
```

## اجرای آزمایشی در ویندوز

بهتر است از Python 3.11 استفاده کنی. داخل پوشه پروژه در ترمینال VS Code اجرا کن:

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

اگر نصب Kivy یا KivyMD در ویندوز خطا داد، ساخت APK را در Ubuntu/WSL انجام بده.

## مسیر پیشنهادی ساخت APK

Buildozer به محیط لینوکس نیاز دارد. در Ubuntu 24.04 (WSL) پروژه را در فایل‌سیستم لینوکس نگه دار، مثلاً `~/projects/KivyMD_Dark_Calculator`، نه در `/mnt/c`؛ ساخت در فایل‌سیستم لینوکس معمولاً سریع‌تر و قابل‌اعتمادتر است.

### 1. نصب پیش‌نیازها

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
  autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake \
  libffi-dev libssl-dev
```

### 2. ساخت محیط و نصب Buildozer

```bash
mkdir -p ~/projects
# پروژه را در ~/projects کپی کن و سپس وارد پوشه‌اش شو:
cd ~/projects/KivyMD_Dark_Calculator
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython
```

### 3. ساخت APK

```bash
buildozer android debug
```

اولین ساخت، فایل‌های Android SDK/NDK و وابستگی‌ها را دانلود می‌کند و ممکن است زمان زیادی ببرد. پس از پایان موفق، APK معمولاً داخل پوشه `bin/` قرار می‌گیرد.

### 4. انتقال APK به Desktop ویندوز

از داخل Ubuntu، پس از جایگزین‌کردن نام فایل با نام واقعی APK:

```bash
cp bin/*.apk /mnt/c/Users/admin/Desktop/
```

## نکته‌های عیب‌یابی

- اگر ساخت شکست خورد، متن کامل خطا را از انتهای ترمینال کپی کن.
- اگر خطای فضای دیسک یا حافظه داشتی، فضای آزاد را بررسی کن و برنامه‌های اضافی را ببند.
- تنظیمات SDK/NDK و نسخه‌های مورد نیاز Buildozer ممکن است با نسخه ابزارهای نصب‌شده فرق داشته باشند؛ اگر Buildozer درباره نسخه SDK/NDK خطا داد، همان خطا را بررسی کن و مقدارها را بی‌دلیل تغییر نده.
- این پروژه برای محاسبات ساده است؛ از وارد کردن کد یا عبارت‌های نامعتبر به عنوان ورودی پشتیبانی نمی‌کند.
