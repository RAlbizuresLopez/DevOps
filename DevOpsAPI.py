import requests
import base64
import json

org = 'edaa-eudl-devops'
proj = 'DBI Data Engineering Support'
pat_token = ''

valid_workItems = ['Task', 'User Story', 'Epic', 'Bug', 'Issue', 'Feature']
valid_relations = {
    'Child': 'System.LinkTypes.Hierarchy-Forward',
    'Parent': 'System.LinkTypes.Hierarchy-Reverse',
    'Duplicate': 'System.LinkTypes.Duplicate-Forward',
    'Duplicate Of': 'System.LinkTypes.Duplicate-Reverse',
    'Predecessor': 'System.LinkTypes.Dependency',
    'Successor': 'System.LinkTypes.Dependency',
    'Related': 'System.LinkTypes.Related',
    'Tested by': 'Microsoft.VSTS.Common.TestedBy-Forward',
    'Tests': 'Microsoft.VSTS.Common.TestedBy-Reverse'
}


# DevOps Object

class DevOpsEnv:

    def __init__(self,
                 organization,
                 project,
                 token):
        self.organization = organization
        self.project = project
        self.token = token
        self.url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0"

    def __str__(self):
        value = f"Organization: {self.organization}\nProject: {self.project}\nurl: {self.url}"
        return value


data_eng_devops = DevOpsEnv(org, proj, pat_token)


