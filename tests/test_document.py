import json
import tempfile
from unittest import TestCase
from unittest.mock import patch

from superannotate_schemas.schemas.classes import AnnotationClass
from superannotate_schemas.schemas.enums import DocumentAnnotationTypeEnum
from superannotate_schemas.validators import AnnotationValidators


class TestDocumentSchemas(TestCase):
    def test_tag_enum_serialization(self):
        annotations_class = AnnotationClass(
            **{'id': 56820, 'project_id': 7617, 'name': 'Personal vehicle', 'color': '#547497', 'count': 18,
               'createdAt': '2020-09-29T10:39:39.000Z', 'updatedAt': '2020-09-29T10:48:18.000Z', 'type': 'tag',
               'attribute_groups': [{'id': 21448, 'class_id': 56820, 'name': 'Large', 'is_multiselect': 0,
                                     'createdAt': '2020-09-29T10:39:39.000Z',
                                     'updatedAt': '2020-09-29T10:39:39.000Z', 'attributes': [
                       {'id': 57096, 'group_id': 21448, 'project_id': 7617, 'name': 'no', 'count': 0,
                        'createdAt': '2020-09-29T10:39:39.000Z', 'updatedAt': '2020-09-29T10:39:39.000Z'},
                       {'id': 57097, 'group_id': 21448, 'project_id': 7617, 'name': 'yes', 'count': 1,
                        'createdAt': '2020-09-29T10:39:39.000Z', 'updatedAt': '2020-09-29T10:48:18.000Z'}]}]})
        data = json.loads(annotations_class.json())
        self.assertEqual(data["type"], "tag")

    def test_validate_document_annotation_without_classname(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            path = f"{tmpdir_name}/test_validate_document_annotation_without_classname.json"
            with open(path, "w") as test_validate_document_annotation_without_classname:
                test_validate_document_annotation_without_classname.write(
                    '''
                    {
                        "metadata": {
                            "name": "text_file_example_1",
                            "status": "NotStarted",
                            "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                            "projectId": 167826,
                            "annotatorEmail": null,
                            "qaEmail": null,
                            "lastAction": {
                                "email": "some.email@gmail.com",
                                "timestamp": 1636620976450
                            }
                        },
                        "instances": [{
                                      "type": "entity",
                                      "start": 253,
                                      "end": 593,
                                      "classId": -1,
                                      "createdAt": "2021-10-22T10:40:26.151Z",
                                      "createdBy": {
                                        "email": "some.email@gmail.com",
                                        "role": "Admin"
                                      },
                                      "updatedAt": "2021-10-22T10:40:29.953Z",
                                      "updatedBy": {
                                        "email": "some.email@gmail.com",
                                        "role": "Admin"
                                      },
                                      "attributes": [],
                                      "creationType": "Manual"
                                    }],
                        "tags": [],
                        "freeText": ""
                    }
                    '''
                )
            with open(path, "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("document")(data)
            self.assertTrue(validator.is_valid())

    def test_validate_document_annotation(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/doc.json", "w") as doc_json:
                doc_json.write(
                    '''
                    {
                        "metadata": {
                            "name": "text_file_example_1",
                            "status": "NotStarted",
                            "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                            "projectId": 167826,
                            "annotatorEmail": null,
                            "qaEmail": null,
                            "lastAction": {
                                "email": "some.email@gmail.com",
                                "timestamp": 1636620976450
                            }
                        },
                        "instances": [],
                        "tags": [],
                        "freeText": ""
                    }
                    '''
                )

            with open(f"{tmpdir_name}/doc.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("document")(data)
            self.assertTrue(validator.is_valid())

    @patch('builtins.print')
    def test_validate_document_annotation_wrong_class_id(self, mock_print):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_document_annotation_wrong_class_id.json",
                      "w") as test_validate_document_annotation_wrong_class_id:
                test_validate_document_annotation_wrong_class_id.write(
                    '''
                    {
                        "metadata": {
                            "name": "text_file_example_1",
                            "status": "NotStarted",
                            "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                            "projectId": 167826,
                            "annotatorEmail": null,
                            "qaEmail": null,
                            "lastAction": {
                                "email": "some.email@gmail.com",
                                "timestamp": 1636620976450
                            }
                        },
                        "instances": [{
                                      "type": "entity",
                                      "start": 253,
                                      "end": 593,
                                      "classId": "string",
                                      "createdAt": "2021-10-22T10:40:26.151Z",
                                      "createdBy": {
                                        "email": "some.email@gmail.com",
                                        "role": "Admin"
                                      },
                                      "updatedAt": "2021-10-22T10:40:29.953Z",
                                      "updatedBy": {
                                        "email": "some.email@gmail.com",
                                        "role": "Admin"
                                      },
                                      "attributes": [
                                      {
                                                    "id": 1175876,
                                                    "groupId": 338357
                                      }
                                      ],
                                      "creationType": "Manual",
                                      "className": "vid"
                                    }],
                        "tags": [],
                        "freeText": ""
                    }
                    '''
                )

            with open(f"{tmpdir_name}/test_validate_document_annotation_wrong_class_id.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("document")(data)
            self.assertFalse(validator.is_valid())
            # TODO adjust
            self.assertEqual(
                validator.generate_report().strip(),
                "instances[0].classId                             integer type expected\n" \
                "instances[0].attributes[0].name                  field required\n" \
                "instances[0].attributes[0].groupName             field required".strip()
            )

    def test_validate_document_annotation_with_null_created_at(self):
        test_validate_document_annotation_with_null_created_at = (
            '''
            {
                "metadata": {
                    "name": "text_file_example_1",
                    "status": "NotStarted",
                    "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                    "projectId": 167826,
                    "annotatorEmail": null,
                    "qaEmail": null,
                    "lastAction": {
                        "email": "some.email@gmail.com",
                        "timestamp": 1636620976450
                    }
                },
                "instances": [{
                              "type": "entity",
                              "start": 253,
                              "end": 593,
                              "classId": 1,
                              "createdAt": null,
                              "createdBy": {
                                "email": "some.email@gmail.com",
                                "role": "Admin"
                              },
                              "updatedAt": null,
                              "updatedBy": {
                                "email": "some.email@gmail.com",
                                "role": "Admin"
                              },
                              "attributes": [],
                              "creationType": "Manual",
                              "className": "vid"
                            }],
                "tags": [],
                "freeText": ""
            }
            '''
        )
        data = json.loads(test_validate_document_annotation_with_null_created_at)
        validator = AnnotationValidators.get_validator("document")(data)
        self.assertTrue(validator.is_valid())

    def test_validate_document_wrong_meta_data(self):
        test_validate_document_annotation_without_classname = (
            '''
            {
                "metadata": {
                    "name": "text_file_example_1",
                    "status": "NotStarted",
                    "width": ["fsda" ,1],
                    "height" : ["dfsadfsdf"],
                    "is_pinned": "afdasdfadf",
                    "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                    "projectId": 167826,
                    "annotatorEmail": null,
                    "qaEmail": null,
                    "lastAction": {
                        "email": "some.email@gmail.com",
                        "timestamp": 1636620976450
                    }
                },
                "instances": [],
                "tags": [],
                "freeText": ""
            }
            '''
        )
        data = json.loads(test_validate_document_annotation_without_classname)
        validator = AnnotationValidators.get_validator("vector")(data)
        validator.is_valid()
        print(validator.generate_report())
        self.assertFalse(validator.is_valid())
        self.assertEqual(len(validator.generate_report()), 141)

    def test_validate_document_with_tag_instance(self):
        test_validate_document_annotation_with_null_created_at = (
            '''
            {
                "metadata": {
                    "name": "text_file_example_1",
                    "status": "NotStarted",
                    "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                    "projectId": 167826,
                    "annotatorEmail": null,
                    "qaEmail": null,
                    "lastAction": {
                        "email": "some.email@gmail.com",
                        "timestamp": 1636620976450
                    }
                },
                "instances": [{
                              "type": "tag",
                              "start": 253,
                              "end": 593,
                              "classId": 1,
                              "createdAt": null,
                              "createdBy": {
                                "email": "some.email@gmail.com",
                                "role": "Admin"
                              },
                              "updatedAt": null,
                              "updatedBy": {
                                "email": "some.email@gmail.com",
                                "role": "Admin"
                              },
                              "attributes": [],
                              "creationType": "Manual",
                              "className": "vid"
                            }],
                "tags": [],
                "freeText": ""
            }
            '''
        )
        data = json.loads(test_validate_document_annotation_with_null_created_at)
        model = AnnotationValidators.get_validator("document").validate(data)
        self.assertEqual(
            model.instances[0].type,
            DocumentAnnotationTypeEnum.TAG.value
        )

    def test_validate_document_wrong_instance_data(self):
        test_validate_document_annotation_without_classname = (
            '''
            {
                "metadata": {
                    "name": "text_file_example_1",
                    "status": "NotStarted",
                    "width": ["fsda" ,1],
                    "height" : ["dfsadfsdf"],
                    "is_pinned": "afdasdfadf",
                    "url": "https://sa-public-files.s3.us-west-2.amazonaws.com/Text+project/text_file_example_1.txt",
                    "projectId": 167826,
                    "annotatorEmail": null,
                    "qaEmail": null,
                    "lastAction": {
                        "email": "some.email@gmail.com",
                        "timestamp": 1636620976450
                    }
                },
                "instances": [
                    {
                              "type": "entit",
                              "start": 253,
                              "end": 593,
                              "classId": 1,
                              "createdAt": null,
                              "createdBy": {
                                "email": "some.email@gmail.com",
                                "role": "Admin"
                              },
                              "updatedAt": null,
                              "updatedBy": {
                                "email": "some.email@gmail.com",
                                "role": "Admin"
                              },
                              "attributes": [],
                              "creationType": "Manual",
                              "className": "vid"
                            }
                ],
                "tags": [],
                "freeText": ""
            }
            '''
        )
        data = json.loads(test_validate_document_annotation_without_classname)
        validator = AnnotationValidators.get_validator("document")(data)
        validator.is_valid()
        self.assertEqual(
            "instances[0].type                                invalid type, valid types are entity, tag".strip(),
            validator.generate_report().strip()
        )
