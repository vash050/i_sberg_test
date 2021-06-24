from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home():
    return {"key": "Hello"}


@app.post('/anagram/')
def anagram(str_1: str, str_2: str):
    new_str_1 = [x for x in str_1 if x.isalpha() or x.isdigit()]
    new_str_2 = [x for x in str_2 if x.isalpha() or x.isdigit()]

    str_1_pars = "".join(new_str_1).lower()
    str_2_pars = "".join(new_str_2).lower()

    flag = False
    if len(str_1_pars) == len(str_2_pars):
        for el in str_1_pars:
            flag = el in str_2_pars
            if flag is False:
                break
    return {'key': flag}