class WorkItem:
    def __init__(self,
                 organization,
                 project,
                 work_type,
                 assigned_to,
                 title,
                 description,
                 acceptance_criteria=None,
                 tags=None,
                 priority=None,
                 url=None,
                 object_id=None,
                 state=None,
                 board_column=None,
                 reason=None,
                 relations=None):
        self.organization = organization
        self.project = project
        self.work_type = work_type
        self.assigned_to = assigned_to
        self.title = title
        self.description = description
        self.acceptance_criteria = acceptance_criteria
        self.tags = tags
        self.priority = priority
        self.board_column = board_column
        self.reason = reason
        self.url = url
        self.id = object_id
        self.state = state
        self.relations = relations

    def __str__(self):
        value = (f"""Organization: {self.organization}
                 Project: {self.project}
                 WorkType: {self.work_type}
                 ID: {self.id}
                 url: {self.url}
                 State: {self.state}
                 AssignedTo: {self.assigned_to if self.assigned_to else f'No User assigned to this {self.work_type}'}
                 Title: {self.title}
                 Description: {self.description if self.description else 'No description available'}
                 Tags: {self.tags if self.tags else 'No tags available'}
                 Acceptance Criteria: {self.acceptance_criteria if self.acceptance_criteria else 'No acceptance criteria set'}
                 Priority: {self.priority if self.priority else '2 (by default)'}
                 BoardColumn: {self.board_column}
                 Reason: {self.reason}
                 Relations {self.relations if self.relations else 'No relations for this ticket'}""")
        return value

    # Setters and Getters
    def update_work_type(self,
                         work_type):
        self.work_type = work_type

    def update_state(self,
                     state):
        self.state = state

    def update_assigned_to(self,
                           email):
        self.assigned_to = email

    def update_title(self,
                     title):
        self.title = title

    def update_description(self,
                           description):
        self.description = description

    def update_acceptance_criteria(self,
                                   acceptance_criteria):
        self.acceptance_criteria = acceptance_criteria

    def update_priority(self,
                        priority):
        self.priority = priority

    def update_reason(self,
                      reason):
        self.reason = reason

    def update_relations(self,
                         relations):
        self.relations = relations

    def update_tags(self,
                    tags):
        self.tags = tags

    def get_organization(self):
        return self.organization

    def get_project(self):
        return self.project

    def get_work_type(self):
        return self.work_type

    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def get_assigned_person(self):
        return self.assigned_to

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_acceptance_criteria(self):
        return self.acceptance_criteria

    def get_priority(self):
        return self.priority

    def get_tags(self):
        return self.tags

    def get_board_column(self):
        return self.board_column

    def get_reason(self):
        return self.reason

    def get_url(self):
        return self.url

    def get_relations(self):
        return self.relations

    def update_work_item(self,
                         devops,
                         work_type=None,
                         state=None,
                         assigned_to=None,
                         title=None,
                         description=None,
                         tags=None,
                         acceptance_criteria=None,
                         priority=None,
                         reason=None,
                         relations=None):
        if work_type:
            self.update_work_type(work_type)
        if state:
            self.update_state(state)
        if assigned_to:
            self.update_assigned_to(assigned_to)
        if title:
            self.update_title(title)
        if description:
            self.update_description(description)
        if relations:
            self.update_relations(relations)
        if acceptance_criteria:
            self.update_acceptance_criteria(acceptance_criteria)
        if tags:
            self.update_tags(tags)
        if priority:
            self.update_priority(priority)
        if reason:
            self.update_reason(reason)
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workitems/${self.id}?api-version=6.0"
        authorizaton = str(base64.b64encode(bytes(':{}'.format(devops.token), 'ascii')), 'ascii')
        headers = {'Content-Type': 'application/json-patch+json', 'Authorization': f'Basic {authorizaton}'}
        task_data = [
            {'op': 'add', 'path': '/fields/System.WorkItemType', 'value': self.work_type},
            {'op': 'add', 'path': '/fields/System.State', 'value': self.state},
            {'op': 'add', 'path': '/fields/System.AssignedTo', 'value': self.assigned_to if self.description else ''},
            {'op': 'add', 'path': '/fields/System.Title', 'value': self.title if self.title else ''},
            {'op': 'add', 'path': '/fields/System.Description', 'value': self.description if self.description else ''},
            {'op': 'add', 'path': 'fields/Microsoft.VSTS.Common.AcceptanceCriteria',
             'value': self.acceptance_criteria if self.reason else ''},
            {'op': 'add', 'path': 'fields/Microsoft.VSTS.Common.Priority',
             'value': self.priority if self.priority else ''},
            {'op': 'add', 'path': '/fields/System.Reason', 'value': self.reason if self.reason else ''},
            {'op': 'add', 'path': '/relations/-', 'value': self.relations if self.relations else ''}
        ]
        if tags:
            task_data.append({'op': 'add', 'path': '/fields/System.Tags', 'value': tags})
        requests.patch(url, headers=headers, json=task_data)

    def delete_object(self,
                      devops):
        authorization = str(base64.b64encode(bytes(':{}'.format(devops.token), 'ascii')), 'ascii')
        headers = {'Content-Type': 'application/json-patch+json', 'Authorization': f'Basic {authorization}'}
        # Send a DELETE request to remove the object
        response = requests.delete(self.url + "?api-version=6.0", headers=headers)
        # Check the response status code
        if response.status_code == 200:
            print("Object removed successfully!")
        else:
            print(f"Failed to remove object. Status code: {response.status_code}\nMesasge: {response.text}")


