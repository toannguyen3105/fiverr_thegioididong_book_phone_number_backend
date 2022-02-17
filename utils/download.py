import csv
from datetime import datetime

from utils.telegram.send_message import send_message_telegram, text_success_output
from utils.find_text import getPrice
from constants.headers import HEADERS


def buy_phone_number(name, phone, identification_card, phone_number_to_buy, start_time):
    import requests

    url = "https://www.thegioididong.com/sim-so-dep/aj/Homev4/SubmitOrder/"

    payload = f"__RequestVerificationToken=EnzvsUigwM13sxXEZi9xJTZVQpZC8nFUIKLkhc-1hT52tFruu0Q3Q6Wlk10jfnNKA2xMANNT_tI_5_POJeImhPfdwKY1&hdprice=270000&hdproductno=5500122000600&hdnetworkid=8&hdoption=store&hdstoreid=1771&hdstoreaddress=QL+31%2C+Khu+Tr%C6%B0%E1%BB%9Dng+Chinh%2C+TT.+Ch%C5%A9%2C+H.+L%E1%BB%A5c+Ng%E1%BA%A1n%2C+T.+B%E1%BA%AFc+Giang++-+C%C3%A1ch+Ng%C3%A3+T%C6%B0+C%C6%A1+Kh%C3%AD+500m+h%C6%B0%E1%BB%9Bng+%C4%91i+B%E1%BA%AFc+Giang&hdsimno={phone_number_to_buy}&hdsimnodisplay=0869.427.121&hdgender=1&hdpackageid=101&hdpackagename=Viettel+V120N&hdgroupname=B%C3%ACnh+d%C3%A2n&PhoneIncluded=0&PartnerPackageTypeId=MYKID50&BrandId=126&CMSPackageId=47&hdTotalpay=270000&txtname={name}&txtphone={phone}&txtcmnd={identification_card}&undefined=ok&txtSearch=&hdCRMFeeResultBO=%7B%22BaseFeeID%22%3A0%2C%22BaseFeeMoney%22%3A0.0%2C%22BaseFeeMoneyAmount%22%3A0.0%2C%22IsHasCheckApplyProduct%22%3Afalse%2C%22IsRightSetupProduct%22%3Afalse%2C%22IsRightDistance%22%3Afalse%2C%22IsRightAmount%22%3Afalse%2C%22ShippingCost%22%3A0.0%2C%22TotalAdvance%22%3A0.0%2C%22cus_FeeBOList%22%3A%5B%5D%2C%22OutGroupID%22%3A1%7D&ShipDay=1&Deposit=0&ShippingCode=0.0&ShippingCost=0.0&DeliveryTypeID=1&SaleOrderDetailOnlineId=8097d71b-9b7e-4ecd-909f-3fecb70c90f8&DeliveryShippingCost=0&TransferShippingCost=0&OpportunityFee=0&TextPayment=&isInvoice=false&CompanyInfo.CompanyName=&CompanyInfo.CompanyAddress=&CompanyInfo.CompanyTaxno=&hdprovinceid=103&hddistrictid=897&hdwardid=0&hdprovincename=B%E1%BA%AFc+Giang&hddistrictname=Huy%E1%BB%87n+L%E1%BB%A5c+Ng%E1%BA%A1n&hdwardname=&hdaddress="
    headers = HEADERS

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    if 'Đặt hàng thành công' in response.text:
        send_message_telegram(text_success_output(name, phone_number_to_buy))
        end_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print("End job: " + end_time)

        # Write name, phone, identification_card, phone_number_to_buy, price to csv file
        data = [name, phone, identification_card, phone_number_to_buy, getPrice(response.text), start_time, end_time]
        # open the file in the write mode
        with open('./exports/accounts.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
