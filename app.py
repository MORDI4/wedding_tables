from flask import Flask, render_template, request, redirect, url_for

from forms import TableForm
from models import tables

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route('/tables/', methods=['GET', 'POST'])
def tables_list():
    form = TableForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            tables.create(form.data)
            tables.save_all()
        return redirect(url_for("tables_list"))
    
    return render_template("wedding_tables.html", form=form, tables=tables.all(), error=error)

@app.route('/tables/<int:table_num>', methods=['GET', 'POST'])
def table_details(table_num):
    table = tables.get(table_num-1)
    form = TableForm(data=table)

    if request.method == 'POST':
        if form.validate_on_submit():
            tables.update(table_num-1, form.data)
        return redirect(url_for("tables_list"))
    return render_template("table.html", form=form, table_num=table_num)

if __name__ == '__main__':
    app.run(debug=True)