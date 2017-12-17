/*
Boilerplate Python 3 SocketIO Flask app
*/

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


graph = create_graph();


function update(data) {
    graph.setTitle({text: data.time});
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
