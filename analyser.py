from select import select
from numpy import average, sort
from math import floor

"""
Program to help codebreak a Vigenere cipher.

Method based off: http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/
"""

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
lettersByFreqEng = ["e", "a", "r", "i", "o", "t", "n", "s", "l", "c", "u", "d", "p", "m", "h", "g", "b", "f", "y", "w", "k", "v", "x", "z", "j", "q"]


def strip(ciphertext):
    ciphertext = ciphertext.lower()
    ciphertext = "".join([char for char in ciphertext if char in letters])
    return ciphertext

def calcIndexOfCoincidence(text):
    """
    Steps of calculating the index of coincidence from:
    https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html 
    """

    n = len(text)

    # Count frequencies
    counts = dict(zip(letters, [0 for i in range(len(letters))]))
    for char in text:
        if char in letters:
            counts[char] = counts[char] + 1
    
    # Actually calculate the IC
    return (sum([freq * (freq - 1) for freq in counts.values()])) / (n * (n - 1))

def calcICForPeriod(ciphertext, period):

    # Calculate individual ICs
    ics = []
    for i in range(period):
        subset = ciphertext[i: len(ciphertext): period]
        ics.append(calcIndexOfCoincidence("".join(subset)))
    
    # Average them
    return average(ics)

def findPeriod(ciphertext, lowerBound, upperBound):

    # Strip spaces and punctuation
    ciphertext = strip(ciphertext)
    
    # Calculate ICs for each possible period
    ics = dict()
    for i in range(lowerBound, upperBound+1):
        ics[i] = calcICForPeriod(ciphertext, i)
    
    print(ics)

    # Find max IC
    maxIC = max(ics.values())
    period = max(ics, key=ics.get)
    print("The max IC is", maxIC, "for a period of", period)

    return period


def mapCipherToPlain(ciphertext, period, maps):

    plaintext = []
    i = 0
    for char in ciphertext:
        if char in letters:
            plaintext.append(maps[i % period][char])
            i += 1
        elif char.lower() in letters:
            plaintext.append(maps[i % period][char])
            i += 1
        else:
            plaintext.append(char)
    
    return "".join(plaintext)


def doLFA(ciphertext):

    # Count frequencies
    counts = dict(zip(letters, [0 for i in range(len(letters))]))
    for char in ciphertext:
        if char in letters:
            counts[char] = counts[char] + 1
        
    # Find letter with max freq
    mostCommon = max(counts, key=counts.get)

    # Work out shift
    shift = letters.index(mostCommon) - letters.index("e")

    # Reverse it
    map = dict(zip(letters[shift:] + letters[0:shift], letters)) #{cipher: plain}

    return map


def makeCorrections(ciphertext, workingText, period, alphabets):

    while True:
        # Ask if needed
        print("Do you require any corrections? (Y/N)")
        need = input()

        # Get required info
        if need.upper() == "Y":

            try:
                print("Period (zero-indexed):")
                selectedPeriod = input()
                selectedPeriod = int(selectedPeriod)

                if selectedPeriod >= 0 and selectedPeriod < period:
                    print("Letter being switched:")
                    oldLetter = input()
                    oldLetter = oldLetter.lower()

                    if oldLetter in letters:
                        print("Letter to switch in:")
                        newLetter = input()
                        newLetter = newLetter.lower()

                        # Find corresponding ciphertext character
                        # How to search by value in dict from: https://stackoverflow.com/a/8023337
                        ciphertextChar = ""
                        for c, p in alphabets[selectedPeriod].items() :
                            if p == oldLetter:
                                ciphertextChar = c
                                break

                        # Work out shift
                        shift = (letters.index(ciphertextChar) - letters.index(newLetter)) % len(letters)
                        print("Shift:", shift)

                        # Update map
                        alphabets[selectedPeriod] = dict(zip(letters[shift:] + letters[0:shift], letters)) #{cipher: plain}

                        # Show updated analysis
                        workingText = mapCipherToPlain(ciphertext, period, alphabets)
                        print(workingText)

            except ValueError:
                print("Value error!")

        elif need.upper() == "N":
            return workingText
        else:
            print("Acceptable answers are 'Y' or 'N'.")


def analyse(ciphertext, lowerBound, upperBound):

    # Find key length
    period = findPeriod(ciphertext, lowerBound, upperBound)

    # Do frequency analysis for each ciphertext subset
    strippedCiphertext = strip(ciphertext)
    alphabets = []
    maps = []
    for i in range(period):
        subset = strippedCiphertext[i: len(strippedCiphertext): period]
        maps.append(doLFA(subset))
    
    # Use maps to get plaintext
    mapCipherToPlain(ciphertext, period, maps)

    # Combine to get final plaintext
    finalPlaintext = "".join(mapCipherToPlain(ciphertext, period, maps))
    print(finalPlaintext)

    # Check if need corrections
    finalPlaintext = makeCorrections(ciphertext, finalPlaintext, period, maps)

    return finalPlaintext

def crackMsg(inputFileName, outputFileName):

    inputFile = open(inputFileName, "r")
    outputFile = open(outputFileName, "w")

    ciphertext = inputFile.read()
    print("Message:", ciphertext)

    print("Estimated lower bound for key length:")
    lower = input()

    print("Estimated upper bound for key length:")
    upper = input()

    try:
        lower = int(lower)
        upper = int(upper)
    except:
        print("Please input integers for the bounds.")
        return
    
    if (lower > upper):
        print("Please input proper bounds.")
        return
    
    
    plaintext = analyse(ciphertext, int(lower), int(upper))
    outputFile.write(plaintext)
    print("Final plaintext:", plaintext)



crackMsg("./encryptedLetter.txt", "./decryptedLetter.txt")