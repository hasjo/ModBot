#This is a sample module, meant as the basis for creating a new module

# The module needs a Dictionary of the command that can be run, and the name of the module.
# The logic for needing the module name is that the main program will run the receiving program
# on the module and the module will handle the input and return the message or do what is needed
CommandDict = {"!test":"SampleModule", "!modname":"SampleModule"}

#This tells the main program what commands the module is looking for and the name of the module
def GiveDict():
    return CommandDict

#This function is what the main program calls to execute the command
def ReceiveMsg(command):
    print(command + " - SampleModule")
    #I used find so you could potentially use arguments
    if command.find("!test") != -1:
        return "THIS IS A TEST OF THE SAMPLE MODULE"
    if command.find("!modname") != -1:
        return "This is the Sample Module"

