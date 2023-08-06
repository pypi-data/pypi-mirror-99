import logging

import asana
from enum import Enum

logging.basicConfig(level=logging.INFO)


class TaskStatuses(Enum):
    IN_PROGRESS = '1177715646699485'
    DESIGN_REVIEW = '1193700203212323'
    BUILD_REVIEW = '1177715646699486'


class AsanaWrapper:
    def __init__(self, token, workspace):
        self.client = asana.Client.access_token(token)
        self.workspace = workspace

    def update_task_field(self, task_name, field_name, field_value):
        task = self._get_task_by_name(task_name)
        field_to_update = self._find_field_to_update(task, field_name)
        new_option = self._find_field_enum_option(field_to_update, field_value)
        logging.info(f"Update task: {task['name']}, field: {field_to_update['name']}, new value: {new_option['name']}")
        self.client.tasks.update_task(
            task['gid'],
            {
                "custom_fields": {
                    field_to_update['gid']: new_option['gid']
                },
            }
        )

    def _find_field_enum_option(self, field, value):
        if 'enum_options' in field:
            for option in field['enum_options']:
                if option['name'] == value:
                    return option



    def _find_field_to_update(self, task, field_name: str):
        if 'custom_fields' in task:
            for field in task['custom_fields']:
                if field['name'] == field_name:
                    return field


    def get_project_by_name(self, project_name: str):
        projects = self.get_projects()
        filtered = filter(lambda name: project_name.lower() in name['name'].lower(), projects)
        if filtered:
            return next(filtered)

    def get_projects(self):
        return tuple(self.client.projects.get_projects_for_workspace(self.workspace))

    def get_project_info(self, project_gid):
        return self.client.projects.get_project(project_gid)

    def _get_custom_field_enum(self, project_id, field_name):
        result = self.client.custom_field_settings.get_custom_field_settings_for_project(project_id)
        filtered = filter(lambda item: field_name in item.get('custom_field').get('name'), result)
        if filtered:
            enums_data = next(filtered)
            enum_opts = map(lambda item: (item['gid'], item['name']), enums_data['custom_field']['enum_options'])
            print(f'Name: {field_name} {enums_data["custom_field"]["gid"]}')
            print(list(enum_opts))

    def switch_status(self, task_name, status_field_id, status: TaskStatuses):
        task_id = self._find_task(task_name)
        if task_id:
            result = self.client.tasks.update_task(  # noqa: F841
                task_id,
                {
                    'custom_fields': {
                        status_field_id: status.value
                    }
                }
            )

    def comment_task(self, task_name, comment):
        t_gid = self._find_task(task_name)
        self._create_story(t_gid, comment)

    def get_task_by_id(self, task_gid):
        return self.client.tasks.get_task(task_gid)

    def _get_task_by_name(self, task_name):
        task_id = self._find_task(task_name)
        return self.get_task_by_id(task_id)

    def _find_task(self, task_name):
        result = self.client.typeahead.typeahead_for_workspace(
            self.workspace,
            {
                'resource_type': 'task',
                'query': task_name,
                'count': 1
            }
        )
        tasks = list(result)
        if tasks:
            return tasks[0]['gid']

    def _create_story(self, task_gid, html_text):
        result = self.client.stories.create_story_for_task(  # noqa: F841
            task_gid,
            {
                'html_text': html_text
            }
        )
