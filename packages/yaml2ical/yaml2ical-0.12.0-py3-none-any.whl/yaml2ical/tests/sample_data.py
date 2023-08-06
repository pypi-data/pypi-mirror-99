#! /usr/bin/env python
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Sample meeting data to use for testing."""

BAD_MEETING_DAY = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: go_bang
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam project.
"""

WEEKLY_MEETING = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

CONFLICTING_WEEKLY_MEETING = """
project: OpenStack Subteam Meeting 2
schedule:
  - time: '1230'
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam 2 project.
agenda: |
  * New features
"""

WEEKLY_OTHER_CHANNEL_MEETING = """
project: OpenStack Subteam Meeting 3
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting-alt
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam 3 project.
agenda: |
  * New features
"""

ALTERNATING_MEETING = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-even
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-odd
chair: Jane Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

BIWEEKLY_EVEN_MEETING = """
project: OpenStack Subteam 12 Meeting
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-even
chair: Jane Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

BIWEEKLY_ODD_MEETING = """
project: OpenStack Subteam 12 Meeting
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-odd
chair: Jane Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

MEETING_SUNDAY_LATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '2330'
    day: Sunday
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly late meeting for Subteam 8 project.
"""

MEETING_MONDAY_EARLY = """
project: OpenStack Subteam Meeting
schedule:
  - time: '0000'
    day: Monday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly long meeting for Subteam project.
"""

MEETING_MONDAY_LATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '2330'
    day: Monday
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly late meeting for Subteam 8 project.
"""

MEETING_TUESDAY_EARLY = """
project: OpenStack Subteam Meeting
schedule:
  - time: '0000'
    day: Tuesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly long meeting for Subteam project.
"""

MEETING_WITH_DURATION = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    duration: 30
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
agenda: |
  * Debate whether this should be a longer meeting
"""

MEETING_WITH_START_DATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    duration: 30
    day: Thursday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
agenda: |
  * Debate whether this should be a longer meeting
"""

MEETING_WITH_SKIP_DATES = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skip_date: 20150810
          reason: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

MEETING_WITH_SKIP_DATES_BAD_DATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skip_date: 2015080
          reason: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

# typo in skip_date
MEETING_WITH_MISSING_SKIP_DATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skiip_date: 20150806
          reason: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

# typo in reason
MEETING_WITH_MISSING_REASON = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skip_date: 20150806
          reaso: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

# adhoc meeting
ADHOC_MEETING = """
project: OpenStack Random Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: adhoc
chair: Shannon Stacker
description: >
    Adhoc random meeting for Subteam project.
"""

QUADWEEKLY_MEETING_ALTERNATING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: quadweekly
  - time: '600'
    duration: 45
    start_date: 20150801
    day: Thursday
    irc: openstack-meeting
    frequency: quadweekly-alternate
chair: John Doe
description:  >
  Example alternating quadweekly meeting
"""

QUADWEEKLY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: quadweekly
chair: John Doe
description:  >
  Example Quadweekly meeting
"""

QUADWEEKLY_MEETING_WEEK_1 = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: quadweekly-week-1
chair: John Doe
description:  >
  Example Quadweekly meeting on week 1
"""

QUADWEEKLY_MEETING_WEEK_2 = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: quadweekly-week-2
chair: John Doe
description:  >
  Example Quadweekly meeting on week 2
"""

QUADWEEKLY_MEETING_WEEK_3 = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: quadweekly-week-3
chair: John Doe
description:  >
  Example Quadweekly meeting on week 3
"""

QUADWEEKLY_MEETING_ALTERNATE = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: quadweekly-alternate
chair: John Doe
description:  >
  Example Quadweekly Alternate meeting
"""

FIRST_MONDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Monday
    irc: openstack-meeting
    frequency: first-monday
chair: John Doe
description:  >
  Example Monthly meeting
"""

FIRST_TUESDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Tuesday
    irc: openstack-meeting
    frequency: first-tuesday
chair: John Doe
description:  >
  Example Monthly meeting
"""

WEEKLY_MEETING_2200 = """
project: OpenStack Subteam Meeting
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

FIRST_WEDNESDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: first-wednesday
chair: John Doe
description:  >
  Example Monthly meeting
"""

FIRST_THURSDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Thursday
    irc: openstack-meeting
    frequency: first-thursday
chair: John Doe
description:  >
  Example Monthly meeting
"""

FIRST_FRIDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Friday
    irc: openstack-meeting
    frequency: first-friday
chair: John Doe
description:  >
  Example Monthly meeting
"""

SECOND_WEDNESDAY_MEETING = """
project: CentOS Cloud SIG
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: centos-meeting
    frequency: second-wednesday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

SECOND_THURSDAY_MEETING = """
project: CentOS Storage SIG
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Thursday
    irc: centos-meeting
    frequency: second-thursday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

SECOND_FRIDAY_MEETING = """
project: CentOS Hyperscale SIG
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Friday
    irc: centos-meeting
    frequency: second-friday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

THIRD_MONDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Monday
    irc: openstack-meeting
    frequency: third-monday
chair: John Doe
description:  >
  Example Monthly meeting
"""

THIRD_TUESDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Tuesday
    irc: openstack-meeting
    frequency: third-tuesday
chair: John Doe
description:  >
  Example Monthly meeting
"""

THIRD_WEDNESDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: third-wednesday
chair: John Doe
description:  >
  Example Monthly meeting
"""

THIRD_THURSDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Thursday
    irc: openstack-meeting
    frequency: third-thursday
chair: John Doe
description:  >
  Example Monthly meeting
"""

THIRD_FRIDAY_MEETING = """
project: OpenStack Random Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Friday
    irc: openstack-meeting
    frequency: third-friday
chair: John Doe
description:  >
  Example Monthly meeting
"""

FOURTH_MONDAY_MEETING = """
project: CentOS SIG Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Monday
    irc: centos-meeting
    frequency: fourth-monday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

FOURTH_TUESDAY_MEETING = """
project: CentOS SIG Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Tuesday
    irc: centos-meeting
    frequency: fourth-tuesday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

FOURTH_WEDNESDAY_MEETING = """
project: CentOS SIG Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Wednesday
    irc: centos-meeting
    frequency: fourth-wednesday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

FOURTH_THURSDAY_MEETING = """
project: CentOS SIG Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Thursday
    irc: centos-meeting
    frequency: fourth-thursday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""

FOURTH_FRIDAY_MEETING = """
project: CentOS SIG Meeting
agenda_url: http://agenda.com/
project_url: http://project.com
schedule:
  - time: '2200'
    day: Friday
    irc: centos-meeting
    frequency: fourth-friday
chair: Jane Deer
description:  >
  Example Monthly meeting
"""
