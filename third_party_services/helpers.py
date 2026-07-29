from django.conf import settings
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import urllib3

def validate_nin(nin):
    """Validate the NIN by calling the external service."""
    url = f"{settings.SERVICE_URL}/ura/services/validate_nin/?nin={nin}"
    response = execute_with_timeout(make_get_request, url)
    return response

def validate_tin(tin):
    """Validate the TIN by calling the external service."""
    url = f"{settings.URA_API}/service/clients/{tin}"
    
    return execute_with_timeout(make_get_request, url)

def validate_brn(brn):
    """Validate the BRN by calling the external service."""
    url = f"{settings.SERVICE_URL}/ura/services/validate_brn/?brn={brn}"
    response = execute_with_timeout(make_get_request, url)
    return response


def validate_obrs_brn(brn):
    """Validate the BRN using the OBRS service."""
    timeout = getattr(settings, "EXTERNAL_SERVICE_TIMEOUT", 30) or 30
    url = (
        f"{settings.SERVICE_URL}/ura/services/"
        f"validate-obrs-brn/?brn={brn}"
    )
    http = urllib3.PoolManager()
    return http.request(
        "GET",
        url,
        timeout=timeout,
    )


def validate_vehicle(plate):
    """Validate the vehicle by calling the external service."""
    url = f"{settings.URA_API}/service/vehicle/{plate}"
    response = execute_with_timeout(make_get_request, url)
    return response


def execute_with_timeout(func, *args, **kwargs):
    """Execute a function with a timeout."""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            # Wait for the future to complete within the specified timeout
            return future.result(timeout=settings.EXTERNAL_SERVICE_TIMEOUT)
        except TimeoutError:
            return {'error': f"Service timeout: The request took longer than {settings.EXTERNAL_SERVICE_TIMEOUT} seconds."}
        except Exception as e:
            return {'error': str(e)}
        
def make_get_request(url):
    """Make a GET request to the specified URL."""
    http = urllib3.PoolManager()
    resp = http.request(
        'GET',
        url,
        timeout=settings.EXTERNAL_SERVICE_TIMEOUT
    )

    return resp
    if resp.status == 200:
        return resp.data
    else:
        return {'error': f"Request failed, status code: {resp.status}"}
    

def mask_string(input_string, mask_length=5):
    if input_string is not None:
        if len(input_string) <= mask_length:
            return input_string
        else:
            masked_part = '*' * (len(input_string) - mask_length)
            visible_part = input_string[-mask_length:]
            masked_string = masked_part + visible_part
            return masked_string
    else:
        return input_string
    

def mask_email(email):
    if '@' in email:
        username, domain = email.split('@')
        return f"{mask_string(username)}@{domain}"
    else:
        return mask_string(email)
