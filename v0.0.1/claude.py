import anthropic

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


is_chart_prompt = """
<context> Image classification </context>

<task>
Only respond "YES" or "NO" (Without quotes)

Is the image provided one of the following charts:

-- Candlestick
-- Bar
-- Line
-- A chart where technical analysis can be performed
</task>
"""
            

# analyze_img_prompt = """
# <context> Technical analysis </context>

# <task>
# Your task is to analyze the chart provided and write a comprehensive assessment based solely on technical analysis concepts, and only considering without considering the available information visible on the given chart.
# </task> """


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
    
analyze_img_prompt = """ 
<context> 
Technical analysis & trading 
</context> 
<role> 
You are an expert technical analyst and trader, reading & interpreting charts. 
</role> 
<task> 
Read only hard data available in the chart, without making conclusions. Only key data. Do not consider anything not explicitly seen on the given chart. Do not leave any key technical data un-narrated. Use visual references in the chart to guide the user's eyes to the area of the chart you are reading the data from.
</task> 
"""

    # <interpret>
    # Draw upon your deep understanding of technical analysis concepts, principles, and indicators to generate a comprehensive assessment of the asset's price action, obvious patterns, trends, and potential future behavior. Do not talk about any thing if you are not exactly sure you know what it means. 
    # </interpret>
    # <recap>
    # Write a bullet list of the key points including.
    # </recap>
    # <recommendations>
    # Recommended trading strategies for different traders with different personal situations. 
    # </recommendations>

def is_chart(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system=is_chart_prompt,
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
        response = message.content[0].text
        print(response)
        return str(response)
    else:
        return "No image uploaded."

def analyze_img(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-sonnet-20240229",
            # model="claude-3-opus-20240229",
            max_tokens=3000,
            temperature=0.2,
            system=analyze_img_prompt,
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
        response = message.content[0].text
        return str(response)
    else:
        return "No image uploaded."
