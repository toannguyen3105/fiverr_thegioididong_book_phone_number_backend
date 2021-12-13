#!/usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import time
from datetime import datetime
from utils.telegram.send_message import send_message_telegram, text_success_output

users = [
    {
        "name": "Anh Cuong",
        "phone": "0983262262",
        "identification_card": "024094006582",
        "phones_number_to_buy": ["0988598696", "0983136189"]
    },
    {
        "name": "Anh Phong",
        "phone": "0981778111",
        "identification_card": "024303013697",
        "phones_number_to_buy": ["0982383558", "0363386638"]
    },
    {
        "name": "Anh Hai",
        "phone": "0965753898",
        "identification_card": "121914018",
        "phones_number_to_buy": ["0345678382", "0336789589"]
    },
    {
        "name": "Anh Chuong",
        "phone": "0983944999",
        "identification_card": "122168763",
        "phones_number_to_buy": ["0346078178", "0965558229"]
    },
    {
        "name": "Anh TOAN",
        "phone": "0983944321",
        "identification_card": "122168233",
        "phones_number_to_buy": ["0869610574"]
    }
]

usersTest = [
    {
        "name": "Anh Toan",
        "phone": "0923242232",
        "identification_card": "024094006585",
        "phones_number_to_buy": ["0869489304", "0983136188"]
    },
]


