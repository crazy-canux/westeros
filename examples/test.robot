*** Settings ***

Resource            ../CommonResource.robot
Force Tags          MyTag
Library        pytestautomation
Library        Selenium2Library

*** Variables ***
{conf_dir}    C:\\Users\\Chengc5\\Desktop\\Src\\pytestautomation\\etc
{global_file}    {conf_dir}\\global.yaml

*** Testcases ***
Test Setup Case
    [Documentation]    Test if browser and dirver and python packages working well.
    [tags]    SETUP
    [Setup]    Load Configurations    ${global_file}
    [Teardown]    Clean Up Environment
    Comment    User Launches Browser
    User Launches Browser

