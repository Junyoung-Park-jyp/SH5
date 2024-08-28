import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shinhan_api.request import post
from shinhan_api.common import make_header
from pprint import pprint
import random


def create_demand_deposit(email, bankcode, bankname):
    """
    2.4.1 상품 등록
    """
    url = "edu/demandDeposit/createDemandDeposit"
    body = make_header(url.split('/')[-1], email)
    del body['Header']['userKey']
    body["bankCode"] = bankcode
    body["accountName"] = f"{bankname} 수시입출금 상품"
    body["accountDescription"] = "0"
    return post(url, body)


def inquire_demand_deposit_list(email):
    """
    2.4.2 상품 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositList"
    body = make_header(url.split('/')[-1], email)
    response = post(url, body)
    ret = []
    for i in response['REC']:
        if i['accountDescription'] == '1':
            ret.append(i)
    return ret[1:-1]


def create_demand_deposit_account(email):
    """
    2.4.3 계좌 생성
    """
    url = "edu/demandDeposit/createDemandDepositAccount"
    accountTypeUniqueNos = []
    for i in inquire_demand_deposit_list(email):
        accountTypeUniqueNos.append(i['accountTypeUniqueNo'])

    
    for accountTypeUniqueNo in ["088-1-8447fb08f3ea43", random.choice(accountTypeUniqueNos)]:
        body = make_header(url.split('/')[-1], email)
        body['accountTypeUniqueNo'] = accountTypeUniqueNo
        response = post(url, body)
        accountNo = response['REC']['accountNo']
        initial_deposit(email, accountNo)
    return


def inquire_demand_deposit_account_list(email):
    """
    2.4.4 계좌 목록 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositAccountList"
    body = make_header(url.split('/')[-1], email)
    response = post(url, body)
    return response


def inquire_demand_deposit_account(email, accountNo):
    """
    2.4.5 계좌 조회(단건)
    """
    url = "edu/demandDeposit/inquireDemandDepositAccount"
    body = make_header(url.split('/')[-1], email)
    body['accountNo'] = accountNo
    '''
    {'REC': [{'bankCode': '088', 'bankName': '신한은행', 'userName': 'oodeng98', 'accountNo': '0886248123734384', 'accountName': '정태완', 'accountTypeCode': '1', 'accountTypeName': '수시입출금', 'accountCreatedDate': '20240817', 'accountExpiryDate': '20290817', 'dailyTransferLimit': '500000000', 'oneTimeTransferLimit': '100000000', 'accountBalance': '0', 'lastTransactionDate': '', 'currency': 'KRW'}]}
    '''
    return post(url, body)


def inquire_demand_deposit_account_holder_name():
    """
    2.4.6 예금주 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositAccountHolderName"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
    '''
    'REC': {'bankCode': '088', 'bankName': '신한은행', 'accountNo': '0886248123734384', 'userName': 'oodeng98', 'currency': 'KRW'}
    '''
    return post(url, body)


def inquire_demand_deposit_account_balance(email, bank_account):
    """
    2.4.7 계좌 잔액 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositAccountBalance"
    body = make_header(url.split('/')[-1], email)
    body['accountNo'] = bank_account
    '''
    'REC': {'bankCode': '088', 'accountNo': '0886248123734384', 'accountBalance': '0', 'accountCreatedDate': '20240817', 'accountExpiryDate': '20290817', 'lastTransactionDate': '', 'currency': 'KRW'}
    '''
    return post(url, body)


def update_demand_deposit_account_withdrawal(bank_account, transactionBalance, email):
    """
    2.4.8 계좌 출금
    """
    url = "edu/demandDeposit/updateDemandDepositAccountWithdrawal"
    body = make_header(url.split('/')[-1], email)
    body['accountNo'] = bank_account
    body['transactionBalance'] = transactionBalance
    body['transactionSummary'] = ""
    '''
    '''
    return post(url, body)


def update_demand_deposit_account_deposit(email, accountNo, transactionBalance):
    """
    2.4.9 계좌 입금
    """
    url = "edu/demandDeposit/updateDemandDepositAccountDeposit"
    body = make_header(url.split('/')[-1], email)
    body['accountNo'] = accountNo
    body['transactionBalance'] = transactionBalance
    body['transactionSummary'] = ""
    '''
    '''
    return post(url, body)


def initial_deposit(email, accountNo):
    """
    초기 잔액 생성용
    """
    url = "edu/demandDeposit/updateDemandDepositAccountDeposit"
    body = make_header(url.split('/')[-1], email)
    body['accountNo'] = accountNo
    body['transactionBalance'] = random.randrange(300000, 10000000)
    body['transactionSummary'] = "초기 잔액 입금"
    '''
    '''
    return post(url, body)


