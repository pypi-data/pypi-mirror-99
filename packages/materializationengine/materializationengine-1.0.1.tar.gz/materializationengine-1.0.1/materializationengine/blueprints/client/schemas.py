from marshmallow import fields, Schema
from marshmallow.validate import Length


class Metadata(Schema):
    user_id = fields.Str(required=False)
    description = fields.Str(required=True)
    reference_table = fields.Str(required=False)


class SegmentationInfoSchema(Schema):
    pcg_table_name = fields.Str(required=True)


class SegmentationTableSchema(SegmentationInfoSchema):
    table_name = fields.Str(order=0, required=True)


class CreateTableSchema(SegmentationTableSchema):
    metadata = fields.Nested(Metadata, required=True, example={"description": "my description"})


class GetDeleteAnnotationSchema(SegmentationInfoSchema):
    annotation_ids = fields.List(fields.Int, required=True)


class PostPutAnnotationSchema(SegmentationInfoSchema):
    annotations = fields.List(fields.Dict, required=True)


class SegmentationDataSchema(Schema):
    pcg_table_name = fields.Str(required=True)
    segmentations = fields.List(fields.Dict, required=True)



class SimpleQuerySchema(Schema):
    filter_in_dict = fields.Dict()
    filter_notin_dict = fields.Dict()
    filter_equal_dict = fields.Dict()
    select_columns = fields.List(fields.Str)
    offset = fields.Integer()
    limit = fields.Integer()

class ComplexQuerySchema(Schema):
    tables = fields.List(fields.List(fields.Str, validate=Length(equal=2)), required=True)
    filter_in_dict = fields.Dict()
    filter_notin_dict = fields.Dict()
    filter_equal_dict = fields.Dict()
    select_columns = fields.List(fields.Str)
    offset = fields.Integer()
    limit = fields.Integer()
    suffixes =  fields.List(fields.Str)