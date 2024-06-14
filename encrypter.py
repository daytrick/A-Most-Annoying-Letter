from sympy import false


letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def encryptLetter(letter, shift):
    """Encrypt a single letter using a shift cipher."""
    return letters[(letters.index(letter) + shift) % len(letters)]

def encrypt(plaintext, key):
    """Encrypt a message using the Vigenere cipher."""

    # Ignore cases
    plaintext = plaintext.lower()
    key = key.lower()

    # Calculate shift of the keys
    keyShifts = [letters.index(letter) + 1 for letter in key]

    # Actually encrypt
    working = []
    ciphertext = []
    i = 0
    for char in plaintext:
        keyPlace = i % len(key)

        if char in letters:
            working.append(key[i % len(key)])
            ciphertext.append(encryptLetter(char, keyShifts[keyPlace]))
            i += 1
        else:
            working.append(char)
            ciphertext.append(char)

    return ("".join(working), "".join(ciphertext))

def bundle(text, size):
    """Remove punctuation from ciphertext and break it into groups."""
    bundledText = []

    text = text.lower()

    i = 0
    for char in text:
        
        if char in letters:

            if (i > 0) and (i % size) == 0:
                bundledText.append(" ")

            bundledText.append(char)
            i += 1
        

    return "".join(bundledText)

def encryptMsg(inputFileName, outputFileName):
    """Do all the user input stuff to get the message, key, and bundle size for encryption."""

    inputFile = open(inputFileName, "r")
    outputFile = open(outputFileName, "w")
    message = inputFile.read()
    print("Message:", message)

    allAlpha = False
    while not allAlpha:
        print("Key:")
        key = input()
        key = key.lower()

        allAlpha = True
        for char in key:
            if char not in letters:
                allAlpha = False
        
        if not allAlpha:
            print("Key can only contain alphabetic characters.")

    while True:
        print("Bundle size (0 for no bundling):")
        bundleSize = input()

        try:
            bundleSize = int(bundleSize)
            if bundleSize < 0:
                print("Bundle size must be a positive integer.")
                continue
        except ValueError:
            print("Bundle size must be a positive integer.")
            continue
        
        break

    if bundleSize != 0:
        message = bundle(message, bundleSize)
    
    outputFile.write(encrypt(message, key)[1])

    inputFile.close()
    outputFile.close()


encryptMsg("./letter.txt", "./encryptedLetter.txt")