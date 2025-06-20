# Automated API Tests for Pomidor Dashboard

## 📝 Project Description

This repository contains a suite of automated API tests developed to verify the basic functionality of the web application **Pomidor Dashboard** ([https://dashboard.pomidor-stage.ru/](https://dashboard.pomidor-stage.ru/)).

The tests are written in **Python** using the **Pytest** testing framework. For generating clear and informative reports, **Allure Reports** are used.

The primary goal of this project is to ensure the stability and correctness of the critical API endpoints for the Pomidor Dashboard staging environment.

## 🚀 Requirements

To successfully run these automated API tests on your local machine, please ensure you have the following tools installed:

  * **Python 3.9+** (latest stable version is recommended)
  * **Git** (for cloning the repository)
  * **Allure Commandline** (for generating and viewing Allure Reports)

## 🛠️ Installation and Setup

Follow these step-by-step instructions to prepare your environment and install the necessary dependencies.

### 1\. Clone the Repository

Open your terminal or command prompt and execute the following command:

```bash
git clone https://github.com/kyryl01011/4_2_homework_task_3.git
cd 4_2_homework_task_3
```

### 2\. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

```bash
python3 -m venv venv
```

After creating the virtual environment, activate it:

  * **For macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```
  * **For Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
  * **For Windows (Command Prompt / CMD):**
    ```cmd
    .\venv\Scripts\activate.bat
    ```

### 3\. Install Python Dependencies

Install all required Python libraries listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4\. Install Allure Commandline

To generate and view Allure Reports, you will need the Allure Commandline tool. If you don't have it installed, follow the instructions for your operating system:

  * **macOS (using Homebrew):**
    ```bash
    brew install allure
    ```
  * **Windows (using Chocolatey):**
    ```bash
    choco install allure
    ```
  * **Linux:** Detailed instructions for various distributions can be found in the official Allure documentation: [Allure Docs](https://www.google.com/search?q=https://docs.qameta.io/allure/%23_install_a_commandline)

### 5\. Configure Environment Variables

This project uses environment variables to store sensitive information (like API credentials) or configurable parameters.

1.  **Create a `.env` file:** Copy the provided `env-copy` file and rename it to `.env` in the root directory of the project.

    ```bash
    cp env-copy .env
    ```

    *(For Windows CMD, use `copy env-copy .env`)*

2.  **Edit the `.env` file:** Open the newly created `.env` file and fill in your specific credentials or configuration details according to the template provided inside.

## 🚀 Running Tests

Once the installation and setup are complete, you are ready to run the tests.

### Run All Tests and Generate Allure Report

This command will execute all tests discovered by Pytest and save the Allure results to the `allure-results/` directory.

```bash
python -m pytest --alluredir=allure-results
```

## 📊 Viewing Allure Reports

After successfully running the tests and saving the results, you can generate and view the interactive Allure report.

### 1\. Generate the Report

This command takes the collected test results from `allure-results/`, generates the HTML report, and saves it to the `allure-report/` directory.

```bash
allure generate allure-results --clean -o allure-report
```

  * `--clean`: Deletes previous report data before generating a new one.
  * `-o allure-report`: Specifies the output directory for the generated report.

### 2\. Open the Report in Your Browser

Once the report is generated, you can open it in your default web browser:

```bash
allure open allure-report
```

## 📚 Pomidor Dashboard API Documentation

For a deeper understanding of the API functionality tested by this project, you can refer to the official Pomidor Dashboard API documentation:
[https://api.pomidor-stage.ru/docs](https://api.pomidor-stage.ru/docs)

-----