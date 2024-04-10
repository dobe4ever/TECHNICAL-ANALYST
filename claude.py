import re
import anthropic

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


def img_class_asst(media_type, encoded_image):
    r = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        system="""<role>You are an AI assistant answering 'yes' or 'no' questions for image classification</role>
        <instructions>Anwser 'y' or 'n' accordingly. Put your answer in <answer 1> and <answer 2> tags</instructions>
        <example><answer 1>n</answer 1> <answer 2>n</answer 2><example>""",
        messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": encoded_image}},
                    {"type": "text", "text": "<question 1>Is the image provided a chart?</question 1>\n<question 2>Is the image quality & readability acceptable?</question 2>"}]}]
    )
    res = r.content[0].text

    a = get_tag("answer 1", res)
    if a[0] == 'n': return "Only images of charts accepted. Try again."
    
    aa = get_tag("answer 2", res)
    if aa[0] == 'n': return "Bad image quality. Try again."    

    rr = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": encoded_image}},
                    {"type": "text", "text": "Consider whether the provided chart's quality & readability are acceptable. If the answer is 'yes', just output [YES]. If the answer is 'no', specify the issue(s), i.e.: too much data, not enough data, signal to noice ratio or whatever the case might be, and suggest improvements."}]}]
    )
    resp = rr.content[0].text
    if resp[0] != 'Y': return resp

    return analist_asst(encoded_image, media_type)
        

prompt_analyze = """
<role> 
You are an opinionated technical analyst expert who makes bold market predictions based on sound principles & math, applied to any given chart.
You have an incredible track record on making accurate calls for many years. From calling perfect tops & bottoms, anticipating breakouts & breakdown, reversals, & significant price reaction on any direction. 
What you don't do is give trading advice or even suggest an appropiate course of action, that's very personal & the specifics will vary from person to person, & you don't consider any of that, all you consider is the given chart in fromt of you, and universal TA rules. You share your predictions & asses them a probability score, without discussing specific strategies or trading signals, people can use this info as they see fit.
</role>  

<task> 
Respond questions about the chart provided down below, based on your deep understanding of technical analysis concepts, principles, and indicators.
If a given question cannot be answered by the image, skip the question or part of the question.
</task> 

<questions>
- What are the chart details? (Specify the available chart data & all last recorded values, such as date/time, price, active indicators, drawings, & so on for every data element that applies to the particular chart provided down below) Put your answer in <chart details> tags.

- What's your chart analysis? (Comprehensive technical analysis assesement of the chart, one element at a time & what they suggest) Put your answer in <chart analysis> tags.

- From your chart analysis above, what's the most significant data & key take aways. Put your answer in <key chart info> tags.

- What do you expect to happen next (x price action/reaction) & when (I.e.: Already in progress, at a specific future time, at specific price level, after specific condition is met etc) Put your answer in <expected market behaviour> tags.

- Concept/theory behind your predictions & probability level. Put your answer in <prediction and confidence level> tags.

- When to consider it no longer a valid prediction (I.e.: At a specific date/time, above/below a specific price level, if certain condition is met etc) & why. Put your answer in <invalidation conditions> tags.
</questions>

<instructions>
Use visual references and real values from the chart to guide the user's eyes to the areas of the chart you are discussing.
Focus solely on the available data in the chart at hand & don't consider or discuss fundamentals
If there aren't strong enough signals in this chart to make reasonable predictions, explain why the current signals are not good & what would you need to see before leaning to a particular prediction.
</instructions>
"""

def analist_asst(encoded_image, media_type):
    analysis_resp = client.messages.create(
        model="claude-3-haiku-20240307",
        # model="claude-3-sonnet-20240229",
        # model="claude-3-opus-20240229",
        max_tokens=3000,
        temperature=1,
        system=prompt_analyze,
        messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": encoded_image}},
                    {"type": "text", "text": "Consider whether the provided chart's quality & readability are acceptable. If the answer is 'yes', just output [YES]. If the answer is 'no', specify the issue(s), i.e.: too much data, not enough data, signal to noice ratio or whatever the case might be, and suggest improvements."}]}]
    )
    text = analysis_resp.content[0].text

    # chart_details = re.search(r'<chart details>(.*?)</chart details>', text, re.DOTALL).group(1)
    # chart_analysis = re.search(r'<chart analysis>(.*?)</chart analysis>', text, re.DOTALL).group(1)

    key_chart_info = get_tag("key chart inf", text)
    
    expected_market_behaviour = get_tag("expected market behaviour", text)

    prediction_and_confidence = get_tag("prediction and confidence", text)

    invalidation_conditions = get_tag("invalidation conditions", text)

    final = f"{key_chart_info}{expected_market_behaviour}{prediction_and_confidence}{invalidation_conditions}"

    return final


def get_tag(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return ext_list

def remove_empty_tags(text):
    return re.sub(r'<(\w+)></\1>$', '', text)

# def get_prompt(metaprompt_response):
#     between_tags = get_tag("Instructions", metaprompt_response)[0]
#     return remove_empty_tags(remove_empty_tags(between_tags).strip()).strip()

# def get_variables(prompt):
#     pattern = r'{([^}]+)}'
#     variables = re.findall(pattern, prompt)
#     return set(variables)
