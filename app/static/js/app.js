function formToJSON(form) {
  return form.serializeArray().reduce(function(obj, item) {
    obj[item.name] = item.value;
    return obj;
  }, {});
}

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10);
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}


var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
  socket.emit('connected', {data: 'Still connected'});
});

socket.on('pong', function() {
  socket.emit('ping', {data: 'Still connected'});
});


socket.on('update', function(data) {
  update(JSON.parse(data));
});

socket.on('checkServices', function(data) {
  setServiceStatuses(JSON.parse(data));
});

socket.on('setInterface', function(response) {
  showAlertMessage(JSON.parse(response));
});

socket.on('setAccessPoint', function(response) {
  json = JSON.parse(response);
  setSSID(json.ssid);
  showAlertMessage(json);
});

socket.on('clientData', function(data) {
  json = JSON.parse(data);
  editClientsTable(json.apclients);
  setClientConnections(Object.keys(json.apclients).length);
});


function editClientsTable(clientData) {
  console.log(clientData);

  var tableRef = document.getElementById("clientsTable");
  for(var key in json.apclients) {
    var newRow = tableRef.insertRow();
    var mac = newRow.insertCell();
    var vendor = newRow.insertCell();
    var connTime = newRow.insertCell();
    var rx = newRow.insertCell();
    var tx = newRow.insertCell();

    mac.appendChild(document.createTextNode(key));
    vendor.appendChild(document.createTextNode(json.apclients[key].vendor));
    connTime.appendChild(document.createTextNode(json.apclients[key].ctime.toHHMMSS()));
    rx.appendChild(document.createTextNode(json.apclients[key].rx));
    tx.appendChild(document.createTextNode(json.apclients[key].tx));
  }
}

function setClientConnections(number) {
  $("#numOfClients").text(number);
}


function setSSID(ssid) {
  $("#SSIDName").text(ssid);
}

function setServiceStatuses(json) {
  $("#hostapd-status").find("i").toggleClass("service-online", json.hostapd);
  $("#dnsmasq-status").find("i").toggleClass("service-online", json.dnsmasq);
  $("#ap-ssid-status").find("i").toggleClass("service-online", json.apssid);
}


function showAlertMessage(response) {
  if(response.success) {
    $("#alertMessage").addClass("alert-success");
    $("#alertMessageContent").html("<strong>Success.</strong> " + response.data);
  }
  else {
    $("#alertMessage").addClass("alert-danger");
    $("#alertMessageContent").html("<strong>Error.</strong> " + response.data);
  }

  $("#alertMessage").slideToggle("fast", function() {
    $(this).delay(5000).slideToggle("fast");
  });
}

$("#InterfaceForm").submit(function( event ) {
  formData = formToJSON($("#InterfaceForm"));
  socket.emit('setInterfaces', formData);
  event.preventDefault();
});

$("#APForm").submit(function( event ) {
  formData = formToJSON($("#APForm"));
  socket.emit('setAccessPoint', formData);
  event.preventDefault();
});


function update(data) {

  // graph.setTitle({text: data.time});

  $("#version").text(data.version);
  $("#time").text(data.time);
}


function create_graph() {

  return Highcharts.chart('graph_container', {
    chart: {
      events: {
        load: function () {
          var series = this.series[0];
          count = 0;
          socket.on('update', function (sample) {
            count += 1;
            data = [0 + count, 1 + count, 2 + count, 3 + count, 4 + count, 5 + count, 6];
            series.setData(data);
          });

          socket.on('chart_data', function (sample) {
            //add chart data to series
            series.addPoint([sample.x, sample.y], true, false);
          });
        }
      }
    },
    title: {
      text: 'Live random data'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150
    },
    yAxis: {
      title: {
        text: 'Value'
      },
      plotLines: [{
        value: 0,
        width: 1,
        color: '#808080'
      }]
    },
    tooltip: {
      formatter: function () {
        return '<b>' + this.series.name + '</b><br/>' +
        Highcharts.dateFormat('%H:%M:%S', this.x) + '<br/>' +
        Highcharts.numberFormat(this.y, 2);
      }
    },
    legend: {
      enabled: false
    },
    exporting: {
      enabled: false
    },
    series: [{
      name: 'Random data',
      data: []
    }]
  });
}
