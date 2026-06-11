from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator


app = FastAPI(title="KBank BillPayment API", version="1.0.0")


# Mock data for inquiry/lookup. Replace this with real database queries in production.
LOOKUP_DATA = {
    ("300000025751", "1733084"): {
        "tranAmount": "120.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
        "isPromptpay": False,
        "merchantError": False,
    },
    ("300000025752", "1733085"): {
        "tranAmount": "250.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
        "isPromptpay": False,
        "merchantError": False,
    },
    # Inquiry Already Paid case
    ("300000025753", "1733086"): {
        "tranAmount": "120.00",
        "isPaid": True,
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
        "isPromptpay": False,
        "merchantError": False,
    },
    # Inquiry Other Merchant Error
    ("300000025754", "1733087"): {
        "tranAmount": "180.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
        "isPromptpay": False,
        "merchantError": True,
    },
    # Inquiry Info EN
    ("300000025755", "1733088"): {
        "tranAmount": "120.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "Electricity Bill",
        "info2": "Bangkok",
        "info3": "Customer: EN",
        "duedate": "",
        "rtpReference": "",
        "isPromptpay": False,
        "merchantError": False,
    },
    # Inquiry Info TH
    ("300000025756", "1733089"): {
        "tranAmount": "120.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "ค่าไฟฟ้า",
        "info2": "กรุงเทพ",
        "info3": "ลูกค้า: TH",
        "duedate": "",
        "rtpReference": "",
        "isPromptpay": False,
        "merchantError": False,
    },
    # Inquiry Success Promptpay
    ("PP3000001", "PP1733081"): {
        "tranAmount": "120.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "PROMPTPAY",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "RTP-0001",
        "isPromptpay": True,
        "merchantError": False,
    },
    # Inquiry Already Paid Promptpay
    ("PP3000002", "PP1733082"): {
        "tranAmount": "120.00",
        "isPaid": True,
        "terminalNo": "xxxxxxx8888",
        "billerType": "PROMPTPAY",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "RTP-0002",
        "isPromptpay": True,
        "merchantError": False,
    },
    # Inquiry Other Merchant Error Promptpay
    ("PP3000003", "PP1733083"): {
        "tranAmount": "120.00",
        "isPaid": False,
        "terminalNo": "xxxxxxx8888",
        "billerType": "PROMPTPAY",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "RTP-0003",
        "isPromptpay": True,
        "merchantError": True,
    },
}


# Inquiry/Payment case: "Reference 1 for return Reference 2 and amount Success"
REFERENCE1_ONLY_DATA = {
    "REF1ONLY300001": {
        "reference2": "RET1733001",
        "tranAmount": "320.00",
        "terminalNo": "xxxxxxx8888",
        "billerType": "",
        "info1": "",
        "info2": "",
        "info3": "",
        "duedate": "",
        "rtpReference": "",
    }
}


class BillPaymentRequest(BaseModel):
    functionName: str
    transactionId: str
    transactionDateTime: datetime
    billerType: str = ""
    billerId: str
    terminalNo: str
    channelCode: str
    tranAmount: str
    senderBankCode: str
    isRetry: str
    reference1: str
    reference2: str
    language: Optional[str] = "EN"
    apiKey: str
    dueDate: Optional[str] = ""
    rtpReference: Optional[str] = ""
    rqAppId: Optional[str] = ""

    @field_validator("functionName")
    @classmethod
    def validate_function_name(cls, value: str) -> str:
        if value != "BillPayment":
            raise ValueError('functionName must be "BillPayment"')
        return value

    @field_validator("billerId")
    @classmethod
    def validate_biller_id(cls, value: str) -> str:
        if value != "98499":
            raise ValueError('billerId must be "98499"')
        return value

    @field_validator("senderBankCode")
    @classmethod
    def validate_sender_bank_code(cls, value: str) -> str:
        if value != "Kbank":
            raise ValueError('senderBankCode must be "Kbank"')
        return value

    @field_validator("isRetry")
    @classmethod
    def validate_is_retry(cls, value: str) -> str:
        if value != "0":
            raise ValueError('isRetry must be "0" for this exercise')
        return value

    @field_validator("apiKey")
    @classmethod
    def validate_api_key(cls, value: str) -> str:
        # Exercise docs sometimes show "SequreKey123" and sometimes "SecureKey123".
        # Accept both values to keep compatibility.
        if value not in {"SequreKey123", "SecureKey123"}:
            raise ValueError('apiKey must be "SequreKey123" or "SecureKey123"')
        return value

    @field_validator("transactionDateTime")
    @classmethod
    def validate_transaction_datetime_today(cls, value: datetime) -> datetime:
        current_date = datetime.now(value.tzinfo).date() if value.tzinfo else datetime.now().date()
        if value.date() != current_date:
            raise ValueError("transactionDateTime must be today")
        return value


