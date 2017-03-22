var Chrome = require('chrome-remote-interface');
Chrome(function (chrome) {
    with (chrome) {
        Page.loadEventFired(function(aa){
		DOM.getDocument(function(err, resp){
			console.log(resp);
			DOM.getOuterHTML({nodeId: resp.root.nodeId}, function(err, resp){
				console.log(resp.outerHTML);
			});
			//Page.captureScreenshot({}, function(err, resp){
			//	console.log(resp.data);
			//	console.log(err);
			//});
		});
	});
        Network.enable();
        Page.enable();
        once('ready', function () {
            Page.navigate({'url': 'https://github.com'});
        });
    }
}).on('error', function () {
    console.error('Cannot connect to Chrome');
});
