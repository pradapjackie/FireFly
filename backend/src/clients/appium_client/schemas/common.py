from enum import StrEnum

ELEMENT = "element-6066-11e4-a52e-4f735466cecf"


class By(StrEnum):
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
    # Appium:
    IOS_PREDICATE = "-ios predicate string"
    IOS_UIAUTOMATION = "-ios uiautomation"
    IOS_CLASS_CHAIN = "-ios class chain"
    ANDROID_UIAUTOMATOR = "-android uiautomator"
    ANDROID_VIEWTAG = "-android viewtag"
    ANDROID_DATA_MATCHER = "-android datamatcher"
    ANDROID_VIEW_MATCHER = "-android viewmatcher"
    ACCESSIBILITY_ID = "accessibility id"
    IMAGE = "-image"
    CUSTOM = "-custom"
