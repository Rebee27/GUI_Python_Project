import argparse

from utils import Utilities


def main(script_exe_path: str) -> None:
    start_toolkit_command = script_exe_path

    Utilities.add_to_windows_context_menu(
        filetype="Directory",
        registry_title="TazzGUI",
        command=start_toolkit_command,
        title="TazzGUI",
        icon_path=r"G:\My Drive\7. Future_Up\Gog_Rebeca_Ana\style\app.ico"
    )
    Utilities.remove_windows_context_menu("Directory", "TazzGUI")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("script_exe_path")

    args = parser.parse_args()
    main(args.script_exe_path)
