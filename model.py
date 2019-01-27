from marshmallow import Schema, fields

class Company(Schema):
    class Meta:
        strict = True
    CEO = fields.Str(required=True)
    companyName = fields.Str(required=True)
    description = fields.Str(required=True)
    exchange = fields.Str(required=True)
    industry = fields.Str(required=True)
    issueType = fields.Str(required=True)
    sector = fields.Str(required=True)
    tags = fields.List(fields.String, required=True)
    website = fields.Str(required=True)
    last_price = fields.Float(required=True)


class History(Schema):
    close = fields.Float(required=True)
    high = fields.Float(required=True)
    low = fields.Float(required=True)
    open = fields.Float(required=True)
    volume = fields.Integer(required=True)


class Stock(Schema):
    class Meta:
        strict = True
    company = fields.Nested(Company, required=True)
    history = fields.Dict(values=fields.Nested(History), required=True)
    symbol = fields.Str(required=True)

stock_schema = Stock(strict=True)
