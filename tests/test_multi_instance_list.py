from unittest import TestCase
from pydantic import BaseModel
from pydantic import Field
from src.schemas.custom_types import BaseDiscriminatedInstances
from typing import List
from typing import Literal
from typing import Optional
from typing import Union
from pydantic import StrictStr
from pydantic import StrictInt
from pydantic.error_wrappers import ValidationError
import pytest



class TestMultiInstance(TestCase):

    def test_multi_list(self):

        class Polygon(BaseModel):
            type: Literal["polygon"]
            string_field: StrictStr

        class Lolygon(BaseModel):
            type: Literal["lolygon"]
            integer_field: StrictInt

        class TestMultipleInstances(BaseDiscriminatedInstances):
            __root__: Union[Polygon, Lolygon]

        class TestBaseModel(BaseModel):
            data: Optional[List[TestMultipleInstances]] = Field(list())

        TestBaseModel(**{
            "data": [
                {
                    "type": "polygon",
                    "string_field": "3"
                },
                {
                    "type": "lolygon",
                    "integer_field": 3
                }
            ]
        })

        with pytest.raises(ValidationError) as exec_info:
            TestBaseModel(**{
                "data": [
                    {
                        "type": "polygon",
                        "string_field": "3"
                    },
                    {
                        "type": "lolygon",
                        "integer_field": "3"
                    }
                ]
            })
        self.assertEqual(str(exec_info.value), "1 validation error for TestBaseModel\ndata -> 1 -> integer_field\n  value is not a valid integer (type=type_error.integer)")


