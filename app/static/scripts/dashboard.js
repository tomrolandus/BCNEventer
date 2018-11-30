var mymap;
recommendedEvents = [];

window.onload = function () {

    // ADD THE MAP
    mymap = L.map('mapid').setView([41.3851, 2.1734], 13);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1Ijoic3R1ZmkwNCIsImEiOiJjam9yOTA0cWcwYzRmM3Bsa24zNzljZTkxIn0.9c2kk60e1nZdk247eAQQng'
    }).addTo(mymap);

    // ADD MARKERS
    recommendedEvents.forEach(function(recommendedEvent,index) {
        var marker = L.marker([recommendedEvent.lat, recommendedEvent.long]).addTo(mymap);
        marker.bindPopup(recommendedEvent.name);
        marker.on('mouseover', function (e) {
            this.openPopup();
        });
        marker.on('mouseout', function (e) {
            this.closePopup();
        });
        marker.on('click', function(e) {
            $('.slider').slick('slickPause');
            $('.slider').slick('slickGoTo', index);
        });
    });

}

// SAVE RECOMMENDED EVENTS
function addRecommendedEvent(lat, long, name) {
    var recommendedEvent = {lat: lat, long: long, name: name};
    recommendedEvents.push(recommendedEvent);
}

// initialize slick slider
$(document).ready(function(){
  $('.slider').slick({
      infinite: true,
      arrows: true,
      dots: true,
      autoplay: true,
      autoplaySpeed: 2000,
  });
});