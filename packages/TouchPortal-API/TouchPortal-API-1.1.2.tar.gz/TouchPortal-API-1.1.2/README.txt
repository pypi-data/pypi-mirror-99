This is TouchPortal API made it easily to create TouchPortal Plugins. Here is some examples

```python
import TouchPortalAPI # Import the api

TPClient = TouchPortalAPI.Client('YourPluginID') # Initiate the client (replace YourPluginID with your ID)

@TPClient.on('info')  # This Will run once You've connected to TouchPortal
def OnStart(client, data):
    # You must provide 2 parm in the function or else it will give error 
    print('I am Connected!', data)
    
    
    TPClient.stateUpdate("(Your State ID)", "State Value") # This if you want to update a dymic states in TouchPortal
    
    updateStates = [
        {
            "id": "(Your State ID)",
            "value": "(The Value You wanted)"
        },
        {
            "id": "(Your 2nd State ID)",
            "value": "(The Value You wanted)"
        }
    ]
    TPClient.stateUpdateMany(updateStates) # Or You can create an list with however many state you want and use this function to send them all
    
@TPClient.on('action')  # This manages when you press a button in TouchPortal it will send here in json format
def Actions(client, data):
    print(data)

@TPClient.on('settingUpdate') # This Function will get called Everytime when someone changes something in your plugin settings
def Settings(client, data):
    print('received data from settings!')
    
@TPClient.on('closePlugin') # When TouchPortal sends close Plugin message it will run this function
def shutDown(client, data):
    print('Received shutdown message!')
    TPClient.disconnect() # This is how you disconnect once you received the closePlugin message
    
    
TPClient.connect() # Connect to Touch Portal
```