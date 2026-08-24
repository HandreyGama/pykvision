from pykvision.models.consts import ISAPI_HTTP_METHODS


class ISAPIInvalidPortError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class ISAPIInvalidCredencialsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class ISAPIInvalidIPAddressError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class ISAPIInvalidEndpointError(Exception):
    def __init__(self, status_code:int,invalid_endpoint:str,text:str) -> None:
        super().__init__(f"""
                Status code: {status_code}\n
                Invalid endpoint: {invalid_endpoint}\n
                Text: {text}
            """)                        
class ISAPIInvalidEndpointMethodError(Exception):
    def __init__(self, status_code:int,endpoint:str,invalid_method:ISAPI_HTTP_METHODS,text:str) -> None:
        super().__init__(f"""
                Status code: {status_code}\n
                endpoint: {endpoint}\n
                invalid method:`{invalid_method}\n
                Text: {text}
            """)                   
class ISAPIAutenticationError(Exception):
    def __init__(self, text:str) -> None:
        super().__init__(f"Text: {text}")        