from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7712256876:AAHiucdxuWBAmuckEHY_297gM6q1-fzNO5E"
TELEGRAM_CHAT_ID = "1310918642"

def send_telegram_message(msg: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    print("[텔레그램 전송 완료]", response.status_code, response.text)

@app.route("/whale", methods=["POST"])
def whale_webhook():
    try:
        data = request.json
        print("[수신된 Webhook 데이터]", data)

        tx = data[0] if isinstance(data, list) else data

        from_address = tx.get("from", "알 수 없음")
        to_address = tx.get("to", "알 수 없음")
        value_wei = int(tx.get("value", "0"))
        tx_hash = tx.get("transactionHash", "")

        value_eth = value_wei / 10**18
        etherscan_link = f"https://etherscan.io/tx/{tx_hash}"

        message = (
            f"🐋 *ETH 고래 트랜잭션 감지!*\n\n"
            f"👤 *보낸 주소*: `{from_address}`\n"
            f"📥 *받는 주소*: `{to_address}`\n"
            f"💰 *전송 금액*: `{value_eth:.2f} ETH`\n"
            f"🔗 [트랜잭션 보기]({etherscan_link})"
        )

        send_telegram_message(message)
        return "OK", 200

    except Exception as e:
        print("[오류 발생]", e)
        return "Error", 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
