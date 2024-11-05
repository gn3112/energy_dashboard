from requests import Session
from datetime import datetime, timedelta
from time import time
import random

from app.utils.convert_unit import convert_unit

class API_Historian():
    """Initialize soap client with stored authentication key, gets type later used in calling functions
    """        
    def _authenticate(self):
        """Load authentication key and set it as cookie.
        """
        with open(self.auth_key_path, "r") as f:
            auth_key = f.read()
        self.session.cookies.set("DnaAuthCookie", auth_key, domain="ah01.local")

    def _new_authentication_key(self):
        """Create a new authentication key and store it in current directory.
        """
        session = Session()

        # Example of API connections:

        # client = Client("http://ah01/DNA/DNAdataWSIForms/AuthenticationService.svc?singleWsdl", transport=Transport(session=session))

        # try:
        #     r = client.service.Login("dna", str(os.environ["VALMET_PW"]), "", True) # Valmet password set as an environment variable
        # except:
        #     print("Could not login")

        # auth_key = session.cookies["DnaAuthCookie"]

        # r = client.service.IsLoggedIn()
        # print(f"Login status: {r}")
        # with open(self.auth_key_path, "w") as f:
        #     f.write(auth_key)
        
        # self._authenticate()
    
    def get_aggregate_over_period(self, time_start: datetime, time_end: datetime, tag: str):
        """Gets the average power consumption of a transformer between two timestamps

        Args:
            time_start: datetime as local time.
            time_end: datetime as local time.
            tag: measurement identification tag.

        Returns:
            returns dictionnary. If getting the data from the historian failed, it returns False.
        """
        method = "Avg" # Method to feed to call to historian API

        time_start = time_start.strftime("%Y-%m-%dT%H:%M:%S") # local time
        time_end = time_end.strftime("%Y-%m-%dT%H:%M:%S")
        
        value = random.randint(0, 1000) # Here call to historian API

        value = convert_unit(value)

        return {
            'tag_name': tag,
            'time_start': time_start,
            'time_end': time_end,
            'value': value,
        }
    
    def get_data_multi(self, time_start: datetime, time_end: datetime, frequency: int, tag_names: list, option: str = "TS_START", method: str = "Avg"):
        """Request data for multiple tags to the Valmet historian between two timestamps. 
           It returns averaged data based on the frequency by default.

        Args:
            time_start: datetime as local time.
            time_end: datetime as local time.
            frequency: evenly spaced data in minutes, should be an integer.
            tag_name: list of tags with reference from the Valmet historian.
            option:
            method:
        Returns:
            returns dictionnary with timestamps and values as keys. The vaalue for values is a dict with keys of the tag list index.
            If getting the data from the historian failed, it returns False.
        """
        # Sample datetime between two datetime at a interval T
        interval = timedelta(minutes=frequency)
        timestamps = []

        current_datetime = time_start
        while current_datetime <= time_end:
            timestamps.append(current_datetime)
            current_datetime += interval

        result = {}

        result['timestamps'] = timestamps

        # Here call to API
        for tag_idx in range(len(tag_names)):
            m = random.randint(100,500)
            result[tag_idx] = [convert_unit(random.gauss(m, m*0.05)) for _ in range(len(timestamps))]

        return result