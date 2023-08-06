# django-apiview

A set of django tools to help you create JSON service.

## Install

```
pip install django-apiview
```

## Installed Decorators

- @apiview
- @requires(*parameter_names)
- @choices(field, choices, allow_none=False)
- @between(field, min, max, include_min=True, include_max=True, annotation=Number, allow_none=False)
- @rsa_decrypt(field, private_key_instance)
- @meta_variable(variable_name, meta_name)
- @cache(key, expire=None, cache_name="default", get_from_cache=True, set_to_cache=True)
- @safe_apiview(get_client_rsa_publickey, **kwargs)
- @decode_encrypted_data(result_encoder=cipherutils.SafeBase64Encoder(), privatekey=None, server_rsa_privatekey_filedname="RSA_PRIVATEKEY", encrypted_password_fieldname="encryptedPassword", encrypted_data_fieldname="encryptedData")
- @check_aclkey(aclkey=None, aclkey_field_name="aclkey")
    - default aclkey=settings.DJANGO_APIVIEW_ACLKEY
- @string_length_limit

**Note:**

- @apiview
    1. apiview = Apiview(SimpleJsonPacker())
- @safe_apiview(...)
    1. Requires django_middleware_global_request, see django_middleware_global_request's usage at https://pypi.org/project/django-middleware-global-request/.
    1. Requires server rsa settings: RSA_PRIVATEKEY_STRING, RSA_PRIVATEKEY (load RSA_PRIVATEKEY_STRING as RsaKey)
    1. Callback function get_client_rsa_publickey defines: `def get_client_rsa_publickey(client_id): pass`
    1. kwargs:
        1. client_id_fieldname = "clientId"
        1. client_rsa_publickey_fieldname = "CLIENT_RSA_PUBLICKEY"
        1. result_encoder = cipherutils.SafeBase64Encoder()
        1. server_rsa_privatekey_filedname = RSA_PRIVATEKEY
        1. encrypted_password_fieldname = encryptedPassword
        1. encrypted_data_fieldname = encryptedData
        1. packer_class = SafeJsonResultPacker
        1. password_length = 32
- @cache(...)
    1. Optional setting: DJANGO_APIVIEW_DISABLE_CACHE_HEADER_NAME = "HTTP_DISABLE_CACHE"
    1. Optional setting: DJANGO_APIVIEW_DEFAULT_CACHE_EXPIRE = None 

## Usage


**Note:**

- Apiview always set csrf_exempt=True.
- @apiview or @safe_apiview decorator must be the first decorator.
- Return raw data without serialized, we'll do result pack for you.
- Set DJANGO_APIVIEW_ENABLE_API_RESPONSE_TIME_LOG=True to enable api response time log.

**app/views.py**

```python
import time
from django_apiview.views import apiview
from django_apiview.views import requires
from django_apiview.views import choices
from django_apiview.views import between

@apiview
def ping():
    return "pong"

@apiview
def timestamp():
    return int(time.time())

@apiview
@requires("msg")
def echo(msg: str):
    return msg

@apiview
def getBooleanResult(value : bool):
    return value

@apiview
def getIntegerResult(value: int):
    return value

@apiview
def getBytesResult(value: bytes):
    return value

@apiview
@choices("op", ["+", "-", "*", "/"])
@between("a", 2, 10, include_min=False)
@between("b", 2, 10, include_max=False)
def calc(a: int, op: str, b: int):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b

@safe_apiview(get_client_rsa_publickey=get_client_rsa_publickey)
def safe_ping():
    return "pong"

```


## Releases

### v0.9.25 2021/03/24

- Fix empty result problem.
- Fix logging problem.

### v0.9.23 2021/02/26

- Handle json dumps error at the last step.
- Create response instance first so that you can handle the response instance: _django_apiview_response.
- rsa_decrypt fix None problem.

### v0.9.21 2020/02/25

- Update dependent packages' version.

### v0.9.20 2021/02/24

- @requires support A-OR-B model parameters check.
- Fix SimpleJsonResultPacker.unpack if missing success filed.
- Remove api response time log models. Waste resources. Get response time from nginx access log instread.
- make cache cleaners setup easy. 

### v0.9.7 2021/02/21

- Add string_length_limit.
- Fix SimpleJsonResultPacker.unpack

### v0.9.2 2021/02/09

- Add log_api_response_time.

### v0.8.9 2021/02/08

- Fix boolean calc problem.

### v0.8.8 2021/02/08

- Use logger.exception instead of logger.error, so that we get running stack message.
- use `cache.expire(key, expire)` after `cache.set(key, value)` instread of `cache.set(key, value, keepttl=expire)`.

### v0.8.6 2020/12/24

- Add check_aclkey.
- Parse json data before doing data unpack.

### v0.8.4 2020/11/18

- Add cache entry_point manage.

### v0.8.3 2020/09/30

- Fix variable reference problem.

### v0.8.2 2020/09/30

- Fix variable reference problem.

### v0.8.1 2020/09/30

- Fix variable reference problem.

### v0.8.0 2020/09/30

- Add ApiviewDecorator to make decorator programming easier.
- Fix some function reference problem.

### v0.7.0 2020/09/28

- Add batch_mode parameter support for cache.

### v0.6.0 2020/09/06

- Add safe_apiview.

### v0.5.0 2020/08/13

- Add cache decorator.
- Add func's default values to View.data.

### v0.4.0 2020/08/06

- Add meta_variable decorator.
- Datetime value encode to native time, and in format like `2020-08-06 14:41:00`.

### v0.3.4 2020/07/26

- Fix BizError class check problem.

### v0.3.3 2020/07/24

- Add rsa_decrypt decorator.

### v0.3.2 2020/07/18

- Add Apiview class based implementation.
- Add setup_result_packer api.
- Rename simple_json_result_packer to simple_result_packer.

### v0.3.1 2020/07/01

- Change app name from `apiview` to `django_apiview`.
- Add parameter validators.
- `WARN`: NOT backward compatible.

### v0.2.0

- Using fastutils.typingutils for annotation cast.
- Add result pack mechanism.
- Move example views from the main app to example app and the example app is not include in published package.
 
### v0.1.3

- Add logging while getting result failed in @apiview.
- Add Map, List annotations.

### v0.1.2

- Fix form process problem.

### v0.1.1

- Add PAYLOAD injection, PAYLOAD field has low priority.

### v0.1.0

- First release,
