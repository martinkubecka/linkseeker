<p align="center">
<img src="https://github.com/martinkubecka/linkseeker/blob/main/docs/banner.png" alt="Logo">
<p align="center"><b>Extract all hyperlinks from the website source code after javascript is loaded.</b><br>
</p>

---
<h2 id="table-of-contents">Table of Contents</h2>

- [Pre-requisites](#notebook_with_decorative_cover-pre-requisites)
  - [Installing Required Packages](#package-installing-required-packages)
  - [Firefox (gecko) driver](#fox_face-firefox-gecko-driver)
- [Usage](#knife-usage)
- [Development](#toolbox-development)
  - [Virtual environment](#office-virtual-environment)

---
## :notebook_with_decorative_cover: Pre-requisites

- clone this project with the following command

```
$ git clone https://github.com/martinkubecka/linkseeker.git
```

### :package: Installing Required Packages

```
$ pip install -r requirements.txt
```

### :fox_face: Firefox (gecko) driver

1. download the latest release of **geckodriver** from https://github.com/mozilla/geckodriver/releases
2. extract the file
3. make the file executable
4. move the **geckodriver** to the `/usr/local/bin/` directory  

```
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.*.*/geckodriver-v0.*.*-linux64.tar.gz
$ tar -xvzf geckodriver* 
$ chmod +x geckodriver
$ sudo mv geckodriver /usr/local/bin/
```

---
## :knife: Usage

```
usage: linkseeker.py [-h] [-q] [-p] [-o FILENAME] URL

Extract all hyperlinks from the website source code after javascript is loaded.

positional arguments:
  URL                             target website URL

options:
  -h, --help                      show this help message and exit
  -q, --quiet                     do not print banner
  -p, --print                     print extracted links to console
  -o FILENAME, --output FILENAME  output file for extracted links (default: extracted_links.txt)
```

---
## :toolbox: Development

### :office: Virtual environment

1. use your package manager to install `python-pip` if it is not present on your system
3. install `virtualenv`
4. verify installation by checking the `virtualenv` version
5. inside the project directory create a virtual environment called `venv`
6. activate it by using the `source` command
7. you can deactivate the virtual environment from the parent folder of `venv` directory with the `deactivate` command

```
$ sudo apt-get install python-pip
$ pip install virtualenv
$ virtualenv --version
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ deactivate
```

---

<div align="right">
<a href="#table-of-contents">[ Table of Contents ]</a>
</div>