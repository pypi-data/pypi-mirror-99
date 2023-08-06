#! /usr/bin/python3
"""
Jira to task-juggler extraction script

This script queries Jira, and generates a task-juggler input file to generate a Gantt chart.
"""
import argparse
import logging
import re
from abc import ABC, abstractmethod
from functools import cmp_to_key
from getpass import getpass

from dateutil import parser
from jira import JIRA, JIRAError
from natsort import natsorted, ns

DEFAULT_LOGLEVEL = 'warning'
DEFAULT_JIRA_URL = 'https://jira.melexis.com/jira'
DEFAULT_OUTPUT = 'jira_export.tjp'

JIRA_PAGE_SIZE = 50

TAB = ' ' * 4


def set_logging_level(loglevel):
    """Sets the logging level

    Args:
        loglevel (str): String representation of the loglevel
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)


def to_identifier(key):
    """Converts given key to identifier, interpretable by TaskJuggler as a task-identifier

    Args:
        key (str): Key to be converted

    Returns:
        str: Valid task-identifier based on given key
    """
    return key.replace('-', '_')


class JugglerTaskProperty(ABC):
    """Class for a property of a Task Juggler"""

    DEFAULT_NAME = 'property name'
    DEFAULT_VALUE = 'not initialized'
    PREFIX = ''
    SUFFIX = ''
    TEMPLATE = TAB + '{prop} {value}\n'
    VALUE_TEMPLATE = '{prefix}{value}{suffix}'

    def __init__(self, jira_issue=None):
        """Initializes the task juggler property

        Args:
            jira_issue (jira.resources.Issue): The Jira issue to load from
            value (object): Value of the property
        """
        self.name = self.DEFAULT_NAME
        self.value = self.DEFAULT_VALUE

        if jira_issue:
            self.load_from_jira_issue(jira_issue)

    @abstractmethod
    def load_from_jira_issue(self, jira_issue):
        """Loads the object with data from a Jira issue

        Args:
            jira_issue (jira.resources.Issue): The Jira issue to load from
        """

    def append_value(self, value):
        """Appends value for task juggler property

        Args:
            value (object): Value to append to the property
        """
        self.value.append(value)

    def validate(self, task, tasks):
        """Validates (and corrects) the current task property

        Args:
            task (JugglerTask): Task to which the property belongs
            tasks (list): List of JugglerTask instances to which the current task belongs. Will be used to
                verify relations to other tasks.
        """

    def __str__(self):
        """Converts task property object to the task juggler syntax

        Returns:
            str: String representation of the task property in juggler syntax
        """
        if self.value is not None:
            return self.TEMPLATE.format(prop=self.name,
                                        value=self.VALUE_TEMPLATE.format(prefix=self.PREFIX,
                                                                         value=self.value,
                                                                         suffix=self.SUFFIX))
        return ''


class JugglerTaskAllocate(JugglerTaskProperty):
    """Class for the allocation (assignee) of a juggler task"""

    DEFAULT_NAME = 'allocate'
    DEFAULT_VALUE = 'not assigned'

    def load_from_jira_issue(self, jira_issue):
        """Loads the object with data from a Jira issue

        Args:
            jira_issue (jira.resources.Issue): The Jira issue to load from
        """
        if hasattr(jira_issue.fields, 'assignee'):
            self.value = jira_issue.fields.assignee.name
        else:
            self.value = self.DEFAULT_VALUE


class JugglerTaskEffort(JugglerTaskProperty):
    """Class for the effort (estimate) of a juggler task"""

    # For converting the seconds (Jira) to days
    UNIT = 'd'
    FACTOR = 8.0 * 60 * 60

    DEFAULT_NAME = 'effort'
    MINIMAL_VALUE = 1.0 / 8
    DEFAULT_VALUE = MINIMAL_VALUE
    SUFFIX = UNIT

    def load_from_jira_issue(self, jira_issue):
        """Loads the object with data from a Jira issue

        Args:
            jira_issue (jira.resources.Issue): The Jira issue to load from
        """
        if hasattr(jira_issue.fields, 'timeestimate'):
            if jira_issue.fields.timeestimate is not None:
                val = jira_issue.fields.timeestimate
                self.value = (val / self.FACTOR)
            else:
                self.value = 0
        else:
            self.value = self.DEFAULT_VALUE
            logging.warning('No estimate found for %s, assuming %s%s', jira_issue.key, self.DEFAULT_VALUE, self.UNIT)

    def validate(self, task, tasks):
        """Validates (and corrects) the current task property

        Args:
            task (JugglerTask): Task to which the property belongs
            tasks (list): List of JugglerTask instances to which the current task belongs. Will be used to
                verify relations to other tasks.
        """
        if self.value == 0:
            logging.warning('Estimate for %s, is 0. Excluding', task.key)
            tasks.remove(task)
        elif self.value < self.MINIMAL_VALUE:
            logging.warning('Estimate %s%s too low for %s, assuming %s%s', self.value, self.UNIT, task.key, self.MINIMAL_VALUE, self.UNIT)
            self.value = self.MINIMAL_VALUE


class JugglerTaskDepends(JugglerTaskProperty):
    """Class for linking of a juggler task"""

    DEFAULT_NAME = 'depends'
    DEFAULT_VALUE = []
    PREFIX = '!'

    @property
    def value(self):
        """list: Value of the task juggler property"""
        return self._value

    @value.setter
    def value(self, value):
        """Sets value for task juggler property (deep copy)

        Args:
            value (object): New value of the property
        """
        self._value = list(value)

    def load_from_jira_issue(self, jira_issue):
        """Loads the object with data from a Jira issue

        Args:
            jira_issue (jira.resources.Issue): The Jira issue to load from
        """
        self.value = self.DEFAULT_VALUE
        if hasattr(jira_issue.fields, 'issuelinks'):
            for link in jira_issue.fields.issuelinks:
                if hasattr(link, 'inwardIssue') and link.type.name == 'Blocker':
                    self.append_value(to_identifier(link.inwardIssue.key))
                if hasattr(link, 'outwardIssue') and link.type.name == 'Dependency':
                    self.append_value(to_identifier(link.outwardIssue.key))

    def validate(self, task, tasks):
        """Validates (and corrects) the current task property

        Args:
            task (JugglerTask): Task to which the property belongs
            tasks (list): List of JugglerTask instances to which the current task belongs. Will be used to
                verify relations to other tasks.
        """
        for val in self.value:
            if val not in [to_identifier(tsk.key) for tsk in tasks]:
                logging.warning('Removing link to %s for %s, as not within scope', val, task.key)
                self.value.remove(val)

    def __str__(self):
        """Converts task property object to the task juggler syntax

        Returns:
            str: String representation of the task property in juggler syntax
        """
        if self.value:
            valstr = ''
            for val in self.value:
                if valstr:
                    valstr += ', '
                valstr += self.VALUE_TEMPLATE.format(prefix=self.PREFIX,
                                                     value=val,
                                                     suffix=self.SUFFIX)
            return self.TEMPLATE.format(prop=self.name,
                                        value=valstr)
        return ''


class JugglerTask:
    """Class for a task for Task-Juggler"""

    DEFAULT_KEY = 'NOT_INITIALIZED'
    MAX_SUMMARY_LENGTH = 70
    DEFAULT_SUMMARY = 'Task is not initialized'
    TEMPLATE = '''
task {id} "{description}" {{
{tab}Jira "{key}"
{props}
}}
'''

    def __init__(self, jira_issue=None):
        logging.info('Create JugglerTask for %s', jira_issue.key)

        self.key = self.DEFAULT_KEY
        self.summary = self.DEFAULT_SUMMARY
        self.properties = {}
        self.issue = None

        if jira_issue:
            self.load_from_jira_issue(jira_issue)

    def load_from_jira_issue(self, jira_issue):
        """Loads the object with data from a Jira issue

        Args:
            jira_issue (jira.resources.Issue): The Jira issue to load from
        """
        self.key = jira_issue.key
        self.issue = jira_issue
        summary = jira_issue.fields.summary.replace('\"', '\\\"')
        self.summary = (summary[:self.MAX_SUMMARY_LENGTH] + '...') if len(summary) > self.MAX_SUMMARY_LENGTH else summary
        self.properties['allocate'] = JugglerTaskAllocate(jira_issue)
        self.properties['effort'] = JugglerTaskEffort(jira_issue)
        self.properties['depends'] = JugglerTaskDepends(jira_issue)

    def validate(self, tasks):
        """Validates (and corrects) the current task

        Args:
            tasks (list): List of JugglerTask instances to which the current task belongs. Will be used to
                verify relations to other tasks.
        """
        if self.key == self.DEFAULT_KEY:
            logging.error('Found a task which is not initialized')

        for task_property in self.properties.values():
            task_property.validate(self, tasks)

    def __str__(self):
        """Converts the JugglerTask to the task juggler syntax

        Returns:
            str: String representation of the task in juggler syntax
        """
        props = "".join(map(str, self.properties.values()))
        return self.TEMPLATE.format(id=to_identifier(self.key),
                                    key=self.key,
                                    tab=TAB,
                                    description=self.summary.replace('\"', '\\\"'),
                                    props=props)


class JiraJuggler:
    """Class for task-juggling Jira results"""

    def __init__(self, url, user, passwd, query):
        """Constructs a JIRA juggler object

        Args:
            url (str): URL to the JIRA server
            user (str): Username on JIRA server
            passwd (str): Password of username on JIRA server
            query (str): The Query to run on JIRA server
        """
        logging.info('Jira server: %s', url)

        self.jirahandle = JIRA(url, basic_auth=(user, passwd))
        logging.info('Query: %s', query)
        self.query = query
        self.issue_count = 0

    @staticmethod
    def validate_tasks(tasks):
        """Validates (and corrects) tasks

        Args:
            tasks (list): List of JugglerTask instances to validate
        """
        for task in list(tasks):
            task.validate(tasks)

    def load_issues_from_jira(self, depend_on_preceding=False, sprint_field_name=''):
        """Loads issues from Jira

        Args:
            depend_on_preceding (bool): True to let each task depend on the preceding task that has the same user
                allocated to it, unless it is already linked; False to not add these links
            sprint_field_name (str): Name of field to sort tasks on

        Returns:
            list: A list of JugglerTask instances
        """
        tasks = []
        busy = True
        while busy:
            try:
                issues = self.jirahandle.search_issues(self.query, maxResults=JIRA_PAGE_SIZE, startAt=self.issue_count)
            except JIRAError:
                logging.error('Invalid Jira query "%s"', self.query)
                return None

            if len(issues) <= 0:
                busy = False

            self.issue_count += len(issues)

            for issue in issues:
                logging.debug('Retrieved %s: %s', issue.key, issue.fields.summary)
                tasks.append(JugglerTask(issue))

        self.validate_tasks(tasks)
        if sprint_field_name:
            self.sort_tasks_on_sprint(tasks, sprint_field_name)
        if depend_on_preceding:
            self.link_to_preceding_task(tasks)
        return tasks

    def juggle(self, output=None, **kwargs):
        """Queries JIRA and generates task-juggler output from given issues

        Args:
            list: A list of JugglerTask instances
        """
        juggler_tasks = self.load_issues_from_jira(**kwargs)
        if not juggler_tasks:
            return None
        if output:
            with open(output, 'w') as out:
                for task in juggler_tasks:
                    out.write(str(task))
        return juggler_tasks

    @staticmethod
    def link_to_preceding_task(tasks):
        """Links task to preceding task with the same assignee.

        If it's the first task for a given assignee and it's not linked with 'depends on'/'is blocked by' through JIRA,
        'start ${now}' is added instead.

        Args:
            tasks (list): List of JugglerTask instances to modify
        """
        assignees_to_tasks = {}
        for task in tasks:
            assignee = str(task.properties['allocate'])
            if assignee in assignees_to_tasks:
                preceding_task = assignees_to_tasks[assignee][-1]
                task.properties['depends'].append_value(to_identifier(preceding_task.key))
                assignees_to_tasks[assignee].append(task)
            else:
                assignees_to_tasks[assignee] = [task]
                depends_property = task.properties['depends']
                if not depends_property.value:
                    depends_property.name = 'start'
                    depends_property.PREFIX = ''
                    depends_property.append_value('${now}')

    def sort_tasks_on_sprint(self, tasks, sprint_field_name):
        """Sorts given list of tasks based on the values of the field with the given name.

        JIRA issues that are not assigned to a sprint will be ordered last.

        Args:
            tasks (list): List of JugglerTask instances to sort in place
            sprint_field_name (str): Name of the field that contains information about sprints
        """
        priorities = {
            "ACTIVE": 3,
            "FUTURE": 2,
            "CLOSED": 1,
        }
        for task in tasks:
            task.sprint_name = ""
            task.sprint_priority = 0
            task.sprint_start_date = None
            if not task.issue:
                continue
            values = getattr(task.issue.fields, sprint_field_name, None)
            if values is not None:
                if isinstance(values, str):
                    values = [values]
                for sprint_info in values:
                    state_match = re.search("state=({})".format("|".join(priorities)), sprint_info)
                    if state_match:
                        state = state_match.group(1)
                        prio = priorities[state]
                        if prio > task.sprint_priority:
                            task.sprint_name = re.search("name=(.+?),", sprint_info).group(1)
                            task.sprint_priority = prio
                            task.sprint_start_date = self.extract_start_date(sprint_info, task.issue.key)
        logging.debug("Sorting tasks based on sprint information...")
        tasks.sort(key=cmp_to_key(self.compare_sprint_priority))

    @staticmethod
    def extract_start_date(sprint_info, issue_key):
        """Extracts the start date from the given info string.

        Args:
            sprint_info (str): Raw information about a sprint, as returned by the JIRA API
            issue_key (str): Name of the JIRA issue

        Returns:
            datetime.datetime/None: Start date as a datetime object or None if the sprint does not have a start date
        """
        start_date_match = re.search("startDate=(.+?),", sprint_info)
        if start_date_match:
            start_date_str = start_date_match.group(1)
            if start_date_str != '<null>':
                try:
                    return parser.parse(start_date_match.group(1))
                except parser.ParserError as err:
                    logging.debug("Failed to parse start date of sprint of issue %s: %s", issue_key, err)
        return None

    @staticmethod
    def compare_sprint_priority(a, b):
        """Compares the priority of two tasks based on the sprint information

        The sprint_priority attribute is taken into account first, followed by the sprint_start_date and, lastly, the
        sprint_name attribute using natural sorting (a sprint with the word 'backlog' in its name is sorted as last).

        Args:
            a (JugglerTask): First JugglerTask instance in the comparison
            b (JugglerTask): Second JugglerTask instance in the comparison

        Returns:
            int: 0 for equal priority; -1 to prioritize a over b; 1 otherwise
        """
        if a.sprint_priority > b.sprint_priority:
            return -1
        if a.sprint_priority < b.sprint_priority:
            return 1
        if a.sprint_priority == 0 or a.sprint_name == b.sprint_name:
            return 0  # no/same sprint associated with both issues
        if a.sprint_start_date == b.sprint_start_date:
            # a sprint with backlog in its name has lower priority
            if "backlog" not in a.sprint_name.lower() and "backlog" in b.sprint_name.lower():
                return -1
            if "backlog" in a.sprint_name.lower() and "backlog" not in b.sprint_name.lower():
                return 1
            if natsorted([a.sprint_name, b.sprint_name], alg=ns.IGNORECASE)[0] == a.sprint_name:
                return -1
            return 1
        elif a.sprint_start_date < b.sprint_start_date:
            return -1
        return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', default=DEFAULT_LOGLEVEL,
                        help='Level for logging (strings from logging python package)')
    parser.add_argument('-j', '--jira', dest='url', default=DEFAULT_JIRA_URL,
                        help='URL to JIRA server')
    parser.add_argument('-u', '--username', required=True,
                        help='Your username on JIRA server')
    parser.add_argument('-q', '--query', required=True,
                        help='Query to perform on JIRA server')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                        help='Output .tjp file for task-juggler')
    parser.add_argument('--depend-on-preceding', action='store_true',
                        help='Flag to let tasks depend on the preceding task with the same assignee')
    parser.add_argument('-s', '--sort-on-sprint', dest='sprint_field_name', default='',
                        help="Sort tasks by using field name that stores sprint(s), e.g. customfield_10851, in "
                             "addition to the original order")
    args = parser.parse_args()

    set_logging_level(args.loglevel)

    PASSWORD = getpass('Enter JIRA password for {user}: '.format(user=args.username))

    JUGGLER = JiraJuggler(args.url, args.username, PASSWORD, args.query)

    JUGGLER.juggle(args.output, depend_on_preceding=args.depend_on_preceding, sprint_field_name=args.sprint_field_name)
    return 0


def entrypoint():
    """Wrapper function of main"""
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
