from request import post
from common import make_header


def create_demand_deposit():
    """
    2.4.1 상품 등록
    """
    url = "edu/demandDeposit/createDemandDeposit"
    body = make_header(url.split('/')[-1])
    del body['Header']['userKey']
    body["bankCode"] = "088"
    body["accountName"] = "정태완"
    body["accountDescription"] = "정태완이임의로만든상품"
    '''
    {'REC': {'accountTypeUniqueNo': '088-1-8bcd47cd8f5143', 'bankCode': '088', 'bankName': '신한은행', 'accountTypeCode': '1', 'accountTypeName': '수시입출금', 'accountName': '정태완', 'accountDescription': '정태완이임의로만든상품', 'accountType': 'DOMESTIC'}}
    '''
    return post(url, body)


def inquire_demand_deposit_list():
    """
    2.4.2 상품 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositList"
    body = make_header(url.split('/')[-1])
    del body['Header']['userKey']
    '''
    {'REC': [{'accountTypeUniqueNo': '001-1-38626eb91f9843', 'bankCode': '001', 'bankName': '한국은행', 'accountTypeCode': '1', 'accountTypeName': '수시입출금', 'accountName': '한국은행 수시입출금 상품', 'accountDescription': '자유로운 수시입출금', 'accountType': 'DOMESTIC'}, {'accountTypeUniqueNo': '088-1-8bcd47cd8f5143', 'bankCode': '088', 'bankName': '신한은행', 'accountTypeCode': '1', 'accountTypeName': '수시입출금', 'accountName': '정태완', 'accountDescription': '정태완이임의로만든상품', 'accountType': 'DOMESTIC'}]}
    '''
    return post(url, body)


def create_demand_deposit_account():
    """
    2.4.3 계좌 생성
    """
    url = "edu/demandDeposit/createDemandDepositAccount"
    body = make_header(url.split('/')[-1])
    body['accountTypeUniqueNo'] = "088-1-8bcd47cd8f5143"
    '''
    {'REC': {'bankCode': '088', 'accountNo': '0886248123734384', 'currency': {'currency': 'KRW', 'currencyName': '원화'}}}
    '''
    return post(url, body)


def inquire_demand_deposit_account_list():
    """
    2.4.4 계좌 목록 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositAccountList"
    body = make_header(url.split('/')[-1])    
    '''
    {'REC': [{'bankCode': '088', 'bankName': '신한은행', 'userName': 'oodeng98', 'accountNo': '0886248123734384', 'accountName': '정태완', 'accountTypeCode': '1', 'accountTypeName': '수시입출금', 'accountCreatedDate': '20240817', 'accountExpiryDate': '20290817', 'dailyTransferLimit': '500000000', 'oneTimeTransferLimit': '100000000', 'accountBalance': '0', 'lastTransactionDate': '', 'currency': 'KRW'}]}
    '''
    return post(url, body)


def inquire_demand_deposit_account():
    """
    2.4.5 계좌 조회(단건)
    """
    url = "edu/demandDeposit/inquireDemandDepositAccountList"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
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


def inquire_demand_deposit_account_balance():
    """
    2.4.7 계좌 잔액 조회
    """
    url = "edu/demandDeposit/inquireDemandDepositAccountBalance"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
    '''
    'REC': {'bankCode': '088', 'accountNo': '0886248123734384', 'accountBalance': '0', 'accountCreatedDate': '20240817', 'accountExpiryDate': '20290817', 'lastTransactionDate': '', 'currency': 'KRW'}
    '''
    return post(url, body)


def update_demand_deposit_account_withdrawal():
    """
    2.4.8 계좌 출금
    """
    url = "edu/demandDeposit/updateDemandDepositAccountWithdrawal"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
    body['transactionBalance'] = "100000"
    body['transactionSummary'] = "메모"
    '''
    '''
    return post(url, body)


def update_demand_deposit_account_deposit():
    """
    2.4.9 계좌 입금
    """
    url = "edu/demandDeposit/updateDemandDepositAccountDeposit"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
    body['transactionBalance'] = "1000000000"
    body['transactionSummary'] = "나 10억 자산가야"
    '''
    '''
    return post(url, body)


def update_demand_deposit_account_Transfer():
    """
    2.4.10 계좌 이체
    """
    url = "edu/demandDeposit/updateDemandDepositAccountTransfer"
    body = make_header(url.split('/')[-1])
    body['depositAccountNo'] = "0885900744426778"
    body['transactionBalance'] = "100000000"
    body['withdrawalAccountNo'] = "0886248123734384"
    
    body['depositTransactionSummary'] = "1억 받음"
    body['withdrawalTransactionSummary'] = "1억 줌"
    '''
    '''
    return post(url, body)


def inquire_transaction_history_list():
    """
    2.4.12 계좌 거래 내역 조회
    """
    url = "edu/demandDeposit/inquireTransactionHistoryList"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
    body['startDate'] = "20240815"
    body['endDate'] = "20240817"
    body['transactionType'] = "A"
    body['orderByType'] = "DESC"
    '''
    'REC': {'totalCount': '8', 'list': [{'transactionUniqueNo': '118', 'transactionDate': '20240817', 'transactionTime': '183432', 'transactionType': '2', 'transactionTypeName': '출금(이체)', 'transactionAccountNo': '0885900744426778', 'transactionBalance': '100000000', 'transactionAfterBalance': '4799900000', 'transactionSummary': '1억 줌', 'transactionMemo': ''}
    '''
    return post(url, body)


def inquire_transaction_history():
    """
    2.4.13 계좌 거래 내역 조회 (단건)
    """
    url = "edu/demandDeposit/inquireTransactionHistory"
    body = make_header(url.split('/')[-1])
    body['accountNo'] = "0886248123734384"
    body['transactionUniqueNo'] = '120'
    '''
    'REC': {'transactionUniqueNo': '116', 'transactionDate': '20240817', 'transactionTime': '182749', 'transactionType': '2', 'transactionTypeName': '출금(이체)', 'transactionAccountNo': '0885900744426778', 'transactionBalance': '100000000', 'transactionAfterBalance': '4899900000', 'transactionSummary': '1억 줌', 'transactionMemo': ''}
    '''
    return post(url, body)


if __name__ == "__main__":
    # create_demand_deposit()
    # inquire_demand_deposit_list()
    # create_demand_deposit_account()
    # inquire_demand_deposit_account_list()
    # inquire_demand_deposit_account()
    # inquire_demand_deposit_account_holder_name()
    # inquire_demand_deposit_account_balance()
    # update_demand_deposit_account_withdrawal()
    # update_demand_deposit_account_deposit()
    # update_demand_deposit_account_Transfer()
    # inquire_transaction_history_list()
    inquire_transaction_history()