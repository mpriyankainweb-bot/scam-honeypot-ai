import re

def extract_intelligence(message: str):

    upi_pattern = r'\b[\w.-]+@[\w.-]+\b'
    phone_pattern = r'\b\d{10}\b'
    url_pattern = r'(https?://\S+)'

    upis = re.findall(upi_pattern, message)
    phones = re.findall(phone_pattern, message)
    urls = re.findall(url_pattern, message)

    return {
        "upi_ids": upis,
        "phone_numbers": phones,
        "urls": urls
    }
