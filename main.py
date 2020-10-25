import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup
from pprint import pprint

app = Flask(__name__)


def get_fact():
    """
    get a random fact from fact service
    """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def get_pig_latin(fact):
    """
    create the mashup of facts with
    pig-latin service to create facts in pig-latin
    """
    print("\nFact is: ", fact)
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    response = requests.post(url, data = {"input_text" : fact})

    location = response.url
    print("\nLocation is: ", location)
    
    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">']
    body.append('<hr>')
    body.append('<h3>Link to Fact in Pig Latin </h3>')
    body.append('<br>')

    my_link = '<a id="pig-latin-fact" href={}> ' + str(location) + ' </a>'
    my_link = my_link.format(str(location))
    parag = '<p style="text-align: left;padding: 0 2%;">{}</p>'.format(str(my_link))
    body.append(parag)
    body.append('<br>')
    body.append('<hr>')
    body.append('</body>')
    return '\n'.join(body)


@app.route('/')
def home():
    fact = get_fact().strip()
    body = get_pig_latin(fact)

    return Response(response=body, mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

