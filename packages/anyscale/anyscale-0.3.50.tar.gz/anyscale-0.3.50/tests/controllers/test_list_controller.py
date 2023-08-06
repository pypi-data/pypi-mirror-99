import json
import time
from unittest.mock import ANY, Mock, patch

import pytest

from anyscale.client.openapi_client.models.cloud import Cloud  # type: ignore
from anyscale.client.openapi_client.models.cloud_list_response import CloudListResponse  # type: ignore
from anyscale.client.openapi_client.models.cloud_response import CloudResponse  # type: ignore
from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.client.openapi_client.models.project_list_response import ProjectListResponse  # type: ignore
from anyscale.client.openapi_client.models.project_response import ProjectResponse  # type: ignore
from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.client.openapi_client.models.session_command import SessionCommand  # type: ignore
from anyscale.client.openapi_client.models.sessioncommand_list_response import SessioncommandListResponse  # type: ignore
from anyscale.controllers.list_controller import ListController
from anyscale.util import humanize_timestamp


@pytest.fixture()
def mock_api_client(
    mock_api_client_with_session: Mock,
    cloud_test_data: Cloud,
    project_test_data: Project,
    session_command_test_data: SessionCommand,
) -> Mock:
    mock_api_client = mock_api_client_with_session
    mock_api_client.get_session_commands_history_api_v2_session_commands_get.return_value = SessioncommandListResponse(
        results=[session_command_test_data]
    )
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value = ProjectResponse(
        result=project_test_data
    )
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get.return_value = CloudResponse(
        result=cloud_test_data
    )
    mock_api_client.list_clouds_api_v2_clouds_get = Mock(
        return_value=CloudListResponse(results=[cloud_test_data])
    )
    mock_api_client.list_projects_api_v2_projects_get.return_value = ProjectListResponse(
        results=[project_test_data]
    )

    return mock_api_client


def test_list_clouds_table(cloud_test_data: Cloud, mock_api_client: Mock) -> None:
    list_controller = ListController(api_client=mock_api_client)
    output = list_controller.list_clouds(json_format=False)
    expected_rows = [
        "Clouds:",
        "ID          name          PROVIDER    REGION    CREDENTIALS",
        f"{cloud_test_data.id}  {cloud_test_data.name}  {cloud_test_data.provider}    {cloud_test_data.region}    {cloud_test_data.credentials}",
    ]
    expected_output = "\n".join(expected_rows)

    assert output == expected_output
    mock_api_client.list_clouds_api_v2_clouds_get.assert_called_once()


def test_list_clouds_json(cloud_test_data: Cloud) -> None:
    mock_api_client = Mock()
    mock_api_client.list_clouds_api_v2_clouds_get = Mock(
        return_value=CloudListResponse(results=[cloud_test_data])
    )

    list_controller = ListController(api_client=mock_api_client)

    output = list_controller.list_clouds(json_format=True)
    expected_output = json.dumps(
        [
            {
                "id": cloud_test_data.id,
                "name": cloud_test_data.name,
                "provider": cloud_test_data.provider,
                "region": cloud_test_data.region,
                "credentials": cloud_test_data.credentials,
            }
        ]
    )

    assert output == expected_output
    mock_api_client.list_clouds_api_v2_clouds_get.assert_called_once()


def test_list_projects_table(project_test_data: Project, mock_api_client: Mock) -> None:
    output = ListController(api_client=mock_api_client).list_projects(json_format=False)
    expected_rows = [
        "Projects:",
        "NAME          URL                                            DESCRIPTION",
        f"{project_test_data.name}  https://beta.anyscale.com/projects/{project_test_data.id}  {project_test_data.description}",
    ]
    expected_output = "\n".join(expected_rows)

    assert output == expected_output
    mock_api_client.list_projects_api_v2_projects_get.assert_called_once()


def test_list_projects_json(
    project_test_data: Project, session_test_data: Session, mock_api_client: Mock,
) -> None:
    output = ListController(api_client=mock_api_client).list_projects(json_format=True)
    expected_output = json.dumps(
        [
            {
                "name": project_test_data.name,
                "sessions": [
                    {"name": session_test_data.name, "status": "TASK_RUNNING"},
                ],
                "url": f"https://beta.anyscale.com/projects/{project_test_data.id}",
            }
        ]
    )
    assert output == expected_output

    mock_api_client.list_projects_api_v2_projects_get.assert_called_once()
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=project_test_data.id
    )
    mock_api_client.get_session_commands_history_api_v2_session_commands_get.assert_called_once_with(
        session_id=session_test_data.id
    )


def test_list_sessions_table(
    session_test_data: Session, mock_api_client: Mock,
) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)

    with patch.multiple(
        "anyscale.controllers.list_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ):
        output = ListController(api_client=mock_api_client).list_sessions(
            None, show_all=True, json_format=False
        )
        expected_rows = [
            f"Active project: {mock_project_definition.root}",
            "ACTIVE    SESSION       STATUS        CREATED       AUTO-SUSPEND",
            f"Y         {session_test_data.name}  TASK_RUNNING  0 second ago  Enabled",
        ]
        expected_output = "\n".join(expected_rows)

        assert output == expected_output

    mock_load_project_or_throw.assert_called_once()
    mock_get_project_id.assert_called_once_with(mock_project_definition.root)
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_test_data.project_id, name=None, active_only=False,
    )
    mock_api_client.get_session_commands_history_api_v2_session_commands_get.assert_called_once_with(
        session_id=session_test_data.id
    )


