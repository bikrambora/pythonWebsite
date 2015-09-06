var chart1 = function() {
    $.get("Graphs/graph1.csv", function(csv) {
        $("#graph1").highcharts({
            chart: {
                type: "bar"
            },
            data: {
                csv: csv
            },
            title: {
                text: "Cancers by sex"
            },
            yAxis: {
                title: {
                    text: "People"
                }
            }
        });
    });
}
    
var chart2 = function() {
    $.get("Graphs/graph2.csv", function(csv) {
        $("#graph2").highcharts({
            chart: {
                type: "bar"
            },
            data: {
                csv: csv
            },
            title: {
                text: "Cancer by Nature"
            },
            yAxis: {
                title: {
                    text: "People"
                }
            }
        });
    });
}
    
var chart3 = function() {
    $.get("Graphs/graph3.csv", function(csv) {
        $("#graph3").highcharts({
            chart: {
                type: "column"
            },
            data: {
                csv: csv
            },
            title: {
                text: "Prostate cancer by year"
            },
            yAxis: {
                title: {
                    text: "People"
                }
            }
        });
    });
}
    
var chart4 = function() {
    $.get("Graphs/graph4.csv", function(csv) {
        $("#graph4").highcharts({
            chart: {
                type: "column"
            },
            data: {
                csv: csv
            },
            title: {
                text: "Lung cancer by year"
            },
            yAxis: {
                title: {
                    text: "People"
                }
            }
        });
    });
}
    
var chart5 = function() {
$('#graph5').highcharts({
    chart: {
      type: 'pie',
    },
    credits: false,
    title: {
      text: "Percentage of cancer diagnosises by sex"
    },
     tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
      series: {
        dataLabels: {
          enabled: true
        },
        showInLegend: false
      }
    },
    series: [{
      name: 'Cancer by sex',
      colorByPoint: true,
      data: [
                ['Male', 68],
                ['Female', 32]
            ]
    }],
  });
}
    
var pivot_graph = function() {
    $.get("Graphs/data.csv", function(csv) {
        $("#container").highcharts({
            chart: {
                type: "bar"
            },
            data: {
                csv: csv
            },
            title: {
                text: "Cancer Data"
            },
            yAxis: {
                title: {
                    text: "Number Of Cases"
               }
            }
        });
    });
}
    
var main = function(){
    chart1();
    chart2();
    chart3();
    chart4();
    chart5();
    pivot_graph();
}
    
$(document).ready(main);