Theorically, default directory paths are changable and specified in path.json. The description are as follows:
```
login:              login details file path

logpath:            logging directory

data:libroot:       default directory of data thread modules
data:rawroot:       default directory of raw data
data:dataroot:      default directory of dataset
data:miscroot:      default default directory of miscellaneous for data thread

model:libroot:      default directory of model thread modules
model:modelroot:    default directory of untrained / created models
model:distroot:     default directory of trained (and tested) models
model:miscroot:     default directory of miscellaneous for model thread

test:libroot:       default directory of test thread modules
test:tmproot:       default directory of untrained / created models
test:modelroot:     default directory of trained (and tested) models
test:distroot:      default directory of exported Algomodels
test:miscroot:      default directory of miscellaneous for test thread

ioHub:libroot:      default directory of script module
ioHub:scriptroot:   default directory of scripts
```
`login.json` is currently just for telegram. Details can be obtained via [BotFather](https://core.telegram.org/bots) of Telegram.
```
telegram:Enable:    true = Enable; false = Disable
telegram:token:     by BotFather
telegram:botname:   by BotFather
telegram:authgroup: via Telegram Web, replacing g to minus
```
A authgroup value is required for the bot to respond. The authgroup can usually be obtained via the Telegram Web view. The value is at the end of the group chat link. e.g. `g98765432`, indicates the authgroup = `-98765432`
