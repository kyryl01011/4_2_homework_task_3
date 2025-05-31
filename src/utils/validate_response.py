from json import JSONDecodeError
from typing import Type

import pytest
from pydantic import BaseModel
from requests import Response


def validate_response(
        response: Response,
        model: Type[BaseModel],
        expected_data_model: BaseModel | None = None
) -> BaseModel:
    try:
        response_json = response.json()
    except Exception as e:
        pytest.fail(f'Failed to parse response JSON: {e}'
                    f'\nResponse: {response.text}')

    try:
        response_model = model(**response_json)
    except Exception as e:
        pytest.fail(f'Failed to validate response model: \n{e}')

    if expected_data_model:
        if expected_data_model.model_dump(exclude_unset=True) != response_model.model_dump(exclude_unset=True):
            pytest.fail(f'Received data not equals to expected: '
                        f'\nExpected: {expected_data_model}'
                        f'\nGot: {response_model}')

    return response_model
