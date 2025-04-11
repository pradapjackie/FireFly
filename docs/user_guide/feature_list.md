# Features List

This section provides an overview of FireFly features for both **Autotests** and **Scripts**, along with code examples and report integration.

---

## 🧪 Auto Test Features

### Stages

Each test can consist of the following stages (all optional):

- **Group Setup** – executed once for all tests in a class.  
  Use this for shared resources like DB connections or sessions (non-stateful).

- **Setup** – executed before each test iteration.

- **Call** – the actual test iteration.

- **Teardown** – executed after each iteration, regardless of the result.

- **Group Teardown** – executed after all iterations are complete.

#### Example:

```python
class StagesExample(TestAbs):
    all_tests_in_class_shared_resource: str | None = None

    def __init__(self):
        self.one_test_iteration_resource: str | None = None

    @classmethod
    async def group_setup(cls):
        cls.all_tests_in_class_shared_resource = "Shared setup"

    async def setup(self, **test_params):
        self.one_test_iteration_resource = "Iteration setup"

    @params([
        dict(iteration_name="First iteration"),
        dict(iteration_name="Second iteration"),
    ])
    async def test_example(self):
        print(self.all_tests_in_class_shared_resource)
        print(self.one_test_iteration_resource)

    async def teardown(self, **test_params):
        self.one_test_iteration_resource = None

    @classmethod
    async def group_teardown(cls):
        cls.all_tests_in_class_shared_resource = None
```

```{image} /_static/images/stages_report.png
:alt: Example of stage usage in report
```

---

### Iterations

Each test must define at least one **iteration** using the `@params` decorator.

```python
@params([
    dict(iteration_name="First iteration"),
    dict(iteration_name="Second iteration"),
])
async def test_example(self):
    pass
```

You can also pass parameters:

```python
@params([
    dict(iteration_name="First", a=1, b="b"),
    dict(iteration_name="Second", a=2),
])
async def test_success(self, a: int, b: str | None = None):
    pass
```

💡 All values must be JSON-serializable.  
Iteration parameters are shown in the report under the **"Parameters"** tab.

```{image} /_static/images/iteration_params.png
:alt: Iteration parameter display
```

---

### Auto-Generated Iterations

Use `@params_product` to create combinations automatically:

```python
@params_product(
    iteration_name="{client_type} client with {account_type} account",
    account_type=["live", "demo"],
    client_type=["Individual", "Corporate"]
)
async def test_example(self, client_type: str, account_type: str):
    pass
```

---

### Inheritance

FireFly supports class inheritance (including multiple inheritance), which is useful for sharing setup/teardown logic.

```python
class MyServiceBaseTest(TestAbs):
    def __init__(self):
        self.example_resource: str | None = None

    async def setup(self, **test_params):
        self.example_resource = "test"

    async def teardown(self, **test_params):
        self.example_resource = None

class Test1(MyServiceBaseTest):
    @params([dict(iteration_name="First iteration")])
    async def test_example(self):
        print(self.example_resource)
```

All stages from base classes are executed in **reverse MRO order**.

---

### Descriptions

Add a docstring inside test methods to make them easier to understand in reports:

```python
@params([dict(iteration_name="First")])
async def test_success(self):
    """
    This test verifies user login with valid credentials.
    """
    pass
```
```{image} /_static/images/auto_test_description.png
:alt: Iteration parameter display
```
---

### Steps

Use `step()` to structure your test and make the report more informative.

```python
@params([dict(iteration_name="First")])
async def test_success(self):
    async with step("Start"):
        async with step("Continue"):
            pass
```

Steps can be nested and used in any test stage or method.

```{image} /_static/images/steps_ui.png
:alt: Step nesting in UI
```

---

### RunConfig

Tests can expose custom configuration through `RunConfig` class:

```python
@register()
class RunConfigExample(TestAbs):
    class RunConfig:
        string_field = StringField(label="Some String")
        number_field = NumberField(label="Some Number")
        switch_field = SwitchFiled(label="Some Switch")
        checkbox_field = CheckboxFiled(label="Some Checkbox")
        autocomplete_field = AutocompleteFiled(
            label="Choose Option", options=["First", "Second", "Third"]
        )

    @params([dict(iteration_name="With config")])
    async def test_success(self):
        print(self.RunConfig.string_field.value)
```

```{image} /_static/images/run_config_setup.png
:alt: Run config setup in UI
```

All values are recorded in the report for reproducibility.

```{image} /_static/images/run_config_in_report.png
:alt: Run config in report
```

---

### Environment Variables

You can access environment variables using the `env` object:

```python
async with step("Print env variable"):
    print(env.application_url)
```

```{image} /_static/images/env_in_settings.png
:alt: Env variable in settings
```

All used variables are saved in the report under **Environment Used** tab.

```{image} /_static/images/env_in_report.png
:alt: Env variable in report
```

---

### Assets