class BillPaymentResponse(BaseModel):
    functionName: str = "BillPaymentResponse"
    transactionId: str
    responseDateTime: str
    billerTransactionId: str
    responseCode: str = "0000"
    responseDescription: str = "Success"
    terminalNo: str
    settlementDate: str = ""
    rsAppId: str = ""


class BillLookupRequest(BaseModel):
    functionName: str
    transactionId: str
    transactionDateTime: datetime
    billerType: str = ""
    billerId: str
    terminalNo: str
    channelCode: str = ""
    tranAmount: str = ""
    senderBankCode: str
    reference1: str = ""
    reference2: str = ""
    language: Optional[str] = "EN"
    apiKey: str

    @field_validator("functionName")
    @classmethod
    def validate_function_name(cls, value: str) -> str:
        if value != "BillLookup":
            raise ValueError('functionName must be "BillLookup"')
        return value

    @field_validator("billerId")
    @classmethod
    def validate_biller_id(cls, value: str) -> str:
        if value != "98499":
            raise ValueError('billerId must be "98499"')
        return value

    @field_validator("senderBankCode")
    @classmethod
    def validate_sender_bank_code(cls, value: str) -> str:
        if value != "Kbank":
            raise ValueError('senderBankCode must be "Kbank"')
        return value

    @field_validator("terminalNo")
    @classmethod
    def validate_terminal_no(cls, value: str) -> str:
        if value != "xxxxxxx8888":
            raise ValueError('terminalNo must be "xxxxxxx8888" for this mock inquiry')
        return value

    @field_validator("channelCode")
    @classmethod
    def validate_channel_code(cls, value: str) -> str:
        if value != "MOB":
            raise ValueError('channelCode must be "MOB" for this mock inquiry')
        return value

    @field_validator("apiKey")
    @classmethod
    def validate_api_key(cls, value: str) -> str:
        if value not in {"SequreKey123", "SecureKey123"}:
            raise ValueError('apiKey must be "SequreKey123" or "SecureKey123"')
        return value

    @field_validator("transactionDateTime")
    @classmethod
    def validate_transaction_datetime_today(cls, value: datetime) -> datetime:
        current_date = datetime.now(value.tzinfo).date() if value.tzinfo else datetime.now().date()
        if value.date() != current_date:
            raise ValueError("transactionDateTime must be today")
        return value


class BillLookupResponse(BaseModel):
    functionName: str = "BillLookupResponse"
    transactionId: str
    transactionDateTime: str
    billerTransactionId: str
    responseCode: str = "0000"
    responseDescription: str = "Success"
    billerType: str
    billerId: str
    terminalNo: str
    reference1: str
    reference2: str
    tranAmount: str = ""
    info1: str = ""
    info2: str = ""
    info3: str = ""
    duedate: str = ""
    rtpReference: str = ""
    rsAppId: str = ""


