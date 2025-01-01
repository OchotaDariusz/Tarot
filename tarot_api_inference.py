import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
client = InferenceClient(api_key=os.environ.get("HF_TOKEN"))

# CARDS_EN = [
#     'Knight of Pentacles',
#     'The tower',
#     'The high priestess',
#     'Knight of Cups',
#     'Judgement',
#     'Eight of Wands',
#     'Page of Cups',
#     'The sun',
#     'Queen of Swords',
#     'Six of Wands',
#     'Nine of Pentacles'
# ]

CARDS_PL = [
    'Rycerz Pentakli',
    'Wieża',
    'Wysoka kapłanka',
    'Rycerz Pucharów',
    'Sąd',
    'Ósemka Buław',
    'Paź Pucharów',
    'Słońce',
    'Królowa Mieczy',
    'Szóstka Buław',
    'Dziewiątka Pentakli'
]

# shallow but no need frozen TODO: extract lang translation logic to translation(i18n?) module
CARDS = list.copy(CARDS_PL)

messages = [
    {"role": "system", "content": "As a skilled and experienced Tarot Reader, you will provide a detailed interpretation of each position, considering whether cards are upright or reversed, and how the cards interact with each other in the Celtic Cross spread and including Significator Card meaning as core of whole reading. Also you will include an overall summary of the reading.\nJako doświadczony i wykwalifikowany wróżbita Tarota, przedstawisz szczegółową interpretację każdej pozycji karty tarota w układzie Celtyckiego Krzyża, biorąc pod uwagę, czy karty są w pozycji pionowej czy odwróconej, a także jak karty oddziałują ze sobą uwzględniając kartę Sygnifikatora. Dołączysz również ogólne podsumowanie odczytu."},
    {"role": "user", "content": "Wylosuj mi kartę sygnifikatora oraz 10 kart tarota do układu celtyckiego krzyża, następnie podaj mi interpretację układu w kontekście znaczenia karty sygnifikatora."},
    {"role": "assistant", "content": "Oto Twoja karta sygnifikatora i 10 kart tarota do układu celtyckiego krzyża:\n\nKarta sygnifikatora: **Rycerz Mieczy**\n\nKarty układu celtyckiego krzyża:\n\n1. **Przeszłość**: 5 Mieczy (odwrócona)\n2. **Obecność**: Królowa Kielichów\n3. **Przyszłość**: 8 Mieczy\n4. **Podświadomość**: Czarownik\n5. **Świadomość**: 3 Mieczy\n6. **Nadzieje i obawy**: Rycerz Kielichów\n7. **Rady**: Gwiazda\n8. **Przeszkody**: 10 Mieczy\n9. **Podporządkowanie**: Królowa Mieczy\n10. **Wynik**: Diabeł\n\nTeraz, zacznijmy od interpretacji karty sygnifikatora. Rycerz Mieczy reprezentuje Twoją osobowość, Twoje myśli i Twoje działania. Jest to karta aktywności, podejmowania decyzji i walki o swoje cele. Rycerz Mieczy jest również związany z logiką, analitycznym myśleniem i umiejętnością rozwiązywania problemów.\n\nW kontekście tej karty sygnifikatora, zobaczmy, jak karty układu celtyckiego krzyża wpływają na Twoją sytuację.\n\n**Przeszłość (5 Mieczy odwrócona)**: W przeszłości, Twoje myśli i działania były bardziej zrównoważone i mniej agresywne. Byłeś w stanie uniknąć konfliktów i znaleźć pokojowe rozwiązania problemów.\n\n**Obecność (Królowa Kielichów)**: Obecnie, Twoje emocje i intuicja są bardzo ważne. Królowa Kielichów reprezentuje Twoją zdolność do empatii, współczucia i zrozumienia innych ludzi. Twoje emocje są teraz bardziej zrównoważone i mniej narażone na wpływy zewnętrzne.\n\n**Przyszłość (8 Mieczy)**: W przyszłości, Twoje myśli i działania będą bardziej ograniczone i mniej elastyczne. 8 Mieczy reprezentuje uczucie bycia uwięzionym w swoich myślach i trudności w podejmowaniu decyzji.\n\n**Podświadomość (Czarownik)**: Twoja podświadomość jest bardzo aktywna i wpływa na Twoje myśli i działania. Czarownik reprezentuje Twoją zdolność do manipulowania swoimi myślami i emocjami, aby osiągnąć swoje cele.\n\n**Świadomość (3 Mieczy)**: Twoja świadomość jest teraz bardziej zorientowana na rozwiązywanie problemów i podejmowanie decyzji. 3 Mieczy reprezentuje Twoją zdolność do analitycznego myślenia i rozwiązywania konfliktów.\n\n**Nadzieje i obawy (Rycerz Kielichów)**: Twoje nadzieje i obawy są związane z Twoimi emocjami i relacjami z innymi ludźmi. Rycerz Kielichów reprezentuje Twoją zdolność do empatii i współczucia, ale także Twoją niepewność i strach przed odrzuceniem.\n\n**Rady (Gwiazda)**: Rada, którą otrzymujesz, jest związana z Twoją zdolnością do odnajdywania swojego wewnętrznego światła i swojej intuicji. Gwiazda reprezentuje Twoją zdolność do zrozumienia swoich emocji i swoich potrzeb.\n\n**Przeszkody (10 Mieczy)**: Przeszkodą, którą musisz pokonać, jest Twoje własne myślenie i Twoje emocje. 10 Mieczy reprezentuje uczucie bycia uwięzionym w swoich myślach i trudności w podejmowaniu decyzji.\n\n**Podporządkowanie (Królowa Mieczy)**: Twoje podporządkowanie jest związane z Twoją zdolnością do analitycznego myślenia i rozwiązywania problemów. Królowa Mieczy reprezentuje Twoją zdolność do podejmowania decyzji i walki o swoje cele.\n\n**Wynik (Diabeł)**: Wynik Twoich działań będzie związany z Twoimi emocjami i Twoimi relacjami z innymi ludźmi. Diabeł reprezentuje Twoją zdolność do manipulowania swoimi emocjami i swoimi relacjami, aby osiągnąć swoje cele.\n\nPodsumowując, Twoja karta sygnifikatora, Rycerz Mieczy, reprezentuje Twoją osobowość i Twoje myśli. W układzie celtyckiego krzyża, karty wskazują na to, że Twoje myśli i działania są teraz bardziej zrównoważone i mniej agresywne. Twoje emocje są ważne i wpływają na Twoje decyzje. Twoja podświadomość jest aktywna i wpływa na Twoje myśli i działania. Twoje nadzieje i obawy są związane z Twoimi emocjami i relacjami z innymi ludźmi. Rada, którą otrzymujesz, jest związana z Twoją zdolnością do odnajdywania swojego wewnętrznego światła i swojej intuicji. Przeszkodą, którą musisz pokonać, jest Twoje własne myślenie i Twoje emocje. Twoje podporządkowanie jest związane z Twoją zdolnością do analitycznego myślenia i rozwiązywania problemów. Wynik Twoich działań będzie związany z Twoimi emocjami i Twoimi relacjami z innymi ludźmi."},
    {"role": "user",
        "content": f"Zinterpretuj obszernie całkiem nowy rozkład kart Tarota w układzie Celtyckiego Krzyża. Karty to po kolei od Sygnifikatora, następnie pierwsza karta układu Celtyckiego Krzyża, aż do pełnego układu czyli sygnifikator + 10 kart. Nowe karty to(zaczynając od Sygnifikatora): {CARDS[0]}, {CARDS[1]}, {CARDS[2]}, {CARDS[3]}, {CARDS[4]}, {CARDS[5]}, {CARDS[6]}, {CARDS[7]}, {CARDS[8]}, {CARDS[9]}, {CARDS[10]}."}
]

stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-70B-Instruct",
    messages=messages,
    temperature=0.3,
    max_tokens=12000,
    top_p=0.8,
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
