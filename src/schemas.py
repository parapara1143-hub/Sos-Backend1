
from marshmallow import Schema, fields

class CompanySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    code = fields.Str(required=True)

class PlantSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    company_id = fields.Int(required=True)

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email(required=True)
    role = fields.Str()
    company_id = fields.Int(allow_none=True)
    plant_id = fields.Int(allow_none=True)

class EmployeeSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Email(allow_none=True)
    phone = fields.Str(allow_none=True)
    role = fields.Str()
    plant_id = fields.Int(required=True)

class IncidentSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    description = fields.Str()
    severity = fields.Str()
    status = fields.Str()
    lat = fields.Float(allow_none=True)
    lng = fields.Float(allow_none=True)
    company_id = fields.Int(allow_none=True)
    plant_id = fields.Int(allow_none=True)
    reporter_id = fields.Int(allow_none=True)
    assigned_to_id = fields.Int(allow_none=True)

class DeviceTokenSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(allow_none=True)
    token = fields.Str(required=True)
    platform = fields.Str()
    company_id = fields.Int(allow_none=True)
    plant_id = fields.Int(allow_none=True)
    role = fields.Str(allow_none=True)
    active = fields.Bool()
