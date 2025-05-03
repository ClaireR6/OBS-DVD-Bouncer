from obswebsocket import obsws, requests


from config import websocket_host, websocket_port, websocket_password


class OBSWebsocketManager:
    ws =  None

    def __init__(self):
        self.ws = obsws(websocket_host, websocket_port, websocket_password)
        self.ws.connect()
        print("Connected to OBS WebSocket")
    

    def disconnect(self):
        self.ws.disconnect()
        print("Disconnected from OBS WebSocket")

    def get_scene_list(self):
        """
        Get the list of scenes in OBS.
        :return: List of scene names.
        """
        try:
            response = self.ws.call(requests.GetSceneList())
            return [scene['name'] for scene in response.getScenes()]
        except Exception as e:
            print(f"Error getting scene list: {e}")
            return []


    def get_source_transform(self, scene_name, source_name):
        """
        Get the transform of a source in OBS.
        :param scene_name: Name of the scene containing the source.
        :param source_name: Name of the source to get transform for.
        """
        try:
            response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
            scene_item_id = response.datain['sceneItemId']
            response = self.ws.call(requests.GetSceneItemTransform(sceneName=scene_name, sceneItemId=scene_item_id))
            transform = {
                "position_x": response.datain['sceneItemTransform']['positionX'],
                "position_y": response.datain['sceneItemTransform']['positionY'],
                "scale_x": response.datain['sceneItemTransform']['scaleX'],
                "scale_y": response.datain['sceneItemTransform']['scaleY'],
                "crop_top": response.datain['sceneItemTransform']['cropTop'],
                "crop_bottom": response.datain['sceneItemTransform']['cropBottom'],
                "crop_left": response.datain['sceneItemTransform']['cropLeft'],
                "crop_right": response.datain['sceneItemTransform']['cropRight'],
                "rotation": response.datain['sceneItemTransform']['rotation']
            }
            return transform
        except Exception as e:
            print(f"Error getting transform for {source_name}: {e}")
            return None, None, None, None

    def set_source_transform(self, scene_name, source_name, new_transform):
        """
        Set the transform of a source in OBS.
        :param source_name: Name of the source to transform.
        :param x: X position of the source.
        :param y: Y position of the source.
        :param width: Width of the source.
        :param height: Height of the source.
        """
        try:
            response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
            scene_item_id = response.datain['sceneItemId']
            self.ws.call(requests.SetSceneItemTransform(sceneName=scene_name, sceneItemId=scene_item_id, sceneItemTransform=new_transform))
            #print(f"Set transform for {source_name}: {new_transform}")
        except Exception as e:
            print(f"Error setting transform for {source_name}: {e}")

    def set_source_filter(self, source_name, filter_name, setting_name, setting_value):
        """
        Update a source filter in OBS.
        :param source_name: Name of the source to update the filter for.
        :param filter_name: Name of the filter to update.
        :param filter_settings: Dictionary of settings to update the filter with.
        """
        try:
            settings = {
                setting_name: setting_value
            }
            self.ws.call(requests.SetSourceFilterSettings(sourceName=source_name, filterName=filter_name, filterSettings=settings))
            #print(f"Updated filter {filter_name} for {source_name}: {filter_settings}")
        except Exception as e:
            print(f"Error updating filter {filter_name} for {source_name}: {e}")

#TODO: Add a function to set the visibility of a source in OBS.
    def set_source_visibility(self, scene_name, source_name, visibility):
        """
        Set the visibility of a source in OBS.
        :param source_name: Name of the source to set visibility for.
        :param visible: Boolean value to set visibility (True for visible, False for hidden).
        """
        try:
            response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
            scene_item_id = response.datain['sceneItemId']
            self.ws.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneItemId=scene_item_id, sceneItemEnabled=visibility))
            #print(f"Set visibility for {source_name}: {visibility}")
        except Exception as e:
            print(f"Error setting visibility for {source_name}: {e}")


#TODO: Add a function to set the visibility of filters of a source in OBS