def create_work_item(devops: DevOpsEnv,
                     work_type: str,
                     title: str,
                     assigned_to: str = '',
                     description: str = '',
                     acceptance_criteria: str = None,
                     priority: str = None,
                     tags: str = None,
                     relations: dict = None):
    """
    Parameters
    ----------
    DevOpsEnv : DevOpsEnv
        DevOps Environment object with connection parameters.
    workType : str
        Valid values: Bug, Task, User Story, Issue, Feature, Epic
    title : str
        Title for Object.
    assignedUser : str
        Email of the user that the task is going to be assigned.
    description : str
        Description for the task.
    tag : list, optional
        Array of tags. The default is [].
    relations : TYPE, optional
        Relations to another Tasks. The default is None.

    Returns
    -------
    TYPE
        DESCRIPTION.
        :param devops:
        :param title:
        :param work_type:
        :param assigned_to:
        :param description:
        :param acceptance_criteria:
        :param relations:
        :param tags:
        :param priority:

    """
    if work_type in valid_workItems:
        url = f"https://dev.azure.com/{devops.organization}/{devops.project}/_apis/wit/workitems/${work_type}?api-version=6.0"
        authorization = str(base64.b64encode(bytes(':{}'.format(devops.token), 'ascii')), 'ascii')
        headers = {'Content-Type': 'application/json-patch+json', 'Authorization': f'Basic {authorization}'}
        task_data = [
            {'op': 'add', 'path': '/fields/System.AssignedTo', 'value': assigned_to},
            {'op': 'add', 'path': '/fields/System.Title', 'value': title},
            {'op': 'add', 'path': '/fields/System.Description', 'value': description}
        ]
        if acceptance_criteria:
            task_data.append(
                {'op': 'add', 'path': '/fields/Microsoft.VSTS.Common.AcceptanceCriteria', 'value': acceptance_criteria})
        if priority:
            task_data.append({'op': 'add', 'path': '/fields/Microsoft.VSTS.Common.Priority', 'value': priority})
        if tags:
            task_data.append({'op': 'add', 'path': '/fields/System.Tags', 'value': tags})
        if relations:
            task_data.append(
                {'op': 'add', 'path': '/relations/-', 'value': {'rel': relations['relation'], 'url': relations['url']}})
        response = requests.post(url, headers=headers, json=task_data)
        if response.status_code == 200:
            print(f"{work_type} Created")
            response_data = json.loads(response.text)
            result = WorkItem(devops.organization, devops.project, work_type, assigned_to, title, description,
                              url=response_data['url'], object_id=response_data['id'], state=None, board_column=None,
                              reason=None)
            return result
        else:
            print(f"Unable to create {work_type}. Reason: {response.text}")
            return response
    else:
        print(f"Invalid workType {work_type}")
        return None


def create_task(devops: DevOpsEnv,
                title: str,
                assigned_to: str = '',
                description: str = '',
                acceptance_criteria: str = None,
                priority: str = None,
                tags: str = None,
                relations=None):
    return create_work_item(devops, 'Task', title, assigned_to, description, acceptance_criteria, priority, tags,
                            relations)


def create_user_story(devops: DevOpsEnv,
                      title: str,
                      assigned_to: str = '',
                      description: str = '',
                      acceptance_criteria: str = None,
                      priority: str = None,
                      tags: str = None,
                      relations=None):
    return create_work_item(devops, 'User Story', title, assigned_to, description, acceptance_criteria, priority, tags,
                            relations)


def create_epic(devops: DevOpsEnv,
                title: str,
                assigned_to: str = '',
                description: str = '',
                acceptance_criteria: str = None,
                priority: str = None,
                tags: str = None,
                relations=None):
    return create_work_item(devops, 'Epic', title, assigned_to, description, acceptance_criteria, priority, tags,
                            relations)


def create_bug(devops: DevOpsEnv,
               title: str,
               assigned_to: str = '',
               description: str = '',
               acceptance_criteria: str = None,
               priority: str = None,
               tags: str = None,
               relations=None):
    return create_work_item(devops, 'Bug', title, assigned_to, description, acceptance_criteria, priority, tags,
                            relations)


def create_issue(devops: DevOpsEnv,
                 title: str,
                 assigned_to: str = '',
                 description: str = '',
                 acceptance_criteria: str = None,
                 priority: str = None,
                 tags: str = None,
                 relations=None):
    return create_work_item(devops, 'Issue', title, assigned_to, description, acceptance_criteria, priority, tags,
                            relations)


def create_feature(devops: DevOpsEnv,
                   title: str,
                   assigned_to: str = '',
                   description: str = '',
                   acceptance_criteria: str = None,
                   priority: str = None,
                   tags: str = None,
                   relations=None):
    return create_work_item(devops, 'Feature', title, assigned_to, description, acceptance_criteria, priority, tags,
                            relations)


