
function callMapBasic(){
	
	//setting icon
	var greenIcon = L.icon({
	    iconUrl: 'leaf-green.png',
	    shadowUrl: 'leaf-shadow.png',

	    iconSize:     [38, 95], // size of the icon
	    shadowSize:   [50, 64], // size of the shadow
	    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
	    shadowAnchor: [4, 62],  // the same for the shadow
	    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
	});



	var map = L.map('map').setView([51.505, -0.09], 13);
	L.tileLayer('http://{s}.tile.cloudmade.com/8b367071a76b43f59a8db9e7bc4900ff/997/256/{z}/{x}/{y}.png', {
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
	    maxZoom: 18
	}).addTo(map);

	var marker = L.marker([51.5, -0.09]).addTo(map);

	var circle = L.circle([51.508, -0.11], 500, {
	    color: 'red',
	    fillColor: '#f03',
	    fillOpacity: 0.5
	}).addTo(map);

	var polygon = L.polygon([
	    [51.509, -0.08],
	    [51.503, -0.06],
	    [51.51, -0.047]
	]).addTo(map);

	marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();
	circle.bindPopup("I am a circle.");
	polygon.bindPopup("I am a polygon.");

	var popup = L.popup();

	function onMapClick(e) {
	    popup
	        .setLatLng(e.latlng)
	        .setContent("You clicked the map at " + e.latlng.toString())
	        .openOn(map);
	}

	map.on('click', onMapClick);


}

function callMapGeoJson(){
	var map = L.map('map').setView([39.74739, -105], 13);
	L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/22677/256/{z}/{x}/{y}.png', {
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
	    maxZoom: 18
	}).addTo(map);

	var geojsonFeature = {
	    "type": "Feature",
	    "properties": {
	        "name": "Coors Field",
	        "amenity": "Baseball Stadium",
	        "popupContent": "This is where the Rockies play!"
	    },
	    "geometry": {
	        "type": "Point",
	        "coordinates": [-104.99404, 39.75621]
	    }
	};

	L.geoJson(geojsonFeature).addTo(map);

	//var myLayer = L.geoJson().addTo(map);
	//myLayer.addData(geojsonFeature);

	var myLines = [{
	    "type": "LineString",
	    "coordinates": [[-100, 40], [-105, 45], [-110, 55]]
	}, {
	    "type": "LineString",
	    "coordinates": [[-105, 40], [-110, 45], [-115, 55]]
	}];

	var myStyle = {
	    "color": "#ff7800",
	    "weight": 5,
	    "opacity": 0.65
	};

	L.geoJson(myLines, {
	    style: myStyle
	}).addTo(map);

	var states = [{
	    "type": "Feature",
	    "properties": {"party": "Republican"},
	    "geometry": {
	        "type": "Polygon",
	        "coordinates": [[
	            [-104.05, 48.99],
	            [-97.22,  48.98],
	            [-96.58,  45.94],
	            [-104.03, 45.94],
	            [-104.05, 48.99]
	        ]]
	    }
	}, {
	    "type": "Feature",
	    "properties": {"party": "Democrat"},
	    "geometry": {
	        "type": "Polygon",
	        "coordinates": [[
	            [-109.05, 41.00],
	            [-102.06, 40.99],
	            [-102.03, 36.99],
	            [-109.04, 36.99],
	            [-109.05, 41.00]
	        ]]
	    }
	}];

	L.geoJson(states, {
	    style: function(feature) {
	        switch (feature.properties.party) {
	            case 'Republican': return {color: "#ff0000"};
	            case 'Democrat':   return {color: "#0000ff"};
	        }
	    }
	}).addTo(map);

}