@app.post("/v1/billpayment/payment", response_model=BillPaymentResponse)
def bill_payment(request: BillPaymentRequest) -> BillPaymentResponse:
    try:
        response_datetime = datetime.now().astimezone().isoformat(timespec="milliseconds")
        lookup_key = (request.reference1, request.reference2)
        record = LOOKUP_DATA.get(lookup_key)

        if request.reference1 == "INVALID_REF1":
            return BillPaymentResponse(
                transactionId=request.transactionId,
                responseDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1004",
                responseDescription="Invalid reference1",
                terminalNo=request.terminalNo,
            )

        if request.reference1 == "INVALID_REF12":
            return BillPaymentResponse(
                transactionId=request.transactionId,
                responseDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1005",
                responseDescription="Invalid reference1 and reference2",
                terminalNo=request.terminalNo,
            )

        if record is None:
            return BillPaymentResponse(
                transactionId=request.transactionId,
                responseDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1001",
                responseDescription="Data not found",
                terminalNo=request.terminalNo,
            )

        if record["merchantError"]:
            return BillPaymentResponse(
                transactionId=request.transactionId,
                responseDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="2001",
                responseDescription="Other merchant error",
                terminalNo=record["terminalNo"],
            )

        if record["isPaid"]:
            return BillPaymentResponse(
                transactionId=request.transactionId,
                responseDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1003",
                responseDescription="Already paid",
                terminalNo=record["terminalNo"],
            )

        if request.tranAmount and request.tranAmount != record["tranAmount"]:
            return BillPaymentResponse(
                transactionId=request.transactionId,
                responseDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1002",
                responseDescription="Invalid amount",
                terminalNo=record["terminalNo"],
            )

        return BillPaymentResponse(
            transactionId=request.transactionId,
            responseDateTime=response_datetime,
            billerTransactionId=request.transactionId,
            terminalNo=record["terminalNo"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/bell/v1/billpayment/payment", response_model=BillPaymentResponse)
def bill_payment_bell(request: BillPaymentRequest) -> BillPaymentResponse:
    return bill_payment(request)


@app.post("/pang/v1/billpayment/payment", response_model=BillPaymentResponse)
def bill_payment_pang(request: BillPaymentRequest) -> BillPaymentResponse:
    return bill_payment(request)


@app.post("/v1/billpayment/lookup", response_model=BillLookupResponse)
def bill_lookup(request: BillLookupRequest) -> BillLookupResponse:
    try:
        response_datetime = datetime.now().astimezone().isoformat(timespec="milliseconds")
        if request.reference1 == "INVALID_REF1":
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1004",
                responseDescription="Invalid reference1",
                billerType=request.billerType,
                billerId=request.billerId,
                terminalNo=request.terminalNo,
                reference1=request.reference1,
                reference2=request.reference2,
            )

        if request.reference1 == "INVALID_REF12":
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1005",
                responseDescription="Invalid reference1 and reference2",
                billerType=request.billerType,
                billerId=request.billerId,
                terminalNo=request.terminalNo,
                reference1=request.reference1,
                reference2=request.reference2,
            )

        if request.reference1 in REFERENCE1_ONLY_DATA and not request.reference2:
            record = REFERENCE1_ONLY_DATA[request.reference1]
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                billerType=record["billerType"],
                billerId=request.billerId,
                terminalNo=record["terminalNo"],
                reference1=request.reference1,
                reference2=record["reference2"],
                tranAmount=record["tranAmount"],
                info1=record["info1"],
                info2=record["info2"],
                info3=record["info3"],
                duedate=record["duedate"],
                rtpReference=record["rtpReference"],
            )

        lookup_key = (request.reference1, request.reference2)
        record = LOOKUP_DATA.get(lookup_key)

        if record is None:
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1001",
                responseDescription="Data not found",
                billerType=request.billerType,
                billerId=request.billerId,
                terminalNo=request.terminalNo,
                reference1=request.reference1,
                reference2=request.reference2,
            )

        if record["merchantError"]:
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="2001",
                responseDescription="Other merchant error",
                billerType=record["billerType"],
                billerId=request.billerId,
                terminalNo=record["terminalNo"],
                reference1=request.reference1,
                reference2=request.reference2,
                tranAmount=record["tranAmount"],
                info1=record["info1"],
                info2=record["info2"],
                info3=record["info3"],
                duedate=record["duedate"],
                rtpReference=record["rtpReference"],
            )

        if record["isPaid"]:
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1003",
                responseDescription="Already paid",
                billerType=record["billerType"],
                billerId=request.billerId,
                terminalNo=record["terminalNo"],
                reference1=request.reference1,
                reference2=request.reference2,
                tranAmount=record["tranAmount"],
                info1=record["info1"],
                info2=record["info2"],
                info3=record["info3"],
                duedate=record["duedate"],
                rtpReference=record["rtpReference"],
            )

        if request.tranAmount and request.tranAmount != record["tranAmount"]:
            return BillLookupResponse(
                transactionId=request.transactionId,
                transactionDateTime=response_datetime,
                billerTransactionId=request.transactionId,
                responseCode="1002",
                responseDescription="Invalid amount",
                billerType=record["billerType"],
                billerId=request.billerId,
                terminalNo=record["terminalNo"],
                reference1=request.reference1,
                reference2=request.reference2,
                tranAmount=record["tranAmount"],
                info1=record["info1"],
                info2=record["info2"],
                info3=record["info3"],
                duedate=record["duedate"],
                rtpReference=record["rtpReference"],
            )

        info1 = record["info1"]
        info2 = record["info2"]
        info3 = record["info3"]
        if request.language == "TH" and request.reference1 == "300000025755":
            info1 = "ค่าไฟฟ้า"
            info2 = "กรุงเทพ"
            info3 = "ลูกค้า: TH"
        if request.language == "EN" and request.reference1 == "300000025756":
            info1 = "Electricity Bill"
            info2 = "Bangkok"
            info3 = "Customer: EN"

        return BillLookupResponse(
            transactionId=request.transactionId,
            transactionDateTime=response_datetime,
            billerTransactionId=request.transactionId,
            billerType=record["billerType"],
            billerId=request.billerId,
            terminalNo=record["terminalNo"],
            reference1=request.reference1,
            reference2=request.reference2,
            tranAmount=record["tranAmount"],
            info1=info1,
            info2=info2,
            info3=info3,
            duedate=record["duedate"],
            rtpReference=record["rtpReference"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/bell/v1/billpayment/lookup", response_model=BillLookupResponse)
def bill_lookup_bell(request: BillLookupRequest) -> BillLookupResponse:
    return bill_lookup(request)


@app.post("/pang/v1/billpayment/lookup", response_model=BillLookupResponse)
def bill_lookup_pang(request: BillLookupRequest) -> BillLookupResponse:
    return bill_lookup(request)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
