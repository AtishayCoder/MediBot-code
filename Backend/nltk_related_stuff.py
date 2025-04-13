import nltk
# noinspection PyUnresolvedReferences
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
# noinspection PyUnresolvedReferences
from nltk import pos_tag, ne_chunk
# noinspection PyUnresolvedReferences
from nltk.chunk import RegexpParser
import requests as r

# Downloading resources
nltk.download('words')
ENDPOINT = "https://api.endlessmedical.com/v1/dx"
session_id = None
reps = 0
last_q = ""
api_feature = ""
api_feature_q = ""
api_q_asked = "U"


def initialize_api_session(text):
    global session_id
    pos_tag_list = process(text)
    if reps == 0:
        # Start API session
        session_id = r.get(f"{ENDPOINT}/InitSession")
        if session_id.status_code == 200:
            session_id = session_id.json()["SessionID"]
            def accept_terms():
                params = {
                    "SessionID": str(session_id),
                    "passphrase": "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and Endless Medical services. The Terms of Use are available on endlessmedical.com"
                }
                terms = r.post(f"{ENDPOINT}/AcceptTermsOfUse", params=params)
                if terms.status_code == 200:
                    pass
                else:
                    accept_terms()
            accept_terms()
    return handle_api(pos_tag_list)


def process(text_):

    # Word Tokenization
    words = word_tokenize(text_)

    # Stop Words Removal
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Part of Speech (POS) Tagging
    pos_tags = pos_tag(filtered_words)
    print("POS Tags:", pos_tags)
    return pos_tags

    # Optional Stuff if needed later


    # Named Entity Recognition (NER)
    # named_entities = ne_chunk(pos_tags, binary=True)

    # Chunking for Specific Patterns
    # pattern = "NP: {<NNP>+}"  # Custom pattern to capture proper nouns
    # parser = RegexpParser(pattern)
    # chunked = parser.parse(pos_tags)

    # # Extracting Matches from Chunks
    # for subtree in chunked.subtrees():
    #     if subtree.label() == "NP":
    #         pass  # Placeholder if further processing is needed


# def calculate_time(pos_list):
#     # Calculate time
#     time = ""
#     index = 0
#     for i in pos_list:
#         if i[1] == "CD":
#             n_index = index + 1
#             after_word = pos_list[n_index][0].lower()
#             match after_word:
#                 case "day":
#                     print("In first day loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "days":
#                     print("In second day loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "week":
#                     print("In first week loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "weeks":
#                     print("In second week loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "month":
#                     print("In first month loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "months":
#                     print("In second month loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "year":
#                     print("In first year loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case "years":
#                     print("In second year loop")
#                     time += f"{i[0]} {list(after_word.lower())[0]}"
#                     break
#                 case _:
#                     print("Didn't match! Going to next loop.")
#                     if pos_list[n_index][1] == "CD":
#                         next_word = pos_list[n_index + 1][0].lower()
#                         match next_word:
#                             case "day":
#                                 print("In third day loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "days":
#                                 print("In fourth day loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "week":
#                                 print("In third week loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "weeks":
#                                 print("In fourth week loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "month":
#                                 print("In third month loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "months":
#                                 print("In fourth month loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "year":
#                                 print("In third year loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case "years":
#                                 print("In fourth year loop")
#                                 time += f"{i[0]} {list(next_word.lower())[0]}"
#                                 break
#                             case _:
#                                 print("No time given.")
#                                 break
#                     break
#
#         index += 1
#     if time is not None:
#         print(time)
#         return time
#     else:
#         pass


