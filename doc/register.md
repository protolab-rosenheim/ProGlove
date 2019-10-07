# ProGlove send function #
If registered, everytime a code is scanned with the ProGlove the OPCUA-Client will call the defined method. As parameter the scanned code is used.
## Register ##
```
{
  "CONF":{
    "UID":111,
    "CON":true,
    "OPCUAURL":"opc.tcp://192.168.1.70:4840/",
    "NODEMETHOD":[
      "0:Objects",
      "2:iot_ready_kit",
      "2:find_part"
    ]
  }
}
```

## UNregister ##

```
{
  "CONF":{
    "UID":111,
    "CON":false,
    "OPCUAURL":"opc.tcp://192.168.1.70:4840/",
    "NODEMETHOD":[
      "0:Objects",
      "2:iot_ready_kit",
      "2:find_part"
    ]
  }
}
```