import json
import sys
import requests
import typer
import urllib3
from loguru import logger
from lwh.report.report import generate_report


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{level}</green>:     <light-blue>{message}</light-blue>")
app = typer.Typer(add_completion=False)


@app.command()
def report(input: str = typer.Option(..., help="path to Lacework scan results file"),
            output: str = typer.Option(".", help="[optional] path to store html report."),
            template: str = typer.Option(None, help="[optional] path to custom html template")):
    """
    Create a Lacework build artifact scan report.
    """
    try:
        generate_report(input, output, template)

    except Exception as ex:
        print(ex)


@app.command()
def opa(url: str = typer.Option(..., help="URL to OPA server"),
        input: str = typer.Option(..., help="path to Lacework scan results file"),
        output: str = typer.Option(".", help="[optional] path to store html report."),
        template: str = typer.Option(None, help="[optional] path to custom html template")):
    """
       Validate Scan Results agains OPA policy
   """
    try:

        with open(input) as f:
            scan_result = f.read()
            resp = requests.post(f"{url}/v1/data/lacework/helios_image_result", json=dict(input=json.loads(scan_result)), verify=False)
            opa_result = resp.json()
            result = 'failed' if opa_result['result']['allowed'] == False else 'passed'
            logger.info( f"Lacework Image Assuance [RESULT]: {result} [REASON] {opa_result['result']['reason']}")

            generate_report(input, output, template, result=dict(result=result, reason=opa_result['result']['reason'] ))
            if result == 'failed':
                sys.exit(1)

            sys.exit(0)

    except Exception as ex:
        print(ex)



if __name__ == "__main__":
    app()