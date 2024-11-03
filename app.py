from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs


app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Search query and URL
        search_query = request.form['content'].replace(" ","")
        flipkart_url = f"https://www.flipkart.com/search?q={search_query}"

        response = requests.get(flipkart_url,headers=headers)

        soup = bs(response.text, "html.parser")

        product_containers = soup.find_all("div", {"class": "cPHDOP col-12-12"})

        del product_containers[0:3]

        product=product_containers[0].div.div.div.a['href']

        productLink = "https://www.flipkart.com" + product

        prodRes = requests.get(productLink,headers=headers)

        prodRes.encoding='utf-8'

        prod_html = bs(prodRes.text, "html.parser")

        commentboxes = prod_html.find_all('div', {'class': "RcXBOT"})

        filename = search_query + ".csv"
        fw = open(filename, "w")
        headers = "Product, Customer Name, Rating, Heading, Comment \n"
        fw.write(headers)
        reviews = []

        for i in range(len(commentboxes)-1):
            name=commentboxes[i].div.div.find_all('p', {'class': "_2NsDsF AwS1CA"})[0].text
            rating_str=commentboxes[i].div.div.div.div.text
            comment = commentboxes[i].div.div.div.find_all('p', {'class': 'z9E0IG'})[0].text
            tag=commentboxes[i].div.div.find_all('div', {'class': ""})[1].text

            mydict = {"Product": search_query, "Name": name, "Rating": rating_str, "CommentHead": comment,
                      "Comment": tag}
            reviews.append(mydict)
        return render_template('results.html',reviews=reviews)
    return render_template('results.html')
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)