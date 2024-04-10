import anthropic
from utils import get_tag

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

img_sys = """
<role>
You are an AI assistant answering 'yes' or 'no' questions for image classification
</role>
<question>
Is the image below an image of a chart? (y/n)
</question>
"""

analist_sys = """
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

def img_class_asst(encoded_image, media_type):
    if encoded_image:
        r = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system=img_sys,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        res = r.content[0].text
        if 'y' not in res:
            return "Only images of charts accepted. Try again."
        else:
            return encoded_image, media_type
    else:
        return "No image uploaded."
    

def analist_asst(encoded_image, media_type):
    if encoded_image:
        an = client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-sonnet-20240229",
            # model="claude-3-opus-20240229",
            max_tokens=3000,
            temperature=0.2,
            system=analist_sys,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        text = an.content[0].text
        # chart_details = re.search(r'<chart details>(.*?)</chart details>', text, re.DOTALL).group(1)
        # chart_analysis = re.search(r'<chart analysis>(.*?)</chart analysis>', text, re.DOTALL).group(1)
        key_chart_info = get_tag("key chart inf", text)
        expected_market_behaviour = get_tag("expected market behaviour", text)
        prediction_and_confidence = get_tag("prediction and confidence", text)
        invalidation_conditions = get_tag("invalidation conditions", text)
        final = f"{key_chart_info}{expected_market_behaviour}{prediction_and_confidence}{invalidation_conditions}"

        return final
    else:
        return "No image uploaded."


