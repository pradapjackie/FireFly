import random
import re
import string
import uuid
from typing import MutableMapping, Optional, Tuple

import exrex
import pendulum
import phonenumbers
from pendulum import date

from src.modules.auto_test.contexts import auto_test_context, auto_test_contexts

def _calc_param_name(current: MutableMapping[str, str], new_param_name: str) -> str:
    if new_param_name not in current:
        return new_param_name
    elif serial_number := re.findall(r"\[(\d+)]$", new_param_name):
        next_name = re.sub(r"\[(\d+)]$", f"[{int(serial_number[0]) + 1}]", new_param_name)
        return _calc_param_name(current, next_name)
    else:
        next_name = f"{new_param_name} [2]"
        return _calc_param_name(current, next_name)


def add_info_to_test_generated_params(param_name: str, param_value: str):
    param_name, param_value = str(param_name), str(param_value)
    if auto_test_context and auto_test_context.get(None):
        param_name = _calc_param_name(auto_test_context.get().generated_params, param_name)
        auto_test_context.get().generated_params[param_name] = param_value
    elif auto_test_contexts and auto_test_contexts.get(None):
        for test_context in auto_test_contexts.get():
            param_name = _calc_param_name(test_context.generated_params, param_name)
            test_context.generated_params[param_name] = param_value


def random_string(n: int, prefix: Optional[str] = "", postfix: Optional[str] = "", allow_digits=True) -> str:
    choice_pool = string.ascii_letters + string.digits if allow_digits else string.ascii_letters
    return prefix + "".join(random.choices(choice_pool, k=n)) + postfix


def random_name(n: int, prefix: Optional[str] = "", postfix: Optional[str] = "") -> str:
    prefix = f"{prefix} " if prefix else ""
    postfix = f" {postfix}" if postfix else ""
    name = prefix + "".join(random.choices(string.ascii_letters, k=n)) + postfix
    add_info_to_test_generated_params(f"Random {prefix}", name.title())
    return name.title()


def random_email(prefix_for_test_generated_params: Optional[str] = "") -> str:
    domains = [
        "gmail",
        "yahoo",
        "express",
        "yandex",
        "finance",
        "company",
    ]
    domain_zones = [
        "com",
        "in",
        "jp",
        "uk",
        "org",
        "edu",
        "co",
        "me",
        "biz",
        "ngo",
        "site",
        "xyz",
    ]

    result = f"{random_string(20)}@{random.choice(domains)}.{random.choice(domain_zones)}"
    add_info_to_test_generated_params("Random email" + prefix_for_test_generated_params, result)
    return result


def random_valid_phone() -> str:
    random_phone = None
    for _ in range(5):
        random_region = random.choice(phonenumbers.SUPPORTED_SHORT_REGIONS)
        region_metadata = phonenumbers.PhoneMetadata.metadata_for_region(random_region)
        try:
            phone_pattern = region_metadata.mobile.national_number_pattern
            random_phone = str(region_metadata.country_code) + exrex.getone(phone_pattern)
        except AttributeError:
            continue
        else:
            break
    if random_phone is None:
        raise ValueError("Fail on phone generation")
    add_info_to_test_generated_params("Random phone", str(random_phone))
    return random_phone


def random_valid_phone_with_plus() -> str:
    return f"+{random_valid_phone()}"


def random_valid_phone_with_code() -> Tuple[str, str]:
    code, random_phone = None, None
    for _ in range(5):
        random_region = random.choice(phonenumbers.SUPPORTED_SHORT_REGIONS)
        region_metadata = phonenumbers.PhoneMetadata.metadata_for_region(random_region)
        try:
            phone_pattern = region_metadata.mobile.national_number_pattern
            code = f"+{region_metadata.country_code}"
            random_phone = code + exrex.getone(phone_pattern)
        except AttributeError:
            continue
        else:
            break
    if code is None or random_phone is None:
        raise ValueError("Fail on phone generation")
    add_info_to_test_generated_params("Random phone", str(random_phone))
    return code, random_phone


def random_ip() -> str:
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    add_info_to_test_generated_params("Random ip", ip)
    return ip


def random_password(add_punctuation: bool = True, save_to_params: bool = True) -> str:
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation) if add_punctuation else ""
    password += random_string(6)
    password = "".join(random.sample(password, len(password)))
    save_to_params and add_info_to_test_generated_params(f"Random password", password)
    return password


def random_date(minus_years: date) -> date:
    now = pendulum.now()
    return date(
        year=random.randrange(now.year - minus_years - 60 - 1, now.year - minus_years - 1),
        month=random.randrange(1, 12),
        day=random.randrange(1, 28),
    )


def random_uuid() -> str:
    unique_id = str(uuid.uuid4())
    add_info_to_test_generated_params("Random uuid", unique_id)
    return unique_id


def random_number(n: int, number_name: str | None = None) -> int:
    result = "".join(random.choices(string.digits, k=n))
    if number_name:
        add_info_to_test_generated_params(f"Random {number_name}", result)
    return int(result)
