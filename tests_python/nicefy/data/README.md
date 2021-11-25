# Borderless360 test task for full-stack / backend developers

Hello there! Thanks for applying to join the Borderless360 team.

Here is a test task for a full-stack or backend developer vacancy.

For general background about the company and our SaaS platform, see
[here](https://www.borderless360.com/global-fulfilment/) and
[here](https://www.borderless360.com/platform-overview/).

## Context

This task is about improving the history feature of the Borderless360 app.

Currently we have a history feature that provides an overview of what actions
have been made while a user is editing an order (or any other API resource). In
other words, several users might be editing the same order, so we need to know
what each of them did.

A user can perform 3 actions (`event_type` name provided in the brackets):

- create an object (`created`)
- update an object (`updated`)
- trigger an action (`transition`)

## Task

Your task is to provide a solution to display this history information in the most
useful way to the users. In the repo is an
[example screenshot](https://github.com/Borderless360/test_task/blob/main/sample4_pic.png)
of how it works right now, but it's up to you to decide if you can improve the feature.

In the [data folder](https://github.com/Borderless360/test_task/tree/main/data)
are 5 data samples which should give you enough information on different cases.

Two subtasks:

1. Your solution;
2. Brief design report communicating the design ideas and decisions and lessons
   to other members of the tech team. Any format is fine (e.g. Markdown or Notion).

Technical requirements for the solution:

- JavaScript (or TypeScript) - provide a script and implement basic HTML and
  CSS. Just make it presentable, no need to copy our styles from the
  screenshot.
- Python - provide a Python script implementing the same solution. It's up to you
  how to present it; simple output into the console could be enough.
- Code requirements. Make sure to follow all JavaScript and Python (PEP8)
  standards. Provide useful comments and docstring in the code.
