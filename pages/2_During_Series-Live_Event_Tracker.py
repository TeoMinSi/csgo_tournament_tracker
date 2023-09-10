import sys
import json
import pandas as pd
from datetime import date
import pandas as pd
import re

import streamlit as st
import streamlit.components.v1 as components
import streamlit_highcharts as hct

from highcharts import Highchart
from highcharts_core.chart import Chart
from highcharts_core.global_options.shared_options import SharedOptions
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.plot_options.bar import BarOptions
from highcharts_core.options.series.bar import BarSeries
from copy import deepcopy

import altair as alt


import plotly.express as px  # interactive charts
import time
from pandas.api.types import is_float_dtype

sys.path.append('../')
from utils import utils

# Load events jsonl file
def load_state():
    with open('../CCT-Online-Finals-1/2578928_state.json', 'r') as json_file:
        state = json.load(json_file)
    return state

@st.cache_data  # 👈 Add the caching decorator
def load_events():
    with open('../CCT-Online-Finals-1/2579089_events.jsonl', 'r') as jsonl_file:
        json_list = list(jsonl_file)
    return json_list


full_events = load_events()
st.button("Rerun")
last_event = json.loads(full_events[5346])["events"][-1]

state = load_state()

match_date = state["startedAt"].split("T")[0]
format = state["format"].replace('-', ' ').capitalize()

