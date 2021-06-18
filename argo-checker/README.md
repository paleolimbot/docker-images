
# argo-checker

Wraps the latest version of the [Ifremer Argo NetCDF file checker](https://doi.org/10.17882/45538) as a Docker image.

As a command-line utility:

``` bash
# once:
# docker pull paleolimbot/argo-checker
docker run --rm paleolimbot/argo-checker check \
    https://data-argo.ifremer.fr/dac/meds/4902533/profiles/R4902533_001.nc
```

    Searching for installed tool in '/argo-checker'
    Installed tool found at '/argo-checker/tool_83774'.
    Downloading <https://data-argo.ifremer.fr/dac/meds/4902533/profiles/R4902533_001.nc>
    Running 'java -cp ./resources:./jar/formatcheckerClassic-1.17-jar-with-dependencies.jar -Dapplication.properties=application.properties -Dfile.encoding=UTF8 oco.FormatControl /tmp/tmps3u3zn3eR4902533_001.nc'

    <?xml version="1.0"?>
    <coriolis_function_report>
        <function>CO-03-08-03</function>
        <comment>Control file data format</comment>
        <date>18/06/2021 19:14:08</date>
        <application_version>1.17</application_version>
        <netcdf_file>/tmp/tmps3u3zn3eR4902533_001.nc</netcdf_file>
        <rules_file>Argo_Prof_c_v3.1_AUM_3.1_20201104.xml</rules_file>
        <title>Argo float vertical profile</title>
        <user_manual_version>3.1</user_manual_version>
        <data_type>Argo profile</data_type>
        <format_version>3.1</format_version>
        <file_error>The variable "LATITUDE" is not correct: attribute "reference" forbidden</file_error>
        <file_error>The variable "LATITUDE" is not correct: attribute "coordinate_reference_frame" forbidden</file_error>
        <file_error>The variable "LONGITUDE" is not correct: attribute "reference" forbidden</file_error>
        <file_error>The variable "LONGITUDE" is not correct: attribute "coordinate_reference_frame" forbidden</file_error>
        <file_error>The optional variable "PRES" is not correct: attribut "coordinate_reference_frame" forbidden</file_error>
        <file_error>The value of the attribute of variable "PRES_ADJUSTED:axis" is not correct: "Z" expected</file_error>
        <file_compliant>no</file_compliant>
        <status>ok</status>
    </coriolis_function_report>

You can also use the 'argo-checker.py' Python file, which will work as long as you have `java` installed and on your PATH.

``` bash
python argo-checker.py --help
```

    usage: argo-checker.py [-h] [--update] [--force] [--quiet] {check,serve} [files_or_urls [files_or_urls ...]]

    Run, serve, or upgrade the Ifremer NetCDF file format checker for Argo floats <https://doi.org/10.17882/45538>.

    positional arguments:
    {check,serve}  Use 'check' to export XML to stdout based on 'files' and 'serve' to serve a minimal web-based interface.
    files_or_urls  Zero or more files or URLs if 'action' is 'check'

    optional arguments:
    -h, --help     show this help message and exit
    --update       Update to the latest distributed version of the tool before running 'action'
    --force        Reinstall even if tool is at latest version.
    --quiet        Suppress status messages.
