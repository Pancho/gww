var GWW = (function () {
	var r = {
		frontCheckChrome: function () {
			if (!u.isOnChrome()) {
				$('#gww-main-speedtracer ol').find('li').remove().end().append('<li><h3>You need to <strong>open</strong> or install Google Chrome and open this page in that browser.</h3><a class="button" href="http://www.google.com/chrome">Install Google Chrome</a></li>');
			}
		},
		frontPerformTests: function () {
			$('#gww-main-start').off().on('click', function (ev) {
				var startButton = $(this);
				$.get('/api/tests', {}, function (data) {
					var win = null;
					var i = 0, j = data.pages.length, windows = [];
					for (; i < j; i += 1) {
						try {
							win = window.open('http://' + data.meta.domain + '/test/' + data.pages[i].slug, 'test_' + data.pages[i].page, 'height=1000, width=1500, menubar=no, toolbar=no, location=no, status=no')
							$(win).trigger('blur');
							windows.push(win);

							startButton.text('Stop tests').off().on('click', function (event) {
								var k = 0, l = windows.length;
								startButton.text('Start Measuring');
								event.preventDefault();
								for (; k < l; k += 1) {
									windows[k].name = windows[k].name + '_close';
								}
								r.frontPerformTests();
							})
						} catch (e) {
							console.log(e);
						}
					}
				}, 'json');
			});
		},
		closeInertWindows: function () {
			$('#gww-close-test-window').on('click', function (ev) {
				ev.preventDefault();
				window.close();
			});
		}
	}, u = {
		isOnChrome: function () {
			return navigator.userAgent.indexOf('Chrome/') > -1;
		},
		initialize: function () {
			r.frontCheckChrome();
			r.frontPerformTests();
			r.closeInertWindows();
		}
	};
	return u.initialize();
})();