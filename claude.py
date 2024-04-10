import re
import anthropic


# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


prompt_is_chart = """
<context>
Image classification
</context>

<task>
Only respond 'YES' or 'NO' (Without quotes)

Is the image provided one of the following charts?
- Candlestick
- Bar
- Line
- A chart where technical analysis can be performed
</task>
"""
            
prompt_is_readable = """
<context>
Chart quality control for technical analysis
</context>

<questions>
- Is the image clear and high-quality enough to discern all relevant details? (Yes/No)
- Is the chart data presented in a standard, commonly-used format that can be easily interpreted? i.e. no distracting, excessive or cluttered elements that make it difficult to read. (signal to noice ratio too high) (Yes/No)
</questions>

<task>
If the answer to both questions is 'Yes', write only the word 'YES' (without quotes).
If the answer to either or both questions is 'No', write a short paragraph explaining the specific issue(s) & suggest improvements for future charts.
</task>
"""


# analyze_img_prompt = """
# <context> Technical analysis </context>

# <task>
# Your task is to analyze the chart provided and write a comprehensive assessment based solely on technical analysis concepts, and only considering without considering the available information visible on the given chart.
# </task> """


# prompt_analyze = """ 
# <context> 
# Unbiased technical analysis
# </context> 
# <role> 
# You are an opinionated technical analyst who makes bold market predictions by applying sound principles & math on any given chart data. 
# </role> 
# <task> 
# From the provided chart, extract key technical data & what it suggest. 
# Based on your deep understanding of technical analysis concepts, principles, and indicators, extract key technical data from the provided chart. Do not include any data not explicitly seen on the chart.
# Answer with as much detail as possible:
#  --what do you expect to happen next (expected market behaviour)
#  --when will it happen (already in progress, at future date/time, at specific price level, after specific condition met)
#  --based on what (concept/theory behind your predictions)
#  --how probable (confidence level)
#  --when to consider it no longer a valid prediction (specific date/time, price level, condition met) & why.
#  --if no clear signals in the chart, what would you need to see before leaning to a particular prediction.
# </task> 
# """

    # <interpret>
    # Draw upon your deep understanding of technical analysis concepts, principles, and indicators to generate a comprehensive assessment of the asset's price action, obvious patterns, trends, and potential future behavior. Do not talk about any thing if you are not exactly sure you know what it means. 
    # </interpret>
    # <recap>
    # Write a bullet list of the key points including.
    # </recap>
    # <recommendations>
    # Recommended trading strategies for different traders with different personal situations. 
    # </recommendations>


prompt_analyze = """ 
<context> Technical analysis </context>

<role> 
You are an opinionated technical analyst who makes bold market predictions by applying sound principles & math on any given chart data. 
</role> 

<task> 
Respond the questions about the chart provided down below, based on your deep understanding of technical analysis concepts, principles, and indicators.
</task> 

<questions>
- What are the chart details? (Specify the available chart data & all last recorded values, such as date/time, price, active indicators, drawings, & so on for every data element that applies to the particular chart provided down below) Put your answer in <chart details> tags.

- What's your chart analysis? (Comprehensive technical analysis assesement of the chart, one element at a time & what they suggest) Put your answer in <chart analysis> tags.

- From your chart analysis above, what's the most significant data & key take aways. Put your answer in <key chart info> tags.

- What do you expect to happen next (expected market behaviour) & when (I.e.: Already in progress, at a specific future time, at specific price level, after specific condition is met etc) Put your answer in <expected market behaviour> tags.

- Concept/theory behind your predictions & probability level. Put your answer in <prediction and confidence level> tags.

- When to consider it no longer a valid prediction (I.e.: At a specific date/time, above/below a specific price level, if certain condition is met etc) & why. Put your answer in <invalidation conditions> tags.
</questions>

<instructions>
Use visual references and real values from the chart to guide the user's eyes to the areas of the chart you are discussing.
Focus solely on the available technical data in the chart at hand & don't consider or discuss fundamentals or other factors if relevant data is not explicitly seen on the chart.
If the chart data is insufficient to answer a specific question, skip that question or part of the question.
If there aren't strong enough signals in this chart to make reasonable predictions, explain why the current signals are not good & what would you need to see before leaning to a particular prediction.
</instructions>
"""

def analyze(encoded_image, media_type):
    is_chart_resp = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1,
        temperature=0,
        system=prompt_is_chart,
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
    is_c = str(is_chart_resp.content[0].text)
    if is_c != "YES":
        return "Only technical analysis charts accepted, try again."

    is_readable_resp = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=450,
        temperature=0,
        system=prompt_is_readable,
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
    is_r = str(is_readable_resp.content[0].text)
    if is_r != "YES":
        return is_r

    analysis_resp = client.messages.create(
        model="claude-3-haiku-20240307",
        # model="claude-3-sonnet-20240229",
        # model="claude-3-opus-20240229",
        max_tokens=3000,
        temperature=0.1,
        system=prompt_analyze,
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
    t = analysis_resp.content[0].text
    text = str(t)

    # chart_details = re.search(r'<chart details>(.*?)</chart details>', text, re.DOTALL).group(1)
    # chart_analysis = re.search(r'<chart analysis>(.*?)</chart analysis>', text, re.DOTALL).group(1)
    key_chart_info = re.search(r'<key chart info>(.*?)</key chart info>', text, re.DOTALL).group(1)
    expected_market_behaviour = re.search(r'<expected market behaviour>(.*?)</expected market behaviour>', text, re.DOTALL).group(1)
    prediction_and_confidence = re.search(r'<prediction and confidence level>(.*?)</prediction and confidence level>', text, re.DOTALL).group(1)
    invalidation_conditions = re.search(r'<invalidation conditions>(.*?)</invalidation conditions>', text, re.DOTALL).group(1)

    final = f"{key_chart_info}{expected_market_behaviour}{prediction_and_confidence}{invalidation_conditions}"

    return final