# List of Event IDs for Round 2
r2_eid_list = ['3bb88790-d6b5-4944-b6df-b3663330c2ff', '1b9802ec-a935-42c0-8396-83a7a3768d2c', 'e2f57ccd-7882-4337-b125-b203a398721e', '3b1adf9f-98d2-49dd-94e8-09c51ef027a9', 'f730a1d1-0010-40cf-8e2c-ec451eaf23e5', '4dcecb0d-d074-4004-a22a-a7c1167c44e1', '8d4634cf-5a90-4938-8f57-dd94f301c0bd', 'c785ed45-9b12-4b7f-851c-465cdd4f8f3a', 'a93a5dab-2f6f-44d6-8355-419d4f5f1ba9', '73ac03f3-795b-4bf9-9543-7baad884b1fc', '81d78168-4c61-4a00-9a1c-b95046aaf555', 'cd454282-eadb-414f-81b6-04c2b3c91672', 'dbdad42d-249b-4836-a92f-7537231ac3cd', '627fda3c-4b57-44ea-8b65-2aae7b8ddd24', 'b9d37c61-9c72-471e-a314-781e64bd9d7a', 'c5f4d3df-917d-4380-beae-781d5b44886e', '2a798fd8-ed28-4499-a4b5-54f625ef31bc', '2450b615-96ee-4976-bc44-4a7955f0f5b9', 'dfbeef63-5409-4042-903a-61df4ae781b1', '03a2192e-c944-4a4e-8c41-ccb06c7689c4', '5f5e35fe-f6a1-4b63-b8b1-b92a9afc998f', 'f3063898-4623-40fb-910f-c2f8e1d23df3', '52df1aab-56e3-4f66-8732-e8e395ee76ba', 'ce313124-1405-4a9e-a248-cc839e6a338d', '3e7a2aa0-8994-488c-9f8e-8d7738353505', 'de27aec6-390d-49f0-a1c5-88b6f30e15ea', 'e2a29785-581a-43d4-85f2-3dfce662b8e0', 'a8c2295a-f565-47de-b517-6465e7d9cf45', 'e8cfb874-ec5b-41aa-b84f-18779c08d5e4', '36b87756-c525-4a75-8fc9-9b23c537239e', '1fa384b9-3240-45f4-b2b4-35aaad22231c', 'e2963b00-59b5-472b-9ea6-f02058cf2fc8', 'bc2a2712-6411-45e9-b477-866135d32a3f', '730cc28f-30a5-49e7-b4d2-7057def37b63', '9a20a001-0651-4975-b44a-220a79fa03d7', 'e174fb6d-5805-4017-b0e4-8eb838a09a91', '386b208e-0f7d-4f02-9e1e-bba07a6119ab', 'ab15d1bc-07b9-46ad-80bb-70570fdd02f6', 'de9cd0dc-cb88-4e1f-b957-090af7b09526', '674ff49f-baea-4c7c-9372-47e8dbf51fc4', 'b60c977d-cf69-4692-b085-19d52197a996', '8ad25215-de7c-4952-a230-3451d864338f', 'e2ccacdf-eb4c-4a53-bc05-5713663b1ce4', 'e5d3b97f-383a-4852-9b5c-41dc88259175', '44886978-2456-4e5f-b4a7-8dd0585242bf', '76ee59b9-b29c-4943-ab10-3e73ed326d0a', '0ea59f6d-a7f9-4bf6-b6db-293257fcd9eb', '69417807-8303-4ea4-85a5-43907e449b5e', '90ee06fb-6ee9-4a25-a819-4893e7a76d8e', '3d380ecc-85b8-41d2-9ac3-fc15c8b213e3', '8c9e6e89-f6b3-42e1-b107-050ece4bae83', 'de71caac-3994-4743-8761-5a4300ae9878', '030fd441-9d0c-4177-810a-30051ed4644c', '22963536-2a91-458e-bb6e-0cc83f06a19f', '1ce3128c-9e4f-41ef-8f3a-b0122630b89f', 'a54390fd-0e49-4bef-8567-22d71d162423', '008ee0f5-3fdc-4d3c-844b-5e1490368883', '17cfd64d-d40a-4300-8c53-4922f7a42ea3', '90c9856c-23e2-4bdd-8996-79ba39c3898b', 'fe57157a-3e43-43ce-a5c5-1356d5096d59', '8ea82f8b-ab45-42fb-9cb1-fe90b8246923', 'd9e7735d-ea9d-41a5-9971-dc77178bec1c', '8c062b3b-624c-422c-9997-631f2b4ee045', 'c99091fb-e18b-418e-a93d-6338907b084a', 'f087de43-8f01-4dc9-9c79-13339454db95', 'eff4e72c-be30-4b8b-9bf9-3fe5661dad64', '0f21b4f6-e31b-46aa-8377-a3bed7dacfe5', '82c5dd64-d0f6-4413-b156-d0ce28fb49e2', 'bf5ce6c6-86ef-49bb-9bbe-690dafd33e42', 'fff8c15a-7868-44ba-a036-947e3766d07c', '42fbeada-e083-4bcc-80f8-a307a9aca72e', '83e93b43-07cc-4c0f-b656-4b208a8d1ba8', '13d1a95e-e5de-4d00-839e-a10ae7c77ea6', '1a6d5931-4fe1-446d-941d-86127bf2da1c', '50de27c8-01ff-45d3-a143-8baa80d695b0', '2457f7de-daf8-4f48-9bb2-6984934aa4c2', 'e532466a-d9cd-47c0-97b6-ec85d97c96a3', '07ed236d-baf7-4fab-9f49-2f5bcb6367d7', '83519a60-6fb3-4c2e-96f9-460c1acb2472', '3eb6828d-9664-4329-b46d-f355b564fb36', '899c5157-fbc8-46ae-9df3-cc9b09f896f6', 'c3b0483b-eda2-41b2-915a-fffceb922753', '4788a6e8-5f26-4288-bf74-801706f92420', 'cdafb888-e229-47b7-9bda-16fd61bd17ee', 'ad23a32d-86a1-4111-b48d-60fd76ac4fe3', '77c655a9-9c9b-4360-8cde-cbe0845af218', '8834adc2-860a-4db5-8003-ae6fd0841d52', '5fb13435-db10-4ad9-83a1-1eda7ee0600d', 'ae5b61b9-e085-4379-a5f4-b1ca453884fe', '9c13a7aa-fd4d-45b9-9749-f4fd05c5df78', 'c6d785dc-dad7-4662-b954-097bad9358d8', 'aa111fe9-2f69-4c42-a694-d51e244711b4', 'c9ce9c60-31b1-4b2e-81d9-97165f403483', 'aa0d2e15-5dfb-4497-9bf3-3b348eec6a18', '9e92ba48-85ae-4ee1-9c48-e17f9672de0e', 'b9cc15f5-715e-4449-ad70-555cd46c34e8', '34007943-82c5-4c23-8944-6a35e8912a19', '8f198336-d4ea-474c-8f9f-348e72a32716', '6b92fce7-f1e0-4370-8d6b-90ad4ccab9d2', '70a3b8d1-850c-4873-96c6-65e7ca7a6f91', '47f945d5-d6aa-4c4f-b985-b707ae7cc7c3', '7f729958-b458-4b84-8b77-1b2bc3d1faa3', 'f899d072-55b3-49b4-95c3-437b1d5c5eb7', '4bf81491-e158-4f8b-81b4-1c6216b87562', 'bea49019-eaac-418a-b05d-3c853a4fb4d0', '011b621f-e6c0-4465-859e-3af42e240f94', '6d4bc6f5-4747-49e7-a70f-0f6737290bfb', '50d292a7-264c-439b-a28b-2f0584f70ca8', '82b8e917-1376-468a-9f87-50f65fa13e44']
# r2_eid_list_map2 = ['f7fb9602-7b18-4efb-b395-7bd6217bad8f', '5978e257-ef99-4c62-979a-35d664aa3995', 'f88b72e2-1407-4e5d-8aa0-a5b3c6819552', '612cfdca-615f-45d7-a5cb-a62a02bea5d3', '9118e5c6-9d07-45fd-bc8c-c28f9d5701ce', '33bb6594-de37-480c-91ad-82d15f274de5', '4e7f56b6-1e05-400b-8a68-9c621e03b182', 'd8171da5-1a74-470e-bdac-adfb69481e7b', '601577a5-b985-4695-ab44-95e62e24b394', '8d5d0e83-3a3c-457e-b6ae-e808fc8e9181', '0499e54c-06db-4021-884c-f98aab7ae6fa', '353a287e-ad44-4c8c-9fc7-1d683d7f8d9c', 'f484c1c5-b85c-4c9b-951d-a8c02f89a303', '3de22ef8-75df-4c5d-975b-cc208bef70d3', '81c84f9f-d69d-4b1d-84cf-0610f65bc789', '3c5ce637-77bc-49fa-ab32-2ede2ecbe5ee', 'e4829f7d-93a5-46a1-b7d8-f5cc1b815bf0', 'ee1b1adb-cbfe-4da4-8298-43bb729bc162', 'bec7f982-a5df-4172-88c8-16276ddfe54d', 'f8d0af99-0c67-475c-a068-6717b1ecb024', '92d7bad2-5489-4763-9410-6967e92e9797', 'bb5f87c8-2526-4bfa-adbd-f95068858d6d', '72a17460-6039-495d-9180-8d56f5968ae0', 'af95b3f4-663a-45c6-b748-62675d535d56', 'ab9f93a9-92dd-48ee-8f6d-960e0dfc1a63', 'd223293f-960c-4088-91c4-0d34e4b6d5ed', 'ec2f5c67-015b-4731-bfaf-7bd6b35a7c5c', '57d4947a-90a4-47e1-b5d5-8f55c98a7ad3', '0c80b5bf-5b8a-4cc7-9e35-3fd5691d75c9', '180a38e8-5526-4d4f-ad97-4594bbd17d5f', '1b303a67-c656-4f8f-906e-1369995edadc', 'e9ddfbed-003b-4327-a1d1-4663bea9bc8d', 'bc4d3165-cdde-44db-acfb-94df9f68f11b', 'a0d4787e-c31e-4387-9879-8b4fcd597081', '04f01830-2910-4a88-a866-ddd2e70dcafc', 'cae28113-c544-495c-b744-17a73e6f9b13', 'a608f4e2-baee-4eda-84a4-35e1d38b4269', 'cca8104c-6b3c-4a2d-97b1-6ac0cb7638cf', 'b6ec1ada-6559-4b0a-bdd5-9a0031492196', '9679f0b8-72c8-40fc-b1a5-1553330dde79', 'e010a966-27eb-4802-87c9-ef46f843b31f', '3d651e59-5dce-46d5-aec9-74b85fc13ffb', 'e4e19680-67b0-4409-a502-2b069bfe73b6', 'f97987b0-3bb4-4b95-b641-5180c3a96f31', 'cc70fdbf-0e28-465e-a86c-ba22ed81a243', 'b83fdedc-a099-4608-a752-ba3c93d9fcca', '697c5b71-4ec8-4f69-ae6c-487596abd116', 'bac61ed5-f8f5-4c79-bc48-adccdd3182b2', '0c172897-0a99-4cbc-9c49-a657f4fa58f3', '04cf294f-6937-4da9-a30d-b04117f1b317', '9489c06b-57b0-49c5-bf40-28004dd5e695', 'd53228d1-94ed-438b-a3c5-6c87fba5cfdc', '08ea0145-0094-4f1d-a253-9821fc6ec26e', '271e1593-80ee-4486-a4ed-f10a797d95a6', 'd75988bd-565d-4660-bfab-a6515b962437', '946de53e-cdff-479d-a3bf-a4381f1b28fc', '4a483322-af64-4420-9d4a-38da00640d8e', 'bb6fbe56-0bcc-416f-b879-ca1e9889f28f', 'df784381-9eb7-46da-84cb-a1b3dbaf6761', '903a531f-aec2-47bb-be16-2f76a1c1c6a8', 'f53c8a8c-ee00-46ef-afb6-7f821bd11a7c', 'ed205303-58e0-4351-84af-0069d4595341', '879a2d75-3541-4f57-973d-8b546185ed59', 'ddeaeacd-81cc-48d5-a870-dee804e5e960', '9f958654-4e38-40cb-9dca-7a63a041755b', '98e8ecc9-9dd2-43eb-8f0a-55b54631ec7c', '36d15b33-055d-46dc-81de-9afa872512d9', 'c78e14ac-2448-40c6-8e23-aee4e0d984a4', 'a00e4256-86ed-4c12-9deb-93ebe4eba20e', '3cd29822-7c3c-4206-99bc-dff254a1ddd6', '72b799ce-0d37-4993-bfbf-52f490dfdf31', 'a64ad328-30ff-495e-b67f-72b9a3d1e309', 'e4117b5c-d0c7-417b-89df-aa5db414e3d9', '10cd2dac-bec8-47b8-8128-3fed70c1c5e9', '54428b60-0682-42b2-bf74-8442f505a116', '723efbc2-715d-4915-8cd3-2c0423a3e086', '4b0b13d9-9b63-4273-8792-30f97ef90206', '04a3ab47-ab8f-49f7-97e0-9a327363f30a', '263c4161-da09-4ca6-83ad-6bb54686aab4', '687d4c0d-e3a5-43b2-a2b6-dd1412bd0d3e']

