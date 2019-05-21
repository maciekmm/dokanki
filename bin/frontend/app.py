from flask import Flask, render_template, make_response
from bin.frontend.forms import InsertForm
import random
from dokanki.dokanki import Dokanki, UnsupportedFormatError


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InsertForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        id = random.randrange(100000000)
        out = "./{}.apkg".format(name)
        steps = [10, 30]
        level = 2

        dokgen = Dokanki(name, id, steps)
        try:
            dokgen.add_source(url, level)
            dokgen.extract().write(out)
        except (ConnectionError, FileNotFoundError, UnsupportedFormatError, RuntimeError) as err:
            print(err)

        with open('{}.apkg'.format(name), 'r') as f:
            content = f.read()
        response = make_response(content)
        response.headers['Content-Disposition'] = "attachment; filename={}.apkg".format(name)
        return response
    return render_template('simple_gdocs_case.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
