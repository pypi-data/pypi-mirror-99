import requests
import yaml
import os
import logging
from askdata.insight import Insight
from askdata.channel import Channel
from askdata.catalog import Catalog
from askdata.dataset import Dataset
from askdata.security import SignUp
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from askdata.askdata_client import Askdata

_LOG_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] - %(asctime)s --> %(message)s"
g_logger = logging.getLogger()
logging.basicConfig(format=_LOG_FORMAT)
g_logger.setLevel(logging.INFO)

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)

class Insight_Definition:


    def __init__(self, env:str, token, defintion):

        self.definition_id = defintion["id"]
        self.agent_id = defintion["agentId"]
        self.collection_id = defintion["collectionId"]
        self.name = defintion["name"]
        self.slug = defintion["slug"]
        self.icon = defintion["icon"]
        self.components: list = defintion["components"]

        self._token = token

        if env.lower() == 'dev':
            self._base_url_askdata = url_list['BASE_URL_ASKDATA_DEV']
            self.smart_insight_url = url_list['BASE_URL_INSIGHT_DEV']
            self.app_url = "https://app-dev.askdata.com/"
        if env.lower() == 'qa':
            self._base_url_askdata = url_list['BASE_URL_ASKDATA_QA']
            self.smart_insight_url = url_list['BASE_URL_INSIGHT_QA']
            self.app_url = "https://app-qa.askdata.com/"
        if env.lower() == 'prod':
            self._base_url_askdata = url_list['BASE_URL_ASKDATA_PROD']
            self.smart_insight_url = url_list['BASE_URL_INSIGHT_PROD']
            self.app_url = "https://app.askdata.com/"


    def add_table(self, query="", columns=[]):

        position = (len(self.components))
        body = {"type": "table", "position": position}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        query_url = self.smart_insight_url + '/definitions/' + self.definition_id + '/components/'
        logging.info("URL {}".format(query_url))
        r = s.post(url=query_url, json=body, headers=headers)
        r.raise_for_status()
        print(r.json())
        self.components = r.json()["components"]

        if(query != "" and columns!=[]):
            self.edit_table(self.components[position]["id"], query, columns)

        return self.components[position]["id"]


    def edit_table(self, table_id, query="", columns=[]):

        url = self.smart_insight_url + "/definitions/" + self.definition_id + "/tables/"+ table_id

        body = {
            "id": table_id,
            "type": "table",
            "name": "Table",
            "customName":False,
            "dependsOn": ["q1"],
            "queryId": query,
            "columns": columns,
            "maxResults":50,
            "valid":True,
            "queryComponent":False
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()
        self.components = r.json()["components"]


    def add_chart(self, type="", query="", params=[]):
        position = (len(self.components))
        body = {"type": "chart", "position": position}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        query_url = self.smart_insight_url + '/definitions/' + self.definition_id + '/components/'
        logging.info("URL {}".format(query_url))
        r = s.post(url=query_url, json=body, headers=headers)
        r.raise_for_status()
        print(r.json())
        self.components = r.json()["components"]

        if (type != "" and query != "" and params!=[]):
            self.edit_chart(self.components[position]["id"], type, query, params)
        else:
            logging.info("One or more arguments between type, query and params are missing to update the chart")

        return self.components[position]["id"]


    def edit_chart(self, chart_id, chart_type:str, query, params):

        url = self.smart_insight_url + "/definitions/" + self.definition_id + "/charts/" + chart_id

        upper_params = [p.upper() for p in params]

        body = {
            "chartType": chart_type.upper(),
            "customName": False,
            "dependsOn": [],
            "id": chart_id,
            "name": "Fusionfood",
            "params": upper_params,
            "queryComponent": False,
            "queryId": query,
            "type": "chart",
            "valid": True
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()
        self.components = r.json()["components"]


    def add_list(self):
        position = (len(self.components))
        list_id = self.add_component("list", position)
        return list_id

    def add_text(self, text):
        position = (len(self.components))
        text_id = self.add_component("text", position)
        self.edit_text(text_id, text)
        return text_id


    def edit_text(self, text_id , text, name="Text"):

        url = self.smart_insight_url+"/definitions/"+self.definition_id+"/texts/"+text_id

        body = {
            "customName": False,
            "dependsOn": [],
            "id": text_id,
            "name": name,
            "queryComponent": False,
            "text": text,
            "type": "text",
            "valid": True
        }

        logging.info("URL: {}".format(url))

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()
        self.components = r.json()["components"]


    def add_html(self, code):
        position = (len(self.components))
        html_id = self.add_component("html", position)
        self.edit_html(html_id, code)
        return html_id


    def edit_html(self, html_id, code):

        url = self.smart_insight_url+"/definitions/"+self.definition_id+"/htmls/"+html_id+"/content"

        body = {
            "html": code
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()
        self.components = r.json()["components"]


    def add_script(self, script):
        position = (len(self.components))
        script_id = self.add_component("script", position)
        self.edit_script(script_id, script)
        return script_id


    def edit_script(self, script_id, script):

        url = self.smart_insight_url+"/definitions/"+self.definition_id+"/scripts/"+script_id+"/content"

        body = {
            "script": script
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()
        self.components = r.json()["components"]

    def add_map(self):
        position = (len(self.components))
        map_id = self.add_component("map", position)
        return map_id

    def add_sql_query(self, query_sql, dataset_slug, is_native = False):

        position = (len(self.components))

        sql_id = self.add_component("sql_query", position)

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        authentication_url = self._base_url_askdata + '/smartdataset/datasets/slug/' + self.agent_id + '/' + dataset_slug
        logging.info("AUTH URL {}".format(authentication_url))

        headers = {"Authorization": "Bearer" + " " + self._token}
        response = s.get(url=authentication_url, headers=headers)
        response.raise_for_status()
        r = response.json()
        dataset_id = r["dataset"]["id"]

        url_put = self.smart_insight_url + "/definitions/" + self.definition_id + "/sql_queries/" + sql_id
        body2 = {
            "datasetId": dataset_id,
            "sql": query_sql,
            "id": sql_id,
            "nativeType": is_native,
            "queryComponent": True,
            "type": "sql_query",
            "valid": True,
            "variableName": sql_id + "Result"
        }
        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url_put, json=body2, headers=headers)
        r.raise_for_status()

        url = self.smart_insight_url+"/definitions/"+self.definition_id+"/sql_queries/"+self.components[position]["id"]+"/sql"

        body = {
            "datasetId": dataset_id,
            "sql": query_sql,
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()

        self.components = r.json()["components"]

        hasResultSet = True

        for component in r.json()["components"]:
            if component["id"] == sql_id:
                if component["preview"] == []:
                    hasResultSet = False
                elif component["preview"][0]["details"]["rows"] == []:
                    hasResultSet = False

        return sql_id , hasResultSet


    def delete(self):

        url= self.smart_insight_url+"/definitions/"+self.definition_id
        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.delete(url=url, headers=headers)
        r.raise_for_status()


    def add_query(self, dataset_slug, fields):

        '''
        fields = [{column: "STATUS_HISTORY_NUOVO_TIME", aggregation: null,…}}
        '''

        position = (len(self.components))

        # Get dataset_id
        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        authentication_url = self._base_url_askdata + '/smartdataset/datasets/slug/' + \
                             self.agent_id + '/' + dataset_slug

        headers = {"Authorization": "Bearer" + " " + self._token}
        response = s.get(url=authentication_url, headers=headers)
        response.raise_for_status()
        r = response.json()

        try:
            dataset_id = r["dataset"]["id"]
        except:
            logging.error("DATASET NOT FOUND")
            return

        url_get = self.smart_insight_url + "/composed_queries?datasetId=" + dataset_id

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {"Authorization": "Bearer" + " " + self._token}
        response = s.get(url=url_get, headers=headers)
        response.raise_for_status()
        r = response.json()

        query_composer = r["qc"]

        url_preview = self.smart_insight_url+"/composed_queries/"+query_composer["id"]+"/preview?limit=100"

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {"Authorization": "Bearer" + " " + self._token}
        response = s.post(url=url_preview, json={}, headers=headers)
        response.raise_for_status()
        r = response.json()
        qc_fields = query_composer["fields"]

        new_fields = []

        for qc_field in qc_fields:
            for field in fields:
                if (field["column"] == qc_field["column"] or field["column"] == qc_field["alias"]):
                    qc_field["aggregation"] = field["aggregation"]
                    del qc_field["internalDataType"]
                    new_fields.append(qc_field)

        query_composer["fields"] = new_fields
        del query_composer["relationships"]
        query_composer["where"] = []
        query_composer["orderBy"] = []

        post_url = self.smart_insight_url+"/composed_queries"

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {"Authorization": "Bearer" + " " + self._token}
        response = s.post(url=post_url, json=query_composer, headers=headers)
        response.raise_for_status()
        r = response.json()

        qc_post_url = self.smart_insight_url+"/definitions/"+self.definition_id+"/query_composers"

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        body = {"type": "query_composer", "position": position, "qc": query_composer["id"]}

        headers = {"Authorization": "Bearer" + " " + self._token}
        response = s.post(url=qc_post_url, json=body, headers=headers)
        response.raise_for_status()
        r = response.json()


    def add_search_query(self, query):

        position = (len(self.components))
        query_id = self.add_component("nl_query", position)

        body_query = {"nl": query, "language": "en"}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        query_url = self.smart_insight_url +'/definitions/'+ self.definition_id +'/nl_queries/'+ query_id + '/nl'

        logging.info("QUERY URL {}".format(query_url))
        r = s.put(url=query_url, json=body_query, headers=headers)

        self.components = r.json()["components"]

        return self.components[position]["id"]


    def add_component(self, type, position):

        body = {"type": type, "position": position}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        query_url = self.smart_insight_url + '/definitions/' + self.definition_id + '/components/'
        logging.info("URL {}".format(query_url))
        r = s.post(url=query_url, json=body, headers=headers)
        r.raise_for_status()
        print(r.json())
        self.components = r.json()["components"]
        return self.components[position]["id"]


    def get_url(self):
        url = self.app_url

        get_url = self._base_url_askdata+"/smartbot/agents/"+self.agent_id

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.get(url=get_url, headers=headers)
        r.raise_for_status()

        agent_slug = r.json()["slug"]

        url += agent_slug

        url += "/card/"
        url += self.slug
        print(url)
        return url

    def add_admin(self, admin_email):

        get_url = self._base_url_askdata+"/smartbot/share/principals?q="+admin_email

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.get(url=get_url, headers=headers)
        r.raise_for_status()
        if(r.json()!=[]):
            body = {
                "role": "ADMIN",
                "userId": r.json()["id"]
            }

            url = self.smart_insight_url+"/insights/8a09ec79-8e1e-401a-bdec-70d33c9c1543/users"

            s = requests.Session()
            s.keep_alive = False
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer" + " " + self._token
            }
            query_url = self.smart_insight_url + '/definitions/' + self.definition_id + '/components/'
            logging.info("URL {}".format(query_url))
            r = s.post(url=url, json=body, headers=headers)
            r.raise_for_status()
        else:
            logging.error("EMAIL ERRATA: Inserire una email corrispondente ad un utente Askdata")


    def add_follower(self, follower_email):

        get_url = self._base_url_askdata+"/smartbot/share/principals?q="+follower_email

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.get(url=get_url, headers=headers)
        r.raise_for_status()
        if(r.json()!=[]):
            body = {
                "role": "FOLLOWER",
                "userId": r.json()["id"]
            }

            url = self.smart_insight_url+"/insights/8a09ec79-8e1e-401a-bdec-70d33c9c1543/users"

            s = requests.Session()
            s.keep_alive = False
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer" + " " + self._token
            }
            query_url = self.smart_insight_url + '/definitions/' + self.definition_id + '/components/'
            logging.info("URL {}".format(query_url))
            r = s.post(url=url, json=body, headers=headers)
            r.raise_for_status()
        else:
            logging.error("EMAIL ERRATA: Inserire una email corrispondente ad un utente Askdata")


    def edit_card(self, icon="", name=""):

        if(icon==""):
            icon = self.icon
        else:
            self.icon=icon

        if(name==""):
            name = self.name
        else:
            self.name=name

        body={
            "icon": icon,
            "name": name,
            "slug": self.slug
        }

        url = self.smart_insight_url+"/definitions/"+self.definition_id

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.put(url=url, json=body, headers=headers)
        r.raise_for_status()
        self.components = r.json()["components"]


    def get(self):

        get_url = self.smart_insight_url+"/definitions/"+self.definition_id+"/card"

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.get(url=get_url, headers=headers)
        r.raise_for_status()


        return r.json()["attachment"]

    def delete_component(self, component_id):

        for component in self.components:
            if(component["id"]==component_id):
                self.components.remove(component)

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        query_url = self.smart_insight_url + '/definitions/' + self.definition_id + '/components/'+component_id
        logging.info("URL {}".format(query_url))
        r = s.delete(url=query_url, headers=headers)
        r.raise_for_status()

    def schedule_daily(self, channel_slug, hours, minutues, seconds):

        cron = seconds + " " + minutues + " " + hours + " * * *"

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        url = self._base_url_askdata + '/smartfeed/channels?agentId=' + self.agent_id + '&slug=' + channel_slug
        r = s.get(url=url, headers=headers)
        r.raise_for_status()

        channel_id = r.json()[0]["id"]

        url = self.smart_insight_url + "/definitions/" + self.definition_id + "/publishing/"

        body = {
            "schedulingCron": cron,
            "enabled": True,
            "destination": {"channels":[channel_id],"code":None,"name":None,"icon":None,"visibility":None,"queryId":None,"empty":None},
            "condition": "always",
            "advancedConditions": None}


        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.post(url=url, json=body, headers=headers)
        r.raise_for_status()


    def schedule_monthly(self, channel_slug, day_of_month, hours, minutues, seconds):

        """day_of_week: day of the week in format MON, TUE, WED, THU, FRI, SAT, SUN"""

        cron = seconds + " " + minutues + " " + hours + day_of_month + " * ?"

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        url = self._base_url_askdata + '/smartfeed/channels?agentId=' + self.agent_id + '&slug=' + channel_slug
        r = s.get(url=url, headers=headers)
        r.raise_for_status()

        channel_id = r.json()[0]["id"]

        url = self.smart_insight_url + "/definitions/" + self.definition_id + "/publishing/"

        body = {
            "schedulingCron": cron,
            "enabled": True,
            "destination": {"channels":[channel_id],"code":None,"name":None,"icon":None,"visibility":None,"queryId":None,"empty":None},
            "condition": "always",
            "advancedConditions": None}


        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.post(url=url, json=body, headers=headers)
        r.raise_for_status()

    def schedule_weekly(self, channel_slug, day_of_week, hours, minutues, seconds):
        """day_of_week: day of the week in format MON, TUE, WED, THU, FRI, SAT, SUN"""

        cron = seconds + " " + minutues + " " + hours + " ? * " + day_of_week

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }
        url = self._base_url_askdata + '/smartfeed/channels?agentId=' + self.agent_id + '&slug=' + channel_slug
        r = s.get(url=url, headers=headers)
        r.raise_for_status()

        channel_id = r.json()[0]["id"]

        url = self.smart_insight_url + "/definitions/" + self.definition_id + "/publishing/"

        body = {
            "schedulingCron": cron,
            "enabled": True,
            "destination": {"channels": [channel_id], "code": None, "name": None, "icon": None, "visibility": None,
                            "queryId": None, "empty": None},
            "condition": "always",
            "advancedConditions": None}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        r = s.post(url=url, json=body, headers=headers)
        r.raise_for_status()
