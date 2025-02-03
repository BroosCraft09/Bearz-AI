import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

API_KEY = "AIzaSyASC5Z9jVG7h2brCzRrUaHLkiw4gBT9sy8"  # Ganti dengan API Key Gemini

@csrf_exempt
def get_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"response": "Pesan tidak boleh kosong!"})

            # Cek jika pertanyaan adalah "Siapa namamu?"
            if "siapa namamu" in user_message.lower():
                return JsonResponse({
                    "response": "Saya Bearz AI, model bahasa AI yang dikembangkan oleh Google. "
                                "Saya tidak memiliki nama karena saya bukan manusia."
                })

            # Kirim request ke Gemini AI
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText?key={API_KEY}"
            payload = {"prompt": {"text": user_message}}
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()

            if "candidates" in result and result["candidates"]:
                return JsonResponse({"response": result["candidates"][0]["output"]})
            else:
                return JsonResponse({"response": "AI tidak memberikan jawaban yang valid."})

        except requests.exceptions.RequestException as e:
            return JsonResponse({"response": f"Terjadi kesalahan saat menghubungi AI: {e}"})
        except Exception as e:
            return JsonResponse({"response": f"Terjadi error: {str(e)}"})

    return JsonResponse({"response": "Hanya menerima metode POST."})
