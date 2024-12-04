*** Settings ***
# Library    RPA.Browser.Selenium    auto_close=${False}
Library  SeleniumLibrary
Library    Collections
Library    OperatingSystem
Library    String


Library    String
Library    RPA.JSON

*** Variables ***


${username}           BUZZWORKS2012           
${password}           Work$2024Bu$$
${bulk_file}      ${EMPTY}
${output_data}  ${EMPTY}
${OUTPUT_DIR}        /home/buzzadmin/Desktop/id_card_api/Project/id_card/



*** Keywords ***
Click Element When Visible
    [Arguments]    ${PreLocator}    ${Elementtype}    ${PostLocator}
    Wait Until Element Is Visible     ${PreLocator}   timeout=120    error=${Elementtype} not visible within 2m
    Click Element     ${PreLocator}
    Wait Until Element Is Visible    ${PostLocator}    timeout=30    error= unable to navigate to next page
    Log    Successfully Clicked on ${Elementtype}


    
Open EPF India Website
    Open Browser    https://www.epfindia.gov.in/site_en/index.php#    chrome    options=add_experimental_option("detach", True)    
Click ECR/Returns/Payment Button
    Wait Until Element Is Visible    xpath://*[@id="ecr_panel_1"]    timeout=30     error=Unbale to launch EPF website..    
    Click Element     xpath://*[@id="ecr_panel_1"]
    Switch Window        EPFO: Home     timeout=30s
    Maximize Browser Window
Accept Popup
    Wait Until Element Is Visible    xpath://*[@id="btnCloseModal"]    timeout=30s     error= Unable to find Alert Popup..
    Click Button    xpath://*[@id="btnCloseModal"]  
    Log    Opened EPFO login page   
Enter Username and Password
    Wait Until Element Is Visible   xpath://*[@id="username1"]    timeout=30s     error=Unable to find username input
    Input Text    xpath://*[@id="username1"]     ${username}       
    Input Text    xpath://*[@id="password"]    ${password}                
    Log    Entered username and password   
Click Signin Button
     Wait Until Element Is Visible     //button[@value="Submit"]  timeout=30s
       Click Button        //button[@value="Submit"]
    TRY
        Wait Until Element Is Visible       //*[contains(@class, 'dropdown-toggle') and contains(text(), 'Payment')]    timeout=30s    error=Unable to login EPFO
    EXCEPT    message 
        Click Element    //*[@id="digitalJeevanAlertBox"]//*[@id="alertButtton"]/a
        Wait Until Element Is Visible       //*[contains(@class, 'dropdown-toggle') and contains(text(), 'Payment')]    timeout=30s    error=Unable to login EPFO
    END    
    Log    Successfully logging EPFO
Go to the member
  Wait Until Element Is Visible    //*[contains(@class, 'dropdown-toggle') and contains(text(), 'Member')]     timeout=30s
  Click Element   //*[contains(@class, 'dropdown-toggle') and contains(text(), 'Member')]        #memeber
  Wait Until Element Is Visible     //ul[@class='dropdown-menu m1']//a[text()='REGISTER-BULK']     timeout=30s
  Click Element     //ul[@class='dropdown-menu m1']//a[text()='REGISTER-BULK']              #registere bulk
  Choose File       //*[@id="bulkRegistrationFile"]   ${bulk_file} 
    Wait Until Element Is Visible    //div//input[@id='aadhaarConsent']     timeout=30s    
    Click Element    //div//input[@id='aadhaarConsent'] 
    Wait Until Element Is Visible    //button[contains(text(), 'Submit')]        timeout=30s
    Click Element    //button[contains(text(), 'Submit')]
    Handle Alert
    # Wait for the member details to load and extract the text
      
    
    ${status}=    Run Keyword And Return Status    Wait Until Element Is Visible    //*[@id="memberDetails"]/div[1]    timeout=30s
    Log    ${status}
    ${output_data}=    Run Keyword If    '${status}' == 'True'    Get Text    //*[@id="memberDetails"]/div[1]    
    ...    ELSE   Log   file not uploaded propelry 
    ${data}    Create Dictionary    output_data=${output_data}    
    ${json_string}=    RPA.JSON.Convert JSON to String    ${data}                                           
    Log    ${data}    console=True
    Create File    ${OUTPUT_DIR}/output_data.json    ${output_data}   encoding=UTF-8

   




*** Test Cases ***
Launch EPFO website
    Log  ${bulk_file} 
    Run Keyword If    '${bulk_file}' == ''    Log    validated_data is empty
    Run Keyword If    '${bulk_file}' != ''    Log    validated data is: ${bulk_file}
    TRY
        Open EPF India Website
    EXCEPT    
        Close Browser
        Open EPF India Website
    END 
  Open EPF India Website
  Click ECR/Returns/Payment Button
  Accept Popup  
Login EPFO Application 
  Enter Username and Password 
  Sleep    15s   
  Click Signin Button
    ${visible}=    Run Keyword And Return Status    Element should be Visible      //*[@id="appletModal"]/div/div/div[1]/button   
    Run Keyword If    ${visible} == True   Log    First alert handled successfully
    Click Button     //*[@id="appletModal"]/div/div/div[1]/button  

    # ${data}=    Set Variable    

    # Lo/g  
    # click register individual

uploading file
  Go to the member
#   Save Output Data to JSON   ${output_data}
  
 
#   file conversion

