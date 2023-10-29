# Press the green button in the gutter to run the script.
import glob

import keyboard
from pick import pick

from macro_classes.recording_macro_manager import RecordingMacroManager


def main(parent_path="macros"):
    manager = RecordingMacroManager(parent_path=parent_path)
    options = ["record", "play"]

    while True:
        files_options = glob.glob("macros/*.json")
        option, _ = pick(options, "What would you like to do?: ")
        if option == "record":
            file_name = input("How would you like to name your macro?: ")
            file_name = file_name + ".json" if not file_name.endswith(".json") else file_name
            print("Press enter to start recording: ")
            keyboard.wait("enter")
            print("Recording started! press F5 to stop recording")
            manager.record_macro(file_name=file_name)
            print(f"Recording saved as {file_name}")
            option, _ = pick(options, "What would you like to do?: ")
        elif len(files_options):
            sub_option, _ = pick(files_options, "Choose your script: ")
            chosen_id = None
            for idx, macro in enumerate(manager):
                if macro.path == sub_option:
                    chosen_id = idx
            if chosen_id != 0 and not chosen_id:
                print("No file with this name")
                continue
            repeats = int(input("Enter repeats: "))
            manager.play_macro(chosen_id, repeats)
        else:
            print("There are no json files in macros folder!!")


if __name__ == "__main__":
    main()
