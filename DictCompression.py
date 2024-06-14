codeSize = 4

def startDict():
    dictionary = dict()

    for i in range(0, 256):
        dictionary[chr(i)] = str(i).rjust(codeSize, '0')

    return dictionary



def compress(inputFileName, outputFileName):

    ### Set up files
    # How to read file from: https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/
    # How to convert char to int from: https://stackoverflow.com/a/704160
    inputFile = open(inputFileName, "r")
    outputFile = open(outputFileName, "w")

    ### Actual compression

    dictionary = startDict()
    buffer = ""
    counter = 256
    
    # Go through input char by char
    while True:

        nextChar = inputFile.read(1)
        print("Next char:", str(nextChar))

        # Stop looping if nothing to read
        if (not nextChar):

            # But clear the buffer first
            if (len(buffer) > 0):
                outputFile.write(dictionary[buffer])

            break

        # Add char to buffer
        newBuff = buffer + str(nextChar)
        print("New buffer:", newBuff)

        # If new buffer in dict, leave alone
        if (code := dictionary.get(newBuff)):
            print("Found " + newBuff + "'s code: " + code)
            buffer = newBuff
            print("Buffer:", buffer)

        # Otherwise, add new buffer to dict
        else:
            dictionary[newBuff] = str(counter).rjust(codeSize, "0")
            counter += 1
        
            # Then send old buffer and make char the new buffer
            if (len(buffer) > 0):
                outputFile.write(dictionary[buffer])
                print("Wrote " + dictionary[buffer] + " to output!")

            buffer = str(nextChar)
            print("Buffer:", buffer) 
        
        print()

    inputFile.close()
    outputFile.close()

compress("./encryptedLetter.txt", "./finalLetter.txt")
