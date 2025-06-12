from typing import Type, TypeVar

import pytest
from pydantic import BaseModel
from requests import Response


ModelType = TypeVar('ModelType', bound=BaseModel)


def validate_response(
        response: Response,
        model: Type[ModelType],
        expected_data_model: BaseModel | None = None
) -> ModelType:
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