def update_demand_deposit_account_Transfer(email, deposit_bank_account, withdrawal_bank_account, transaction_balance):
    """
    2.4.10 계좌 이체
    """
    url = "edu/demandDeposit/updateDemandDepositAccountTransfer"
    body = make_header(url.split('/')[-1], email)
    body['depositAccountNo'] = deposit_bank_account
    body['transactionBalance'] = transaction_balance
    body['withdrawalAccountNo'] = withdrawal_bank_account
    
    body['depositTransactionSummary'] = "1억 받음"
    body['withdrawalTransactionSummary'] = "1억 줌"
    '''
    '''
    return post(url, body)


def inquire_transaction_history_list(bank_account, start_date, end_date):
    """
    2.4.12 계좌 거래 내역 조회
    """
    url = "edu/demandDeposit/inquireTransactionHistoryList"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = bank_account
    body['startDate'] = start_date
    body['endDate'] = end_date
    body['transactionType'] = "A"
    body['orderByType'] = "DESC"
    '''
    'REC': {'totalCount': '8', 'list': [{'transactionUniqueNo': '118', 'transactionDate': '20240817', 'transactionTime': '183432', 'transactionType': '2', 'transactionTypeName': '출금(이체)', 'transactionAccountNo': '0885900744426778', 'transactionBalance': '100000000', 'transactionAfterBalance': '4799900000', 'transactionSummary': '1억 줌', 'transactionMemo': ''}
    '''
    return post(url, body)


def inquire_transaction_history(bank_account, transaction_unique_number, email):
    """
    2.4.13 계좌 거래 내역 조회 (단건)
    """
    url = "edu/demandDeposit/inquireTransactionHistory"
    body = make_header(url.split('/')[-1], email)
    body['accountNo'] = bank_account
    body['transactionUniqueNo'] = transaction_unique_number
    '''
    'REC': {'transactionUniqueNo': '116', 'transactionDate': '20240817', 'transactionTime': '182749', 'transactionType': '2', 'transactionTypeName': '출금(이체)', 'transactionAccountNo': '0885900744426778', 'transactionBalance': '100000000', 'transactionAfterBalance': '4899900000', 'transactionSummary': '1억 줌', 'transactionMemo': ''}
    '''
    return post(url, body)


def create_demand_deposit_for_each_bank():
    rec =  [{'bankCode': '001', 'bankName': '한국은행'},
        {'bankCode': '002', 'bankName': '산업은행'},
        {'bankCode': '003', 'bankName': '기업은행'},
        {'bankCode': '004', 'bankName': '국민은행'},
        {'bankCode': '011', 'bankName': '농협은행'},
        {'bankCode': '020', 'bankName': '우리은행'},
        {'bankCode': '023', 'bankName': 'SC제일은행'},
        {'bankCode': '027', 'bankName': '시티은행'},
        {'bankCode': '032', 'bankName': '대구은행'},
        {'bankCode': '034', 'bankName': '광주은행'},
        {'bankCode': '035', 'bankName': '제주은행'},
        {'bankCode': '037', 'bankName': '전북은행'},
        {'bankCode': '039', 'bankName': '경남은행'},
        {'bankCode': '045', 'bankName': '새마을금고'},
        {'bankCode': '081', 'bankName': 'KEB하나은행'},
        {'bankCode': '088', 'bankName': '신한은행'},
        {'bankCode': '090', 'bankName': '카카오뱅크'},
        {'bankCode': '999', 'bankName': '싸피은행'}]
    for i in rec:
        create_demand_deposit("oodeng98@naver.com", i['bankCode'], i['bankName'])
    


if __name__ == "__main__":
    # create_demand_deposit_for_each_bank()
    # create_demand_deposit("oodeng98@naver.com")
    # inquire_demand_deposit_list("oodeng98@naver.com")
    # create_demand_deposit_account("oodeng98@naver.com")
    pprint(inquire_demand_deposit_account_list("email9629@naver.com")['REC'])
    pprint(inquire_demand_deposit_account("email9629@naver.com", "0882943094128264")['REC'])
    # inquire_demand_deposit_account_holder_name()
    # pprint(inquire_demand_deposit_account_balance("email9629@naver.com", "0372462077415412"))
    # pprint(update_demand_deposit_account_withdrawal("0817158183605808", 10000))
    # update_demand_deposit_account_deposit()
    # pprint(update_demand_deposit_account_Transfer("email1@naver.com", "0817158183605808", "0880493544778029", 3000))
    # pprint(inquire_transaction_history_list("0817158183605808"))
    # inquire_transaction_history()
