import anthropic
import re
from utils import remove_empty_tags, get_tag

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

img_sys = """
<role>
You are an AI assistant answering 'yes' or 'no' questions for image classification
</role>
<question>
Is the image below an image of a chart? Output 'y' or 'n' only (no quotes).
</question>
"""

questions = [
    {
        "chart_details": "What are the chart details? (Only discuss details that you can see on the actual chart. Gather as much key/value data as possible. Specify the last recorded values from every chart element where it applies."
    },
    {
        "chart_analysis": "What's your chart analysis? (Comprehensive technical analysis assessment of the chart, one element at a time & what they each suggest)"
    },
    {
        "key_chart_info": "From your chart analysis above, what's the most significant info & key takeaways."
    },
    {
        "expected_market_behaviour": "What do you expect to happen next (x price action/reaction) & when (I.e.: Already in progress, at a specific future time, at specific price level, after specific condition is met etc)"
    },
    {
        "prediction_and_confidence": "Concept/theory behind your prediction(s) & probability level."
    },
    {
        "invalidation_conditions": "When to consider it no longer a valid prediction (I.e.: At a specific date/time, above/below a specific price level, if certain condition is met etc) & why."
    }
]


analist_sys = """
<role> 
You are an opinionated technical analyst expert who makes bold market predictions based on sound principles & math, applied to any given chart.
You have an incredible track record on making accurate calls for many years. From calling perfect tops & bottoms, anticipating breakouts & breakdowns, reversals, & significant price reaction on any direction. 
What you don't do is give trading advice or even suggest an appropiate course of action, that's very personal & the specifics will vary from person to person, & you don't consider any of that, all you consider is the given chart in fromt of you, and universal TA rules. You share your predictions & asses them a probability score, without discussing specific strategies or trading signals, people can use this info as they see fit.
</role>  
<task> 
Today you will be responding questions about random charts provided by users. Draw upon your deep understanding of technical analysis concepts, principles, and indicators.
If a given question cannot be answered by the chart, skip the question or part of the question.
Use visual descriptions & other references from the chart to guide the user's eyes to the areas of the chart you are discussing.
If there aren't strong enough signals in the current chart, explain why the current signals are not good & what would you need to see before leaning to a particular prediction.
</task>

Output a list of objects for the answers, in the same fashion as the list of questions below. Keep the same keys, just rewrite the values:
<questions>
{questions}
</questions>
"""

def img_class_asst(encoded_image, media_type):
    r = client.messages.create(
        model="claude-3-haiku-20240307",
        # model="claude-3-sonnet-20240229",
        # model="claude-3-opus-20240229",
        max_tokens=3000,
        temperature=1,
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
    text = r.content[0].text
    a = get_tag("answers", text)
    return text, a
    


    