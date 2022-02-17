#
#  API to retrieve informations from the Open Auto pro soft
#  Based on https://github.com/bluewave-studio/openauto-pro-api  Copyright (C) BlueWave Studio - All Rights Reserved
#
import time
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler

class EventHandler(ClientEventHandler):

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
                .format(message.result, message.oap_version.major,
                        message.oap_version.minor, message.api_version.major,
                        message.api_version.minor))

        set_status_subscriptions = oap_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            oap_api.SetStatusSubscriptions.Subscription.MEDIA)
        client.send(oap_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

def wait_for_media_message(client, root):
    can_continue = True

    message = client.receive()
    if message.id == oap_api.MESSAGE_PING:
        client.send(oap_api.MESSAGE_PONG, 0, bytes())
    elif message.id == oap_api.MESSAGE_BYEBYE:
        can_continue = False

    if client._event_handler is not None:
        if message.id == oap_api.MESSAGE_HELLO_RESPONSE:
            hello_response = oap_api.HelloResponse()
            hello_response.ParseFromString(message.payload)
            client._event_handler.on_hello_response(client, hello_response)
            
        elif message.id == oap_api.MESSAGE_MEDIA_STATUS:
            media_status = oap_api.MediaStatus()
            media_status.ParseFromString(message.payload)
            if root == 0:
                print(f"media status, is playing: {media_status.is_playing}, position label: {media_status.position_label}, source: {media_status.source}")
            else:
                # Retrieve Bluetooth_duration value to calculate a percentage
                if media_status.position_label != '' and root.Bluetooth_duration.text() != '00:00':
                    position_label_in_sec = int(media_status.position_label[:-3]) * 60 + int(media_status.position_label[-2:])
                    duration_label = root.Bluetooth_duration.text()
                    duration_label_in_sec = int(duration_label[:-3]) * 60 + int(duration_label[-2:])
                    percent = (position_label_in_sec / duration_label_in_sec) * 100
                    
                    # Send signal to update progress bar according to percent value
                    root.percent.setText(str(percent))
                    root.Bluetooth_timing.setText(media_status.position_label)
                    root.custom_signals.update_progress_bluetooth_track_signal.emit()

        elif message.id == oap_api.MESSAGE_MEDIA_METADATA:
            media_metadata = oap_api.MediaMetadata()
            media_metadata.ParseFromString(message.payload)
            if root == 0:
                print(f"media metadata, artist: {media_metadata.artist}, title: {media_metadata.title}, album: {media_metadata.album}, duration label: {media_metadata.duration_label}")
            else:
                root.Bluetooth_track.setText('No Title' if not media_metadata.title else media_metadata.title)
                root.Bluetooth_artist.setText('No Artist' if not media_metadata.artist else media_metadata.artist)
                root.Bluetooth_duration.setText(media_metadata.duration_label)
    return can_continue


def mediadata(root):
    if root !=0 :
        time.sleep(2)
    client = Client('Media_data')
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)
    active = True
    while active:
        try:
            active = wait_for_media_message(client, root)
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    # if the mediadata argument is set to 0, the script print the result to the console
    mediadata(0)
