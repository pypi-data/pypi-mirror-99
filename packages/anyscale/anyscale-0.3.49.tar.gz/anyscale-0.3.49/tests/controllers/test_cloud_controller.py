from typing import List, Optional
from unittest.mock import Mock, patch

from click import ClickException
import pytest

from anyscale.client.openapi_client.models import (  # type: ignore
    AnyscaleAWSAccount,
    AnyscaleawsaccountResponse,
    Cloud,
    CloudResponse,
)
from anyscale.client.openapi_client.models.cloud_config import CloudConfig  # type: ignore
from anyscale.controllers.cloud_controller import CloudController


@pytest.fixture()
def mock_api_client(cloud_test_data: Cloud) -> Mock:
    mock_api_client = Mock()
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete = Mock(return_value={})
    mock_api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put = Mock(
        return_value={}
    )

    return mock_api_client


def mock_role() -> Mock:
    mock_role = Mock()

    mock_role.arn = "ARN"
    mock_role.attach_policy = Mock()

    return mock_role


def test_setup_cloud_aws(mock_api_client: Mock) -> None:
    with patch.object(
        CloudController, "setup_aws", return_value=None
    ) as mock_setup_aws:
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_cloud(
            provider="aws", region=None, name="test-aws", yes=False
        )

        mock_setup_aws.assert_called_once_with(
            region="us-west-2", name="test-aws", yes=False
        )


def test_setup_cloud_gcp(mock_api_client: Mock) -> None:
    mock_launch_gcp_cloud_setup = Mock(return_value=None)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        launch_gcp_cloud_setup=mock_launch_gcp_cloud_setup,
    ):
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_cloud(provider="gcp", region=None, name="test-gcp")

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west1", name="test-gcp"
        )


def test_setup_cloud_invalid_provider(mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    with pytest.raises(ClickException):
        cloud_controller.setup_cloud(
            provider="azure",
            region="azure-west-1",
            name="invalid cloud provider",
            yes=False,
        )


def test_delete_cloud_by_name(cloud_test_data: Cloud, mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    success = cloud_controller.delete_cloud(
        cloud_id=None, cloud_name=cloud_test_data.name, skip_confirmation=True
    )
    assert success

    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
        cloud_name_options={"name": cloud_test_data.name}
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_delete_cloud_by_id(cloud_test_data: Cloud, mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    success = cloud_controller.delete_cloud(
        cloud_id=cloud_test_data.id, cloud_name=None, skip_confirmation=True
    )
    assert success

    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
        cloud_id=cloud_test_data.id
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_missing_name_and_id(mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)

    with pytest.raises(ClickException):
        cloud_controller.delete_cloud(None, None, True)

    with pytest.raises(ClickException):
        cloud_controller.update_cloud_config(None, None, 0)

    with pytest.raises(ClickException):
        cloud_controller.get_cloud_config(None, None)


def test_setup_cross_region(mock_api_client: Mock) -> None:
    mock_api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get = Mock(
        return_value=AnyscaleawsaccountResponse(
            result=AnyscaleAWSAccount(anyscale_aws_account="aws_account_type")
        )
    )
    mocked_role = mock_role()

    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        _get_role=Mock(return_value=mocked_role),
    ):
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_aws_cross_account_role("us-west-2", "user_id", "name")
    mock_api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get.assert_called_once()
    mocked_role.attach_policy.assert_called()


@pytest.mark.parametrize(
    "roles",
    [
        pytest.param([None, mock_role()], id="role_doesnt_exist"),
        pytest.param([mock_role()], id="role_already_exists"),
    ],
)
def test_setup_aws_ray_role(mock_api_client: Mock, roles: List[Optional[Mock]]) -> None:
    assert roles[-1] is not None, "roles must end with a real role"

    mock_iam = Mock()
    mock_iam.create_role = Mock()

    with patch.multiple(
        "anyscale.controllers.cloud_controller", _get_role=Mock(side_effect=roles),
    ), patch.multiple(
        "boto3", resource=Mock(return_value=mock_iam),
    ):
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_aws_ray_role("us-west-2", "ray-autoscaler-v1")

    if roles[0] is None:
        # Role didn't exist at the start and had to be "created"
        mock_iam.create_role.assert_called_once()

    # Assert we actually attached the base policies
    roles[-1].attach_policy.assert_called()

    # And let it created our PassRole policy as well
    roles[-1].Policy.assert_called_with("PassRoleToSelf")
    roles[-1].Policy().put.assert_called()


def test_update_cloud_config_by_name(
    cloud_test_data: Cloud, mock_api_client: Mock
) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    cloud_controller.update_cloud_config(
        cloud_id=None, cloud_name=cloud_test_data.name, max_stopped_instances=100,
    )

    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
        cloud_name_options={"name": cloud_test_data.name}
    )
    mock_api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put.assert_called_once_with(
        cloud_id=cloud_test_data.id,
        cloud_config=CloudConfig(max_stopped_instances=100),
    )


def test_update_cloud_config_by_id(
    cloud_test_data: Cloud, mock_api_client: Mock
) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    cloud_controller.update_cloud_config(
        cloud_id=cloud_test_data.id, cloud_name=None, max_stopped_instances=100,
    )

    mock_api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put.assert_called_once_with(
        cloud_id=cloud_test_data.id,
        cloud_config=CloudConfig(max_stopped_instances=100),
    )
