import winreg


class Utilities:
    @staticmethod
    def add_to_windows_context_menu(filetype: str, registry_title: str, command: str, title: str = None, icon_path : str=None):
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Classes", 0, winreg.KEY_SET_VALUE)
        k1 = winreg.CreateKey(reg, filetype)
        k2 = winreg.CreateKey(k1, "shell")
        k3 = winreg.CreateKey(k2, registry_title)
        k4 = winreg.CreateKey(k3, "command")

        # set icon
        if icon_path is not None:
            print(icon_path)
            winreg.SetValueEx(k3, "Icon", 0, winreg.REG_SZ, icon_path)
        if title is not None:
            winreg.SetValueEx(k3, None, 0, winreg.REG_SZ, title)

        winreg.SetValueEx(k4, None, 0, winreg.REG_SZ, command)
        winreg.CloseKey(k3)
        winreg.CloseKey(k2)
        winreg.CloseKey(k1)
        winreg.CloseKey(reg)

    @staticmethod
    def remove_windows_context_menu(filetype: str, registry_title: str):
        base_key_path = "Software\\Classes\\" + filetype + "\\" + "shell" + "\\"
        key_to_delete_path = base_key_path + registry_title

        base_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key_path, 0, winreg.KEY_ALL_ACCESS)
        key_to_delete = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_to_delete_path, 0, winreg.KEY_ALL_ACCESS)

        info_key = winreg.QueryInfoKey(key_to_delete)
        for i in range(0, info_key[0]):
            sub_key = winreg.EnumKey(key_to_delete, 0)
            try:
                winreg.DeleteKey(key_to_delete, sub_key)
            except OSError as e:
                raise OSError

        winreg.DeleteKey(base_key, registry_title)
