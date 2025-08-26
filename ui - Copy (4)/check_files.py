import os

# مسیر را به پوشه ui/Images تغییر می دهیم
folder_path = 'ui/Images'

try:
    files = os.listdir(folder_path)
    print("فایل‌های موجود در پوشه ui/Images:")
    if not files:
        print("پوشه خالی است.")
    else:
        for file in files:
            print(f"- {file}")
except FileNotFoundError:
    print("خطا: پوشه ui/Images پیدا نشد. لطفا مطمئن شوید که مسیر صحیح است.")
except Exception as e:
    print(f"خطایی رخ داد: {e}")