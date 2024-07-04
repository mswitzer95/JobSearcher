import asyncio
from aiohttp import ClientSession
from json import dumps
from urllib.parse import urlencode


async def fetch_response_text(
        session: ClientSession,
        url: str,
        method: str,
        params: (dict, None)=None,
        headers: dict={}
        ) -> str:
    """
    GET requests a given URL, and gets the response's text in an async fashion
    
    Args:
        session (ClientSession): The session to make the request
        url (str): The URL to request
        method (str): The method to use when making the request; either "GET" 
            or "POST"
        params (dict, None; default=None): The payload to send with the 
            request, either as a query string if method is "GET" or as a body 
            if metohd is "POST".
        headers (dict, default={}): Extra headers to send with the request.
    Returns:
        str: The response's text
    """
    
    if (
        not isinstance(session, ClientSession)
        or not all(isinstance(arg, str) for arg in [url, method])
        or method not in ["GET", "POST"]
        or not isinstance(params, (dict, type(None)))
        or not isinstance(headers, dict)):
        raise Exception("Invalid args.")
    
    if method == "GET":
        url += (f"?{urlencode(params)}" if params else "")
        fetch_method = session.get(url)
    else:
        if params:
            data = dumps(params)
            headers["Content-Type"] = "application/json"
        else:
            data = ""
        fetch_method = session.post(url, data=data, headers=headers)
    async with fetch_method as response:
        status_code = response.status
        text = await response.text()
        
        if status_code // 100 != 2:
            raise Exception(f"Requesting URL {url} returned status code of " + 
                            f"{status_code} with text of:\n\n{text}")
        
    return text
