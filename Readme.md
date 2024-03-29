# Daily Tech Brief Bot

For those of us who are always in a rush and on the go but want to stay up to date on all things tech! Uses the emails from the popular TLDR email server and provides text summaries to super short reads on the go.


## Setup and Installation

This section guides you through setting up your project environment and installing all necessary dependencies.

### Prerequisites

- Python 3.x installed on your system
- Basic knowledge of terminal or command line

### Step 1: Create a Virtual Environment

Creating a virtual environment for your project is crucial for managing dependencies separately from your other Python projects.

1. **Open your Terminal** and navigate to your project's directory, or create a new one if it doesn't exist:

    ```bash
    mkdir my_project
    cd my_project
    ```

2. **Create the virtual environment** by running:

    ```bash
    python3 -m venv venv
    ```

    This command creates a directory named `venv` in your project folder, which will contain the Python executable and libraries.

3. **Activate the virtual environment**:

    - On macOS or Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows (using Command Prompt):

        ```cmd
        .\venv\Scripts\activate
        ```

    You should now see `(venv)` at the beginning of your terminal line, indicating that the virtual environment is active.

### Step 2: Install Necessary Libraries

With your virtual environment activated, install the necessary libraries for your project:


pip install beautifulsoup4 requests openai twilio
## Working with Branches

Instructions for merging changes between the `production` and `build` branches.

### Merging `production` into `build`

To merge changes from `production` into the `build` branch, follow these steps:

1. **Switch to the `build` branch:**

   - For Git version 2.23 or newer:
     ```
     git switch build
     ```
   - For older versions of Git:
     ```
     git checkout build
     ```

2. **Fetch the latest changes from your remote repository:**

3. **Merge `production` into `build`:**

4. **Resolve any merge conflicts**, commit, and then push your changes to the remote repository:

### Merging `build` into `production`

To incorporate changes from the `build` branch into `production`, reverse the process:

1. **Switch to the `production` branch:**

- For Git version 2.23 or newer:
  ```
  git switch production
  ```
- For older versions of Git:
  ```
  git checkout production
  ```

2. **Fetch the latest changes from your remote repository:**
  ```
  git fetch origin
  ```

3. **Merge `build` into `production`:**

4. **Resolve any merge conflicts**, commit, and then push your changes to the remote repository:

## Contributing

Please read [CONTRIBUTING.md](http://example.com) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](http://example.com).

## Authors

* **Jason Pien** - *Initial work* - [jpien13](https://github.com/jpien13)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
