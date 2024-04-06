ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map('map', {
        center: [55.755814, 37.617635],
        zoom: 10
    });

    var placemark = new ymaps.Placemark([55.755814, 37.617635], {}, {
        draggable: true
    });

    myMap.geoObjects.add(placemark);

    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        placemark.geometry.setCoordinates(coords);
    });
    document.getElementById('getCoordsButton').addEventListener('click', function() {
        var placemarkCoords = placemark.geometry.getCoordinates();
        console.log('Координаты метки:', placemarkCoords);
    });
}