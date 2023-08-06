# `Lacework Helios cli`

Create a Lacework build artifact scan report.

**Usage**:


**Options**:

* `--input TEXT`: path to Lacework scan results file  [required]
* `--output TEXT`: [optional] path to store html report.  [default: .]
* `--template TEXT`: [optional] path to custom html template
* `--help`: Show this message and exit.

**Usage**:
```console
lwh [OPTIONS] COMMAND [ARGS]...
```

**Options**:
*  `--help  Show this message and exit.`

**Commands**:<br/>
*  `opa     Validate Scan Results against OPA policy`
*  `report  Create a Lacework build artifact scan report`



<br/><br/>
### Installation
`pip install lwh`

### Custom Reports
If you're interested in customizing the report check out the sample template in the examples folder.
lwh cli simply renders the scan results json object to any provided template as {{ scan_result_json }}.
You also have access to a python dictionary {{ data }} as a convenience object if using jinja. If using opa integration
policy decision is also passed to report as {{result}}. You don't need to use React or Jinja. Feel free to use your 
existing tool chain.<br/><br/>

From here the [lacework-razr](https://github.com/jeffthorne/lacework-razr) React components take over. But they don't have to. 
Feel free to customize or get in touch if you need any changes.
