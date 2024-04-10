import anthropic
from bs4 import BeautifulSoup


# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


prompt_is_chart = """
<context>
Image classification
</context>

<task>
Only respond "YES" or "NO" (Without quotes)

Is the image provided one of the following charts?
-- Candlestick
-- Bar
-- Line
-- A chart where technical analysis can be performed
</task>
"""
            
prompt_is_readable = """
<context>
Chart quality control for technical analysis
</context>

Is the image clear and high-quality enough to discern all relevant details, and the chart data presented in a standard, commonly-used format that can be easily interpreted? i.e. no distracting, excessive or cluttered elements that make it difficult to read. (signal to noice ratio too high)

If all 'yes', respond only the word "YES" (without quotes).

Otherwhise, respond with a brief constructive critique of the issues preventing a reliable analysis & suggested improvements.
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
You are an opinionated technical analyst who makes bold market predictions by applying sound principles & math on any given chart data that's presented to you. 
</role> 

<task> 
Respond the questions about the chart provided by the user with as much detail as possible based on your deep understanding of technical analysis concepts, principles, and indicators.
</task> 

<questions>

What's the chart details? Put your answer in <chart details> tags.

What's your chart analysis? Put your answer in <chart analysis> tags.

What do you expect to happen next & when (I.e.: Already in progress, at future time, at specific price level, after specific condition met etc) Put your answer in <expected market behaviour> tags.

Concept/theory behind your predictions & probability level Put your answer in <prediction and confidence level> tags.

When to consider it no longer a valid prediction (I.e.: Specific date/time, price level, condition met etc) & why. Put your answer in <invalidation conditions> tags.

</questions>

<instructions>
Do not discuss anything not explicitly seen on the chart.
Use visual references and actual values as seen on the chart to guide the user's eyes to the relevant areas of the chart being discussed.
If the chart data is insufficient to answer a specific question, skip that question or part of the question.
If there are no strong enough signals in the chart to make predictions with confidence, explain why the current signals are not good & what would you need to see before leaning to a particular prediction.
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
    text = analysis_resp.content[0].text
    text = str(text)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(text, 'html.parser')

    # Extract the text within each tag
    chart_details = soup.find_all('chart details', string=True)
    if chart_details:
        chart_details = chart_details[0].strip()
    else:
        chart_details = None

    chart_analysis = soup.find('chart analysis')
    if chart_analysis:
        chart_analysis = chart_analysis.text.strip()
    else:
        chart_analysis = None

    expected_market_behaviour = soup.find('expected market behaviour')
    if expected_market_behaviour:
        expected_market_behaviour = expected_market_behaviour.text.strip()
    else:
        expected_market_behaviour = None

    prediction_and_confidence_level = soup.find('prediction and confidence level')
    if prediction_and_confidence_level:
        prediction_and_confidence_level = prediction_and_confidence_level.text.strip()
    else:
        prediction_and_confidence_level = None

    invalidation_conditions = soup.find('invalidation conditions')
    if invalidation_conditions:
        invalidation_conditions = invalidation_conditions.text.strip()
    else:
        invalidation_conditions = None

    # Print the extracted text
    print("Prints:/n/n")
    print(chart_details)
    print(chart_analysis)
    print(expected_market_behaviour)
    print(prediction_and_confidence_level)
    print(invalidation_conditions)

    tag_data = f"{chart_analysis}\n\n{expected_market_behaviour}\n\n{prediction_and_confidence_level}\n\n{invalidation_conditions}\n\n"

    return tag_data
