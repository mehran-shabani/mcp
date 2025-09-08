# Model: فقط داده‌ها را نگه می‌دارد
class User:
    def __init__(self, name):
        self.name = name
        self.status = "inactive"  # وضعیت اولیه

    def __str__(self):
        return f"user: '{self.name}' status: '{self.status}'"
    

# Protocol: منطق و قوانین در اینجا قرار دارد
class UserManagementProtocol:
    def activate_user(self, user_model):
        """قانون فعال کردن کاربر"""
        print(f" activating:{user_model.name}...")
        user_model.status = "active"

    def deactivate_user(self, user_model):
        """قانون غیرفعال کردن کاربر"""
        print(f" deactivating:{user_model.name}...")
        user_model.status = "inactive"


 # Context: مدل و پروتکل را به هم وصل می‌کند
class UserContext:
    def __init__(self, name):
        self._user = User(name)  # یک نمونه از مدل را در خود نگه می‌دارد
        self._protocol = UserManagementProtocol()  # یک نمونه از پروتکل را هم دارد

    def activate(self):
        """درخواست فعال‌سازی را به پروتکل می‌سپارد"""
        self._protocol.activate_user(self._user)

    def deactivate(self):
        """درخواست غیرفعال‌سازی را به پروتکل می‌سپارد"""
        self._protocol.deactivate_user(self._user)

    def show_status(self):
        """وضعیت فعلی مدل را نمایش می‌دهد"""
        print(str(self._user))   