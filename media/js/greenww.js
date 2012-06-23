var GWW = (function () {
	var r = {
		frontCheckChrome: function () {
			if (!u.isOnChrome()) {
				$('#gww-main-speedtracer ol').find('li').remove().end().append('<li><h3>You need to <strong>open</strong> or install Google Chrome and open this page in that browser.</h3><a class="button" href="http://www.google.com/chrome">Install Google Chrome</a></li>');
			}
		},
		frontPerformTests: function () {

		},
		closeInertWindows: function () {
			$('#gww-close-test-window').on('click', function (ev) {
				ev.preventDefault();
				window.close();
			});
		},
		markUser: function () {
			if (u.isOnChrome()) {
				if (localStorage) {
					if (!localStorage.getItem('gww-mark-browser')) {
						localStorage.setItem('gww-mark-browser', Math.uuid(25));
					}
				}
			}
		},
		displayBundleCharts: function () {
			var placeholder = $('.gww-bundle-graph'), bundleId = '', browserId = localStorage.getItem('gww-mark-browser');

			if (placeholder.length) {
				bundleId = placeholder.attr('id').replace(/gww-bundle-results-/, ''); // Only here we really know there's a chance that the id exists

				if (bundleId) {
					if (browserId) {
						$.get('/api/results/bundle/' + bundleId + '/' + browserId + '/', {}, function (resultsData) {
							google.setOnLoadCallback(drawChart);
							function drawChart () {
								var i = 0, j = resultsData.charts.length, charts = [resultsData.columns];

								for (; i < j; i += 1) {
									charts.push(resultsData.charts[i]);
								}
								var data = google.visualization.arrayToDataTable(charts);

								var options = {
									title: resultsData.title,
									height: 600,
									hAxis: {title: 'Tests', titleTextStyle: {color: 'red'}}
								};

								var chart = new google.visualization.ColumnChart(placeholder.get(0));
								chart.draw(data, options);
							}
						});
					} else {
						placeholder.before($('<p class="gww-error">Error drawing chart. Could not identify your browser or you haven\'t performed any tests yet.</p>'));
					}
				} else {
					placeholder.before($('<p class="gww-error">Error drawing chart. Could not find bundle in database.</p>'));
				}
			}
		},
		displayTextLightbox: function () {
			$('.gww-text-lgihtbox').on('click', function (ev) {
				ev.preventDefault();
			});
		},
		fixEmails: function () {
			$('.gww-email').each(function (i, elm) {
				elm = $(elm);
				elm.attr('href', elm.attr('href').replace(' | a t | ', '@'));
				elm.text(elm.text().replace(' | a t | ', '@'));
			})
		}
	}, u = {
		isOnChrome: function () {
			return navigator.userAgent.indexOf('Chrome/') > -1;
		},
		initialize: function () {
			r.frontCheckChrome();
			r.frontPerformTests();
			r.closeInertWindows();
			r.markUser();
			r.displayBundleCharts();
			r.displayTextLightbox();
			r.fixEmails();
		}
	};
	return u.initialize();
})();