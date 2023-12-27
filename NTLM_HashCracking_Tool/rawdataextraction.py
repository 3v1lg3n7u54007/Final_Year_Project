import re

# Regex Pattern to Extract NTLM Hashes...
pattern = r"^([^:]+):(\d+):([a-fA-F0-9]{32}):([a-fA-F0-9]{32}):::$"

try:
    with open("rawdump.txt",'r',encoding="utf-8") as file:
        rawdata = file.readlines()
        rawdata = [value.replace("\n","").strip() for value in rawdata]

    NTLMHashes = []

    for hash in rawdata:
        match = re.match(pattern, hash)
        if match:
            username = match.group(1)
            RID = match.group(2)
            # LMhash = match.group(3)
            NTLMhash = match.group(4)

            NTLMHashes.append({"username":username,"RID":RID,"NTLMhash":NTLMhash,"Password":""})
except Exception as error:
    print(f"--[ ERROR ]--[ RAW DATA EXTRACTION ERROR ]--[ {error} ]")