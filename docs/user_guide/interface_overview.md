# Interface Overview

## Menu

In the menu, you will find sections dedicated to:

- Autotests
- Scripts
- Load tests

```{image} /_static/images/interface_overview_menu.png
:alt: Menu Overview
```

---

## Environments

Running the same tests or scripts across different environments is critical — and **FireFly** fully supports this.

The history and statistics of autotests and scripts, as well as the selected execution environment, are controlled through the environment selector in the header.

```{image} /_static/images/interface_overview_env_open.png
:alt: Environment Selector
```

You can easily modify environment settings without changing the code:

```{image} /_static/images/interface_overview_env_overview.png
:alt: Edit Environment Settings
```

Filtering is also available — you can quickly find the desired parameter by applying filters across one or multiple columns.

```{image} /_static/images/interface_overview_env_search.png
:alt: Environment Filtering
```

Additionally, you can delete, edit, or add new environment parameters as needed.  
Don't forget to save your changes!

```{image} /_static/images/interface_overview_env_edit.png
:alt: Manage Environment Parameters
```

---

## Run Auto Tests

On the **Run Auto Tests** page, you will see:

- A list of recent test runs
- A tree view of available autotests
- Autotest execution statistics

To run tests, simply select the ones you need using checkboxes, and press the big green button.

```{image} /_static/images/interface_overview_autotest_overview.png
:alt: Run Auto Tests
```

Some tests may require additional run configuration.  
After selecting such a test, the "Additional Settings" button will become active.

```{image} /_static/images/interface_overview_autotest_run_config_open.png
:alt: Additional Settings Button
```

Click it to configure specific parameters before running:

```{image} /_static/images/interface_overview_autotest_run_config_edit.png
:alt: Configure Test Run
```

You can also click on any specific test to view statistics related only to that test.

```{image} /_static/images/interface_overview_autotest_one_test_history.png
:alt: Test Statistics
```

---

### Recent Test Runs

The recent runs list shows summaries of previously launched tests.

```{image} /_static/images/interface_overview_test_runs.png
:alt: Recent Test Runs
```

---

### Test Run Report

Click on a test run to view its detailed report.

On the left side, you will see a tree of all test results, while the right side shows overall statistics for the selected run.

```{image} /_static/images/interface_overview_test_run_select.png
:alt: Test Run Overview
```

To inspect an individual test report, simply click on it.

```{image} /_static/images/interface_overview_test_run_one_test_view.png
:alt: Individual Test Report
```

Each test report contains:

- Step-by-step execution details
- Run configuration (if any)
- Used environment variables and their values
- Values generated during the test
- Files generated during the test (screenshots, videos, logs)

```{image} /_static/images/interface_overview_one_test_report_run_config.png
:alt: Run Config Info
```

```{image} /_static/images/interface_overview_one_test_report_env_used.png
:alt: Environment Variables Used
```

```{image} /_static/images/interface_overview_one_test_report_generated.png
:alt: Generated Values
```

```{image} /_static/images/interface_overview_one_test_report_assets.png
:alt: Assets view
```

---

## Script Selection Widget

On the **Script Runner** page, you can find a list of available scripts for each brand.

The search bar allows you to quickly locate scripts by either their name or description.

```{image} /_static/images/interface_overview_scripts_overview.png
:alt: Script Selection
```
```{image} /_static/images/interface_overview_scripts_search.png
:alt: Script Search
```

---

## Script Execution

To launch a script:

1. Click on a script from the list.
2. The launch form will appear on the right side.

If the script has parameters, fill them in (some scripts might not require any parameters).

```{image} /_static/images/interface_overview_scripts_run_1.png
:alt: Script Launch Form 1
```

```{image} /_static/images/interface_overview_scripts_run_2.png
:alt: Script Launch Form 2
```

If a parameter has a default value, it will be automatically populated — but you can modify it if needed.

After completing the form, click the green button to start the script.

The script will launch instantly, and you will see the result without reloading the page.

```{image} /_static/gif/interface_overview_scripts_execute.gif
:alt: Script Execution Result
```

---

### Last Executed Script Results

A widget displays the latest script result, including:

- Execution status
- Result content
- Log messages
- Environment variables used

```{image} /_static/images/interface_overview_scripts_result.png
:alt: Script Result Widget
```

Scripts may also complete with one or more errors.  
You can expand the Traceback section to see detailed error traces.

```{image} /_static/images/interface_overview_scripts_error.png
:alt: Script Traceback
```

---

### Script Run History

To view the history of a script's executions:

1. Click the **View history** button located in the upper right corner of the script card.

```{image} /_static/images/interface_overview_scripts_view_history.png
:alt: View Script History
```

The history displays all runs of the script by all users, showing:

- Run parameters
- Results
- Log
- Environment variables used
- Any errors that occurred

```{image} /_static/images/interface_overview_scripts_history.png
:alt: Script Execution History
```

To return to the script execution form, click **Return to script** at the top right corner.

---