def handle_api(pos_list):
    global reps, last_q
    # Gender
    if reps == 0:
        g = 1
        for i in pos_list:
            if str(i[0]).lower() == "male" or str(i[0]).lower() == "boy" or str(i[0]).lower() == "guy" or str(i[0]).lower() == "man" or str(i[0]).lower() == "gentleman":
                g = 2
            elif str(i[0]).lower() == "female" or str(i[0]).lower() == "girl" or str(i[0]).lower() == "lady":
                g = 3
        params = {
            "SessionID": session_id,
            "name": "Gender",
            "value": str(g)
        }
        response = r.post(f"{ENDPOINT}/UpdateFeature", params=params)
        reps += 1
        return "ask/What is your age?"
    # Age
    elif reps == 1:
        age = 1
        for i in pos_list:
            if str(i[1]) == "CD":
                age = int(str(i[0]))
        params = {
            "SessionID": session_id,
            "name": "Age",
            "value": str(age)
        }
        response = r.post(f"{ENDPOINT}/UpdateFeature", params=params)
        reps += 1
        last_q = "fever"
        return "ask/Do you have any fever?"
    # Get Main Symptom
    elif reps == 2:
        params = dict(SessionID=session_id, name="", value="")
        if last_q == "fever":
            for i in pos_list:
                if str(i[0]).lower() == "yes" or str(i[0]).lower() == "present" or str(i[0]).lower() == "mild" or str(i[0]).lower() == "moderate" or str(i[0]).lower() == "high" or str(i[0]).lower() == "severe":
                    params["name"] = "HistoryFever"
                    params["value"] = str(3)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "cough"
                    return "ask/Do you have any cough?"
                else:
                    params["name"] = "HistoryFever"
                    params["value"] = str(2)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "cough"
                    return "ask/Do you have any cough?"
        elif last_q == "cough":
            for i in pos_list:
                if str(i[0]).lower() == "yes" or str(i[0]).lower() == "present" or str(i[0]).lower() == "mild" or str(i[0]).lower() == "moderate" or str(i[0]).lower() == "bit" or str(i[0]).lower() == "severe" or str(i[0]).lower() == "excessive" or str(i[0]).lower() == "excess":
                    params["name"] = "SeverityCough"
                    params["value"] = str(4)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "sore throat"
                    return "ask/Do you have a sore throat?"
                else:
                    params["name"] = "SeverityCough"
                    params["value"] = str(2)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "sore throat"
                    return "ask/Do you have a sore throat?"
        elif last_q == "sore throat":
            for i in pos_list:
                if str(i[0]).lower() == "yes" or str(i[0]).lower() == "present" or str(i[0]).lower() == "bit":
                    params["name"] = "SoreThroat"
                    params["value"] = str(4)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "runny nose"
                    return "ask/Do you have a runny nose?"
                else:
                    params["name"] = "SoreThroat"
                    params["value"] = str(2)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "runny nose"
                    return "ask/Do you have a runny nose?"
        elif last_q == "runny nose":
            for i in pos_list:
                if str(i[0]).lower() == "yes" or str(i[0]).lower() == "present":
                    params["name"] = "RunnyNoseCongestion"
                    params["value"] = str(3)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "fatigue"
                    return "ask/Do you experience fatigue?"
                else:
                    params["name"] = "RunnyNoseCongestion"
                    params["value"] = str(2)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "fatigue"
                    return "ask/Do you experience fatigue?"
        elif last_q == "fatigue":
            for i in pos_list:
                if str(i[0]).lower() == "yes" or str(i[0]).lower() == "present" or str(i[0]).lower() == "severe" or str(i[0]).lower() == "mild" or str(i[0]).lower() == "moderate":
                    params["name"] = "GeneralizedFatigue"
                    params["value"] = str(3)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "headache"
                    return "ask/Do you experience headache?"
                else:
                    params["name"] = "RunnyNoseCongestion"
                    params["value"] = str(2)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    last_q = "headache"
                    return "ask/Do you experience headache?"
        elif last_q == "headache":
            for i in pos_list:
                if str(i[0]).lower() == "yes" or str(i[0]).lower() == "present" or str(i[0]).lower() == "severe" or str(i[0]).lower() == "mild" or str(i[0]).lower() == "moderate":
                    params["name"] = "HeadacheOther"
                    params["value"] = str(3)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    reps += 1
                    return ask_api_recommended_questions(pos_list)
                else:
                    params["name"] = "HeadacheOther"
                    params["value"] = str(2)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params)
                    reps += 1
                    return ask_api_recommended_questions(pos_list)
    # Diagnose
    elif reps == 7:
        params = {
            "SessionID": session_id,
            "NumberOfResults": 1
        }
        diagnosis = r.get(f"{ENDPOINT}/Analyze", params=params)
        diagnosis = list(diagnosis.json()["Diseases"][0].keys())[0]
        return f"result/The diagnosis is {diagnosis}"



def return_tests():
    tests = r.get(f"{ENDPOINT}/GetSuggestedFeatures_Tests", params={"SessionID": session_id, "TopDiseasesToTake": 2})
    return tests.json()["Tests"]


# noinspection PyUnboundLocalVariable
def ask_api_recommended_questions(pos_list):
    global api_feature_q, api_feature, api_q_asked
    if 3 <= reps < 7:
        params = {
            "SessionID": session_id,
            "TopDiseasesToTake": 1,
        }
        features = r.get(f"{ENDPOINT}/GetSuggestedFeatures_PatientProvided", params=params).json()["SuggestedFeatures"][0]
        api_feature = features[0]
        api_feature_q = features[1]
        if api_q_asked == "U":
            api_q_asked = "A"
            return f"ask/{api_feature_q}"
        elif api_feature_q == "A":
            params2 = {
                "SessionID": session_id,
                "name": api_feature,
                "value": str(2)
            }
            for i in pos_list:
                if i[0].lower() == "yes" or i[0].lower() == "present":
                    params2["value"] = str(3)
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params2)
                else:
                    r.post(f"{ENDPOINT}/UpdateFeature", params=params2)
            api_q_asked = "U"
            ask_api_recommended_questions(None)


def specialist():
    specialist_name = r.get(f"{ENDPOINT}/GetSuggestedSpecializations", params={"SessionID": session_id, "NumberOfResults": 1}).json()["SuggestedSpecializations"][0]
    return specialist_name


def reset():
    global session_id, reps
    session_id = None
    reps = 0