# Get round number
for i in range(4, len(full_events) - 1):
    json_event = json.loads(full_events[i])["events"][-1]
    if json_event["id"] == r2_eid_list[0]:
        round_num = json_event["seriesState"]["games"][-1]["segments"][-1]["id"].replace('round-', '')
        break

# Get list of Round 2 events
r2_events_list = []
for i in range(4, len(full_events)-1):
    loaded_events = json.loads(full_events[i])
    if loaded_events["events"][-1]["id"] in r2_eid_list:
        r2_events_list.append(loaded_events)

primary = ['mag7','nova','xm1014','mac10','mp9','ak47','aug','famas','galilar','m4a1','m4a1_silencer','ssg08','awp','m249','negev','scar20','g3sg1','sg553','ppbizon','mp7','ump45','p90','mp5_silencer','sawedoff']
secondary = ['hkp2000','cz75a','deagle','fiveseven','glock','p250','tec9','usp_silencer', 'elite', 'revolver']
melee = ['knife','knife_t']

all_weapons = ["mag7", "nova", "xm1014", "mac10", "mp9", "ak47", "aug", "famas", "galilar", "m4a1", "m4a1_silencer", "ssg08", "awp", "m249", "negev", "scar20", "g3sg1", "sg553", "ppbizon", "mp7", "ump45", "p90", "mp5_silencer", "sawedoff", "hkp2000", "cz75a", "deagle", "fiveseven", "glock", "p250", "tec9", "usp_silencer", "elite", "revolver", "knife", "knife_t"]
all_weapons_url = ["https://drive.google.com/uc?export=view&id=1TYwFThhXuwl4loAL23h3TYudsPFAB6wG", "https://drive.google.com/uc?export=view&id=1TzSoDC8qoePLn9BY8JkBGWuFkXfj9LYb", "https://drive.google.com/uc?export=view&id=1VGoZbAwa8j8v6YvDlTzXv-e2cc6-I7QN/view?usp=sharing", "https://drive.google.com/uc?export=view&id=16nSK03F4OVcfUrtTvPcQG5ZLZ4vx6-wG", "https://drive.google.com/uc?export=view&id=1-bNHjjeFZr9cPTQ0dRxmpF--RA8wM2k-", "https://drive.google.com/uc?export=view&id=1wXXNUghdmk-Z5zHcfLo_R17jS0vjEgX0", "https://drive.google.com/uc?export=view&id=19VudK8bk9ILrtR5GxUanhT569Mdn--Uo", "https://drive.google.com/uc?export=view&id=19FCk0PvrXjRDMuohrEKhEmL4qb_glKc9", "https://drive.google.com/uc?export=view&id=19Q8-gM1x1XMY-CBXoJGHDkeDxpSmV9Q2", "https://drive.google.com/uc?export=view&id=1bemYjPcgAklZUSSDWpwucN_IbSejBazX", "https://drive.google.com/uc?export=view&id=1ee4uA887OqwiYx6SM-uuMeHccGOYAMJX", "https://drive.google.com/uc?export=view&id=1_nNCLtXccij1rd9VZbx2QSSO7m1OCUMW", "https://drive.google.com/uc?export=view&id=1pmrxVQvIxN3BlQMdB6_3AiHdg6Rhc_4T", "https://drive.google.com/uc?export=view&id=1elHN1KEuyI0QwqZbDC1fkeWr7auhYf3h", "https://drive.google.com/uc?export=view&id=1tWjoczrhGyhwENXBpxZ7O-_OufVxPT0e", "https://drive.google.com/uc?export=view&id=1ycR8w8gbw2lOUy1gFhrEizzn75fDO6tn", "https://drive.google.com/uc?export=view&id=1IRutvTpczBbHYm8DCeQP7a0d3hMuN9lZ", "https://drive.google.com/uc?export=view&id=18nk-5PcL_ABDlYjXglhm-R9_0avMh98f", "https://drive.google.com/uc?export=view&id=14WytS4VfGRxZm_d5cqfR8AZ-SxpWPE6i", "https://drive.google.com/uc?export=view&id=1tMGhG61oLDiOa2u_a2UsDOA50aagprBq", "https://drive.google.com/uc?export=view&id=1Y84_Mcp-t-RgVP5fLI0KVPsIZNlCYYLd", "https://drive.google.com/uc?export=view&id=14e-YQhcPTajsolMR3GIIOEHVM164L7SA", "https://drive.google.com/uc?export=view&id=1zCjIZ7cJ7_NW1ArQX1-8DLCjM3x43Ar5", "https://drive.google.com/uc?export=view&id=1oYgGvY8RyviQ5zhe4AoEdxUohFkJLBPS", "https://drive.google.com/uc?export=view&id=1Wy8RlSmKPP53t6jjrglFu-WmTG47k-4w", "https://drive.google.com/uc?export=view&id=1wj5wWAmAUGl349gyLVKjjFedBnDU6SPD", "https://drive.google.com/uc?export=view&id=1d3RfyfITMwq7aNtkgC86HS2ZtdXQbb1L", "https://drive.google.com/uc?export=view&id=18IDDh2iF4mUMhr0pVU-qdJaZSjJKHcOr", "https://drive.google.com/uc?export=view&id=1OB67qm_fFOailqianmj3-thghFwHVKKF", "https://drive.google.com/uc?export=view&id=1-yVlvPxdzk9Cxt1qM6LNsix1NqO4-7lj", "https://drive.google.com/uc?export=view&id=1cT16kX_t-vnkzqXqMivtW9Y3xNf26kQT", "https://drive.google.com/uc?export=view&id=1EkJSBiFtu-1TQrMo_9myBAgU2kJDcwcF", "https://drive.google.com/uc?export=view&id=1E8_HAVSMDbL4fKfdZ1qKNX__kIAuaQtl", "https://drive.google.com/uc?export=view&id=1scG9H9uaFDhVwfysSTrlrxh941al7ZeF", "https://drive.google.com/uc?export=view&id=1f_NHYPBLgHNC-KJbx8XD9igoai1BbJ8M", "https://drive.google.com/uc?export=view&id=1KH5UBZsKzkwjTO-AXkeuQjxcNMQIn32N"]
weapons_dict = dict(zip(all_weapons, all_weapons_url))

