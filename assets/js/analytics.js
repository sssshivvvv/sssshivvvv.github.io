// Google Analytics 4 (GA4)
// Measurement ID for the "Web" data stream (https://sssshivvvv.github.io).
// To change it, grab the G-XXXXXXXXXX id from https://analytics.google.com (Admin -> Data streams) and paste it here.
var GA_MEASUREMENT_ID = 'G-ESPXWGZ8RH';

(function () {
  // Stay dormant if no real id has been set.
  if (!GA_MEASUREMENT_ID || GA_MEASUREMENT_ID === 'G-XXXXXXXXXX') return;
  // Only track on the live site -- keeps localhost / preview visits out of your stats.
  if (location.hostname !== 'sssshivvvv.github.io') return;

  var loader = document.createElement('script');
  loader.async = true;
  loader.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(loader);

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_MEASUREMENT_ID);
})();
