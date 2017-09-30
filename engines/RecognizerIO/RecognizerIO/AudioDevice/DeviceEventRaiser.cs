using System;
using RecognizerIO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace RecognizerIO.AudioDevice
{
    class DeviceEventRaiser
    {
        private NAudio.CoreAudioApi.MMDeviceEnumerator deviceEnum = new NAudio.CoreAudioApi.MMDeviceEnumerator();
        private NotificationClientImplementation notificationClient;
        private NAudio.CoreAudioApi.Interfaces.IMMNotificationClient notifyClient;
        private RecognizerIO.Engines.EngineManager Engine;

        public DeviceEventRaiser(RecognizerIO.Engines.EngineManager engine)
        {
            Engine = engine;
            notificationClient = new NotificationClientImplementation(onDeviceChanged);
            notifyClient = (NAudio.CoreAudioApi.Interfaces.IMMNotificationClient)notificationClient;
            deviceEnum.RegisterEndpointNotificationCallback(notifyClient);
        }

        void onDeviceChanged()
        {
            // Send a message back to Python, which echos it back to read loop. I
            // have no idea why it works but calling Engine.ResetDevice() doesn't
            Debug.sendMessage("", "RESET_DEVICE");
            //Engine.ResetDevice();
        }

    }
}
