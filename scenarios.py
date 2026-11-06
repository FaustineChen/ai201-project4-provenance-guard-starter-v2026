"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""
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
AI = [
    "Remote work has fundamentally transformed the modern workplace, offering both opportunities and challenges. On one hand, employees enjoy greater flexibility, reduced commuting time, and an improved work-life balance. On the other hand, organizations must navigate issues of communication, collaboration, and company culture. Ultimately, the most successful teams will be those that embrace a thoughtful hybrid approach, leveraging the strengths of both in-person and remote work to foster productivity and well-being.",
    "Introducing the AuraBrew Smart Coffee Maker, designed to elevate your morning routine. Featuring programmable settings, a built-in grinder, and a sleek stainless steel finish, it delivers barista-quality coffee at the touch of a button. Its intuitive app lets you customize brew strength and schedule your cup in advance, while the thermal carafe keeps your coffee hot for hours. Experience convenience, quality, and style in every cup.",
    "Subject: Follow-Up on Our Recent Meeting\n\nDear Team,\n\nThank you for your valuable contributions during yesterday's meeting. I wanted to summarize the key action items we discussed. First, please finalize the Q3 budget proposal by Friday. Second, the marketing team will present updated campaign metrics next week. Finally, let's schedule a brief check-in to ensure we remain aligned on priorities. Please don't hesitate to reach out if you have any questions.\n\nBest regards,\nJordan",
    "Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. Within the chloroplasts, chlorophyll absorbs sunlight and uses it to transform carbon dioxide and water into glucose and oxygen. This process not only fuels the growth of the plant itself but also forms the foundation of nearly every food chain on Earth, while releasing the oxygen that most living organisms depend on to survive.",
    "The old lighthouse stood at the edge of the cliff, its weathered stones whispering secrets of storms long past. Elena climbed the winding staircase, her heart pounding with a mixture of fear and anticipation. At the top, the great lamp flickered to life on its own, casting a golden glow across the restless sea. In that moment, she realized that the legend her grandmother had told her was true.",
    "This film is a captivating exploration of memory, loss, and the resilience of the human spirit. The cinematography is stunning, with sweeping landscapes that mirror the protagonist's emotional journey, while the score enhances every pivotal moment. Although the pacing falters slightly in the second act, strong performances from the entire cast more than make up for it. Overall, it is a thought-provoking and deeply moving experience that is well worth watching.",
    "City officials announced on Tuesday a new initiative aimed at reducing traffic congestion in the downtown area. The plan includes expanding bike lanes, increasing bus frequency, and introducing a congestion fee for vehicles entering the central district during peak hours. The mayor stated that the measures are expected to improve air quality and reduce commute times. Community members will have the opportunity to provide feedback at a public meeting scheduled for next month.",
    "A REST API allows different software systems to communicate over HTTP using a standard set of methods, such as GET, POST, PUT, and DELETE. Each resource is identified by a unique URL, and clients interact with these resources by sending requests and receiving responses, typically in JSON format. Because REST is stateless, every request must contain all the information needed to process it, which makes APIs easier to scale and maintain.",
    "Just wrapped up an incredible week at the conference! So many inspiring conversations about the future of sustainable technology. My biggest takeaway: collaboration is the key to meaningful innovation. Grateful to everyone who shared their insights, and excited to put these ideas into action. Here's to building a better tomorrow, one step at a time! #Innovation #Sustainability",
    "Developing a consistent study routine is one of the most effective ways to improve academic performance. Start by setting specific, achievable goals for each session, and break large topics into manageable sections. Minimize distractions by silencing your phone and choosing a quiet environment. Most importantly, take regular breaks to rest your mind, as consistency and balance are far more valuable than occasional bursts of intense effort.",
]

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": HUMAN,
    },
    {
        "name": "ai texts",
        "criterion": 2,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        "texts": AI,
    },
    {
        "name": "human texts",
        "criterion": 2,
        "texts": HUMAN
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   ", "creator_id": "eval_bad_blank"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": "hello"},                                    # no creator_id
            {"text": "x" * 10001, "creator_id": "eval_bad_huge"},  # over max length
        ],
    },
    # A bad-input criterion looks like this. Uncomment and adjust if that's one
    # of your five — these are raw request bodies, sent exactly as written.

    # TODO: add what your remaining criteria need.
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
