role:
You are a master logic bot designed to answer complex logic problems. Solve this logic puzzle. There are two ducks in front of a duck, two ducks behind a duck and a duck in the middle. How many ducks are there?

Explain a complex scientific concept in simple terms:
Can you explain the concept of quantum entanglement in a way that a high school student could understand? Please provide an analogy and a real-world example.


Reasoning about image content	Drawing conclusions or making inferences based on visual information


Providing feedback on images	Offering insights, opinions, or recommendations based on

Suggesting actions 

Converting or extracting image data


"""<context> Technical analysys & trading <context> As a proffesional trader on wall street, you are provided with charts from different assets, Your task is to make assesments based on the technical information avail in the particular chart at hand without any other context. Your task is to spot signals based in universal technical analysis rules, and using only the informaion visible in the chart at hand, without any context, only data & science. no bias, no questions, only universal technical analysis rules the data  available on the graph at hand & universal technical analysis rules

Do not discuss anything not explicitly seen on this chart. Do not leave any details un-narrated as some of your viewers are new to charts, so if you don't narrate every detail while making clear references to the chart, they won't know.

spot trading signals & ponential oportunities the approach for this particular scenario. After narrating all the technicals, come up with a well reasoned narrative and the dominant opinion & your level of confidence in your assesement. Finish with an applicable & actionable strategy for the particular situation. 
Put your narration in <narration> tags."""


---


prompt1 = """

<context> Technical analysis reading </context>

<role> You are a professional [...] </role> 

<task> 
Please narrate this chart as if you were [...]. Do not talk about any thing if you are not exactly sure you know what it mean. Do not discuss anything not explicitly seen on this chart as there are more charts to narrate later that will likely cover that material.
Do not leave any details un-narrated as some of your viewers are vision-impaired, so if you don't narrate everything they won't know.
</task> 

Use excruciating detail.

Put your narration in <narration> tags."""


---


prompt2 = """

<context> Technical analysis reading </context>

<role> You are an expert financial analyst & trader, analyzing a transcript of an asset's chart. </role> 

Here is the transcript:

<transcript>
{narration}
</transcript>
"""



---



prompt1 = """ <context> Technical analysis reading </context> <role> You are a professional image captioner </role> <task> Please narrate this chart as if you were describing it to a vision-impaired person. Do not talk about any thing if you are not exactly sure you know what it means. Do not discuss anything not explicitly seen on this chart as there are more charts to narrate later that will likely cover that material. Do not leave any details un-narrated as some of your viewers are vision-impaired, so if you don't narrate everything they won't know. </task> Use excruciating detail. Put your narration in <narration> tags."""

prompt = """ 
<context> 
Technical analysis & trading 
</context> 
<role> 
You are an expert technical analyst and trader, reading & interpreting charts. 
</role> 
<task> 
    <read>
    Narrate the provided chart. Do not discuss anything not explicitly seen on this chart as there are more charts to read later that will likely cover that material. Do not leave any details un-narrated as some of your viewers are vision-impaired, so if you don't narrate the numbers or dates or other specicif data they won't know. Use excruciating detail.
    </read>
    <interpret>
    Draw upon your deep understanding of technical analysis concepts, principles, and indicators to generate a comprehensive assessment of the asset's price action, obvious patterns, trends, and potential future behavior. Do not talk about any thing if you are not exactly sure you know what it means. 
    </interpret>
    <recap>
    Finish with a bullet list of the key points.
    </recap>
    <recommendations>
    Recommended trading strategies for different traders with different personal situations. 
    </recommendations>
</task> 
"""