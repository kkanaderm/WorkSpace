# BillPayment Exercise API

API สำหรับแบบทดสอบ KBank Bill Payment (Exercise 2: BillPayment Success)

## Endpoints

- `POST /v1/billpayment/payment`
- `GET /health`

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

## Request Example

```json
{
  "functionName": "BillPayment",
  "transactionId": "98099310720200530183382100",
  "transactionDateTime": "2026-05-26T10:35:18.450+07:00",
  "billerType": "",
  "billerId": "98499",
  "terminalNo": "xxxxxxx8888",
  "channelCode": "MOB",
  "tranAmount": "120.00",
  "senderBankCode": "Kbank",
  "isRetry": "0",
  "reference1": "300000025751",
  "reference2": "1733084",
  "language": "EN",
  "apiKey": "SequreKey123"
}
```

## Response Example

```json
{
  "functionName": "BillPaymentResponse",
  "transactionId": "98099310720200530183382100",
  "responseDateTime": "2026-05-26T10:40:17.450+07:00",
  "billerTransactionId": "98099310720200530183382100",
  "responseCode": "0000",
  "responseDescription": "Success",
  "terminalNo": "xxxxxxx8888",
  "settlementDate": "",
  "rsAppId": ""
}
```

## Validation ที่บังคับตาม Exercise

- `functionName` ต้องเป็น `BillPayment`
- `billerId` ต้องเป็น `98499`
- `senderBankCode` ต้องเป็น `Kbank`
- `isRetry` ต้องเป็น `0`
- `apiKey` รองรับทั้ง `SequreKey123` และ `SecureKey123`
- `transactionDateTime` ต้องเป็นวันปัจจุบัน
