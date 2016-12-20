@machines
Feature: Actions for machines

  Background:
    Given I am logged in to mist.core

  @machine-create
  Scenario: Create a machine in Docker provider and check the ssh connection
    When I visit the Machines page
#    Given "Docker" cloud has been added
#    Given "Testkey" key has been added
#    When I visit the Machines page
#    And I click the button "+"
#    Then I expect the "Machine" add form to be visible within max 10 seconds
#    When I open the "Choose Cloud" drop down
#    And I wait for 1 seconds
#    When I click the button "Docker" in the "Choose Cloud" dropdown
#    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
#    When I select the proper values for "Docker" to create the "docker-ui-test" machine
#    Then I click the "Launch" button
#    And I wait for 3 seconds
#    Then I visit the Machines page
#    Then "docker-ui-test" machine should be present within 40 seconds
    And I wait for 1 seconds
    When I click the "docker-ui-test" "machine"

#    Then I click the Shell button in the machine edit form
    #Then I test the ssh connection
    # Then I test the ssh connection 2 times for max 100 seconds each time
    And I wait for 5 seconds
    Then I visit the Home page


  @machine-stop
  Scenario: Stop the machine created above
    When I visit the Machines page
    When I click the "docker-ui-test" "machine"
    Then I click the button "Stop" from the menu of the "machine" edit form
    And I expect the dialog "Stop 1 Machines" is open within 2 seconds
    And I click the "Stop" button in the dialog "Stop 1 Machines"
    When I visit the Machines page
    Then "docker-ui-test" machine state should be "stopped" within 10 seconds


  @machine-start
  Scenario: Start the machine that was stopped above
    When I click the "docker-ui-test" "machine"
    Then I click the button "Start" from the menu of the "machine" edit form
    And I expect the dialog "Start Machine" is open within 2 seconds
    And I click the "Start" button in the dialog "Start Machine"
    When I visit the Machines page
    Then "docker-ui-test" machine state should be "running" within 10 seconds


  @machine-reboot
  Scenario: Reboot the machine
    When I click the "docker-ui-test" "machine"
    Then I click the button "Reboot" from the menu of the "machine" edit form
    And I expect the dialog "Reboot Machine" is open within 2 seconds
    And I click the "Reboot" button in the dialog "Reboot Machine"


  @machine-destroy
  Scenario: Destroy the machine created
    When I wait for the dashboard to load
    When I visit the Machines page
    And I wait for 2 seconds
    When I click the "docker-ui-test" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I click the button "Destroy" from the menu of the "machine" edit form
    And I expect the dialog "Destroy 1 Machine" is open within 4 seconds
    And I click the "Destroy" button in the dialog "Destroy 1 Machine"
    And I expect the dialog "Destroy 1 Machine" is closed within 4 seconds
    Then I visit the Machines page
    Then "docker-ui-test" machine should be absent within 40 seconds
