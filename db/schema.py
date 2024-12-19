from mongoengine import *

connect('dialogue')


class Dialogue(Document):
    instruction = StringField()
    input = StringField()
    output = StringField()
    skip = BooleanField(default=False)
