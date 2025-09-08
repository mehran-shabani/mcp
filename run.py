from mcp import *


user_session = UserContext('mehran')

user_session.deactivate()
user_session.show_status()


# --- اجرای برنامه ---

# ما فقط یک زمینه (Context) برای کاربر "آرش" می‌سازیم
user_session = UserContext("arash")

# وضعیت اولیه را چک می‌کنیم
user_session.show_status()
# خروجی: کاربر 'آرش' در وضعیت 'inactive' قرار دارد.

print("-" * 20)

# کاربر را فعال می‌کنیم
user_session.activate()
# خروجی: در حال اجرای پروتکل: فعال کردن کاربر آرش...

# وضعیت جدید را چک می‌کنیم
user_session.show_status()
# خروجی: کاربر 'آرش' در وضعیت 'active' قرار دارد.