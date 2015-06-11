
var app = angular.module('myApp', []);
app.controller('customersCtrl', function($scope, $http) {
	console.log("asdfasfsadf");
    $http.get("http://54.173.157.204/appindex/")
    .success(function(response) {
    	console.log("here");
    	//$scope.names = response.records;
    });
});


/*static SocketIOClient *static_socket;

+(NSString*)getWebsiteURL
{
    return @"http://54.173.157.204/appindex/";
}

+(NSArray*) getUpcomingEvents
{
    __block NSArray *eventD;
    __block BOOL returned;
    NSURLSession *defaultSession = [NSURLSession sharedSession];
    
    NSURL * url = [NSURL URLWithString:[SDSAPI getWebsiteURL]];
    NSURLSessionDataTask *dataTask = [defaultSession dataTaskWithURL:url
                                                   completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                                       if(error == nil)
                                                       {
                                                           eventD = [NSJSONSerialization JSONObjectWithData:data
                                                                                                    options:kNilOptions
                                                                                                      error:&error];
                                                           for(NSDictionary *item in eventD) {
                                                               NSLog (@"nsdic = %@", item);
                                                           }
                                                           returned = TRUE;
                                                       }
                                                   }];
    [dataTask resume];
    returned = FALSE;
    while(returned == FALSE){
        [NSThread sleepForTimeInterval:0.1f];
    }
    return eventD;
}

+(void) login:(NSString*)username password:(NSString*)pass ID:(id)callingViewController
{
    // at the top
    static NSString *csrf_cookie;
    
    // in a function:
    NSURL *url = [[NSURL alloc] initWithString:@"http://54.173.157.204/"];
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url];
    [request setHTTPShouldHandleCookies:YES];
    
    [request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:[[NSHTTPCookieStorage sharedHTTPCookieStorage] cookiesForURL:url]]];
    
    // make GET request are store the csrf
    [NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue]
                           completionHandler:^(NSURLResponse *response, NSData *data, NSError *connectionError) {
                               NSArray *cookies = [NSHTTPCookie cookiesWithResponseHeaderFields:[(NSHTTPURLResponse *)response allHeaderFields] forURL:url];
                               [[NSHTTPCookieStorage sharedHTTPCookieStorage] setCookies:cookies forURL:url mainDocumentURL:nil];
                               // for some reason we need to re-store the CSRF token as X_CSRFTOKEN
                               for (NSHTTPCookie *cookie in cookies) {
                                   if ([cookie.name isEqualToString:@"csrftoken"]) {
                                       csrf_cookie = cookie.value;
                                       NSLog(@"cookie.value=%@", cookie.value);
                                       break;
                                   }
                               }
                               NSString* urlString = @"http://54.173.157.204/auth/loginViewiOS/";
                               NSURL *url = [NSURL URLWithString:urlString];
                               
                               NSMutableURLRequest *urlRequest = [NSMutableURLRequest requestWithURL:url];
                               [urlRequest setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:[[NSHTTPCookieStorage sharedHTTPCookieStorage] cookiesForURL:url]]];
                               [urlRequest addValue:csrf_cookie forHTTPHeaderField:@"X_CSRFTOKEN"];
                               [urlRequest setHTTPMethod:@"POST"];
                               NSString* bodyData = [NSString stringWithFormat:@"username=%@&password=%@", username, pass];
                               [urlRequest setHTTPBody:[NSData dataWithBytes:[bodyData UTF8String] length:strlen([bodyData UTF8String])]];
                               NSOperationQueue *queue = [[NSOperationQueue alloc] init];
                               
                               [NSURLConnection sendAsynchronousRequest:urlRequest queue:queue completionHandler:^(NSURLResponse *response, NSData *data, NSError *error)
                                {
                                    NSString *responseString = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
                                    if ([responseString  isEqual: @"successful_login"]) {
                                        [callingViewController performSelectorOnMainThread:@selector(loginReturnedTrue) withObject:nil waitUntilDone:NO];
                                    }
                                    else{
										[callingViewController performSelectorOnMainThread:@selector(loginReturnedFalse) withObject:nil waitUntilDone:NO];
                                    }
                                }];
                           }];
}
//+(void) mixes ID:(id)callingViewController
//{
//}
+(void) signup:(NSString*)username password:(NSString*)pass email:(NSString*)email ID:(id)callingViewController
{
	// at the top
	static NSString *csrf_cookie;
	
	// in a function:
	NSURL *url = [[NSURL alloc] initWithString:@"http://54.173.157.204/"];
	NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url];
	[request setHTTPShouldHandleCookies:YES];
	
	[request setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:[[NSHTTPCookieStorage sharedHTTPCookieStorage] cookiesForURL:url]]];
	
	// make GET request are store the csrf
	[NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue]
						   completionHandler:^(NSURLResponse *response, NSData *data, NSError *connectionError) {
							   NSArray *cookies = [NSHTTPCookie cookiesWithResponseHeaderFields:[(NSHTTPURLResponse *)response allHeaderFields] forURL:url];
							   [[NSHTTPCookieStorage sharedHTTPCookieStorage] setCookies:cookies forURL:url mainDocumentURL:nil];
							   // for some reason we need to re-store the CSRF token as X_CSRFTOKEN
							   for (NSHTTPCookie *cookie in cookies) {
								   if ([cookie.name isEqualToString:@"csrftoken"]) {
									   csrf_cookie = cookie.value;
									   NSLog(@"cookie.value=%@", cookie.value);
									   break;
								   }
							   }
							   NSString* urlString = @"http://54.173.157.204/auth/createprofileiOS/";
							   NSURL *url = [NSURL URLWithString:urlString];
							   
							   NSMutableURLRequest *urlRequest = [NSMutableURLRequest requestWithURL:url];
							   [urlRequest setAllHTTPHeaderFields:[NSHTTPCookie requestHeaderFieldsWithCookies:[[NSHTTPCookieStorage sharedHTTPCookieStorage] cookiesForURL:url]]];
							   [urlRequest addValue:csrf_cookie forHTTPHeaderField:@"X_CSRFTOKEN"];
							   [urlRequest setHTTPMethod:@"POST"];
							   
							   AppDelegate* appDelegate = [[UIApplication sharedApplication]delegate];
							   
							   NSString* bodyData = [NSString stringWithFormat:@"username=%@&password=%@&email=%@&mixpanel_distinct_id=%@", username, pass, email, appDelegate.mixpanel.distinctId];
							   [urlRequest setHTTPBody:[NSData dataWithBytes:[bodyData UTF8String] length:strlen([bodyData UTF8String])]];
							   NSOperationQueue *queue = [[NSOperationQueue alloc] init];
							   
							   [NSURLConnection sendAsynchronousRequest:urlRequest queue:queue completionHandler:^(NSURLResponse *response, NSData *data, NSError *error)
								{
									NSString *responseString = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
									
									if ([responseString  isEqual: @"True"]) {
										[callingViewController performSelectorOnMainThread:@selector(signupSuccess) withObject:nil waitUntilDone:NO];
									}
									else{
										[callingViewController performSelectorOnMainThread:@selector(signupFailure:) withObject:responseString waitUntilDone:NO];
									}
								}];
						   }];
}
*/