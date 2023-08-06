import json
import os
import typer
from jinja2 import Environment, BaseLoader
from lwh.utils import get_template

app = typer.Typer(add_completion=False)


@app.command()
def create(input: str = typer.Option(..., help="path to Lacework scan results file"),
            output: str = typer.Option(".", help="[optional] path to store html report."),
            template: str = typer.Option(None, help="[optional] path to custom html template")):
    """
    Create a Lacework build artifact scan report.
    """
    try:
        output_file = f"{os.getcwd()}/helios_report.html" if output == "." else output
        report_template = get_template(template)
        html_report = ""
        with open(input) as f:
            data = f.read()
            report_template = Environment(loader=BaseLoader).from_string(report_template)
            html_report = report_template.render(data=json.loads(data), data_string=data)

        with open(output_file, "w") as report:
            report.write(html_report)

    except Exception as ex:
        print(ex)
