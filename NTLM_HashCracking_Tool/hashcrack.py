import hashlib
from rawdataextraction import NTLMHashes

def create_ntlm_hash(input_string):
    return hashlib.new('md4', input_string.encode('utf-16le')).hexdigest()

def crack(hashValue,testValue):
    if(hashValue==testValue):
        return True

passwordFile = "passwords.txt"
with open(passwordFile,"r") as file:
    passwords = file.readlines()
    passwords = [value.replace("\n","") for value in passwords]

if(len(passwords) == 0):
    print("--[ ERROR ]--[ Passwords.txt is empty ]")

print("--[ INFO ]--[ EXTRACTED DATA ]")
for value in NTLMHashes:
    print(f"{value}")

print("\n--[ INFO ]--[ CRACKING PASSWORDS ]",end="")

crackedPassword = []
count = 0
for hash in NTLMHashes:
    for index,value in enumerate(passwords):
        testvalue = create_ntlm_hash(value)
        # print(testvalue)
        if crack(hash["NTLMhash"],testvalue):
            hash["Password"] = value
            crackedPassword.append(hash)
            count += 1
            break
    
if(crackedPassword == ""):
    print("\n--[ RESULT ]--[ No Hashes Matched ]")
else:
    print(f"\n--[ RESULT ]--[ {count} Passwords Cracked Successfully ]")
    # print(f"--PASSWORD--[ {crackedPassword} ]")
    for value in crackedPassword:
        del value["NTLMhash"]
        print(f"{value}")