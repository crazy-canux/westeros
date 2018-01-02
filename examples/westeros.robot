*** Settings ***
Library    westeros.keywords.workflows.Workflows

*** Variables ***
${conf_path}    /etc/westeros
# For debug
#${conf_path}    ../etc

${global_conf_file}    ${conf_path}/global.yaml
${shared_conf_file}    ${conf_path}/shared.yaml

*** Test Cases ***
[Setup] Installing and Configuration env for new major.minor.
    [Documentation]    Before run test case, you should setup the environment,
    ...    Include database and all processes, just for new major and minor
    [Tags]    SETUP
    [Setup]    Load Configurations    ${global_conf_file}    ${shared_conf_file}
    [Teardown]    Clean Environment
    comment    Install and config on the cluster.
    Setup Environment

[Update] Upgrade on cluster for new patch.
    [documentation]    Before run test case, you should update the environment.
    ...    Include database and all processes, just for new patch.
    [Tags]    UPDATE
    [Setup]    Load Configurations    ${global_conf_file}    ${shared_conf_file}
    [Teardown]    Clean Environment
    comment    Update and config on cluster.
    Update Environment

[Teardown] Destroy the test environment. Dont's run this case until you know what you are doing.
    [Documentation]    After you finish test this version major.minro.patch.
    ...    Or before you install a new version.
    [Tags]    TEARDOWN    DISABLED
    [Setup]    Load Configurations    ${global_conf_file}    ${shared_conf_file}
    [Teardown]    Destroy Environment
    comment    Warning!

[WF-1] Westeros Workflow 1.
    [Documentation]    test basic functions.
    [Tags]    Start
    [Setup]    Load Configurations    ${global_conf_file}    ${shared_conf_file}
    [Teardown]

