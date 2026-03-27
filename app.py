from flask import Flask, render_template, redirect, url_for
import requests 

app = Flask(__name__)

url = "https://api.internal.temp-mail.io/api/v3"

headers = {
    "accept": "application/json",
    "application-name": "web",
    "application-version": "4.0.0",
    "x-cors-header": "iaWg3pchvFx48fY"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate')
def generate():
    try: 
        res = requests.post(
            f"{url}/email/new",
            headers=headers,
            json={"min_name_length": 10, "max_name_length": 10}
        )
        data = res.json()
        email = data.get('email')

        return redirect(url_for('inbox', email=email))

    except Exception as e:
        return f"error: {e}"

@app.route('/inbox/<email>')
def inbox(email):
    try: 
        res = requests.get(f"{url}/email/{email}/messages", headers=headers)
        msg = res.json()
    except:
        msg = []

    return render_template("inbox.html", email=email, msg=msg)


if __name__ == '__main__':
    app.run(debug=True)