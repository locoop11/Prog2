import sys
from runner import Runner

def main():
    """
    Main program.
    Requires:
    Three command-line arguments, corresponding to the names of the files
    with the list of doctors, the list of birth assistances and the list of requests, respectively.
    """
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Error: invalid number of arguments.")
        print("Usage: python refresh.py <doctors filename> <schedule filename> <requests filename>")
        return
    
    # Extract the file names from the command-line arguments
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]

    doctorsFileName = ""
    requestsFilName = ""
    scheduleFileName = ""

    for file in sys.argv:
        if file.find("doctors") != -1:
            doctorsFileName = file
        if file.find("schedule") != -1:
            scheduleFileName = file
        if file.find("requests") != -1:
            requestsFilName = file
    if( doctorsFileName == "" or requestsFilName == "" or scheduleFileName == ""):
        print("Usage Error: Missing mandatory file.")
        print("Usage: python refresh.py <doctors filename> <schedule filename> <requests filename>")
        exit(1)
    try:
        #"Para os testes" runner = Runner("./testSets_v1/testSet1/doctors10h00.txt", "./testSets_v1/testSet1/requests10h30.txt", "./testSets_v1/testSet1/schedule10h00.txt")
        runner = Runner(doctorsFileName, requestsFilName, scheduleFileName)
        runner.run()
        

    except Exception as e:
        print(f"An error occurred: {e.with_traceback()}")
        print(f"An error occurred: {e}")
        # Optionally, you can perform additional error handling here if needed

        # Exit in a controlled way (e.g., with a specific exit code)
        exit(1)  # Exit with a non-zero exit code to indicate an error

    


if __name__ == "__main__":
    main()
        