def get_work_items(devops: DevOpsEnv,
                   object_filter: dict):
    filter_string = ''
    if 'tpye' in object_filter.keys():
        filter_string += f" and [System.WorkItemType] = '{object_filter['type']}'"
    if 'title' in object_filter.keys():
        filter_string += f" and [System.Title] = '{object_filter['title']}'"
    if 'user' in object_filter.keys():
        user_list = object_filter['user'].split(';') if ';' in object_filter['user'] else object_filter['user']
        if user_list is str:
            filter_string += f""" and [System.AssignedTo] = '{object_filter['title']}')"""
        elif user_list is list:
            filter_string += f""" and [System.AssignedTo] in ('{"','".join(object_filter['title'])}')"""
    if 'tags' in object_filter.keys():
        filter_string += f""" and [System.Tags] = '{object_filter['tags']}'"""
    if 'id' in object_filter.keys() and object_filter is not None:
        filter_string += f' and [System.Id] in ("{object_filter["id"]}")'
    url = f"https://dev.azure.com/{devops.organization}/{devops.project}/_apis/wit/wiql?api-version=6.0"
    work_item_url_template = f"https://dev.azure.com/{devops.organization}/{devops.project}/_apis/wit/workitems/{{}}?api-version=6.0"
    authorization = str(base64.b64encode(bytes(':{}'.format(devops.token), 'ascii')), 'ascii')
    headers = {'Content-Type': 'application/json', 'Authorization': f'Basic {authorization}'}
    # Define the WIQL query to get all tasks and apply filter if necessary
    query_str = f"SELECT * FROM workitems WHERE [System.AreaPath] = '{devops.project}'{filter_string}"
    # Send the request
    response = requests.post(url, headers=headers, json=query_str)

    # Check the request was successful
    if response.status_code == 200:
        work_list = []
        work_items = response.json()['workItems']
        for item in work_items:
            work_item_id = item['id']
            work_item_url = work_item_url_template.format(work_item_id)
            work_item_response = requests.get(work_item_url, headers=headers)
            # Check the Get Work Item request was successful
            if work_item_response.status_code == 200:
                # Print the work item properties
                work_item_data = work_item_response.json()
                work_object = WorkItem(
                    organization=str(work_item_data['url']).split('/')[3],
                    project=work_item_data['fields']['System.TeamProject'] if 'System.TeamProject' in work_item_data[
                        'fields'].keys() else None,
                    work_type=work_item_data['fields']['System.WorkItemType'],
                    assigned_to=work_item_data['fields']['System.AssigendTo']['_links'][
                        'uniqueName'] if 'System.AssigendTo' in work_item_data['fields'].keys() else None,
                    title=work_item_data['fields']['System.Title'],
                    description=work_item_data['fields']['System.Description'] if 'System.Description' in
                                                                                  work_item_data[
                                                                                      'fields'].keys() else None,
                    acceptance_criteria=work_item_data['fields'][
                        'Microsoft.VSTS.Common.AcceptanceCriteria'] if 'Microsoft.VSTS.Common.AcceptanceCriteria' in
                                                                       work_item_data['fields'].keys() else None,
                    priority=work_item_data['fields'][
                        'Microsoft.VSTS.Common.Priority'] if 'Microsoft.VSTS.Common.Priority' in work_item_data[
                        'fields'].keys() else None,
                    tags=work_item_data['fields']['Tags'] if 'System.Tags' in work_item_data['fields'].keys() else None,
                    url=work_item_data['url'],
                    object_id=work_item_data['id'],
                    state=work_item_data['fields']['System.State'] if 'System.State' in work_item_data[
                        'fields'].keys() else None,
                    board_column=work_item_data['fields']['System.BoardColumn'] if 'System.BoardColumn' in
                                                                                   work_item_data[
                                                                                       'fields'].keys() else None,
                    reason=work_item_data['fields']['System.Reason'] if 'System.Reason' in work_item_data[
                        'fields'].keys() else None
                )
                work_list.append(work_object)
            else:
                print('Error getting work item: ' + work_item_response.text)
        if work_list:
            if len(work_list) == 1:
                return work_list[0]
            else:
                return work_list
        else:
            return None
    else:
        print('Error: ' + response.text)
        return None