def get_match_result(state_dict, key):
    teams = state_dict['teams']
    result_dict = {}
    for team in teams:
        team_name = team['name']
        value = team[key]
        result_dict[team_name] = value
    return result_dict

def get_weapons_img_path(df, weapons_col=["loadout.primary", "loadout.secondary"]):
    """ Gets image path from weapon name """
    url = "https://raw.githubusercontent.com/jfcheong/csgo_tournament_tracker/feature/weapons/assets/%s.png"
    for col in weapons_col:
        img_col = [url % (str(val)) if val else "" for val in df[col]]
        df[f"{col}.img"] = img_col
    return df

def format_items(loadout, df):
    cols = [col for col in loadout.columns.str.startswith('loadout.')
                            if col not in ["loadout.primary", "loadout.secondary"]]
    print(cols)
    items = loadout.loc[:, cols].values.tolist()
    df["Items"] = [cleaned if (cleaned := [elem for elem in sublist 
                                                    if elem is not None])
                        else None for sublist in items]
    return df

# Data Engineering

match_result = get_match_result(state, key='score')
final_teams = list(match_result.keys())

def get_player_state(event, return_df=True):
    """ Returns df of players' most updated state """
    players = []
    event = deepcopy(event)
    teams = event["seriesState"]["games"][-1]["teams"]
    for team in teams:
        for _player in team["players"]:
            player = {}
            player["team"] = team["name"]

            # Flatten objectives
            objectives = {}
            for objective in _player["objectives"]:
                objectives[objective["id"]] = objective["completionCount"]

            # Flatten loadout
            player_loadout = {"loadout":
                              {
                                  "primary":None,
                                  "secondary":None,
                                  "melee":None,
                                  "helm":None,
                                  "kevlarVest":None,
                                  "bomb":None,
                                  "defuser":None,
                                  "decoy":None,
                                  "flashbang":None,
                                  "hegrenade":None,
                                  "incgrenade":None,
                                  "molotov":None,
                                  "smokeGrenade":None,
                                  "taser":None
                                  }
                              }

            for item in _player["items"]:
                item_id = item["id"]
                if item_id in primary:
                    player_loadout["loadout"]["primary"] = item_id
                elif item_id in secondary:
                    player_loadout["loadout"]["secondary"] = item_id
                elif item_id in melee:
                    player_loadout["loadout"]["melee"] = item_id
                else:
                    player_loadout["loadout"][item_id] = item_id

            # Remove useless fields
            redundant_fields = ["statePath", "character", "items", "externalLinks", "objectives"]
            for field in redundant_fields:
                _player.pop(field)

            player.update(_player)
            player.update(objectives)
            player.update(player_loadout)
            players.append(player)

    players = sorted(players, key=lambda x: (x["team"], x["name"]))
    if return_df:
        return pd.json_normalize(players)
    else:
        return players

