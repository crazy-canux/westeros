*** Settings ***
Library    pytestautomation.keywords.aggregated_workflow.AggregatedWorkflow

*** Variables ***
{conf_dir}    ~/pytestautomation/etc/
{global_file}    {conf_dir}/global.yaml

*** Test Cases ***

Test Setup Case
    [Documentation]    Test if browser and dirver and python packages working well.
    [tags]    SETUP
    [Setup]    Load Configurations    ${global_file}
    [Teardown]    Clean Up Environment
    Comment    User Launches Browser
    User Launches Browser