function callMapGeo(){
	var freeBus = {
	    "type": "FeatureCollection",
	    "features": [
	        {
	            "type": "Feature",
	            "geometry": {
	                "type": "LineString",
	                "coordinates": [
	                    [-105.00341892242432, 39.75383843460583],
	                    [-105.0008225440979, 39.751891803969535]
	                ]
	            },
	            "properties": {
	                "popupContent": "This is free bus that will take you across downtown.",
	                "underConstruction": false
	            },
	            "id": 1
	        },
	        {
	            "type": "Feature",
	            "geometry": {
	                "type": "LineString",
	                "coordinates": [
	                    [-105.0008225440979, 39.751891803969535],
	                    [-104.99820470809937, 39.74979664004068]
	                ]
	            },
	            "properties": {
	                "popupContent": "This is free bus that will take you across downtown.",
	                "underConstruction": true
	            },
	            "id": 2
	        },
	        {
	            "type": "Feature",
	            "geometry": {
	                "type": "LineString",
	                "coordinates": [
	                    [-104.99820470809937, 39.74979664004068],
	                    [-104.98689651489258, 39.741052354709055]
	                ]
	            },
	            "properties": {
	                "popupContent": "This is free bus that will take you across downtown.",
	                "underConstruction": false
	            },
	            "id": 3
	        }
	    ]
	};

	var lightRailStop = {
	    "type": "FeatureCollection",
	    "features": [
	        {
	            "type": "Feature",
	            "properties": {
	                "popupContent": "18th & California Light Rail Stop"
	            },
	            "geometry": {
	                "type": "Point",
	                "coordinates": [-104.98999178409576, 39.74683938093904]
	            }
	        },{
	            "type": "Feature",
	            "properties": {
	                "popupContent": "20th & Welton Light Rail Stop"
	            },
	            "geometry": {
	                "type": "Point",
	                "coordinates": [-104.98689115047453, 39.747924136466565]
	            }
	        }
	    ]
	};

	var bicycleRental = {
	    "type": "FeatureCollection",
	    "features": [
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9998241,
	                    39.7471494
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 51
	        },
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9983545,
	                    39.7502833
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 52
	        },
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9963919,
	                    39.7444271
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 54
	        },
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9960754,
	                    39.7498956
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 55
	        },
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9933717,
	                    39.7477264
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 57
	        },
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9913392,
	                    39.7432392
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 58
	        },
	        {
	            "geometry": {
	                "type": "Point",
	                "coordinates": [
	                    -104.9788452,
	                    39.6933755
	                ]
	            },
	            "type": "Feature",
	            "properties": {
	                "popupContent": "This is a B-Cycle Station. Come pick up a bike and pay by the hour. What a deal!"
	            },
	            "id": 74
	        }
	    ]
	};

	var campus = {
	    "type": "Feature",
	    "properties": {
	        "popupContent": "This is the Auraria West Campus",
	        "style": {
	            weight: 2,
	            color: "#999",
	            opacity: 1,
	            fillColor: "#B0DE5C",
	            fillOpacity: 0.8
	        }
	    },
	    "geometry": {
	        "type": "MultiPolygon",
	        "coordinates": [
	            [
	                [
	                    [-105.00432014465332, 39.74732195489861],
	                    [-105.00715255737305, 39.74620006835170],
	                    [-105.00921249389647, 39.74468219277038],
	                    [-105.01067161560059, 39.74362625960105],
	                    [-105.01195907592773, 39.74290029616054],
	                    [-105.00989913940431, 39.74078835902781],
	                    [-105.00758171081543, 39.74059036160317],
	                    [-105.00346183776855, 39.74059036160317],
	                    [-105.00097274780272, 39.74059036160317],
	                    [-105.00062942504881, 39.74072235994946],
	                    [-105.00020027160645, 39.74191033368865],
	                    [-105.00071525573731, 39.74276830198601],
	                    [-105.00097274780272, 39.74369225589818],
	                    [-105.00097274780272, 39.74461619742136],
	                    [-105.00123023986816, 39.74534214278395],
	                    [-105.00183105468751, 39.74613407445653],
	                    [-105.00432014465332, 39.74732195489861]
	                ],[
	                    [-105.00361204147337, 39.74354376414072],
	                    [-105.00301122665405, 39.74278480127163],
	                    [-105.00221729278564, 39.74316428375108],
	                    [-105.00283956527711, 39.74390674342741],
	                    [-105.00361204147337, 39.74354376414072]
	                ]
	            ],[
	                [
	                    [-105.00942707061768, 39.73989736613708],
	                    [-105.00942707061768, 39.73910536278566],
	                    [-105.00685214996338, 39.73923736397631],
	                    [-105.00384807586671, 39.73910536278566],
	                    [-105.00174522399902, 39.73903936209552],
	                    [-105.00041484832764, 39.73910536278566],
	                    [-105.00041484832764, 39.73979836621592],
	                    [-105.00535011291504, 39.73986436617916],
	                    [-105.00942707061768, 39.73989736613708]
	                ]
	            ]
	        ]
	    }
	};

	var coorsField = {
	    "type": "Feature",
	    "properties": {
	        "popupContent": "Coors Field"
	    },
	    "geometry": {
	        "type": "Point",
	        "coordinates": [-104.99404191970824, 39.756213909328125]
	    }
	};




	var map = L.map('map').setView([39.74739, -105], 13);

	L.tileLayer('http://{s}.tile.cloudmade.com/{key}/22677/256/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2012 CloudMade',
		key: 'BC9A493B41014CAABB98F0471D759707'
	}).addTo(map);

	var baseballIcon = L.icon({
		iconUrl: 'baseball-marker.png',
		iconSize: [32, 37],
		iconAnchor: [16, 37],
		popupAnchor: [0, -28]
	});

	function onEachFeature(feature, layer) {
		var popupContent = "<p>I started out as a GeoJSON " +
				feature.geometry.type + ", but now I'm a Leaflet vector!</p>";

		if (feature.properties && feature.properties.popupContent) {
			popupContent += feature.properties.popupContent;
		}

		layer.bindPopup(popupContent);
	}

	L.geoJson([bicycleRental, campus], {

		style: function (feature) {
			return feature.properties && feature.properties.style;
		},

		onEachFeature: onEachFeature,

		pointToLayer: function (feature, latlng) {
			return L.circleMarker(latlng, {
				radius: 8,
				fillColor: "#ff7800",
				color: "#000",
				weight: 1,
				opacity: 1,
				fillOpacity: 0.8
			});
		}
	}).addTo(map);

	L.geoJson(freeBus, {

		filter: function (feature, layer) {
			if (feature.properties) {
				// If the property "underConstruction" exists and is true, return false (don't render features under construction)
				return feature.properties.underConstruction !== undefined ? !feature.properties.underConstruction : true;
			}
			return false;
		},

		onEachFeature: onEachFeature
	}).addTo(map);

	var coorsLayer = L.geoJson(coorsField, {

		pointToLayer: function (feature, latlng) {
			return L.marker(latlng, {icon: baseballIcon});
		},

		onEachFeature: onEachFeature
	}).addTo(map);
}

