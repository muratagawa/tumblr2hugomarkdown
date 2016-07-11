+++
date = "2014-11-15T04:01:00+00:00"
draft = false
tags = ["geek", "ionic", "amazon sns", "android"]
title = "Amazon SNS with Ionic Framework - Part 1: Android"
+++


Recently I found out about [Ionic](http://ionicframework.com/) and decided to use it to build the Android and iOS mobile apps for [Huat.SG](http://huat.sg). In their own words:

> “**Create hybrid mobile apps with the web technologies you love. **Free and open source, Ionic offers a library of mobile-optimized HTML, CSS and JS components, gestures, and tools for building highly interactive apps. Built with Sass and optimized for AngularJS.”

I had written apps for Android a few years ago, but have not been involved in mobile development since then, and have been wanting to build something again. I have heard of PhoneGap previously but never got around to using it, and since then there’re many other hybrid frameworks that have popped up. Ionic is one of them (which is powered by Cordova, which is very closely related to PhoneGap; see [here](http://ionicframework.com/blog/what-is-cordova-phonegap/) for more info). I decided on Ionic over the other choices as it seems to be quite actively developed, has an active community, and it’s open-sourced. In addition, it uses [AngularJS](https://angularjs.org), which is something I’ve been wanting to pick up for a while, and using Ionic will indirectly force me to use AngularJS.

During the development of Huat.SG, one of the things I wanted to do was to make use of Amazon SNS to handle the push notifications. I’ve found a lot of different tips and ways to get it working in the Ionic Forums, and also tried to follow the guidelines at [Implementing GCM Client](http://developer.android.com/google/gcm/client.html) as closely as possible. Below are the steps I’ve taken in order to make push notification work on Ionic for Android with Amazon SNS.

**_Part A: Create a Google API Project and Enable GCM_**

The official documentation on this can be found [here](http://developer.android.com/google/gcm/gs.html). The most important things to take note of are:

  * Enable GCM
  * Project ID/Sender ID (they are the same thing)
  * API Key



**_Part B: Register Mobile App with Amazon SNS_**

The official documentation on this can be found [here](http://docs.aws.amazon.com/sns/latest/dg/mobile-push-send-register.html). You would need the API Key created in Part A for this.

**_Part C: Ionic_**

**Step 1: Add the required plugins to your Ionic project**

**PushPlugin**
[code] 
    cordova plugin add com.phonegap.plugins.PushPlugin
[/code]

**AppVersion**
[code] 
    cordova plugin add uk.co.whiteoctober.cordova.appversion
[/code]

**Step 2: Get ngCordova**

I made use of [ngCordova](http://ngcordova.com/) so that the plugins downloaded in Step 1 can be used in an Angular way. Go to <http://ngcordova.com/docs/> and follow the Install instructions. Once done, include ngCordova in your index.html, BEFORE Cordova. Mine looks like this:
[code] 
    <script src="js/ng-cordova.min.js" type="text/javascript"></script>  
    <script src="cordova.js" type="text/javascript"></script>
[/code]

**Step 3: Ionic/AngularJS .run()**

Edit your project’s .run() method so that it looks something similar to the following code.
[code] 
    .run(function($ionicPlatform, $localStorage, $cordovaPush) {
      $ionicPlatform.ready(function() {
        // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
        // for form inputs)
        if(window.cordova && window.cordova.plugins.Keyboard) {
          cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
        }
        if(window.StatusBar) {
          // org.apache.cordova.statusbar required
          StatusBar.styleDefault();
        }
    
        //Main part of the code
        cordova.getAppVersion(function(version) {
          appVersion = version;
          console.info("Version: " + appVersion);
          registerPushNotification();
        });
    
        var androidConfig = {
          "senderID":"GOOGLE_PROJECT_API_KEY", //This is the project/sender ID from Google, created in Part A
          "ecb":"onAndroidNotification" //This is the function we will call when a push notification arrives. This will be detailed in the next step.
        };
    
        storedPushNotificationId = $localStorage.get("pushNotificationId", "");
        storedRegisteredAppVersion = $localStorage.get("registeredAppVersion", "");
        var shouldRegister = false;
    
        var registerPushNotification = function() {
          if (storedPushNotificationId == "") {
            shouldRegister = true;
          }
          else {
            if (storedRegisteredAppVersion != appVersion) {
              shouldRegister = true;
            }
          }
    
          if (shouldRegister) {
            if (device.platform == "Android") {
              $cordovaPush.register(androidConfig).then(function(result) {
                console.info('$cordovaPush.register succeeded. Result: '+ result);
              }, function(err) {
                console.info('$cordovaPush.register failed. Error: ' + err);
              });
            }
          }
          //End of main part of the code
        };
      });
    })
    
[/code]

We are using local storage to store the token (see next step), and we check if we have any token stored before deciding whether to register for a new token. In addition, as per the GCM Client Implementation, we are going to register for a new token whenever there is a new/different version of the app being used. To achieve that, we store the app version using local storage (see next step) and retrieve it when the app runs so we can compare if the app is still the same version. If not, we will also register for a new token.

**Step 4: onAndroidNotification**

As you can see from Step 3, onAndroidNotification is the method that gets called whenever a push notification is received.
[code] 
    var onAndroidNotification = function(e) {
      switch( e.event )
      {
      case 'registered':
        if (e.regid.length > 0)
        {
            console.info("Android Registration ID: " + e.regid);       
            
            //Your GCM push server needs to know the regID before it can push to this device here is where you might want to send it the regID for later use.
            var postData = {
              "token": e.regid,
              "platform": "GCM"
            };
    
            var elem = angular.element(document.querySelector('[ng-app]'));
            var injector = elem.injector();
            var httpService = injector.get('$http');
    
            //POST_ADDRESS should point to a server somewhere, where you then register the token with Amazon SNS. See Part D for a short snippet.
            var responsePromise = httpService.post(“POST_ADDRESS”, postData);
    
            responsePromise.success(function(data, status, headers, config) {
              var localStorageService = injector.get('$localStorage');
              localStorageService.set("pushNotificationId", e.regid);
              localStorageService.set("registeredAppVersion", appVersion);
            });
    
            responsePromise.error(function(data, status, headers, config) {
              console.log(JSON.stringify(data));
            });
        }
        break;
    
      case 'message':
        if (e.foreground)
        {
          var elem = angular.element(document.querySelector('[ng-app]'));
          var injector = elem.injector();
          var ionicPopupService = injector.get('$ionicPopup');
    
          var confirmPopup = ionicPopupService.confirm({
            title: e.payload.title,
            template: e.payload.message
          });
          confirmPopup.then(function(res) {
            if(res) {
              var stateService = injector.get('$state');
              stateService.go(e.payload.action);
            }
          });
        }
        else
        {
          var elem = angular.element(document.querySelector('[ng-app]'));
          var injector = elem.injector();
          var stateService = injector.get('$state');
          stateService.go(e.payload.action);
        }
        break;
    
      case 'error':
        break;
    
      default:
        break;
      }
    }
    
[/code]

In the event where we get a ‘registered’ message, we send the registration token that is received to a server (see Part D), which will then add the token to Amazon SNS as an endpoint. Upon success, the token and the app version will be stored using local storage.

On the other hand, when we get an actual push ‘message’, if we are already in the app (foreground), we popup an alert (instead of a status bar notification) to get the user’s attention. If we are in the background, we do something else. In the sample code above, I’m using ui-router (which comes with Ionic), and making use of $state.go to change the tab/state to another view, based on the payload’s action.

The injector is used to make use of the Angular services. Also, I’ve saved the entire piece of code in a separate file push-notification.js, since it really doesn’t fit anywhere else within the Ionic project.

**_Part D: Sample Server_**

I used Tornado for my backend and also used Botocore, and below are the parts related to push notification.
[code] 
    import botocore.session
    from tornado_botocore import Botocore
    # More imports...
    
    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
                (r'/subscribePush/?', SubscribePushNotificationHandler),
                # More handlers
            ]
            settings = dict(
                template_path = os.path.join(os.path.dirname(__file__), "templates"),
                static_path = os.path.join(os.path.dirname(__file__), "static"),
                debug=options.debug_mode
            )
            tornado.web.Application.__init__(self, handlers, **settings)
    
    # Main code
    class SubscribePushNotificationHandler(tornado.web.RequestHandler):
        @gen.coroutine
        def post(self):
            data = tornado.escape.json_decode(self.request.body)
            token = None
            platform = None
    
            try:
                token = data["token"]
            except KeyError:
                logging.warning("SubscribePushNotificationHandler: No Token")
                self.set_status(400)
                self.write({"status": "error", "message": "Please provide a token."})
                return
    
            try:
                platform = data["platform"]
            except KeyError:
                logging.warning("SubscribePushNotificationHandler: No Platform")
                self.set_status(400)
                self.write({"status": "error", "message": "Please provide a platform."})
                return
    
            platformApplicationArn = None
    
            if platform == "GCM":
                platformApplicationArn = "AMAZON_SNS_PLATFORM_ARN" # This is the platform ARN you created in Part B.
            else:
                self.set_status(400)
                self.write({"status": "error", "message": "Please provide a valid platform."})
                return
    
            sns = connect_to_sns('CreatePlatformEndpoint')
            response = yield gen.Task(sns.call, PlatformApplicationArn=platformApplicationArn, Token=token)
    
            if "Error" in response:
                logging.warning(response)
                self.set_status(400)
                self.write({"status": "error", "message": response["Error"]})
            else:
                self.set_status(200)
                self.write({"status": "ok"})
    
    def connect_to_sns(action):
        sess = botocore.session.get_session()
        sess.set_credentials(access_key='IAM_ACCESS_KEY', secret_key='IAM_SECRET_KEY')
        return Botocore(service='sns', operation=action, region_name='ap-southeast-1', session=sess)
    
[/code]

As you can see, it really does nothing other than creating a platform endpoint via CreatePlatformEndpoint. You can probably add a lot more code to make it more robust.

**_Part E: Simple Test_**

You can make use of Amazon SNS’s console to send a notification (JSON). Below is a sample that is applicable to our code so far.
[code] 
    {
     "GCM":"{\"data\":{\"message\":\" Hello world!”, \"msgcnt\":2, \"title\":\"App Notification!\”, \"action\":\"tab.somestate\"}}"
    }
    
[/code]

That’s about it! You should have Ionic receiving push notifications for Android, from Amazon SNS. I will write the iOS part once I figure it out (have not worked on it yet) :P. If you have any questions, please leave it in the comments or reach out to me [@Wysie_Soh](denied:“https://twitter.com/Wysie_Soh”) on Twitter.
