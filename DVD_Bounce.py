
from OBS_Websocket import OBSWebsocketManager
import atexit, time, json, sys

def display_usage():
    print("Usage: python DVD_Bounce.py <config_name>")
    print("Available config names:")
    with open("dvd_bounce_config.json", "r") as file:
        config = json.load(file)
        for key in config.keys():
            print(f" - {key}")

class DVD_Bounce:

    if len(sys.argv) < 2:
        display_usage()
        sys.exit(1)


    config_name = sys.argv[1]

    with open("dvd_bounce_config.json", "r") as file:
        config = json.load(file)
        if config_name not in config:
            print(f"Config name '{config_name}' not found.")
            display_usage()
            sys.exit(1)



    setting = config[config_name]


    scene_name = setting["scene_name"]
    source_name = setting["source_name"]
    screen_width = setting["screen_width"]
    screen_height = setting["screen_height"]
    logo_width = setting["logo_width"]  
    logo_height = setting["logo_height"]
    fps_time = setting["fps_time"]
    pixels_per_second_mod = setting["pixels_per_second_mod"]
    top = setting["top"]
    left = setting["left"]

    # Initialize OBS WebSocket Manager
    manager = OBSWebsocketManager()

    try: 
        transform = manager.get_source_transform(scene_name, source_name)
        if not transform:
            raise Exception("Could not get initial transform.")
        
        manager.set_source_visibility(scene_name, source_name, True)

        x = transform["position_x"]
        y = transform["position_y"]
        dx = 4 * pixels_per_second_mod
        dy = 3 * pixels_per_second_mod
        hue_shift = 0

        def increment_hue_shift(hue_shift):
            hue_shift += 40
            if hue_shift > 180:
                hue_shift = -180 + hue_shift % 180
            return hue_shift

        while True:
            # Bounce logic
            flag_x = False
            flag_y = False
            if x <= left or x + logo_width >= screen_width + left:
                #print(f"Bounce X {x}, Screen Width {screen_width}, Logo Width {logo_width}")
                dx = abs(dx) if x <= left else -abs(dx)
                hue_shift = increment_hue_shift(hue_shift)
                manager.set_source_filter(source_name, "HueShift", "hue_shift", hue_shift)
                flag_x = True

            if y <= top or y + logo_height >= screen_height + top:
                #print(f"Bounce Y {y}, Screen Width {screen_height}, Logo Width {logo_height}")
                dy = abs(dy) if y <= top else -abs(dy)
                hue_shift = increment_hue_shift(hue_shift)
                manager.set_source_filter(source_name, "HueShift", "hue_shift", hue_shift)
                flag_y = True
            
            if flag_x and flag_y:
                print("CORNER!!!")
                flag_x = False
                flag_y = False

            x += dx
            y += dy

            # Update position
            new_transform = {
                "positionX": x,
                "positionY": y
            }

            manager.set_source_transform(scene_name, source_name, new_transform)
            time.sleep(fps_time)  # ~100 FPS bounce, smooth

    except KeyboardInterrupt:
        print("Exiting DVD_Bounce...")
        manager.set_source_visibility(scene_name, source_name, False)
        manager.disconnect()
        exit(0)


    