def test_list_sessions_json(
    cloud_test_data: Cloud,
    session_test_data: Session,
    session_command_test_data: SessionCommand,
    mock_api_client: Mock,
) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)

    with patch.multiple(
        "anyscale.controllers.list_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ):
        output = ListController(api_client=mock_api_client).list_sessions(
            None, show_all=True, json_format=True
        )
        expected_output = json.dumps(
            [
                {
                    "name": session_test_data.name,
                    "status": "TASK_RUNNING",
                    "startup_error": {},
                    "stop_error": {},
                    "created_at": time.mktime(session_test_data.created_at.timetuple()),
                    "jupyter_notebook_url": None,
                    "ray_dashboard_url": None,
                    "grafana_url": None,
                    "tensorboard_url": None,
                    "session_idle_timeout_minutes": session_test_data.idle_timeout,
                    "session_idle_time_remaining_seconds": None,
                    "commands": [
                        {
                            "id": session_command_test_data.id,
                            "name": session_command_test_data.name,
                            "created_at": humanize_timestamp(
                                session_command_test_data.created_at
                            ),
                            "status": "RUNNING",
                        }
                    ],
                    "project": session_test_data.project_id,
                    "cloud": {
                        "id": cloud_test_data.id,
                        "name": cloud_test_data.name,
                        "provider": cloud_test_data.provider,
                        "region": cloud_test_data.region,
                        "credentials": cloud_test_data.credentials,
                    },
                }
            ]
        )

        assert output == expected_output

    mock_load_project_or_throw.assert_called_once()
    mock_get_project_id.assert_called_once_with(mock_project_definition.root)
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_test_data.project_id, name=None, active_only=False
    )
    mock_api_client.get_session_commands_history_api_v2_session_commands_get.assert_called_once_with(
        session_id=session_test_data.id
    )
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
        cloud_id=session_test_data.cloud_id
    )


def test_list_ips_table(session_test_data: Session, mock_api_client: Mock) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)

    with patch.multiple(
        "anyscale.controllers.list_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ), patch.object(
        ListController, "_get_head_and_worker_ips", return_value=("1.2.3.4", "")
    ) as mock_get_head_and_worker_ip:
        list_controller = ListController(api_client=mock_api_client)
        output = list_controller.list_ips(None, False, True)
        expected_rows = [
            "SESSION       IP ADDRESS    NODE TYPE",
            f"{session_test_data.name}  1.2.3.4       head",
        ]
        expected_output = "\n".join(expected_rows)

        assert output == expected_output

    mock_load_project_or_throw.assert_called_once()
    mock_get_project_id.assert_called_once_with(mock_project_definition.root)
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_test_data.project_id,
        name_match=None,
        state_filter=["AwaitingFileMounts", "Running"],
        _request_timeout=ANY,
    )
    mock_get_head_and_worker_ip.assert_called_once_with(
        session_name=session_test_data.name
    )


def test_list_ips_json(
    cloud_test_data: Cloud,
    project_test_data: Project,
    session_test_data: Session,
    mock_api_client: Mock,
) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)

    with patch.multiple(
        "anyscale.controllers.list_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ), patch.object(
        ListController, "_get_head_and_worker_ips", return_value=("1.2.3.4", "")
    ) as mock_get_head_and_worker_ip:
        list_controller = ListController(api_client=mock_api_client)
        output = list_controller.list_ips(None, True, True)
        expected_output = json.dumps(
            [
                {
                    "session": {
                        "name": session_test_data.name,
                        "status": "TASK_RUNNING",
                    },
                    "project": {"name": project_test_data.name},
                    "cloud": {
                        "id": cloud_test_data.id,
                        "name": cloud_test_data.name,
                        "provider": cloud_test_data.provider,
                        "region": cloud_test_data.region,
                        "credentials": cloud_test_data.credentials,
                        "config": '{"max_stopped_instances": 0}',
                    },
                    "head-ip": "1.2.3.4",
                    "worker-ips": "",
                }
            ]
        )

        assert output == expected_output

    mock_load_project_or_throw.assert_called_once()
    mock_get_project_id.assert_called_once_with(mock_project_definition.root)
    # TODO (jbai): code can be optimized, this api request is issued multiple times
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_with(
        project_id=session_test_data.project_id,
        name_match=session_test_data.name,
        state_filter=["AwaitingFileMounts", "Running"],
        _request_timeout=ANY,
    )
    mock_api_client.get_session_commands_history_api_v2_session_commands_get.assert_called_once_with(
        session_id=session_test_data.id
    )
    mock_api_client.get_project_api_v2_projects_project_id_get.assert_called_once_with(
        project_id=session_test_data.project_id, _request_timeout=ANY,
    )
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
        cloud_id=session_test_data.cloud_id
    )
    mock_get_head_and_worker_ip.assert_called_once_with(
        session_name=session_test_data.name
    )
