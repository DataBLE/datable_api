==================
API Documentation
==================
URL root: http://protected-springs-5667.herokuapp.com/

Motes
===============

/motes/sighting (POST)
-------------------------------------------------------------------------
:Description: 
    Tells the service that an app on a device has found a mote in the wild,
:Method: 
    POST  content-type: application/x-www-form-urlencoded
:Parameters: 
    :app: 
        Application BundleID/packageName string
    :platform:
        String choice (ios|android)
    :mote:
        32 char string of the found mote UUID
    :major:
        Integer of the found mote major number
    :minor:
        Integer of the found mote minor number
:Response:
    Empty JSON response dictionary
               {}
:Errors:
    JSON response with an object containing error descriptions
    
            {
                "errors":{
                "__all__":[
                "Invalid application"
                ],
                "app":[
                "This field is required."
                ],
                ],
                "mote":[
                "This field is required."
                ],
                "platform":[
                "This field is required."
                ]
                }
            } 

:Sample curl:
    curl -d "app=com.foo.canabalt&mote=B9407F30-F5F8-466E-AFF9-25556B57&major=2257&minor=6406&platform=ios"  http://protected-springs-5667.herokuapp.com/motes/sighting



/motes/discover (POST)
-------------------------------------------------------------------------
:Description: 
    Tells the service that an app on a device has found a mote in the wild,
    and that it should take a gender based action
:Method: 
    POST  content-type: application/x-www-form-urlencoded
:Parameters: 
    :app: 
        Application BundleID/packageName string
    :platform:
        String choice (ios|android)
    :mote:
        32 char string of the found mote UUID
    :major:
        Integer of the found mote major number
    :minor:
        Integer of the found mote minor number
    :rssi:
        Floating point value of the mote RSSI value
    :gender:
        String choice (male|female) denoting the gender of the app user
:Response:
    JSON response denoting the action that the device should take

               {"action":"video",
               "question":"Question here",
               "resource":"http://youtube.com/foo"
               "repeat": True,
               "repeat_interval": 5,
               "uuid": ""698df5fe7195478ea6649981c6d0a596"
               }
:Errors:
    JSON response with an object containing error descriptions
    
            {
                "errors":{
                "__all__":[
                "Invalid application"
                ],
                "app":[
                "This field is required."
                ],
                "gender":[
                "This field is required."
                ],
                "mote":[
                "This field is required."
                ],
                "platform":[
                "This field is required."
                ]
                }
            } 

:Sample curl:
    curl -d "app=com.foo.canabalt&gender=male&mote=B9407F30-F5F8-466E-AFF9-25556B57&major=2257&minor=6406&platform=ios&rssi=1.5"  http://protected-springs-5667.herokuapp.com/motes/discover






/motes/app (POST)
-------------------------------------------------------------------------
:Description: 
    Informs the application which motes are available to be discovered for
    the given application
:Method: 
    POST  content-type: application/x-www-form-urlencoded
:Parameters: 
    :app: 
        Application BundleID/packageName string
    :platform:
        String choice (ios|android)
    :lat:
        Latitude string (-118.038)
    :lon:
        Longitude string (34.003)
    :distance:
        Distance in floating point miles to search for motes.  
        Not required.  Defaults to 5.0
:Response:
    JSON response listing motes available for that application within
    a certain distance of the lat/lon values

                {
                    "motes":[
                    {
                    "major":"10",
                    "minor":"5",
                    "uuid":"217cbd82af2d4b8cae7917e51e6c9d59"
                    }
                    ]
                }


:Errors:
    JSON response with an object containing error descriptions

        
            {
                "errors":{
                "app":[
                "This field is required."
                ],
                "platform":[
                "This field is required."
                ]
                "lat":[
                "This field is required."
                ]
                "lon":[
                "This field is required."
                ]
                }
            } 





/motes/confirm (POST)
-------------------------------------------------------------------------
:Description: 
    Perform a POST to this URL after the user has accepted or rejected any
    action.
:Method: 
    POST  content-type: application/x-www-form-urlencoded
:Parameters: 
    Same parameters as /motes/discover API, but also add the following
    
    :uuid
        String uuid from the /motes/discover API reponse
    :response
        String that notifies the action taken by the user.  Could be
        anything you wish. 'OK', 'yes', 'no', 'false', etc...
:Response:
    JSON response denoting the action that the mote device is going to take

               {"action":"tv-video",
               "question":"Question here",
               "resource":"http://youtube.com/foo"
               "repeat": True,
               "repeat_interval": 5,
               }
:Errors:
    JSON response with an object containing error descriptions
    
            {
                "errors":{
                "__all__":[
                "Invalid application"
                ],
                "app":[
                "This field is required."
                ],
                "gender":[
                "This field is required."
                ],
                "mote":[
                "This field is required."
                ],
                "platform":[
                "This field is required."
                ]
                }
            } 
:Sample curl:
    curl -d "app=com.foo.canabalt&gender=male&mote=B9407F30-F5F8-466E-AFF9-25556B57&major=2257&minor=6406&platform=ios&rssi=1.5&uuid=<UUID FROM /motes/dicover API RESPONSE&response=yes"  http://protected-springs-5667.herokuapp.com/motes/confirm

