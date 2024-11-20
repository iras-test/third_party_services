from django.conf import settings
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import urllib3

def validate_nin(nin):
    """Validate the NIN by calling the external service."""
    url = f"{settings.SERVICE_URL}/ura/services/validate_nin/?nin={nin}"
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