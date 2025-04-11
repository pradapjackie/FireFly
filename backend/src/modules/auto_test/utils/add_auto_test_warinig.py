from src.modules.auto_test.contexts import auto_test_context


def add_warning_to_test(warning_message: str):
    if auto_test_context and auto_test_context.get(None):
        auto_test_context.get().warnings.append(warning_message)
