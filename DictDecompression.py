codeSize = 4

def startDict():
    dictionary = dict()

    for i in range(0, 256):
        dictionary[str(i).rjust(codeSize, '0')] = chr(i)

    return dictionary

def decompress(inputFileName, outputFileName):

    ### Set up files
    # How to read file from: https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/
    # How to convert char to int from: https://stackoverflow.com/a/704160
    inputFile = open(inputFileName, "r")
    outputFile = open(outputFileName, "w")

    ### Actual decompression

    dictionary = startDict()
    prevCode = ""
    counter = 256

    # Go through input code by code
    while True:

        code = inputFile.read(codeSize)
        print("Next code: '" + str(code) + "'")

        # Stop looping if nothing to read
        if (not code):
            break

        # If code in dict, decode
        if (phrase := dictionary.get(code)):

            # Create new code if need to
            if (prevCode != ""):
                print("Attempting to add new phrase!")
                newPhrase = prevCode + phrase[0]

                if (newPhrase not in dictionary.values()):
                    dictionary[str(counter).rjust(codeSize, '0')] = newPhrase
                    print("Made new code:", counter, "for", newPhrase)
                    counter += 1
        
        # Otherwise, must be the Special Case
        else:
            print("Last counter:", counter - 1)
            print("Last code:", dictionary.get(counter - 1))
            phrase = prevCode + prevCode[0]
            dictionary[str(counter).rjust(codeSize, '0')] = phrase
            counter += 1
        
        # Once gotten, write it to the output file
        outputFile.write(phrase)
        print("Wrote " + phrase + " to file")

        prevCode = phrase

        print()
    
    inputFile.close()
    outputFile.close()

decompress("./finalLetter.txt", "./decompressedLetter.txt")

        


        