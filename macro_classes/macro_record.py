import json
import time

import keyboard
import mouse
from keyboard import KeyboardEvent, KEY_DOWN
from mouse import MoveEvent, ButtonEvent, WheelEvent, UP
from mouse._winmouse import move_to


class MacroRecord:
    __names_to_actions = {"MoveEvent": MoveEvent, "ButtonEvent": ButtonEvent, "WheelEvent": WheelEvent}

    def __init__(self, events=None):
        events = [] if not events else events
        events.sort(key=lambda e: e.time)
        self.events = events
        self.path = ""

    def __mouse_event_from_dict(self, _input: dict):
        action_class = self.__names_to_actions[_input.pop("name")]
        result = action_class(**_input)

        return result

    @staticmethod
    def __keyboard_event_from_dict(json_dict):
        k = KeyboardEvent(scan_code=json_dict.pop("scan_code"), event_type=json_dict.pop("event_type"))
        for key, value in json_dict.items():
            setattr(k, key, value)
        k.action_type = "k"
        return k

    def load_macro_from_file(self, file_path: str):
        self.path = file_path
        with open(file_path) as file:
            data = json.load(file)
            keyboard_events = [self.__keyboard_event_from_dict(d) for d in data["k_events"]]
            mouse_events = [self.__mouse_event_from_dict(m) for m in data["m_events"]]
            events = keyboard_events + mouse_events
            self.events = events
            self.events.sort(key=lambda e: e.time)

    def play(self, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
        state = keyboard.stash_state()

        last_time = None
        for event in self.events:
            if keyboard.is_pressed("esc"):
                print("macro aborted!")
                break
            if speed_factor > 0 and last_time is not None:
                time.sleep((event.time - last_time) / speed_factor)
            last_time = event.time
            if hasattr(event, "name"):
                key = event.scan_code or event.name
                keyboard.press(key) if event.event_type == KEY_DOWN else keyboard.release(key)

            else:
                if isinstance(event, ButtonEvent) and include_clicks:
                    if event.event_type == UP:
                        mouse.release(event.button)
                    else:
                        mouse.press(event.button)
                elif isinstance(event, MoveEvent) and include_moves:
                    move_to(event.x, event.y)
                elif isinstance(event, WheelEvent) and include_wheel:
                    mouse.wheel(event.delta)
        keyboard.restore_modifiers(state)
        print("action ended")





