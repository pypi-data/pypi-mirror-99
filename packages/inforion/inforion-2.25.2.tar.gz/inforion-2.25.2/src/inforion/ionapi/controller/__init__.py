import logging
import sys
import time
from datetime import datetime
from datetime import timedelta

import curlify
import inforion.ionapi.model.inforlogin as inforlogin
from inforion.ionapi.controller import *
from inforion.ionapi.model import *
from inforion.logger.logger import get_logger

# from io import BytesIO
# import gzip

# import inforion.ionapi.basic as inforlogin

# from logger import get_logger

# import inforion.ionapi.basic as inforlogin

logger = get_logger("main", True)


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def requests_retry_session(
    retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def sendresults(url, _headers, data, timeout=65, stream=False):

    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "POST", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(
        max_retries=retry_strategy, pool_connections=100, pool_maxsize=100
    )
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    if datetime.now() > inforlogin._GLOBAL_session_expire:

        headers = inforlogin.reconnect()
        logger.info(
            " Reconnect and Next Reconnect will be "
            + str(inforlogin._GLOBAL_session_expire)
        )

    try:
        max_attempt = 10
        for z in range(0, max_attempt):

            response = http.request(
                "POST",
                url,
                headers=inforlogin.header(),
                data=json.dumps(data),
                timeout=timeout,
                stream=stream,
            )
            logger.debug("Sending request: " + curlify.to_curl(response.request))
            # logger.debug("Response received: " + response.content)
            if response.status_code == 200:
                try:
                    r = response.json()
                    logger.debug("Response received: " + json.dumps(r))
                    break
                except ValueError:
                    r = "JSON Error"
                    logger.error(r)
            else:
                r = "Session Error " + str(z)
                logger.error(r)
                logger.error(f'Response: {response.status_code}: {response.content}')
                logger.error(f'Response content {response.content}')
                if z < max_attempt:
                    logger.info(" Error try to get new session " + str(z) + "/5")
                    headers = inforlogin.reconnect()
                    time.sleep(10)
                elif z == max_attempt:
                    raise SystemExit(r)

    except requests.exceptions.TooManyRedirects:
        logger.error("Too many redirects")
        r = "Error - Too many redirects"
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error("OOps: Something Else", e)
        raise SystemExit(e)
        r = "Error"

    return r


def saveresults(r, df, program, index, chunk, MaxChunk=150, elements=1):

    message = ""
    max_elements = elements
    try:
        if chunk == 0:
            newindex = index - MaxChunk
        else:
            newindex = index - MaxChunk + chunk
        if newindex < 0:
            newindex = 0
        if len(r) > 0:
            if "results" in r.keys():

                if len(r["results"]) > 0:

                    for key in r["results"]:

                        methode = key["transaction"]

                        if "errorMessage" in key:
                            error = key["errorMessage"]
                            error = error.rstrip("\r\n")
                            error = " ".join(error.split())
                            message += methode + ":" + error + "^_^"

                        else:
                            message += methode + ":OK^_^"

                        df.loc[newindex, "MESSAGE"] = message

                        if elements == 1:
                            newindex = newindex + 1
                            elements = max_elements
                            message = ""
                        else:
                            elements = elements - 1

                else:

                    df.loc[
                        df.index.to_series().between(newindex, index), "MESSAGE"
                    ] = "Results are empty"
            else:

                df.loc[
                    df.index.to_series().between(newindex, index), "MESSAGE"
                ] = "Results are missing"
        else:
            for newindex in range(index):
                # logging.info('Write JSON Error:', str(newindex))
                df.loc[newindex, "MESSAGE"] = " JSON Error"
    except Exception as e:
        logger.exception(e)
        df.loc[
            df.index.to_series().between(newindex, index), "MESSAGE"
        ] = "Unclear Error"

    chunk = MaxChunk
    data = {"program": program, "cono": 409}

    return df, data, chunk
