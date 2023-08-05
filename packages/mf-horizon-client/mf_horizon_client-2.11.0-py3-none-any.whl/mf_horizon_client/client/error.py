from requests import Response


class HorizonError(RuntimeError):
    """Wrapper class for an error :class:`.Response` received from Horizon."""

    def __init__(self, response: Response) -> None:
        self.status_code = response.status_code
        try:
            response_json = response.json()
            self.message = response_json["summary"] or response_json["message"]
        except BaseException:
            self.message = response.content.decode() if response.content else ""
        super().__init__(f"Status: {self.status_code}  Message: {self.message}")
