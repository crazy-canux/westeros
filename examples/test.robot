*** Settings ***
Library    westeros.keywords.workflow.Workflow

*** Variables ***
{conf_dir}       ../etc
{global_file}    {conf_dir}/global.yaml

*** Test Cases ***
[Test-1] Test basic functions.
    [Documentation]    Test this package.
    [Tags]    SETUP
    [Setup]    Load Configurations    ${global_file}
    [Teardown]    Tear Down
    Comment    User Open Browser
    User Open Browser
    User Close Browser
    Clean Up Environment