def get_player_health_armor(event):
    """ Returns df of players' most updated health and armor values """

    required_fields = ["currentHealth", "currentArmor"]
    players = get_player_state(event).filter(items=(["team", "name"] + required_fields))
    return players

def get_player_economy(event):
    required_fields = ["money", "inventoryValue", "netWorth", "loadout.primary", "loadout.secondary"]
    players = get_player_state(event).filter(items=(["team", "name"] + required_fields))
    return players

def get_player_kdao(event):
    required_fields = ["kills", "killAssistsGiven", "deaths", "beginDefuseWithKit", "beginDefuseWithoutKit", "defuseBomb", "explodeBomb", "plantBomb"]
    players = get_player_state(event).filter(items=(["team", "name"] + required_fields)).fillna(0)
    for col in ["beginDefuseWithKit", "beginDefuseWithoutKit", "defuseBomb", "explodeBomb", "plantBomb"]:
        players[col] = players[col].astype('Int64')
    return players

def get_loadout(event):
    required_fields = ["loadout.*"]
    players = get_player_state(event).filter(regex="|".join(["^team$", "^name$"] + required_fields))
    return players

event = json.loads(json_list[2443])["events"][-1]

economy = get_player_economy(event)
loadout = get_loadout(event)

# Common Variables
team1=economy["team"].unique()[0]
team2=economy["team"].unique()[-1]
forze_url = "https://preview.redd.it/new-forze-logo-v0-x31u5t3sg8ba1.png?width=600&format=png&auto=webp&s=041b6912e65d06e150219f63f79dc05b911e9c04"
ecstatic_url = "https://img-cdn.hltv.org/teamlogo/Ox1eFAB6o8VM6jwgPbQuks.svg?ixlib=java-2.1.0&s=66680f6d946ff4a93bc311f3bbab8d9e"

# Streamlit Visuals
## Top Header Section
st.title("During Series")

st.subheader(f"Date of Match: {match_date}")
st.subheader(f"Match format: {format}")
st.subheader(f"Round: {round_num}")

components.html(
    f"""
    <div style="height:200px; background-color:#F0F2F6;display: grid;column-gap: 2%;grid-template-columns: auto auto;padding: 10px;">
        <div style="text-align: center;">
            <h3 style="color:black;font-family: Cambria, Georgia, serif;">{final_teams[0]}</h3>
            <img style="height:50px;" src="{ecstatic_url}" />
        </div>

        <div style="text-align: center;">
            <h3 style="color:black;">{final_teams[1]}</h3>
            <img style="height:50px;" src="{forze_url}" />
        </div>
    </div>

    """
)

## Tabs
preround_tab, duringround_tab, postround_tab = st.tabs(["Pre-Round", "During Round", "Post-Round"])

