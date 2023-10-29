from macro_classes.macro_record import MacroRecord
import json

import keyboard
import mouse
import glob


class RecordingMacroManager:

    def __init__(self, parent_path):
        self.macros = []
        self.parent_path = parent_path
        files = glob.glob(f"{parent_path}\\*.json")
        for file_path in files:
            macro_record = MacroRecord()
            macro_record.load_macro_from_file(file_path)
            self.macros.append(macro_record)

    @staticmethod
    def __save_macro_as_json(mouse_events, keyboard_events, name: str):
        result = {"m_events": mouse_events, "k_events": keyboard_events}
        json_object = json.dumps(result, indent=3)
        with open(name, 'w') as outfile:
            outfile.write(json_object)

    @staticmethod
    def __get_keyboard_event(event):
        json_dict = event.to_json()
        json_dict = json.loads(json_dict)
        return json_dict

    @staticmethod
    def __get_all_attributes(event):
        attributes = dir(event)
        forbidden = ["count", "index"]
        attributes = [attr for attr in attributes if
                      not attr.startswith("_") and attr not in forbidden]

        return attributes

    def __get_mouse_event_dict(self, event):
        attributes = self.__get_all_attributes(event)
        result = {"name": type(event).__name__}
        for attr in attributes:
            result[attr] = getattr(event, attr)
        return result

    def record_macro(self, file_name: str):
        mouse_events = []
        # keyboard.hook(lambda _: keyboard_events.append(_))
        mouse.hook(mouse_events.append)
        keyboard.start_recording()
        keyboard.wait("f5")

        mouse.unhook(mouse_events.append)
        keyboard_events = keyboard.stop_recording()

        keyboard_jsons = [self.__get_keyboard_event(event) for event in keyboard_events]
        mouse_jsons = [self.__get_mouse_event_dict(event) for event in mouse_events]
        keyboard_jsons = keyboard_jsons[:-1]
        mapped_path = f"{self.parent_path}\\{file_name}"
        self.__save_macro_as_json(mouse_jsons, keyboard_jsons, name=mapped_path)

        common_list = mouse_events + keyboard_events
        macro_record = MacroRecord(events=common_list)
        macro_record.path = mapped_path
        self.append(macro_record)

    def play_macro(self, macro_id, repeat: int = 1):
        macro = self[macro_id]
        for iteration in range(repeat):
            print(f"Running {iteration + 1}/{repeat} iteration...")
            macro.play()
            print(f"Finished {iteration + 1}/{repeat} iteration...")
            if keyboard.is_pressed("esc"):
                print("stopping!")
                break

    def __getitem__(self, item):
        return self.macros[item]

    def append(self, argument):
        self.macros.append(argument)
