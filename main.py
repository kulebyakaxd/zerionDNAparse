from moralis import evm_api
import time
from config import *
import pandas as pd

def get_tokenid(address):
    tokenid = -100

    params = {
    "chain": "eth",
    "format": "decimal",
    "media_items": False,
    "address": address
    }

    result = evm_api.nft.get_wallet_nfts(
    api_key=Moralis_api_key,
    params=params,
    )


    wall_data = result['result']
    for x in wall_data:
        if x['token_address'] == zeriondna_contract:
            tokenid = x['token_id'] 
    return tokenid

def resync_metadata(token_id_input):
    params = {
    "chain": "eth",
    "flag": "uri",
    "mode": "async",
    "token_id": token_id_input,
    "address": zeriondna_contract
    }

    result = evm_api.nft.re_sync_metadata(
    api_key=Moralis_api_key,
    params=params,
    )

def get_metadata(wallets,token_id_input,address):
    params = {
    "chain": "eth",
    "format": "decimal",
    "media_items": False,
    "normalize_metadata": True,
    "address": zeriondna_contract,
    "token_id": token_id_input
    }

    result = evm_api.nft.get_nft_metadata(
    api_key=Moralis_api_key,
    params=params,
    )

    lastsync  = result['last_metadata_sync']
    result = result['metadata']

    data = eval(result)
    image = data['image']
    attributes = data['attributes']
    if attributes[7]['value'] == "Yes":
        r1 = {'адресс':address,
              'последее обновление метадаты':lastsync,
              'image': image}
        r2 = {attributes[i]['trait_type']: attributes[i]['value'] for i in range(0,10)}
        row = {**r1,**r2}

        wallets.append(row)

def main():
    print("Скрипт запущен!")
    wallets = []
    adresses_with_nft = []
    for adr_to_check in adresses:
        id = get_tokenid(adr_to_check)
        if id != -100:  # проверка что на кошельке есть нфт
            resync_metadata(id)
            adresses_with_nft.append({
                'adress': adr_to_check,
                'id':id
            })
        
    print("ждем обновления метаданных")
    time.sleep(10)
    for adr in adresses_with_nft:
        id = adr['id']
        addr = adr['adress']
        get_metadata(wallets,id,addr)

    metadata_df =pd.DataFrame(wallets)
    metadata_df.to_csv('data.csv', index=False)
    print('Данные записаны в csv!')



main()