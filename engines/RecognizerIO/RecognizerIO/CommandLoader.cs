using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace RecognizerIO
{
    class CommandLoader
    {

        string RootPath;
        string StartSettingsPath;
        public Dictionary<string, CommandModule> CmdModules;

        public CommandLoader()
        {
            //RootPath = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName) + @"..\..\..\..\..\OSSpeak\commands";
            RootPath = @"C:\Users\evan\modules\OSSpeak\user\commands";
            StartSettingsPath = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName) + @"\settings.json";

            CmdModules = new Dictionary<string, CommandModule>();
        }

        public void LoadModules()
        {
            DirSearch(RootPath);
        }

        public void LoadJson(string path)
        {
            using (StreamReader r = new StreamReader(path))
            {
                string json = r.ReadToEnd();
                CommandModule module = JsonConvert.DeserializeObject<CommandModule>(json);
                CmdModules[path] = module;
            }
        }

        public Settings LoadSettings()
        {
            using (StreamReader r = new StreamReader(StartSettingsPath))
            {
                string json = r.ReadToEnd();
                var settings = JsonConvert.DeserializeObject<Settings>(json);
                foreach (var scope in settings.Scopes)
                {
                    Debug.Assert(scope.Value.Options.Contains(scope.Value.Current));
                }
                return settings;
            }
        }

        private void DirSearch(string sDir)
        {
            foreach (string f in Directory.GetFiles(sDir))
            {
                LoadJson(f);
            }
            foreach (string d in Directory.GetDirectories(sDir))
            {
                this.DirSearch(d);
            }
        }
    }

    class CommandModule
    {
        public Dictionary<string, string> Scopes;
        public Dictionary<string, string> NumberedCommands;
        public Dictionary<string, string> Commands;
    }

    class Settings
    {
        public Dictionary<string, Scope> Scopes;
        public string EnableKeyword;
        public string DisableKeyword;
    }

    class Scope
    {
        public string Current;
        public string[] Options;
    }

}
