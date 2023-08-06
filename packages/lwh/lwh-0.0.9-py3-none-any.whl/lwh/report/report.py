import os
import json
from jinja2 import Environment, BaseLoader


def generate_report(input:str, output:str, template:str, result:dict = None):
    output_file = f"{os.getcwd()}/helios_report.html" if output == "." else output
    report_template = get_template(template)
    html_report = ""
    with open(input) as f:
        data = f.read()
        report_template = Environment(loader=BaseLoader).from_string(report_template)
        html_report = report_template.render(data=json.loads(data), scan_result_json=data, result=result)

    with open(output_file, "w") as report:
        report.write(html_report)



def get_template(template_arg: str):

    if template_arg is None:
        return template_string
    else:
        with open(template_arg, 'r') as file:
            return file.read()


template_string: str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <style>
        body{
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
        }

        th {font-weight: bold;}
        td { padding-right: 20px;}
        tr.heading td { font-weight: bold;;}
        .critical {background-color: #F41806;}
        .high{background-color: #F66E0A; }
        .medium{background-color: #FBBC02;}
        .low{background-color: #24B801;}
        .info{background-color: #02AEEF;}
        .fixable{background-color: green;}
        .tile{width: 30px; color: white; border-radius: 5px; text-align: center;}
        .failed{color: red}

    </style>
   
</head>
 <body>
<div class="container">

    <div class="row" style="margin-top: 70px;">
        <div class="col-md-12">

            <div style="display: inline-block; float: right;margin-top:-20px;margin-right: -20px;"><img src="https://www.lacework.com/wp-content/uploads/2019/07/Lacework_Logo_color_2019.svg" width="350px" height="150px"></div>
            <h1 style="margin-top: 23px; font-size: 30px;">{{ data['image']['image_info']['repository']}}:{{ data['image']['image_info']['tags'][0] }}</h1>
            Registry:  {{ data['image']['image_info']['registry']}}<br/>
            Scan Time:  {{ data['last_evaluation_time']}}<br/><br/>
        
        {% if result != None %}
        <hr/>
        <div>
        <div style="display: inline-block; margin-top: 25px;">
        <div style=";font-size: 18px; font-weight: bold;">Scan Result: <span class="{{result['result']}}">{{ result['result']}}</span><br/>Reason:</div>
        
            {% for r in result['reason']%}
            <div>{{r}}</div>
            {% endfor %}
            </div>
            <div style="display: inline-block; vertical-align: top; margin-left: 70px; margin-top:20px; margin-bottom:15px;"><img src="https://d33wubrfki0l68.cloudfront.net/5305a470ca0260247560b4f94daf68ed62d4a514/85ceb/img/logos/opa-no-text-color.png" height="100px" width="100px"/></div>
            <hr/>
        {% endif %}
        
        </div>

        
        </div> <!-- end col -->
    </div><!-- end row -->

    <div class="row" style="margin-top: 25px;">
        <div class="col-md-7">
            <h5>Image Details</h5>

            <table>
                <tr><td>Digest</td><td>{{ data['image']['image_info']['image_digest']}}</td></tr>
                <tr><td>ID</td><td>{{ data['image']['image_info']['image_id']}}</td></tr>
                <tr><td>Created</td><td>{{ data['image']['image_info']['created_time']}}</td></tr>
                <tr><td>Size</td><td>{{ data['image']['image_info']['size']}}</td></tr>


            </table>

        </div> <!-- end col -->

    </div><!-- end row -->

    <div class="row" style="margin-top: 75px;">
        <div class="col-md-4">
            <h5>Risk Summary - Vulnerabilities</h5> test<i class="fas fa-sort-amount-up-alt"></i>

            <table>
                <tr><td>Total</td><td style="text-align: center">{{ data['total_vulnerabilities']}}</td></tr>
                <tr><td>Fixable</td><td style="text-align: center">{{ data['fixable_vulnerabilities']}}</td></tr>
                <tr><td>Critical</td><td><div class="critical tile">{{ data['critical_vulnerabilities']}}</div></td></tr>
                <tr><td>High</td><td><div div class="high tile">{{ data['high_vulnerabilities']}}</div></td></tr>
                <tr><td>Medium</td><td><div div class="medium tile">{{ data['medium_vulnerabilities']}}</div></td></tr>
                <tr><td>Low</td><td ><div div class="low tile">{{ data['low_vulnerabilities']}}</div></td></tr>
                <tr><td>Info</td><td><div div class="info tile">{{ data['info_vulnerabilities']}}</div></td></tr>



            </table>

        </div> <!-- end col -->
        <div class="col-md-4">
            <div class="" style="margin-top: -25px">
                <canvas id="myChart" width="250" height="250"></canvas>
            </div>
        </div>
    </div><!-- end row -->

<div class="row" style="margin-top: 75px">
<div class="col-md-12">
    <div id="app"></div>
</div>
</div>


</div><!-- end container -->

<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"></script>
<script>
    var scan_result = {{ scan_result_json }}
    console.log(typeof(scan_result))
    var layers = scan_result.image.image_layers
    var ctx = document.getElementById('myChart');
    var colors = ["#F41806", "#F66E0A", "#FBBC02", "#24B801","#02AEEF"]


    //options
    var options = {
        responsive: false,
        legend: {
            display: false,
            position: "bottom",
            labels: {
                fontColor: "#333",
                fontSize: 16
            }
        }
    };


    //doughnut chart data
    var data1 = {
        labels: ["Critical", "High", "Medium", "Low", "Info"],
        datasets: [
            {
                data: [ scan_result.critical_vulnerabilities,  scan_result.high_vulnerabilities,  scan_result.medium_vulnerabilities,  scan_result.low_vulnerabilities,  scan_result.low_vulnerabilities ],
                backgroundColor: colors,
            }
        ]
    };


    //create Chart class object
    var chart1 = new Chart(ctx, {
        type: "doughnut",
        data: data1,
        options: options
    });

    function truncateString(str, num) {
        if (str.length <= num) {
            return str
        }
        return str.slice(0, num) + '...'
    }

    function getBackground(severity){
        switch (severity.color.toLowerCase()) {
            case "critical":
                return colors[0];
            case "high":
                return colors[1];
            case "medium":
                return colors[2];
            case "low":
                return colors[3];
            case "info":
                return colors[4];
            default:
                return "#fff";
        }
    }

</script>

<script src="https://cdn.jsdelivr.net/npm/@jeffthorne/lacework-razr@1.0.5/lacework-razr.min.js"></script>

</body>
</html>
"""
