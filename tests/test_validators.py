import json
import tempfile
from unittest import TestCase
from unittest.mock import patch

from superannotate_schemas.schemas.classes import AnnotationClass
from superannotate_schemas.schemas.enums import ClassTypeEnum
from superannotate_schemas.validators import AnnotationValidators


class TestSchemas(TestCase):
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

    def test_validate_annotation_with_wrong_bbox(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/vector.json", "w") as vector_json:
                vector_json.write(
                    """
                                        {
                      "metadata": {
                        "name": "example_image_1.jpg",
                        "width": 1024,
                        "height": 683,
                        "status": "Completed",
                        "pinned": false,
                        "isPredicted": null,
                        "projectId": null,
                        "annotatorEmail": null,
                        "qaEmail": null
                      },
                      "instances": [
                        {
                          "type": "bbox",
                          "classId": 72274,
                          "probability": 100,
                          "points": {
                            
                            "x2": 465.23,
                            "y1": 341.5,
                            "y2": 357.09
                          },
                          "groupId": 0,
                          "pointLabels": {},
                          "locked": false,
                          "visible": false,
                          "attributes": [
                            {
                              "id": 117845,
                              "groupId": 28230,
                              "name": "2",
                              "groupName": "Num doors"
                            }
                          ],
                          "trackingId": "aaa97f80c9e54a5f2dc2e920fc92e5033d9af45b",
                          "error": null,
                          "createdAt": null,
                          "createdBy": null,
                          "creationType": null,
                          "updatedAt": null,
                          "updatedBy": null,
                          "className": "Personal vehicle"
                        }
                      ]
                    }

                    """

                )

            with open(f"{tmpdir_name}/vector.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(len(validator.generate_report()), 63)

            # sa.validate_annotations("Vector", os.path.join(self.vector_folder_path, f"{tmpdir_name}/vector.json"))
            # mock_print.assert_any_call(
            #     "instances[0].type                                invalid type, valid types are bbox, "
            #     "template, cuboid, polygon, point, polyline, ellipse, rbbox"
            # )

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

    def test_validate_pixel_annotation(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/pixel.json", "w") as pix_json:
                pix_json.write(
                    '''
                    {
                    "metadata": {
                        "lastAction": {
                            "email": "some.email@gmail.com",
                            "timestamp": 1636627539398
                        },
                        "width": 1024,
                        "height": 683,
                        "name": "example_image_1.jpg",
                        "projectId": 164324,
                        "isPredicted": false,
                        "isSegmented": false,
                        "status": "NotStarted",
                        "pinned": false,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "comments": [],
                    "tags": [],
                    "instances": []
                    }
                    '''
                )

            with open(f"{tmpdir_name}/pixel.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("pixel")(data)
            self.assertTrue(validator.is_valid())

    def test_validate_video_export_annotation(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/video_export.json", "w") as video_export:
                video_export.write(
                    '''
                    {
                        "metadata": {
                            "name": "video.mp4",
                            "width": 848,
                            "height": 476,
                            "status": "NotStarted",
                            "url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
                            "duration": 2817000,
                            "projectId": 164334,
                            "error": null,
                            "annotatorEmail": null,
                            "qaEmail": null,
                            "lastAction": {
                                "timestamp": 1636384061135,
                                "email": "some.email@gmail.com"
                            }
                        },
                        "instances": [],
                        "tags": []
                    }
                    '''
                )

            with open(f"{tmpdir_name}/video_export.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("video")(data)
            self.assertTrue(validator.is_valid())

    def test_validate_vector_empty_annotation(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/vector_empty.json", "w") as vector_empty:
                vector_empty.write(
                    '''
                    {
                        "metadata": {
                            "lastAction": {
                                "email": "some.email@gmail.com",
                                "timestamp": 1636627956948
                            },
                            "width": 1024,
                            "height": 683,
                            "name": "example_image_1.jpg",
                            "projectId": 162462,
                            "isPredicted": false,
                            "status": "NotStarted",
                            "pinned": false,
                            "annotatorEmail": null,
                            "qaEmail": null
                        },
                        "comments": [],
                        "tags": [],
                        "instances": []
                    }
                    '''
                )

            with open(f"{tmpdir_name}/vector_empty.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("video")(data)
            self.assertTrue(validator.is_valid())

    def test_validate_error_message_format(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_error_message_format.json",
                      "w") as test_validate_error_message_format:
                test_validate_error_message_format.write(
                    '''
                    {
                        "metadata": {}
                    }
                    '''
                )

            with open(f"{tmpdir_name}/test_validate_error_message_format.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(validator.generate_report(),
                             "metadata.name                                    field required")

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
                """instances[0].classId                             integer type expected
                instances[0].attributes[0].name                  field required
                instances[0].attributes[0].groupName             field required""".strip()
            )

    def test_validate_document_annotation_with_null_created_at(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_document_annotation_with_null_created_at.json",
                      "w") as test_validate_document_annotation_with_null_created_at:
                test_validate_document_annotation_with_null_created_at.write(
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

            with open(f"{tmpdir_name}/test_validate_document_annotation_with_null_created_at.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("document")(data)
            self.assertTrue(validator.is_valid())

    @patch('builtins.print')
    def test_validate_vector_instance_type_and_attr_annotation(self, mock_print):
        json_name = "test.json"
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/{json_name}", "w") as json_file:
                json_file.write(
                    '''
                    {
                    "metadata": {
                        "lastAction": {
                            "email": "some.email@gmail.com",
                            "timestamp": 1636958573242
                        },
                        "width": 1234,
                        "height": 1540,
                        "name": "t.png",
                        "projectId": 164988,
                        "isPredicted": false,
                        "status": "Completed",
                        "pinned": false,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "comments": [],
                    "tags": [],
                    "instances": [
                        {
                            "classId": 880080,
                            "probability": 100,
                            "points": {
                                "x1": 148.99,
                                "x2": 1005.27,
                                "y1": 301.96,
                                "y2": 1132.36
                            },
                            "groupId": 0,
                            "pointLabels": {},
                            "locked": false,
                            "visible": true,
                            "attributes": [],
                            "trackingId": null,
                            "error": null,
                            "createdAt": "2021-11-15T06:43:09.812Z",
                            "createdBy": {
                                "email": "shab.prog@gmail.com",
                                "role": "Admin"
                            },
                            "creationType": "Manual",
                            "updatedAt": "2021-11-15T06:43:13.831Z",
                            "updatedBy": {
                                "email": "shab.prog@gmail.com",
                                "role": "Admin"
                            },
                            "className": "kj"
                        }
                    ]
                }
                '''
                )

            with open(f"{tmpdir_name}/{json_name}", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(validator.generate_report(),
                             "instances[0].type                                field required")

    @patch('builtins.print')
    def test_validate_vector_invalid_instance_type_and_attr_annotation(self, mock_print):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_vector_invalid_instace_type_and_attr_annotation.json",
                      "w") as test_validate_vector_invalid_instace_type_and_attr_annotation:
                test_validate_vector_invalid_instace_type_and_attr_annotation.write(
                    '''
                    {
                    "metadata": {
                        "lastAction": {
                            "email": "some.email@gmail.com",
                            "timestamp": 1636958573242
                        },
                        "width": 1234,
                        "height": 1540,
                        "name": "t.png",
                        "projectId": 164988,
                        "isPredicted": false,
                        "status": "Completed",
                        "pinned": false,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "comments": [],
                    "tags": [],
                    "instances": [
                        {
                            "type": "bad_type",
                            "classId": 880080,
                            "probability": 100,
                            "points": {
                                "x1": 148.99,
                                "x2": 1005.27,
                                "y1": 301.96,
                                "y2": 1132.36
                            },
                            "groupId": 0,
                            "pointLabels": {},
                            "locked": false,
                            "visible": true,
                            "attributes": [],
                            "trackingId": null,
                            "error": null,
                            "createdAt": "2021-11-15T06:43:09.812Z",
                            "createdBy": {
                                "email": "shab.prog@gmail.com",
                                "role": "Admin"
                            },
                            "creationType": "Manual",
                            "updatedAt": "2021-11-15T06:43:13.831Z",
                            "updatedBy": {
                                "email": "shab.prog@gmail.com",
                                "role": "Admin"
                            },
                            "className": "kj"
                        }
                    ]
                }
                '''
                )

            with open(f"{tmpdir_name}/test_validate_vector_invalid_instace_type_and_attr_annotation.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(len(validator.generate_report()), 148)

    @patch('builtins.print')
    def test_validate_video_invalid_instance_type_and_attr_annotation(self, mock_print):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_video_invalid_instace_type_and_attr_annotation.json",
                      "w") as test_validate_video_invalid_instace_type_and_attr_annotation:
                test_validate_video_invalid_instace_type_and_attr_annotation.write(
                    '''
                    {
                    "metadata": {
                        "name": "video.mp4",
                        "width": 480,
                        "height": 270,
                        "status": "NotStarted",
                        "url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
                        "duration": 30526667,
                        "projectId": 152038,
                        "error": null,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "instances": [
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "pointLabels": {
                                    "3": "point label bro"
                                },
                                "start": 0,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 0,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 223.32,
                                                "y1": 78.45,
                                                "x2": 312.31,
                                                "y2": 176.66
                                            },
                                            "timestamp": 0,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 182.08,
                                                "y1": 33.18,
                                                "x2": 283.45,
                                                "y2": 131.39
                                            },
                                            "timestamp": 17271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.32,
                                                "y1": 36.33,
                                                "x2": 284.01,
                                                "y2": 134.54
                                            },
                                            "timestamp": 18271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 45.09,
                                                "x2": 283.18,
                                                "y2": 143.3
                                            },
                                            "timestamp": 19271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.9,
                                                "y1": 48.35,
                                                "x2": 283.59,
                                                "y2": 146.56
                                            },
                                            "timestamp": 19725864,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 52.46,
                                                "x2": 283.18,
                                                "y2": 150.67
                                            },
                                            "timestamp": 20271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 63.7,
                                                "x2": 283.18,
                                                "y2": 161.91
                                            },
                                            "timestamp": 21271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 72.76,
                                                "x2": 283.76,
                                                "y2": 170.97
                                            },
                                            "timestamp": 22271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 81.51,
                                                "x2": 283.76,
                                                "y2": 179.72
                                            },
                                            "timestamp": 23271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 24271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 30526667,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "start": 29713736,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 29713736,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 29713736,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 30526667,
                                            "attributes": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "bad_type",
                                "classId": 859496,
                                "className": "vid",
                                "start": 5528212,
                                "end": 7083022
                            },
                            "parameters": [
                                {
                                    "start": 5528212,
                                    "end": 7083022,
                                    "timestamps": [
                                        {
                                            "timestamp": 5528212,
                                            "attributes": []
                                        },
                                        {
                                            "timestamp": 6702957,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "timestamp": 7083022,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "tags": [
                        "some tag"
                    ]
                }
                '''
                )

            with open(f"{tmpdir_name}/test_validate_video_invalid_instace_type_and_attr_annotation.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("video")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(validator.generate_report(),
                             "instances[2].meta.type                           invalid type, valid types are bbox, event")

    @patch('builtins.print')
    def test_validate_video_invalid_instance_without_type_and_attr_annotation(self, mock_print):
        json_name = "test.json"
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/{json_name}", "w") as json_file:
                json_file.write(
                    '''
                    {
                    "metadata": {
                        "name": "video.mp4",
                        "width": 480,
                        "height": 270,
                        "status": "NotStarted",
                        "url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
                        "duration": 30526667,
                        "projectId": 152038,
                        "error": null,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "instances": [
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "pointLabels": {
                                    "3": "point label bro"
                                },
                                "start": 0,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 0,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 223.32,
                                                "y1": 78.45,
                                                "x2": 312.31,
                                                "y2": 176.66
                                            },
                                            "timestamp": 0,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 182.08,
                                                "y1": 33.18,
                                                "x2": 283.45,
                                                "y2": 131.39
                                            },
                                            "timestamp": 17271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.32,
                                                "y1": 36.33,
                                                "x2": 284.01,
                                                "y2": 134.54
                                            },
                                            "timestamp": 18271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 45.09,
                                                "x2": 283.18,
                                                "y2": 143.3
                                            },
                                            "timestamp": 19271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.9,
                                                "y1": 48.35,
                                                "x2": 283.59,
                                                "y2": 146.56
                                            },
                                            "timestamp": 19725864,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 52.46,
                                                "x2": 283.18,
                                                "y2": 150.67
                                            },
                                            "timestamp": 20271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 63.7,
                                                "x2": 283.18,
                                                "y2": 161.91
                                            },
                                            "timestamp": 21271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 72.76,
                                                "x2": 283.76,
                                                "y2": 170.97
                                            },
                                            "timestamp": 22271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 81.51,
                                                "x2": 283.76,
                                                "y2": 179.72
                                            },
                                            "timestamp": 23271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 24271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 30526667,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "start": 29713736,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 29713736,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 29713736,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 30526667,
                                            "attributes": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "classId": 859496,
                                "className": "vid",
                                "start": 5528212,
                                "end": 7083022
                            },
                            "parameters": [
                                {
                                    "start": 5528212,
                                    "end": 7083022,
                                    "timestamps": [
                                        {
                                            "timestamp": 5528212,
                                            "attributes": []
                                        },
                                        {
                                            "timestamp": 6702957,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "timestamp": 7083022,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "tags": [
                        "some tag"
                    ]
                }
                '''
                )

            with open(f"{tmpdir_name}/{json_name}", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("video")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(validator.generate_report(),
                             "instances[2].meta.type                           field required")

    @patch('builtins.print')
    def test_validate_vector_template_polygon_polyline_min_annotation(self, mock_print):
        json_name = "test.json"
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/{json_name}", "w") as json_file:
                json_file.write(
                    '''
                    {
                            "metadata": {
                                "lastAction": {
                                    "email": "some@some.com",
                                    "timestamp": 1636964198056
                                },
                                "width": "1234",
                                "height": 1540,
                                "name": "t.png",
                                "projectId": 164988,
                                "isPredicted": false,
                                "status": "Completed",
                                "pinned": false,
                                "annotatorEmail": null,
                                "qaEmail": null
                            },
                            "comments": [],
                            "tags": [],
                            "instances": [
                             {
                            "type": "template",
                            "classId": 880080,
                            "probability": 100,
                            "points": [
                            ],
                            "connections": [
                                {
                                    "id": 1,
                                    "from": 1,
                                    "to": 2
                                }
                            ],
                            "groupId": 0,
                            "pointLabels": {},
                            "locked": false,
                            "visible": true,
                            "attributes": [],
                            "templateId": 4728,
                            "trackingId": null,
                            "error": null,
                            "createdAt": "2021-11-15T08:24:40.712Z",
                            "createdBy": {
                                "email": "shab.prog@gmail.com",
                                "role": "Admin"
                            },
                            "creationType": "Manual",
                            "updatedAt": "2021-11-15T08:24:46.440Z",
                            "updatedBy": {
                                "email": "shab.prog@gmail.com",
                                "role": "Admin"
                            },
                            "className": "kj",
                            "templateName": "templ1"
                        },
                                {
                                    "type": "polygon",
                                    "classId": 880080,
                                    "probability": 100,
                                    "points": [
                                        233.69
                                    ],
                                    "groupId": 0,
                                    "pointLabels": {},
                                    "locked": true,
                                    "visible": true,
                                    "attributes": [],
                                    "trackingId": null,
                                    "error": null,
                                    "createdAt": "2021-11-15T08:18:16.103Z",
                                    "createdBy": {
                                        "email": "some@some.com",
                                        "role": "Admin"
                                    },
                                    "creationType": "Manual",
                                    "updatedAt": "2021-11-15T08:18:20.233Z",
                                    "updatedBy": {
                                        "email": "some@some.com",
                                        "role": "Admin"
                                    },
                                    "className": "kj"
                                },
                                {
                                    "type": "polyline",
                                    "classId": 880080,
                                    "probability": 100,
                                    "points": [
                                        218.22
                                    ],
                                    "groupId": 0,
                                    "pointLabels": {},
                                    "locked": false,
                                    "visible": true,
                                    "attributes": [],
                                    "trackingId": null,
                                    "error": null,
                                    "createdAt": "2021-11-15T08:18:06.203Z",
                                    "createdBy": {
                                        "email": "some@some.com",
                                        "role": "Admin"
                                    },
                                    "creationType": "Manual",
                                    "updatedAt": "2021-11-15T08:18:13.439Z",
                                    "updatedBy": {
                                        "email": "some@some.com",
                                        "role": "Admin"
                                    },
                                    "className": "kj"
                                },
                                {
                                    "type": "bbox",
                                    "classId": 880080,
                                    "probability": 100,
                                    "points": {
                                        "x1": 487.78,
                                        "x2": 1190.87,
                                        "y1": 863.91,
                                        "y2": 1463.78
                                    },
                                    "groupId": 0,
                                    "pointLabels": {},
                                    "locked": false,
                                    "visible": true,
                                    "attributes": [],
                                    "trackingId": null,
                                    "error": null,
                                    "createdAt": "2021-11-15T06:43:09.812Z",
                                    "createdBy": {
                                        "email": "some@some.com",
                                        "role": "Admin"
                                    },
                                    "creationType": "Manual",
                                    "updatedAt": "2021-11-15T08:16:48.807Z",
                                    "updatedBy": {
                                        "email": "some@some.com",
                                        "role": "Admin"
                                    },
                                    "className": "kj"
                                }
                            ]
                        }
                '''
                )

            with open(f"{tmpdir_name}/{json_name}", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(len(validator.generate_report()), 246)

    def test_validate_video_point_labels(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_video_point_labels.json",
                      "w") as test_validate_video_point_labels:
                test_validate_video_point_labels.write(
                    '''
                    {
                    "metadata": {
                        "name": "video.mp4",
                        "width": 480,
                        "height": 270,
                        "status": "NotStarted",
                        "url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
                        "duration": 30526667,
                        "projectId": 152038,
                        "error": null,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "instances": [
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "pointLabels": "bad_point_label",
                                "start": 0,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 0,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 223.32,
                                                "y1": 78.45,
                                                "x2": 312.31,
                                                "y2": 176.66
                                            },
                                            "timestamp": 0,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 182.08,
                                                "y1": 33.18,
                                                "x2": 283.45,
                                                "y2": 131.39
                                            },
                                            "timestamp": 17271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.32,
                                                "y1": 36.33,
                                                "x2": 284.01,
                                                "y2": 134.54
                                            },
                                            "timestamp": 18271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 45.09,
                                                "x2": 283.18,
                                                "y2": 143.3
                                            },
                                            "timestamp": 19271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.9,
                                                "y1": 48.35,
                                                "x2": 283.59,
                                                "y2": 146.56
                                            },
                                            "timestamp": 19725864,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 52.46,
                                                "x2": 283.18,
                                                "y2": 150.67
                                            },
                                            "timestamp": 20271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 63.7,
                                                "x2": 283.18,
                                                "y2": 161.91
                                            },
                                            "timestamp": 21271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 72.76,
                                                "x2": 283.76,
                                                "y2": 170.97
                                            },
                                            "timestamp": 22271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 81.51,
                                                "x2": 283.76,
                                                "y2": 179.72
                                            },
                                            "timestamp": 23271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 24271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 30526667,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "start": 29713736,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 29713736,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 29713736,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 30526667,
                                            "attributes": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "event",
                                "classId": 859496,
                                "className": "vid",
                                "start": 5528212,
                                "end": 7083022
                            },
                            "parameters": [
                                {
                                    "start": 5528212,
                                    "end": 7083022,
                                    "timestamps": [
                                        {
                                            "timestamp": 5528212,
                                            "attributes": []
                                        },
                                        {
                                            "timestamp": 6702957,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "timestamp": 7083022,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "tags": [
                        "some tag"
                    ]
                }
                '''
                )

            with open(f"{tmpdir_name}/test_validate_video_point_labels.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("video")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(validator.generate_report(),
                             "instances[0].meta.pointLabels                    value is not a valid dict")

    def test_validate_video_point_labels_bad_keys(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/test_validate_video_point_labels_bad_keys.json",
                      "w") as test_validate_video_point_labels_bad_keys:
                test_validate_video_point_labels_bad_keys.write(
                    '''
                    {
                    "metadata": {
                        "name": "video.mp4",
                        "width": 480,
                        "height": 270,
                        "status": "NotStarted",
                        "url": "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
                        "duration": 30526667,
                        "projectId": 152038,
                        "error": null,
                        "annotatorEmail": null,
                        "qaEmail": null
                    },
                    "instances": [
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "pointLabels": {
                                        "bad_key_1" : "a",
                                        "bad_key_2" : "b",
                                        "  " : "afsd",
                                        "1" : ["fasdf","sdfsdf"]
                                },
                                "start": 0,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 0,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 223.32,
                                                "y1": 78.45,
                                                "x2": 312.31,
                                                "y2": 176.66
                                            },
                                            "timestamp": 0,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 182.08,
                                                "y1": 33.18,
                                                "x2": 283.45,
                                                "y2": 131.39
                                            },
                                            "timestamp": 17271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.32,
                                                "y1": 36.33,
                                                "x2": 284.01,
                                                "y2": 134.54
                                            },
                                            "timestamp": 18271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 45.09,
                                                "x2": 283.18,
                                                "y2": 143.3
                                            },
                                            "timestamp": 19271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.9,
                                                "y1": 48.35,
                                                "x2": 283.59,
                                                "y2": 146.56
                                            },
                                            "timestamp": 19725864,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 52.46,
                                                "x2": 283.18,
                                                "y2": 150.67
                                            },
                                            "timestamp": 20271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 181.49,
                                                "y1": 63.7,
                                                "x2": 283.18,
                                                "y2": 161.91
                                            },
                                            "timestamp": 21271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 72.76,
                                                "x2": 283.76,
                                                "y2": 170.97
                                            },
                                            "timestamp": 22271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.07,
                                                "y1": 81.51,
                                                "x2": 283.76,
                                                "y2": 179.72
                                            },
                                            "timestamp": 23271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 24271058,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "points": {
                                                "x1": 182.42,
                                                "y1": 97.19,
                                                "x2": 284.11,
                                                "y2": 195.4
                                            },
                                            "timestamp": 30526667,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "bbox",
                                "classId": 859496,
                                "className": "vid",
                                "start": 29713736,
                                "end": 30526667
                            },
                            "parameters": [
                                {
                                    "start": 29713736,
                                    "end": 30526667,
                                    "timestamps": [
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 29713736,
                                            "attributes": []
                                        },
                                        {
                                            "points": {
                                                "x1": 132.82,
                                                "y1": 129.12,
                                                "x2": 175.16,
                                                "y2": 188
                                            },
                                            "timestamp": 30526667,
                                            "attributes": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "meta": {
                                "type": "event",
                                "classId": 859496,
                                "className": "vid",
                                "start": 5528212,
                                "end": 7083022,
                                "pointLabels": {}
                            },
                            "parameters": [
                                {
                                    "start": 5528212,
                                    "end": 7083022,
                                    "timestamps": [
                                        {
                                            "timestamp": 5528212,
                                            "attributes": []
                                        },
                                        {
                                            "timestamp": 6702957,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "timestamp": "7083022",
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "parameters": [
                                {
                                    "start": 5528212,
                                    "end": 7083022,
                                    "timestamps": [
                                        {
                                            "timestamp": 5528212,
                                            "attributes": []
                                        },
                                        {
                                            "timestamp": 6702957,
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        },
                                        {
                                            "timestamp": "7083022",
                                            "attributes": [
                                                {
                                                    "id": 1175876,
                                                    "groupId": 338357,
                                                    "name": "attr",
                                                    "groupName": "attr g"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                        "meta": "afsdfadsf"
                        },
                        {
                        "meta" : []
                        }
                    ],
                    "tags": [
                        123
                    ]
                }
                '''
                )

            with open(f"{tmpdir_name}/test_validate_video_point_labels_bad_keys.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("video")(data)
            self.assertFalse(validator.is_valid())
            self.assertEqual(len(validator.generate_report()), 409)

    def test_validate_vector_empty_annotation(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/vector_empty.json", "w") as vector_empty:
                vector_empty.write(
                    '''
                {
                   "metadata":{
                      "lastAction":{
                         "email":"test@test.com",
                         "timestamp":1641910273710
                      },
                      "width":480,
                      "height":270,
                      "name":"1 copy_001.jpg",
                      "projectId":181302,
                      "isPredicted":false,
                      "status":"Completed",
                      "pinned":false,
                      "annotatorEmail":null,
                      "qaEmail":null
                   },
                   "comments":[

                   ],
                   "tags":[

                   ],
                   "instances":[
                      {
                         "type":"rbbox",
                         "classId":901659,
                         "probability":100,
                         "points":{
                            "x1":213.57,
                            "y1":74.08,
                            "x2":275.65,
                            "y2":128.66,
                            "x3":238.51,
                            "y3":170.92,
                            "x4":176.43,
                            "y4":116.34
                         },
                         "groupId":0,
                         "pointLabels":{

                         },
                         "locked":false,
                         "visible":true,
                         "attributes":[

                         ],
                         "trackingId":null,
                         "error":null,
                         "createdAt":"2022-01-11T14:11:30.772Z",
                         "createdBy":{
                            "email":"test@test.com",
                            "role":"Admin"
                         },
                         "creationType":"Manual",
                         "updatedAt":"2022-01-11T14:11:35.852Z",
                         "updatedBy":{
                            "email":"test@test.com",
                            "role":"Admin"
                         },
                         "className":"df"
                      }
                   ]
                }
                    '''
                )

            with open(f"{tmpdir_name}/vector_empty.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertTrue(validator.is_valid())

    def test_validate_pixel_annotation_instance_without_class_name(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/pixel.json", "w") as pix_json:
                pix_json.write(
                    '''
                    {
                      "metadata": {
                        "name": "example_image_1.jpg",
                        "lastAction": {
                          "email": "shab.prog@gmail.com",
                          "timestamp": 1637306216
                        }
                      },
                      "instances": [
                        {
                          "creationType": "Preannotation",
                          "classId": 887060,
                          "visible": true,
                          "probability": 100,
                          "attributes": [
                            {
                              "id": 1223660,
                              "groupId": 358141,
                              "name": "no",
                              "groupName": "small"
                            }
                          ],
                          "parts": [
                            {
                              "color": "#000447"
                            }
                          ]
                        }
                      ],
                      "tags": [],
                      "comments": []
                    }
                    '''
                )

            with open(f"{tmpdir_name}/pixel.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("pixel")(data)
            self.assertTrue(validator.is_valid())

    def test_validate_document_wrong_meta_data(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            path = f"{tmpdir_name}/test_validate_document_annotation_without_classname.json"
            with open(path, "w") as test_validate_document_annotation_without_classname:
                test_validate_document_annotation_without_classname.write(
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
            with open(path, "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            validator.is_valid()
            print(validator.generate_report())
            self.assertFalse(validator.is_valid())
            self.assertEqual(len(validator.generate_report()), 141)

    def test_validate_vector_empty_annotation_bad_role(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/vector_empty.json", "w") as vector_empty:
                vector_empty.write(
                    '''
                    
                    
                {
                   "metadata":{
                      "lastAction":{
                         "email":"test@test.com",
                         "timestamp":1641910273710
                      },
                      "width":480,
                      "height":270,
                      "pinned": [ "fasdf" ],
                      "name":"1 copy_001.jpg",
                      "projectId":181302,
                      "isPredicted":false,
                      "status":"Completed",
                      "annotatorEmail":null,
                      "qaEmail":null
                   },
                   "comments":[

                   ],
                   "tags":[

                   ],
                   "instances":[
                   {       "type": "tag",
                            "classId": 530982,
                            "className": "Weather",
                            "probability": 100,
                            "attributes": [
                              {
                                "id": 94853,
                                "groupId": 23650,
                                "name": "Winter",
                                "groupName": "Season"
                              }
                            ],
                            "createdAt": "2021-12-24T12:12:07.324Z",
                            "createdBy": {
                              "email": "annotator@superannotate.com",
                              "role": "Annotator"
                            },
                            "creationType": "Manual",
                            "updatedAt": "2021-12-24T12:12:58.011Z",
                            "updatedBy": {
                              "email": "qa@superannotate.com",
                              "role": "QA"
                            }
                      },
                      {      "type": "tags",
                            "classId": 530982,
                            "className": "Weather",
                            "probability": 100,
                            "attributes": [
                              {
                                "id": 94853,
                                "groupId": 23650,
                                "name": "Winter",
                                "groupName": "Season"
                              }
                            ],
                            "createdAt": "2021-12-24T12:12:07.324Z",
                            "createdBy": {
                              "email": "annotator@superannotate.com",
                              "role": "Annotator"
                            },
                            "creationType": "Manual",
                            "updatedAt": "2021-12-24T12:12:58.011Z",
                            "updatedBy": {
                              "email": "qa@superannotate.com",
                              "role": "QA"
                            }
                      },
                      {
                         "type":"rbbox",
                         "classId":901659,
                         "probability":100,
                         "points":{
                            "x1":213.57,
                            "y1":74.08,
                            "x2":275.65,
                            "y2":128.66,
                            "x3":238.51,
                            "y3":170.92,
                            "x4":176.43,
                            "y4":116.34
                         },
                         "groupId":0,
                         "pointLabels":{

                         },
                         "locked":false,
                         "visible":true,
                         "attributes":[

                         ],
                         "trackingId":null,
                         "error":null,
                         "createdAt":"2022-01-11T14:11:30.772Z",
                         "createdBy":{
                            "email":"test@test.com",
                            "role":"bad_role"
                         },
                         "creationType":"Manual",
                         "updatedAt":"2022-01-11T14:11:35.852Z",
                         "updatedBy":{
                            "email":"test@test.com",
                            "role":"Admin"
                         },
                         "className":"df"
                      }
                   ]
                }
                    '''
                )

            with open(f"{tmpdir_name}/vector_empty.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            print(validator.generate_report())
            self.assertEqual(len(validator.generate_report()), 340)

    def test_validate_tag_without_class_name(self):
        with tempfile.TemporaryDirectory() as tmpdir_name:
            with open(f"{tmpdir_name}/tag.json", "w") as vector_empty:
                vector_empty.write(
                    '''


                {
                   "metadata":{
                      "lastAction":{
                         "email":"test@test.com",
                         "timestamp":1641910273710
                      },
                      "width":480,
                      "height":270,
                      "pinned": true,
                      "name":"1 copy_001.jpg",
                      "projectId":181302,
                      "isPredicted":false,
                      "status":"Completed",
                      "annotatorEmail":null,
                      "qaEmail":null
                   },
                   "comments":[

                   ],
                   "tags":[

                   ],
                   "instances":[
                   {       "type": "tag",
                            "classId": 530982,
                            "probability": 100,
                            "attributes": [
                              {
                                "id": 94853,
                                "groupId": 23650
                              }
                            ],
                            "createdAt": "2021-12-24T12:12:07.324Z",
                            "createdBy": {
                              "email": "annotator@superannotate.com",
                              "role": "Annotator"
                            },
                            "creationType": "Manual",
                            "updatedAt": "2021-12-24T12:12:58.011Z",
                            "updatedBy": {
                              "email": "qa@superannotate.com",
                              "role": "QA"
                            }
                      }
                   ]
                }
                    '''
                )

            with open(f"{tmpdir_name}/tag.json", "r") as f:
                data = json.loads(f.read())
            validator = AnnotationValidators.get_validator("vector")(data)
            self.assertFalse(validator.is_valid())
            print(validator.generate_report())
            self.assertEqual(len(validator.generate_report()),191)
