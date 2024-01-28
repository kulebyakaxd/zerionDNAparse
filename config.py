with open("adresses.txt", 'r') as f:
    adresses = [r.strip() for r in f.readlines()]
    
zeriondna_contract = '0x932261f9fc8da46c4a22e31b45c4de60623848bf'
Moralis_api_key = ""  # нужно получить web3 api key тут https://admin.moralis.io/settings#api_keys
