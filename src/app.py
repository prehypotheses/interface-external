"""Module app.py"""
import os
import sys

import gradio
import pandas as pd
import transformers

# Paths
root = os.getcwd()
sys.path.append(root)
sys.path.append(os.path.join(root, 'src'))

# Modules
import src.algorithms.interface

# Examples
examples = [
    ["The Musée Rodin contains most of Rodin's significant creations, including The Thinker, The Kiss and The Gates of Hell. Many of his sculptures are displayed in the museum's extensive garden. The museum includes a room dedicated to the works of Camille Claudel and one of the two castings of The Mature Age.\n\nFrom Wikipedia"],
    ["The Dakar Rally (French: Le Rallye Dakar) or simply 'The Dakar' (Le Dakar), formerly known as the Paris–Dakar Rally (Le Rallye Paris-Dakar), is an annual rally raid organised by the Amaury Sport Organisation (ASO). It is an off-road endurance event traversing terrain much tougher than conventional rallying, and the vehicles used are typically true off-road vehicles and motorcycles, rather than modified on-road vehicles. Most of the competitive special sections are off-road, crossing dunes, mud, camel grass, rocks, and erg. Stages vary from short distances up to 800–900 kilometres (500–560 mi) per day. The rough terrain, driver fatigue, and lack of skill usually results in accidents and serious injuries.\n\nThe event began in 1978 as a rally from Paris, France, to Dakar, Senegal. Between 1992 and 2007 some editions did not start in Paris or did not arrive in Dakar, but the rally kept its name.\n\nFrom Wikipedia"],
    [('There were more than a hundred wolves in the Tiger Basin.  It is a dangerous place '
      'after 9 p.m., especially near Lake Victoria.')],
    ["The AK-47, officially known as the Avtomat Kalashnikova, is an assault rifle that is chambered for the 7.62×39mm cartridge. Developed in the Soviet Union by Russian small-arms designer Mikhail Kalashnikov, it is the originating firearm of the Kalashnikov (or 'AK') family of rifles. After more than seven decades since its creation, the AK-47 model and its variants remain one of the most popular and widely used firearms in the world.\n\nFrom Wikipedia"],
    ["\"... John’s authority fell to its lowest point and when he asked for more money the barons rebelled and forced him to sign the Great Charter (Magna Carta) that greatly limited the monarchical power and established the basis for common law in 1215. John tried to evade the Charter’s provisions shortly after signing it which provoked the outbreak of a civil war known as the First Barons’ War. The rebellious barons offered the English crown to Prince Louis of France who landed in Kent to assist the rebels in 1216. The barons switched sides and attacked Louis after John’s death in 1216 and reissue of the Magna Carta by the regent of John’s successor Henry III, William Marshal. The fighting lasted for about a year resulting in the defeat of Louis of France who gave up his claims to the English throne in 1217 ...\"\n\nFrom https://englishhistory.net"]
]

# Pipeline
# noinspection PyTypeChecker
classifier = transformers.pipeline(task='ner', model=os.path.join(os.getcwd(), 'data', 'model'),
    device='cpu')


def custom(piece):
    """

    :param piece: A piece of text; composed of sentences or/and paragraphs
    :return:
    """

    tokens = classifier(piece)

    # Reconstructing & Persisting
    tokens = tokens if len(tokens) == 0 else src.algorithms.interface.Interface().exc(
        piece=piece, tokens=tokens)

    # Summary
    summary = pd.DataFrame.from_records(data=tokens)
    summary = summary.copy()[['word', 'entity', 'score']] if not summary.empty else summary

    return {'text': piece, 'entities': tokens}, summary.to_dict(orient='records'), tokens


with gradio.Blocks() as demo:

    gradio.Markdown(value=('<h1>Token Classification</h1><br><b>An illustrative interactive interface; the '
                           'interface software allows for advanced interfaces.</b><br>The classes are '
                           '<b>art</b>, <b>building</b>, <b>event</b>, <b>location</b>, <b>organisation</b>, '
                           'and <b>product-weapon</b>.'), line_breaks=True)

    with gradio.Row():
        with gradio.Column(scale=3):
            text = gradio.Textbox(label='TEXT', placeholder="Enter sentence here...", max_length=2000)
        with gradio.Column(scale=2):
            detections = gradio.HighlightedText(label='DETECTIONS', interactive=False)
            scores = gradio.JSON(label='SCORES')
            compact = gradio.Textbox(label='COMPACT')
    with gradio.Row():
        detect = gradio.Button(value='Submit', variant='huggingface')
        gradio.ClearButton([text, detections, scores, compact], variant='secondary')

    detect.click(custom, inputs=text, outputs=[detections, scores, compact])    
    gradio.Examples(examples=examples, inputs=[text], examples_per_page=1)

demo.launch(server_port=7860)
