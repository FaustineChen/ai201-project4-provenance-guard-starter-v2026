import requests

base = "http://127.0.0.1:9000"
ids = []
HUMAN = [
    "Hi, I reviewed your medical documents and as we discussed I can make a payment to you in the amount of $500 for the pain and suffering bodily injury claim. This is separate from the medical billing claim that Tailandia is handling for you. \n\nI am sending a release form to your email, please review and electronically sign it. Once it is back, I can send your $500 payment!\n\nIf you have any questions, please let me know. If you need an access code for the form, it is your zip code. ",
    "For the project, we sometimes allow certain third-party components and libraries to make your implementation easier. In general, I am open to allowing additional components, as long as they don't affect the 'core' of the project. For instance, I wouldn't allow anyone to use memcached, Apache, or Node.js, since these are very closely related to components I want you to build by yourself, but I might allow, e.g., the use of a style sheet package to help you make a prettier web interface. ",
    "The price part-worths generally decrease as price increases, which is consistent with the expectation that consumers prefer lower-priced products, holding other attributes constant. However, the magnitude of the decline varies across respondents, suggesting different levels of price sensitivity. In addition, the changes in utility between $20–$30 and $30–$40 are not necessarily equal, indicating that price preferences may be nonlinear.",
    "While navigating my uncertainties, I actively sought opportunities to bridge the gap between academic and practical work. I sent out numerous applications, pursued courses with real-world relevance, and had discussions with senior students to gain insights into career possibilities.",
    "This framework included clear evaluation dimensions, a 5-point scoring system with well-defined criteria for each dimension, and suggested interview framework questions. We conducted training sessions to help interviewers understand the new framework and [FC4.1]ensur everyone was familiar with the process before implementation.",
    "Hi\n\nI noticed that after regrades are processed in Gradescope, the updated scores do not seem to be reflected in Canvas for some assignments.\n\nI wanted to ask whether this is a known issue and if the regrade scores will be synced to Canvas later, or if there is anything students need to do on our end.\n\nThank you very much for your help!",
    "The code is actually pretty vague. It actually depending on how the C- compiler is built: it can either interpret the code as *(ptr++) as Andrea stated or (*ptr)++. One will give the solution that the solution file present, one will give x7FFF, x8000, and 124 as you stated. ",
    "To get an S grade, students must submit 14 summaries via the form below on each of the seminars viewed/attended. Each summary must include topics discussed and a discussion of what they have learned from the seminar. Student must use their school email credentials to submit all summaries. Failure to do this may result in an inaccurate summary count. ",
    "So like pick tablet 1 and then just show all row/cols/values inside it?\n\nHmm maybe it’s simpler to have a page with a search form that you put your row column value information into and it just outputs the result of the hash, and then with the hash/tablet mapping information you’re supposed to manually check the tablet\n\n^ doesn’t require backend integration\n\nJust need to share the hash function to frontend page",
    "For people coming to the party, when you get to EVO, you can either just follow other people coming in and out and go to 33rd floor (top floor). Or if you can’t get in, let us know here so somebody can pick you up. (Lowkey don’t approach the lobby receptionist because they usually turn people away - this happened to me before)",
]

def appeal_entries():
    log = requests.get(f"{base}/log").json()
    entries = log if isinstance(log, list) else log.get("entries", [])
    return [e for e in entries if e.get("event") == "appeal"]


# submit
for i, t in enumerate(HUMAN):
    r = requests.post(f"{base}/submit", json={"text": t, "creator_id": f"eval_appeal_{i}"})
    ids.append(r.json()["content_id"])

# appeal
for cid in ids:
    r = requests.post(f"{base}/appeal", json={"content_id": cid, "reasoning": "eval"})
    print(cid, r.status_code)

print(requests.get(f"{base}/log").json())

r = requests.post(f"{base}/appeal", json={"content_id": "no-such-id", "reasoning": "x"})
print(r.status_code)   # 404


# 10 appeals
mine = [e for e in appeal_entries() if e.get("content_id") in ids]
print("appeals recorded:", len(mine), "/ 10")
print("under_review:", sum(e.get("status") == "under_review" for e in mine), "/ 10")
print("with reasoning:", sum(bool(e.get("reasoning")) for e in mine), "/ 10")

# 404, nonexistent content_id
before = len(appeal_entries())
r = requests.post(f"{base}/appeal", json={"content_id": "no-such-id", "reasoning": "x"})
after = len(appeal_entries())
print("404 test:", r.status_code, "| appeal records before/after:", before, after)  # expect 404，before == after