def buy_phone_number(name, phone, identification_card, phone_number_to_buy):
    import requests

    url = "https://www.thegioididong.com/sim-so-dep/aj/Homev4/SubmitOrder/"

    payload = f"__RequestVerificationToken=EnzvsUigwM13sxXEZi9xJTZVQpZC8nFUIKLkhc-1hT52tFruu0Q3Q6Wlk10jfnNKA2xMANNT_tI_5_POJeImhPfdwKY1&hdprice=270000&hdproductno=5500122000600&hdnetworkid=8&hdoption=store&hdstoreid=1771&hdstoreaddress=QL+31%2C+Khu+Tr%C6%B0%E1%BB%9Dng+Chinh%2C+TT.+Ch%C5%A9%2C+H.+L%E1%BB%A5c+Ng%E1%BA%A1n%2C+T.+B%E1%BA%AFc+Giang++-+C%C3%A1ch+Ng%C3%A3+T%C6%B0+C%C6%A1+Kh%C3%AD+500m+h%C6%B0%E1%BB%9Bng+%C4%91i+B%E1%BA%AFc+Giang&hdsimno={phone_number_to_buy}&hdsimnodisplay=0869.427.121&hdgender=1&hdpackageid=101&hdpackagename=Viettel+V120N&hdgroupname=B%C3%ACnh+d%C3%A2n&PhoneIncluded=0&PartnerPackageTypeId=MYKID50&BrandId=126&CMSPackageId=47&hdTotalpay=270000&txtname={name}&txtphone={phone}&txtcmnd={identification_card}&undefined=ok&txtSearch=&hdCRMFeeResultBO=%7B%22BaseFeeID%22%3A0%2C%22BaseFeeMoney%22%3A0.0%2C%22BaseFeeMoneyAmount%22%3A0.0%2C%22IsHasCheckApplyProduct%22%3Afalse%2C%22IsRightSetupProduct%22%3Afalse%2C%22IsRightDistance%22%3Afalse%2C%22IsRightAmount%22%3Afalse%2C%22ShippingCost%22%3A0.0%2C%22TotalAdvance%22%3A0.0%2C%22cus_FeeBOList%22%3A%5B%5D%2C%22OutGroupID%22%3A1%7D&ShipDay=1&Deposit=0&ShippingCode=0.0&ShippingCost=0.0&DeliveryTypeID=1&SaleOrderDetailOnlineId=8097d71b-9b7e-4ecd-909f-3fecb70c90f8&DeliveryShippingCost=0&TransferShippingCost=0&OpportunityFee=0&TextPayment=&isInvoice=false&CompanyInfo.CompanyName=&CompanyInfo.CompanyAddress=&CompanyInfo.CompanyTaxno=&hdprovinceid=103&hddistrictid=897&hdwardid=0&hdprovincename=B%E1%BA%AFc+Giang&hddistrictname=Huy%E1%BB%87n+L%E1%BB%A5c+Ng%E1%BA%A1n&hdwardname=&hdaddress="
    headers = {
        'authority': 'www.thegioididong.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.thegioididong.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.thegioididong.com/sim-so-dep/dat-mua/101/0869489153',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'cookie': 'ShowLocationSuggest=hide; chat.info=; chat.username=20210701ky_kzNgvYMyBb9svACY9; chat.notifychatmsg=; lhc_per=vid|50aa1b811e651c1fb77c; __RequestVerificationToken_L3NpbS1zby1kZXA1=AE68xztk1r6jcVqYwfeXOsyUTgLayrWhCQHVTRcVOuQHTJgyU97CkTQH51JJoaxOuDpajyMz13rG0DNJjwdJU_YW7JU1; ASP.NET_SessionId=f2mi2en40sxjjzfrluy1bfix; _gid=GA1.2.915844042.1639063754; .AspNetCore.Antiforgery.Z2GafvQY0KE=CfDJ8Nm2VFJYRBBKp48Zlw4KkRccAq9uuiNXR62sRW2cv2-K5UnJi3KYC4X5FnLcrtJDJwnIOrwOj1YnZybLiOkOfhSlN9gvgk79g0Bbn3nT4TxNAbWekUlFVFdQKDr1a-Mp_BT5ufcU3xKn0LvZ3r2kkww; DMX_Personal=%7b%22UID%22%3a%22DMX%22%2c%22ProvinceId%22%3a5%2c%22Culture%22%3a%22vi-3%22%2c%22Lat%22%3a0.0%2c%22Lng%22%3a0.0%2c%22DistrictId%22%3a0%2c%22WardId%22%3a0%2c%22CRMCustomerId%22%3anull%2c%22CustomerSex%22%3a1%2c%22CustomerName%22%3a%22NGUYEN+HUY+TOAN%22%2c%22CustomerPhone%22%3a%220363629811%22%2c%22CustomerEmail%22%3anull%2c%22CustomerIdentity%22%3a%22011123123%22%2c%22CustomerBirthday%22%3anull%2c%22CustomerAddress%22%3a%5b%7b%22Id%22%3a0%2c%22Address%22%3a%22%2c+H%c3%a0+N%e1%bb%99i%22%2c%22ProvinceId%22%3a5%2c%22ProvinceName%22%3a%22H%c3%a0+N%e1%bb%99i%22%2c%22DistrictId%22%3a0%2c%22DistrictName%22%3a%22%22%2c%22WardId%22%3a0%2c%22WardName%22%3a%22%22%7d%5d%2c%22IsDefault%22%3afalse%2c%22IsFirst%22%3afalse%7d; _gcl_au=1.1.1503582967.1639063800; _ga_TLRZMSX5ME=GS1.1.1639063753.16.1.1639064054.31; _ga=GA1.2.447763645.1624776545; SvID=line8084|YbIo7|YbIgy; DMX_Personal=%7b%22UID%22%3a%22DMX%22%2c%22ProvinceId%22%3a103%2c%22Culture%22%3a%22vi-3%22%2c%22Lat%22%3a0.0%2c%22Lng%22%3a0.0%2c%22DistrictId%22%3a0%2c%22WardId%22%3a0%2c%22CRMCustomerId%22%3anull%2c%22CustomerSex%22%3a1%2c%22CustomerName%22%3a%22Anh+Cuong%22%2c%22CustomerPhone%22%3a%220983262261%22%2c%22CustomerEmail%22%3anull%2c%22CustomerIdentity%22%3a%22024094006582%22%2c%22CustomerBirthday%22%3anull%2c%22CustomerAddress%22%3a%5b%7b%22Id%22%3a0%2c%22Address%22%3a%22%2c+B%e1%ba%afc+Giang%22%2c%22ProvinceId%22%3a103%2c%22ProvinceName%22%3a%22B%e1%ba%afc+Giang%22%2c%22DistrictId%22%3a0%2c%22DistrictName%22%3a%22%22%2c%22WardId%22%3a0%2c%22WardName%22%3a%22%22%7d%5d%2c%22IsDefault%22%3afalse%2c%22IsFirst%22%3afalse%7d; SvID=liol8085|YbIv+|YbIgy'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print("phone_number_to_buy! " + phone_number_to_buy)
    if 'Đặt hàng thành công' in response.text:
        send_message_telegram(text_success_output(name, phone_number_to_buy))


def job():
    print("Start job: " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    for user in users:
        name = user["name"]
        phone = user["phone"]
        identification_card = user["identification_card"]
        phones_number_to_buy = user["phones_number_to_buy"]

        for phone_number_to_buy in phones_number_to_buy:
            buy_phone_number(name, phone, identification_card, phone_number_to_buy)


schedule.every(3).seconds.do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
