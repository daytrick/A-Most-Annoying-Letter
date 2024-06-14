# DECRYPTION TOOLS

All files assumed to be in the same directory as the Python files.

1. Decompress the letter, which should be named `finalLetter.txt`: `python ./DictDecompression.py`. This will output a file holding the decompressed letter, called `encryptedLetter.py`.
2. Decrypt the decompressed letter: `python ./analyser.py`. You will be asked for an estimate on the bounds of a key word length, so that the analyser can use the key word length with the best index of coincidence.
3. The analyser will then try to decrypt the letter based on letter frequency analysis on the text, where letters are grouped by which key word letter they were encrypted with. You may have to make some corrections. There is an interface for doing so.

<details>
  <summary>PLEASE JUST TELL ME HOW TO READ IT!</summary>
  
  The letter is encrypted using the Vigenere cipher, with the code word "suffer" (but treated as "sufer", to avoid repetition). 

  As mentioned in the main README, the compression is erroneous, so please don't think about it.
  
</details>