### Pre-Round Tab
with preround_tab:
    st.header(f"Round {round_num}")
    st.subheader("Pre-Round Economy", divider='rainbow')

    # Format economy df
    economy = format_items(loadout, economy)
    economy = get_weapons_img_path(economy)


    economy.rename(columns= {'name':'Player',"loadout.primary": "Primary", 
                            "loadout.secondary":"Secondary", 
                            'money':'Money',
                            "inventoryValue": "Inventory Value"}, 
                            inplace = True)

    # Split df by team
    team1_economy = economy[economy["team"]==team1]
    team1_total = team1_economy["Inventory Value"].sum()

    team2_economy = economy[economy["team"]==team2]
    team2_total = team2_economy["Inventory Value"].sum()

    # Display
    col1, col2 = st.columns([3,2])
    with col1:
        st.subheader(f"{team1}")
    with col2:
        st.write(f"Total Inventory Value: {team1_total}")
    st.dataframe(team1_economy, 
                column_config={
                    "loadout.primary.img": st.column_config.ImageColumn(
                        "Primary Weapon", help="Primary Weapon"
                    ),
                    "loadout.secondary.img": st.column_config.ImageColumn(
                        "Secondary Weapon", help="Secondary Weapon"
                    )
                },
                hide_index=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.subheader(f"{team2}")
    with col2:
        st.write(f"Total Inventory Value: {team2_total}")
    st.dataframe(team2_economy, 
                column_config={
                    "loadout.primary.img": st.column_config.ImageColumn(
                        "Primary Weapon", help="Primary Weapon"
                    ),
                    "loadout.secondary.img": st.column_config.ImageColumn(
                        "Secondary Weapon", help="Secondary Weapon"
                    )
                },
                hide_index=True)

### During Round Tab
with duringround_tab:
    def get_player_kda(kda_df, latest_round_df, player_df, index):
        kda_filtered = kda_df.loc[(kda_df['name'] == player_df.loc[index, 'name']) & (
                kda_df['map_name'] == latest_round_df.loc[latest_round_df['side'] == 'terrorists', 'map'].values[0])]
        kda_str = kda_filtered["kills"].values[0].astype(str) + "/" + kda_filtered["deaths"].values[0].astype(
            str) + "/" + kda_filtered["killAssistsGiven"].values[0].astype(str)
        return kda_str

    placeholder = st.empty()
    placeholder2 = st.empty()
    kill_log_list = []
    obj_log_list = []

    for event_num in range(len(r2_events_list)):
        selected_event = r2_events_list[event_num]["events"][-1]
        pha = utils.get_player_health_armor(selected_event)
        kda = utils.get_player_kdao(selected_event, 'game')
        gti = utils.get_team_info(selected_event, 'round')
        ps = utils.get_player_state(selected_event, 'game')
        lo = utils.get_loadouts(selected_event)
        gti_latest_round = gti.loc[gti['round_seq'] == int(round_num)].reset_index(drop=True)

        with placeholder.container():
            col1, col2 = st.columns(2)
            st.text(event_num)

            with col1:
                st.subheader("Kills", divider='rainbow')

                # for event in r2_events_list:
                #     if event["events"][-1]["type"] == "player-killed-player":
                #         actor, target, action, weapon, round_time, action_log, event_log = utils.get_event_log(event["events"][-1])
                #         kill_list = [round_time, actor, weapon, target]
                #         kill_log_list.append(kill_list)

                if selected_event["type"] == "player-killed-player":
                    actor, target, action, weapon, round_time, action_log, event_log = utils.get_event_log(selected_event)
                    kill_list = [round_time, actor, weapon, target]
                    kill_log_list.append(kill_list)

                kill_log_list.sort(reverse=True)
                kills_df = pd.DataFrame(kill_log_list, columns=['round_time', 'actor', 'weapon', 'target'])
                kills_df['weapon'] = kills_df['weapon'].map(weapons_dict)
                st.dataframe(kills_df, column_config={"weapon": st.column_config.ImageColumn(label="weapon", width='small')},
                             hide_index=True, use_container_width=True)

            with col2:
                st.subheader("Objectives", divider='rainbow')

                # for event in r2_events_list:
                #     if re.search(r"\bplayer.*completed.*\b", event["events"][-1]["type"]):
                #         round_time, action_log, event_log = utils.get_event_log(event["events"][-1])
                #         obj_list = [event_log]
                #         obj_log_list.append(obj_list)

                if re.search(r"\bplayer.*completed.*\b", selected_event["type"]):
                    round_time, action_log, event_log = utils.get_event_log(selected_event)
                    obj_list = [event_log]
                    obj_log_list.append(obj_list)

                obj_log_list.sort(reverse=True)
                obj_df = pd.DataFrame(obj_log_list, columns=['objective_log'])
                st.dataframe(obj_df, hide_index=True, use_container_width=True)

            # Players' Info Section
            st.subheader("Players' Info", divider='rainbow')
            colors = ['#edb5b5', '#52c222']
            with st.container():
                # st.image("https://drive.google.com/uc?export=view&id=13PSGt16GwmH4SxLK1vJEObH2i6OL3W7Z")
                components.html("""
                <div style="text-align: center;">
                        <h4 style="color:black;font-family: Cambria, Georgia, serif;">Legend</h4>
                        <img style="height:50px;" src="https://drive.google.com/uc?export=view&id=13PSGt16GwmH4SxLK1vJEObH2i6OL3W7Z" />
                    </div>
                """)

            col_t, col_ct = st.columns(2)

            with (col_t):
                st.markdown("#### Terrorists")
                team_t = gti_latest_round.loc[gti_latest_round['side'] == 'terrorists', 'name'].values[0]
                st.markdown(f"##### Team: {team_t}")
                pha_filtered = pha.loc[pha['team'] == team_t].reset_index(drop=True)
                df_t = pha_filtered.set_index('name')
                df_t = pha_filtered.pivot(index="name", columns="team", values=['currentHealth', 'currentArmor']).reset_index()
                bar_chart_day = alt.Chart(df_t).transform_fold(['currentHealth', 'currentArmor']) \
                    .mark_bar(clip=True).encode(x=alt.X('value:Q', stack='zero', scale=alt.Scale(domain=(0, 200)), title=''),
                                                y=alt.Y('name', title=''),
                                                color=alt.Color('key:N').legend(None),
                                                ).properties(width=300, height=200
                                                             ).repeat(layer=["currentHealth", "currentArmor"]
                                                                      ).configure_range(category=alt.RangeScheme(colors))
                bar_chart_day
                # st.table(pha_filtered)
                # st.table(df_t)
                # TODO: fix
                # pha_filtered_player = pha_filtered.loc[pha_filtered['name'] == 'Jerry', ['currentHealth', 'currentArmor']]
                # st.table(pha_filtered_player)

                for i in range(len(pha_filtered)):
                    lo_filtered = lo.loc[(lo['team'] == team_t) & (lo['name'] == pha_filtered.loc[i, 'name'])].filter(like='loadout').reset_index(drop=True)
                    lo_mapped = lo_filtered[['loadout.primary', 'loadout.secondary', 'loadout.melee']].applymap(weapons_dict.get).rename(columns={'loadout.primary': 'Primary', 'loadout.secondary': 'Secondary', 'loadout.melee': 'Melee'})
                    st.markdown(f"##### Player {i+1}: {pha_filtered.loc[i, 'name']} ({get_player_kda(kda, gti_latest_round, pha_filtered, i)})")
                    st.dataframe(lo_mapped, column_config={
                        "Primary": st.column_config.ImageColumn(label="Primary", width='small'),
                        "Secondary": st.column_config.ImageColumn(label="Secondary", width='small'),
                        "Melee": st.column_config.ImageColumn(label="Melee", width='small'),
                        # "loadout.helm": st.column_config.ImageColumn(label="loadout.helm", width='medium'),
                        # "loadout.kevlarVest": st.column_config.ImageColumn(label="loadout.kevlarVest", width='medium'),
                        # "loadout.bomb": st.column_config.ImageColumn(label="loadout.bomb", width='medium'),
                        # "loadout.defuser": st.column_config.ImageColumn(label="loadout.defuser", width='medium'),
                        # "loadout.decoy": st.column_config.ImageColumn(label="loadout.decoy", width='medium'),
                        # "loadout.flashbang": st.column_config.ImageColumn(label="loadout.flashbang", width='medium'),
                        # "loadout.hegrenade": st.column_config.ImageColumn(label="loadout.hegrenade", width='medium'),
                        # "loadout.incgrenade": st.column_config.ImageColumn(label="loadout.incgrenade", width='medium'),
                        # "loadout.molotov": st.column_config.ImageColumn(label="loadout.molotov", width='medium'),
                        # "loadout.smokeGrenade": st.column_config.ImageColumn(label="loadout.smokeGrenade", width='medium'),
                        # "loadout.taser": st.column_config.ImageColumn(label="loadout.taser", width='medium')
                    }, hide_index=True)

            with (col_ct):
                st.markdown("#### Counter Terrorists")
                team_ct = gti_latest_round.loc[gti_latest_round['side'] == 'counter-terrorists', 'name'].values[0]
                st.markdown(f"##### Team: {team_ct}")
                pha_filtered = pha.loc[pha['team'] == team_ct].reset_index(drop=True)
                df_ct = pha_filtered.set_index('name')
                df_ct = pha_filtered.pivot(index="name", columns="team", values=['currentHealth', 'currentArmor']).reset_index()
                bar_chart_day = alt.Chart(df_ct).transform_fold(['currentHealth', 'currentArmor']) \
                    .mark_bar(clip=True).encode(x=alt.X('value:Q', stack='zero', scale=alt.Scale(domain=(0, 200)), title=''),
                                                y=alt.Y('name', title=''),
                                                color=alt.Color('key:N').legend(None),
                                                ).properties(width=300, height=200
                                                             ).repeat(layer=["currentHealth", "currentArmor"]
                                                                      ).configure_range(category=alt.RangeScheme(colors))
                bar_chart_day
                # st.table(pha_filtered)
                # st.table(df_ct)
                for i in range(len(pha_filtered)):
                    lo_filtered = lo.loc[(lo['team'] == team_ct) & (lo['name'] == pha_filtered.loc[i, 'name'])].filter(like='loadout').reset_index(drop=True)
                    lo_mapped = lo_filtered[['loadout.primary', 'loadout.secondary', 'loadout.melee']].applymap(weapons_dict.get).rename(columns={'loadout.primary': 'Primary', 'loadout.secondary': 'Secondary', 'loadout.melee': 'Melee'})
                    st.markdown(f"##### Player {i+1}: {pha_filtered.loc[i, 'name']} ({get_player_kda(kda, gti_latest_round, pha_filtered, i)})")
                    st.dataframe(lo_mapped, column_config={
                        "Primary": st.column_config.ImageColumn(label="Primary", width='small'),
                        "Secondary": st.column_config.ImageColumn(label="Secondary", width='small'),
                        "Melee": st.column_config.ImageColumn(label="Melee", width='small'),
                        # "loadout.helm": st.column_config.ImageColumn(label="loadout.helm", width='medium'),
                        # "loadout.kevlarVest": st.column_config.ImageColumn(label="loadout.kevlarVest", width='medium'),
                        # "loadout.bomb": st.column_config.ImageColumn(label="loadout.bomb", width='medium'),
                        # "loadout.defuser": st.column_config.ImageColumn(label="loadout.defuser", width='medium'),
                        # "loadout.decoy": st.column_config.ImageColumn(label="loadout.decoy", width='medium'),
                        # "loadout.flashbang": st.column_config.ImageColumn(label="loadout.flashbang", width='medium'),
                        # "loadout.hegrenade": st.column_config.ImageColumn(label="loadout.hegrenade", width='medium'),
                        # "loadout.incgrenade": st.column_config.ImageColumn(label="loadout.incgrenade", width='medium'),
                        # "loadout.molotov": st.column_config.ImageColumn(label="loadout.molotov", width='medium'),
                        # "loadout.smokeGrenade": st.column_config.ImageColumn(label="loadout.smokeGrenade", width='medium'),
                        # "loadout.taser": st.column_config.ImageColumn(label="loadout.taser", width='medium')
                    }, hide_index=True)
            time.sleep(0.1)

        # st.table(ps)
        # st.table(lo)

        # # Dummy Variables
        # team1='TeamA'
        # team2='TeamB'
        # round_num=2
        #
        # event_time1 = '00:59'
        # event_log1 = 'FaZe Player A planted a bomb at Theta site'
        # event_time2 = '01:23'
        # event_log2 = 'FaZe Player B picked up a Deagle'
        # events_df = pd.DataFrame(columns=['event_time', 'event_log'])
        # events_df.loc[0] = [event_time1, event_log1]
        # events_df.loc[1] = [event_time2, event_log2]
        #
        # kill_time1 = '00:27'
        # kill_actor1 = 'FaZe Player C + D'
        # weapon1 = 'https://static.wikia.nocookie.net/cswikia/images/8/80/CSGO_AK-47_Inventory.png'
        # killed_actor1 = 'Navi Player A'
        # kill_time2 = '00:49'
        # weapon2 = 'https://static.wikia.nocookie.net/cswikia/images/f/f3/CSGO_Desert_Eagle_Inventory.png'
        # kill_actor2 = 'FaZe Player B'
        # killed_actor2 = 'Navi Player E'
        # kills_df = pd.DataFrame(columns=['kill_time', 'kill_actor', 'weapon', 'killed_actor'])
        # kills_df.loc[0] = [kill_time1, kill_actor1, weapon1, killed_actor1]
        # kills_df.loc[1] = [kill_time2, kill_actor2, weapon2, killed_actor2]
        #
        #
        # # Round Status
        # st.markdown(f"## Round {round_num}")
        #
        # # Events Log
        # st.subheader("Latest Events", divider='rainbow')
        # st.dataframe(events_df, hide_index=True)
        #
        # # Kills Log
        # st.subheader("All Kills", divider='rainbow')
        # st.dataframe(kills_df, column_config={"weapon": st.column_config.ImageColumn(label="weapon", width='small')},
        #              hide_index=True)
        #
        # # Player Health Log
        # st.subheader("Players' Stats", divider='rainbow')
        # col1, col2 = st.columns(2)
        # col1.markdown("### Terrorists")
        # df_t = pha.set_index('name')
        # df_t = pha.pivot(index="name", columns="team", values=['currentHealth', 'currentArmor']).reset_index()
        # bar_chart_day = alt.Chart(df_t).transform_fold(['currentHealth', 'currentArmor']) /
        #     .mark_bar(clip=True).encode(x=alt.X('value:Q', stack='zero', scale=alt.Scale(domain=(0, 100))),
        #                                 y=alt.Y('name'), color='key:N')
        # bar_chart_day
        # st.table(df_t)
        # col2.markdown("### Counter Terrorists")


### Post Round Tab
with postround_tab:
    # st.text("Hello")
    counter_list = [100, 238, 357, 476, 595, 714, 833, 952, 1071, 1190, 1309, 1428, 1547, 1666, 1785, 1904, 2023, 2142,
                    2261, 2380, 2499, 2618, 2737,
                    2856, 2975, 3094, 3213, 3332, 3451, 3570, 3689, 3808, 3927, 4046, 4165, 4284, 4403, 4522, 4641,
                    4760, 4879, 4998,
                    5117, 5236, 5355, 5474, 5593, 5712, 5831, 5993]
    placeholder = st.empty()
    placeholder2 = st.empty()
    map1 = "Inferno"
    for seconds in range(30):
        row = counter_list[seconds]
        event = json.loads(full_events[row])["events"][-1]
        map = utils.get_team_info(event, granularity="game").iloc[[-1]]["map"]
        with placeholder.container():
            try:
                map = utils.get_team_info(event, granularity="game").iloc[[-1]]["map"]
            except KeyError:
                event = json.loads(full_events[row])["events"][-2]
                map = utils.get_team_info(event, granularity="game").iloc[[-1]]["map"]

            full_df = utils.get_team_info(event, granularity="round")
            team_round_kills = full_df.loc[full_df.map_seq == (1)]

            st.subheader(map1)

            fig2 = px.line(data_frame=team_round_kills, y=team_round_kills['kills'], x=team_round_kills['round_seq'],
                           color=team_round_kills['name'])
            st.write(fig2)
            time.sleep(0.5)

        with placeholder2.container():
            player_kda = utils.get_player_kdao(event, granularity="game").loc[
                utils.get_player_kdao(event, granularity="game").map_seq == (1)]
            team1 = player_kda["team"].unique()[0]
            team2 = player_kda["team"].unique()[1]

            bomb_info = ['objectives.plantBomb', 'objectives.beginDefuseWithKit', 'objectives.beginDefuseWithoutKit',
                         'objectives.defuseBomb', 'objectives.explodeBomb']

            team1_df = player_kda.loc[player_kda.team == team1].drop(["map_name", "team"], axis=1)
            team2_df = player_kda.loc[player_kda.team == team2].drop(["map_name", "team"], axis=1)

            for metric in bomb_info:
                if metric not in team1_df:
                    team1_df[metric] = 0
                if metric not in team2_df:
                    team2_df[metric] = 0

            team1_killInfo = team1_df[['map_seq', 'name', 'kills', 'killAssistsGiven', 'multikills', 'deaths', 'adr']]
            team1_bombInfo = team1_df[['map_seq', 'name', 'objectives.plantBomb', 'objectives.beginDefuseWithKit',
                                       'objectives.beginDefuseWithoutKit', 'objectives.defuseBomb',
                                       'objectives.explodeBomb']]

            team2_killInfo = team2_df[['map_seq', 'name', 'kills', 'killAssistsGiven', 'multikills', 'deaths', 'adr']]
            team2_bombInfo = team2_df[['map_seq', 'name', 'objectives.plantBomb', 'objectives.beginDefuseWithKit',
                                       'objectives.beginDefuseWithoutKit', 'objectives.defuseBomb',
                                       'objectives.explodeBomb']]
            st.subheader(team1)
            st.write("Kill Information")
            st.table(team1_killInfo)
            st.write("Bomb Information")
            st.table(team1_bombInfo)

            st.subheader(team2)
            st.write("Kill Information")
            st.table(team2_killInfo)
            st.write("Bomb Information")
            st.table(team2_bombInfo)
            time.sleep(0.5)

