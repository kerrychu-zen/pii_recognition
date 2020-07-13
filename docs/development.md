# Setting Up a Development Environment


## Table of contents

1. [Installing the Zendesk App Tools (ZAT)](#dev-zat)
2. [Setting up the Python environment](#dev-python)
3. [Lauching the Flask app](#dev-flask)
4. [Having browser connected to the Zendesk Support instance](#dev-instance)


## Installing the Zendesk App Tools (ZAT) <a name='dev-zat'></a>
ZAT is the bridge that enables bi-directional communications between your local (or remote) app and your Zendesk product instance.

Tog get it running, first you must install Ruby as ZAT is a Ruby gem.

Then, install `rake` a build automation tool.
```sh
gem install rake
```

Next, install ZAT
```sh
gem install zendesk_apps_tools
```

In the project structure, navigate to **app_local** directory, this directory contains all necessary files for any ZAT commands to run. Here, start a local HTTP server talking to your Zendesk instance.
``` sh
zat server
```

If you want to customise anything the ZAT service, use **manifest.json** file. This file specifies one or more locations in one or more Zendesk products. We are building a Support app and will serve this app at `localhost:8080/sidebar`.
```
...

  "location": {
    "support": {
      "ticket_sidebar": "http://127.0.0.1:8080/sidebar"
    }
  },

...

```

## Setting up the Python environment <a name='dev-python'></a>
Install Python 3.7 and then `poetry` package. `poetry` is a dependency management tool. If you have multiple Pythons running, I recommend `pyenv` for version management.
```
pip install --user poetry
```
Install ML libraries and Flask dependencies using `poetry`. Make sure the installation happens in the root directory.
```sh
poetry install
```
Activate the virtual environment and use commands starting a poetry shell.
```
poetry shell
```

## Launching the Flask app <a name='dev-flask'></a>
Run the application on localhost at port 8080 under directory `app_remote`.
```sh
flask run -p 8080
```

## Having a browser connecting to the Zendesk Support instance <a name='dev-instance'></a>
Open your favorite browser and type `https://z3n-numbat-piiredaction.zendesk.com/` in the location bar and hit Enter! You are now in the Support instance. Append `?zat=true` to the page url and open a ticket now you shall be seeing the app running in the sidebar. Or you may have to ask @gabechu for access to the instance.

## Troubleshooting
- Is your ZAT server running?
- Is your Flask app running at port 8080?
- Have you connected to the correct instance at `https://z3n-numbat-piiredaction.zendesk.com/`?
- Have you appended to append `?zat=true` to the page url?
- Getting troubles installing ZAT [page](https://develop.zendesk.com/hc/en-us/articles/360001075048-Installing-and-using-the-Zendesk-apps-tools) for details.