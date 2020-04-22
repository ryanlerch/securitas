from flask import current_app
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

from noggin.form.base import ButtonWidget, ModestForm, SubmitButtonField, CSVListField


def test_buttonwidget(client):
    class TestForm(FlaskForm):
        submit = SubmitField()
        text = StringField()

    form = TestForm()
    widget = ButtonWidget()
    kwargs = {"class": "testclass", "testattr": "testvalue"}
    output = widget(form.submit, **kwargs)
    assert output == (
        '<button class="btn testclass" id="submit" name="submit" '
        'testattr="testvalue" type="button">Submit</button>'
    )


def test_modestform(client):
    class TestForm(ModestForm):
        text = StringField()
        submit = SubmitButtonField()

    with current_app.test_request_context('/', method="POST", data={"submit": "1"}):
        form = TestForm()
        assert form.is_submitted()


def test_modestform_button_not_clicked(client):
    class TestForm(ModestForm):
        text = StringField()
        submit = SubmitButtonField()

    with current_app.test_request_context(
        '/', method="POST", data={"text": "dummy value"}
    ):
        form = TestForm()
        assert not form.is_submitted()


def test_modestform_no_submit_button(client):
    class TestForm(ModestForm):
        text = StringField()

    with current_app.test_request_context(
        '/', method="POST", data={"text": "dummy value"}
    ):
        form = TestForm()
        assert form.is_submitted()


def test_csvlistfield(client):
    class DummyForm(FlaskForm):
        csvfield = CSVListField('csv field')

    form = DummyForm()

    # check normal use
    form.csvfield.process_formdata(["one,two,three"])
    assert form.csvfield.data == ["one", "two", "three"]

    # check we strip single spaces string, and return []
    form.csvfield.process_formdata([" "])
    assert form.csvfield.data == []

    # check we return empty when spaces are comma separated
    form.csvfield.process_formdata([" , , , "])
    assert form.csvfield.data == []

    # check the empty string case
    form.csvfield.process_formdata([""])
    assert form.csvfield.data == []

    # check the empty list case
    form.csvfield.process_formdata([])
    assert form.csvfield.data == []