Save files (logs, screenshots, etc.) into reports via `AssetsHelper`.

```python
@register()
class AssetHelperExample:
    assets_helper: Optional[AssetsHelper] = None

    @classmethod
    async def group_setup(cls):
        cls.assets_helper = AssetsHelper()

    @params([dict(iteration_name="Attach file")])
    async def test_success(self):
        await self.assets_helper.add_text("log.txt", b"Some log")

    @classmethod
    async def group_teardown(cls):
        await cls.assets_helper.close_connection()
```

```{image} /_static/images/assets_in_report.png
:alt: Assets in report
```

---

### Generated Parameters

To make dynamic data visible in reports, use `add_info_to_test_generated_params()`:

```python
add_info_to_test_generated_params("random_email", f"user_{randint(100)}@mail.com")
```

```{image} /_static/images/generated_params_in_report.png
:alt: Generated params in report
```

---

### Warnings

If something goes wrong, but the test shouldn’t fail — add a warning:

```python
add_warning_to_test("Service responded with error on first attempt")
```

```{image} /_static/images/warning_in_report.png
:alt: Warning in report
```

---

### Errors

Unhandled exceptions in tests are captured and shown in the report, with full traceback.

```{image} /_static/images/errors_in_report.png
:alt: Errors in report
```

```{image} /_static/images/errors_traceback_in_report.png
:alt: Open errors traceback in report
```

---

### Comparisons

FireFly provides helper methods based on **Pydantic**:

```python
compare_pydantic_models(real=actual, expected=expected)
```

It highlights differences in the report.
```{image} /_static/images/comparation_error_in_report.png
:alt: Comparation error in report
```


Other helpers include:

- `ApproximatelyEqual`, `ApproximatelyDateEqual`
- `FromProtobufModel`
- `BCryptPasswordEqual`
- `all_optional`
- `CamelCaseModel`, `PascalCaseModel`
- etc...
---

## ⚙️ Script Runner Features

### Dynamic Parameters

Use type annotations to declare script parameters:

```python
from enum import StrEnum
from src.modules.script_runner.register import register

class MyEnum(StrEnum):
    a = "a"
    b = "b"

@register
async def my_script(
    some_float: float,
    some_str_enum: MyEnum,
    some_date_one: date,
    some_file: BytesIO,
    some_date_two: pendulum.Date = pendulum.Date(year=2023, month=11, day=11),
    some_string: str = "test",
    some_int: int = 10,
    some_bool: bool = True,
):
    pass
```

Required in UI if no default is provided.

```{image} /_static/images/script_parameters_in_ui.png
:alt: Script paramenters in UI
```

---

### Description

Add a docstring to explain the script’s behavior:

```python
@register
async def my_script():
    """
    Cleans up unused client records in test DB.
    """
```

```{image} /_static/images/script_description_in_ui.png
:alt: Script description in UI
```

---

### Logging

Use `log()` to track progress inside scripts:

```python
@register
async def example():
    for i in range(3):
        await log(f"Step {i}")
```

```{image} /_static/images/script_logs_in_ui.png
:alt: Script logs in UI
```

If called inside `step()`, logs for entering/exiting each step will appear automatically.

---

### Smart Result Formatting

FireFly auto-formats results:

| Type                              | UI Display                   |
|-----------------------------------|------------------------------|
| `dict`/`Pydantic` with primitives | Two-column table             |
| List of dicts/models              | Multi-row table with headers |
| FileResult/List of FileResult     | File response                |
| Other                             | Stringified output           |


```{image} /_static/images/script_result_dict.png
:alt: Script result dict
```
```{image} /_static/images/script_result_list_of_models.png
:alt: Script result list of models
```
```{image} /_static/images/script_result_files.png
:alt: Script file result
```

---

### Environment Variables

Access them just like in autotests:

```python
await log(env.db_password)
```

All variables used are shown in report + history.

```{image} /_static/images/script_feature_env_set.png
:alt: Set env variable in settings
```
```{image} /_static/images/script_feature_env_in_ui_1.png
:alt: Env variable in last script result
```
```{image} /_static/images/script_feature_env_in_ui_2.png
:alt: Env variable in script result history
```

---

### Error Handling

Uncaught exceptions are recorded. If using `ExceptionGroup`, all grouped exceptions will be shown separately in the report.

```{image} /_static/images/script_errors_on_ui.png
:alt: Script errors on UI
```

---

### Shareable Link

You can share script result links — just copy the address bar after selecting a script.

---

### Class-Based Scripts

Scripts can also be written as classes:

```python
@register
class ThirdScript(ScriptClassAbs):
    def __init__(self):
        self.counter = 0

    async def run(self, value: str):
        await log(value)
        for i in range(5):
            self.counter += 1
            await log(self.counter)
```

- Must inherit from `ScriptClassAbs`
- Must define `run()` as async method

All script features work the same way.

---
