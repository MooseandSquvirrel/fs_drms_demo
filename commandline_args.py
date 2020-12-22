    
def args():
    print("\n\n\n\t\t\t\t***** MAKE SURE YOU HAVE 'FT_CLIENT' AND 'FT_SECRET' FOR 42 API ACCESS SET AS ENV VARIABLES IN TERMINAL  *****")
    args_check = ""
    while args_check != 'y':
        commandline_arg = input("\n\n\n\nIf you would like to run a 'Close' on all 'FAIL'-ed room inspections: \nEnter 'c'\n\nTo run an 'Open' on previously 'FAIL'-ed room inspections:\nFIRST, change the Pisciner(s) status in Google Sheet to 'PASS'.\nMake sure their account(s) Close Status is 'y' for yes in the last column of Google Form.\nThen on command line enter 'o'\n")
        if (commandline_arg != 'c') and (commandline_arg != 'o'):
            print("\n\n\n\n\n\n\nPlease type only a 'c' or 'o'.\nDon't be one of those dumb users. You're not dumb...\nare you...?")
            continue
        print("You Entered: " + commandline_arg)
        args_check = input("If this is correct enter 'y', otherwise press Enter to try again.\n")
    return commandline_arg