def get_epic(devops, project_name, create=True):
    data = get_work_items(devops, object_filter={'type': "Epic", 'title': project_name})
    if (data is None) and (create is True):
        exist = False
        print("Epic doesn´t exist in this board. Creating a new Epic object")
        epic = create_epic(devops=devops, title=f'{project_name.upper()}', tags=f'{project_name.upper()}')
        return epic, exist
    else:
        exist = True
        if data is list:
            print("There are more than 1 Epic with this title. Change the name of this task and check the board")
            return None
        else:
            print("Epic exist and it's being returned by this function")
            return data, exist


def get_feature(devops, project_name):
    data = get_work_items(devops, object_filter={'type': "Feature", 'title': project_name})
    if data is None:
        exist = False
        print("Feature doesn´t exist in this board. Creating a new Epic object")
        epic = create_epic(devops=devops, title=f'{project_name.upper()}', tags=f'{project_name.upper()}')
        return epic, exist
    else:
        exist = True
        if data is list:
            print("There are more than 1 Features with this title. Change the name of this task and check the board")
            return None
        else:
            print("Feature exist and it's being returned by this function")
            return data, exist


def get_user_story(devops, project_name):
    data = get_work_items(devops, object_filter={'type': "User Story", 'title': project_name})
    if data is None:
        exist = False
        print("User Story doesn´t exist in this board. Creating a new Epic object")
        epic = create_epic(devops=devops, title=f'{project_name.upper()}', tags=f'{project_name.upper()}')
        return epic, exist
    else:
        exist = True
        if data is list:
            print(
                "There are more than 1 User Stories with this title. Change the name of this task and check the board")
            return None
        else:
            print("User Story exist and it's being returned by this function")
            return data, exist