function callCloropeth(){

	var map = L.map('map').setView([37.8, -96], 4);

	var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
		key: 'BC9A493B41014CAABB98F0471D759707',
		styleId: 22677
	}).addTo(map);


	// control that shows state info on hover
	var info = L.control();

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		this._div.innerHTML = '<h4>US Population Density</h4>' +  (props ?
			'<b>' + props.name + '</b><br />' + props.density + ' people / mi<sup>2</sup>'
			: 'Hover over a state');
	};

	info.addTo(map);


	// get color depending on population density value
	function getColor(d) {
		return d > 1000 ? '#800026' :
		       d > 500  ? '#BD0026' :
		       d > 200  ? '#E31A1C' :
		       d > 100  ? '#FC4E2A' :
		       d > 50   ? '#FD8D3C' :
		       d > 20   ? '#FEB24C' :
		       d > 10   ? '#FED976' :
		                  '#FFEDA0';
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: getColor(feature.properties.density)
		};
	}

	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera) {
			layer.bringToFront();
		}

		info.update(layer.feature.properties);
	}

	var geojson;

	function resetHighlight(e) {
		geojson.resetStyle(e.target);
		info.update();
	}

	function zoomToFeature(e) {
		map.fitBounds(e.target.getBounds());
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: zoomToFeature
		});
	}

	geojson = L.geoJson(statesData, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);

	map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');


	var legend = L.control({position: 'bottomright'});

	legend.onAdd = function (map) {

		var div = L.DomUtil.create('div', 'info legend'),
			grades = [0, 10, 20, 50, 100, 200, 500, 1000],
			labels = [],
			from, to;

		for (var i = 0; i < grades.length; i++) {
			from = grades[i];
			to = grades[i + 1];

			labels.push(
				'<i style="background:' + getColor(from + 1) + '"></i> ' +
				from + (to ? '&ndash;' + to : '+'));
		}

		div.innerHTML = labels.join('<br>');
		return div;
	};

	legend.addTo(map);
}