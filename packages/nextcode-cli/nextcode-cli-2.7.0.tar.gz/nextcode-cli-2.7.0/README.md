# NextCODE Command Line Interface

- [Requirements](#requirements)
- [Installation](#installation)
  * [End-user installation](#end-user-installation)
  * [Developer installation](#developer-installation)
  * [Set up a service profile](#set-up-a-service-profile)
    + [Create a service profile](#create-a-service-profile)
    + [Running the CLI for the first time](#running-the-cli-for-the-first-time)
- [Releasing](#releasing)

# Requirements
 * Python 3.7

# Installation

## End-user installation
To install the package you have to run the following command:
```bash
$ pip3 install nextcode-cli -U
```

To verify that the installation was successful you can run the following command:
```bash
$ nextcode version
nextcode-cli/x.y.z (yyyy.mm.dd)
```

## Developer installation
Start by pulling the sourcecode from git (usually from develop to be on the bleeding edge).

There are two ways to set up the CLI. We recommend trying to install it into your system python in `develop` mode by simply running the following command in the nextcode-cli folder (depending on your system setup you might need `sudo`)
```bash
$ pip3 install -e .
```

If you get any errors you can set up a local virtualenv in the nextcode-cli path:
```bash
$ source ./setup.sh
$ pip3 install -e .
```
Using this method means that you will always need to do `source ./setup.sh` to enter the virtualenv before using the tool, so we would recommend getting the first method to work unless you intend on make edits to the code yourself.

## Set up a service profile
### Create a service profile
For any work to happen a service profile must be defined. One example is the one here below, which is Platform Dev test specific. For QA purposes this is of course **test environment dependent**!:

The command is:
```bash
$ nextcode profile add <profile-name>
```

Follow the prompts to enter a server name and then log in through the browser window that opens up.

You can also set up the profile without a prompt like this:
```bash
$ nextcode profile add <profile-name> --domain=mydomain.wuxinextcode.com --api-key=<key>
```

### Running the CLI for the first time

Once your installation has succeeded you can run the following command anywhere in your system:
```bash
nextcode status
```
Once you finish the authentication process you should be able to view workflow jobs:
```bash
nextcode workflow jobs
```

To start familiarizing yourself with the sdk you can use the --help option on all commands to see detailed information about their use.
```bash
$ nextcode --help
Usage: nextcode [OPTIONS] COMMAND [ARGS]...

  A utility for interfacing with WuXi Nextcode services.

  This tool allows you to communicate with the pipelines service, CSA,
  workflow service and GOR Query API. For all usage you will need to
  authenticate against the specific service profile you are using.

  Please look at the subcommands below for details.

Options:
  -v, --verbose [warning|error|info]
                                  Output logs for debugging
  -p, --profile TEXT              Use a specific profile for this command
  --help                          Show this message and exit.

Commands:
  csa_authenticate  Authenticate against CSA (for import).
  import            Import a TSV manifest into CSA.
  keycloak          Manage keycloak users Requires the keycloak admin...
  login             Authenticate against keycloak.
  pipelines         Root subcommand for pipelines functionality
  profile           Configure server profile to use.
  query             Root subcommand for query api functionality
  token             Print out an access token for the current profile
  version           Show the Nextcode CLI version.
  workflow          Root subcommand for workflow functionality

$ nextcode workflow --help
Usage: nextcode workflow [OPTIONS] COMMAND [ARGS]...

  Root subcommand for workflow functionality

Options:
  --help  Show this message and exit.

Commands:
  job        View or manage individual jobs.
  jobs       List jobs
  pipelines  List pipelines
  projects   List projects
  run        Start a new nextflow job.
  smoketest  Run a smoketest of the workflow service
  status     Show the status of the workflow service
```

# Releasing
* Bump version and update the a date in [nextcodecli/VERSION](nextcodecli/VERSION)
* Merge to master
* Tag in Gitlab
* Watch the CI fireworks. 