def data_source_ingestion_pipe(devops,
                               country,
                               bu,
                               source_name,
                               source_type,
                               project_name,
                               dbip_code,
                               api_extractor: bool = True,
                               move_it_job: bool = True,
                               envs: tuple = ('DEV', 'UAT', 'PROD')):
    # Function to get if exists or create if it doesn't exist
    epic, epic_exist = get_epic(devops, f'{project_name.upper()}')
    if epic:
        # Update Tags
        epic.update_work_item(devops, tags=f'{dbip_code.upper()}')
        feature, feature_exist = get_feature(devops, f'{dbip_code.upper()} - {source_name.upper()} Ingestion')
        if feature and not feature_exist:
            feature.update_work_item(devops, tags=f'{dbip_code.upper()};{source_name.upper()}', relations={'relation': valid_relations['Parent'], 'url': epic.get_url()})
            us_tags = f'{dbip_code.upper()};{source_name.upper()}'
            us_relation = {'relation': valid_relations['Parent'], 'url': feature.get_url()}
            user_stories = [
                {
                    'Title': 'Define and agree the on-boarding plan',
                    'Description': """Define source priority and plan delivery times
                    
                    Input: Proposal presentation with all the details and kick off meeting to understand the scope and objectives.""",
                    'AcceptanceCriteria': 'Delivery times for this Source in each environment and priority',
                    'Priority': '1'
                },
                {
                    'Title': 'Planview entry',
                    'Description': """Ensure we have a PV entry from project""",
                    'AcceptanceCriteria': 'PV entry to register hours for the whole ZIDP CVS Team',
                    'Priority': '1'
                },
                {
                    'Title': f'Request source information {source_name}',
                    'Description': """Receive source information to perform the ingestion properly
                    
                    Input: Fill excel with all the information required to be able to perform the ingestion properly""",
                    'AcceptanceCriteria': '"Source Basic Information" -> Is the excel for each source with all the required information to be able to perform the ingestion properly',
                    'Priority': '1'
                },
                {
                    'Title': 'Source Infra creation ',
                    'Description': """A ticket with the list of sources and their information must be sent to the snow group DBI-PLT-CONNECT-FK (combined value stream group)
                    More information in https://rmp-confluence.zurich.com/display/ZZIDP/Source+Onboarding
                    
                    Input: Ticket in SNOW with Source Basic Information""",
                    'AcceptanceCriteria': f'Evidences resources created in all environments ({"/".join(envs)}). It should contain: \n- Link to blob storage container for this source.\n- KeyVault',
                    'Priority': '1'
                }
            ]
            for ENV in envs:
                user_stories.append({
                    'Title': f'{ENV} - Test access to new resources and documentation',
                    'Description': f""""Ensure we can access to:
            - 2 Container in Blob Storage : Landing & Data -> ensure we have access to them.
            - KeyVault
            - All environments
            
            All the evidences will be registered in the Devops Wiki following the template."
                        
                        Input: Ticket in SNOW with "Source Basic Information" resolved.""",
                    'AcceptanceCriteria': f""""Registered evidences in Wiki with SNOW ticket number.
            link in task comments.""",
                    'Priority': '1'
                })
            user_stories = user_stories + [
                {
                    'Title': 'Register metadata in all environments',
                    'Description': """Register source information in metadata table in ZIDP. ZIDP team will create AD groups and Unity  Catalog schema for the registered data.
                    How to insert data in metadata table:https://forms.office.com/Pages/DesignPageV2.aspx?subpage=design&FormId=unI2RwfNcUOirniLTGGEDtvAZMrvPglOjY2x4Y0hKdBUREpIRUI5NEJXTFhTVktNOEk1TDYxN1RLTS4u 
                    Input: "Fill form\n- Send team chat to Pablo Frutos mentioning that the form has been filled""",
                    'AcceptanceCriteria': 'Feedback from ZIDP in Teams chat informing that all the resources has been  created in all the environments.',
                    'Priority': '1'
                },
                {
                    'Title': 'Request SNOW assigment group',
                    'Description': """Assignment group owner should send the request to create the specific groups which will be used for this source/project.  [ADD SHAREPOINT DOC WITH THE DETAILS]
                    Input: Fill word document and send it via email to servicenow.governance@uk.zurich.com""",
                    'AcceptanceCriteria': 'Service Now governance group will send back the approval and group creation',
                    'Priority': '1'
                }
            ]
            if api_extractor:
                user_stories = user_stories + [
                    {
                        'Title': ' API Extractor Implementation',
                        'Description': """In case a custom API extractor must be developed, data engineering should have configure his local environment to be prepared, following the guideline: https://dev.azure.com/edaa-eudl-devops/DBI%20Data%20Engineering%20Support/_wiki/wikis/Support/6083/Api-Extractor-configuration
                        Input: 
                        - URL
                        - User / password
                        - Which information we want to extract
                        - Periodicity
                        - Format""",
                        'AcceptanceCriteria': 'Local code extracting properly the data',
                        'Priority': '1'
                    },
                    {
                        'Title': 'API Extractor deployment',
                        'Description': """This task involves the pull request to incluide the new api extractor in the repository, and the deployment in DEV environment. It requires a ticket to platform (DBI-PLT-CONNECT-FK) to ensure we have access to the source.
                        Dividir esta tarea mejor, según las acciones que tenemos sque hacer nosotros (pull request al equipo de desarrollo del ZIDP para mergear el código, tarea a plataforma, test en DEV)""",
                        'AcceptanceCriteria': '',
                        'Priority': '1'
                    }
                ]
            if move_it_job:
                user_stories.append(
                    {
                        'Title': 'Request MOVEit job',
                        'Description': """if a MOVEit job is needed to move the files to the landing container, we should request it following the documentation: https://dev.azure.com/edaa-eudl-devops/DBI%20Data%20Engineering%20Support/_wiki/wikis/Support/6213/MOVEit-jobs.
                        NOTE: Allways advice to the project manager about which MoveIt are we going to use, in case the customer have their own MOveIt instance/service, they should request it.
                        Dividir en varias tareas según lo que necesitamos en el input para realizar esta.
                        Input:
                        - FileServer
                        - File location
                        - Credentials to acces fileServer(in case we need a new Service Account, to request it)
                        - Credentials from platform to access to the blobstorage/s3  using MoveIT
                        - Create request ticket in SNOW with all the details""",
                        'AcceptanceCriteria': 'Ticket resolved and validation that MoveIT job works as expected',
                        'Priority': '1'
                    })
            user_stories.append({
                'Title': 'Source configuration',
                'Description': """Configure the new source creating a new branch in repo: https://dev.azure.com/edaa-eudl-devops/edaa-eudl-zuglhu/_git/edaa-zuglhu-airflow-configuration following the guideline: https://dev.azure.com/edaa-eudl-devops/edaa-eudl-zuglhu/_wiki/wikis/edaa-eudl-zuglhu.wiki/2172/4.4-Generate-the-InferSchemaInfo-Json-Conf-of-ZIH
                    Input: Source Basic Information""",
                'AcceptanceCriteria': 'Yaml file created in a new branch in the official repo with all the required information to be able to ingest source data.',
                'Priority': '1'
            })
            for ENV in envs:
                user_stories = user_stories + [
                    {
                        'Title': f'{ENV} - Request official deployment to ZIDP Core team for {ENV} env',
                        'Description': f"""IN order to test the configured ingestion, a new PR must be created to merge our branch code with the source configuration file into the main branch. This PR will only contain the yaml in {ENV} .
                        Input: PR created and ZIDP core team informed via chat teams.""",
                        'AcceptanceCriteria': f'Code deployment in {ENV} environment. ZIDP core team provide feedback in Teams chat',
                        'Priority': '1'
                    },
                    {
                        'Title': f'{ENV} - Source manual execution test',
                        'Description': f"""Test that Airlfow pipeline and source configuration in current branch works properly. By default, airflow dags are created to be executed once.
                        Input: Execute DAG manually.""",
                        'AcceptanceCriteria': f'Ensure data is ingested properly and with the expected format.',
                        'Priority': '1'
                    },
                    {
                        'Title': f'{ENV} - Request add users to new Schema in {ENV}',
                        'Description': f"""Request to ZIDP Core team the addition of users for the new schemas created, via Teams chat or NOW ticket [AÑADIR SNOW GROUP, TICKET, DOC..]
                        Input: 
                        - Request addition of zidp_combined_value_stream group with write access
                        - Request addition of users provided by customer with read access""",
                        'AcceptanceCriteria': f'"zidp_combined_value_stream has the proper access to the schema.\nUsers can read the new schema"',
                        'Priority': '1'
                    },
                    {
                        'Title': f'{ENV} - Ingested data on databricks',
                        'Description': f"""Ensure the process can perform properly the first ingestion and also test incrementals and other cases to ensure it works smoothly.""",
                        'AcceptanceCriteria': f'Ensure all the expected properties for this source are working as expected (append, incremental, or any other agreed feature, to be align with the customer).',
                        'Priority': '1'
                    },
                    {
                        'Title': f'{ENV} - Customer validation',
                        'Description': f"""Validate with customer ingested data in current environment.
                        Input: Data ingested in {ENV} and available for the customer""",
                        'AcceptanceCriteria': f'Customer provides their OK to deploy to production',
                        'Priority': '1'
                    }
                ]
            # Creating User Stories
            for us in user_stories:
                create_user_story(devops=devops, title=us['Title'], description=us['Description'],
                                  acceptance_criteria=us['AcceptanceCriteria'], priority=us['Priority'], tags=us_tags,
                                  relations=us_relation)
        else:
            print("Fiter and Epic already exist for this project and code. The User Stories won't be created")


if __name__ == '__main__':
    print("")
    # data = getEpicObject(data_eng_devops, 'RODRIGOTEST1')
    # print(data)
    # x.delete_object(data_eng_devops)
# WorkItem(organization=i['fields'])
# Method to update element
# Method to delete element
