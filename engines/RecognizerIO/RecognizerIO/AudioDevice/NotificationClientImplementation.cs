using System;
using NAudio.CoreAudioApi;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RecognizerIO.AudioDevice
{
    class NotificationClientImplementation : NAudio.CoreAudioApi.Interfaces.IMMNotificationClient
    {
        private Action onDeviceChanged;
        private string ActiveDeviceId;

        public NotificationClientImplementation()
        {
            //_realEnumerator.RegisterEndpointNotificationCallback();
            if (System.Environment.OSVersion.Version.Major < 6)
            {
                throw new NotSupportedException("This functionality is only supported on Windows Vista or newer.");
            }
        }

        public NotificationClientImplementation(Action onDeviceChanged)
        {
            this.onDeviceChanged = onDeviceChanged;
        }

        public void OnDefaultDeviceChanged(DataFlow dataFlow, Role deviceRole, string defaultDeviceId)
        {
            //Do some Work
            if (dataFlow.ToString() != "Capture" || defaultDeviceId == ActiveDeviceId) return;
            ActiveDeviceId = defaultDeviceId;
            this.onDeviceChanged();
        }

        public void OnDeviceAdded(string deviceId)
        {
            //Do some Work
            //Console.WriteLine("OnDeviceAdded -->");
        }

        public void OnDeviceRemoved(string deviceId)
        {

            //Console.WriteLine("OnDeviceRemoved -->");
            //Do some Work
        }

        public void OnDeviceStateChanged(string deviceId, DeviceState newState)
        {
           // Console.WriteLine("OnDeviceStateChanged\n Device Id -->{0} : Device State {1}", deviceId, newState);
            //Do some Work
        }

        public void OnPropertyValueChanged(string deviceId, PropertyKey propertyKey)
        {
            //Do some Work
            //fmtid & pid are changed to formatId and propertyId in the latest version NAudio
            //Console.WriteLine("OnPropertyValueChanged: formatId --> {0}  propertyId --> {1}", propertyKey.formatId.ToString(), propertyKey.propertyId.ToString());
        }

    }
}
