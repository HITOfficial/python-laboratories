from thefuzz import fuzz, process
from datetime import datetime

# niekoniecznie na roznych pietrach te same urzadzenia maja takie same swiatla

# istnieje problem ze wlacz jest rozpoznawane czesciej jako stan OFF zamiast ON
# czasami istnieje problem ze podczas wylaczenie po

# parter: kuchnia, lazienka
# pierwsze pietro: salon, sypialnia, lazienka
# drugie pietro salon kuchnia, sypialnia, lazienka


def decision(input_val, array, id=None):
    res = process.extract(input_val, array, limit=2)
    if len(res) > 1:
        tmp1, tmp2 = process.extract(input_val, array, limit=2)
        # best choice formula
        a, b = tmp1
        c, d = tmp2
        if ((b / d > 3) and b >= 50) or b >= 55:
            return a, b, id
        return None
    a,b = res[0]
    if b >= 55:
        return a,b,id
    return None

def correct_state(input_val, state_on, state_off, state_toggle):
    res1 = decision(input_val, state_on, "on")
    res2 = decision(input_val, state_off, "off")
    res3 = decision(input_val, state_toggle, "toggle")
    if not res1 and not res2 and not res3:
        return None
    return max(list(filter(None, [res1, res2, res3])), key=lambda x: x[1])


def storey_all_devices_change(input_val, state_on_all, devices, storey):
    tmp = process.extract(input_val, state_on_all, limit=1)
    accuracy = tmp[0][1]
    if accuracy > 50:
        return list(filter(lambda x: x[3] == storey[0], devices))
    return []


def place_device_change(input_val, devices, storey, place):
    filtered_devices = list(filter(lambda x: x[2] == place[0] and x[3] == storey[0], devices))
    return decision(input_val, filtered_devices)


def listen(places, devices, storeys, state_on_all, state_on, state_off, state_toggle):
    input_val = input(">>")

    with open("logs.txt", "a") as f:
        f.write(input_val + "\n")

    # state
    state = correct_state(input_val, state_on, state_off, state_toggle)
    if not state:
        print("no state status")
        return

    # storey
    storey = decision(input_val, storeys)

    if not storey:
        print("status fault")
        return

    # place
    place = decision(input_val, places)

    if not place:
        for device in storey_all_devices_change(input_val, state_on_all, devices, storey):
            splice_result(place, device, storey, state)
    else:
        results = place_device_change(input_val, devices, storey, place)
        if results is not None:
            device = results[0]
            splice_result(place, device, storey, state)
        else:
            print("there is no device in this place")
            return


def splice_result(place, device, storey, state):
    res = ""
    d = datetime.now()
    date_time = d.strftime("%m/%d/%Y, %H:%M:%S")
    res += date_time
    res += " >> " + storey[0]
    if place is not None:
        res += "/" + place[0]
    res += "/" + device[1]
    res += " " + state[2]
    with open("logs.txt", "a") as f:
        f.write(res + "\n")
    print(res)


def controller():
    places = ["kuchnia", "salon", "sypialnia", "łazienka"]

    devices = [
        ("oświetlenie górne", "firstFloor/light/up/livingroom", "salon", "pierwsze pietro"),
        ("oświetlenie górne", "secondFloor/light/up/bathroom", "łazienka", "drugie pietro"),
        ("oświetlenie górne", "secondFloor/light/up/bedroom", "sypialnia", "drugie pietro"),
        ("oświetlenie górne", "groundFloor/light/up/kitchen", "kuchnia", "parter"),
        ("oświetlenie górne", "secondFloor/light/up/kitchen", "kuchnia", "drugie pietro"),

        ("lampa prawa", "firstFloor/light/right/livingroom", "salon", "pierwsze pietro"),
        ("lampa prawa", "firstFloor/light/right/bedroom", "sypialnia", "pierwsze pietro"),
        ("lampa prawa", "light/right/bedroom", "sypialnia", "drugie pietro"),

        ("lampa prawa", "firstFloor/light/right/bedroom", "sypialnia", "pierwsze pietro"),
        ("lampa lewa", "light/left/livingroom", "salon", "drugie pietro"),
        ("lampa lewa", "light/left/bedroom", "sypialnia", "drugie pietro"),

        ("lampa nad stołem", "firstFloor/light/onTable/livingroom", "salon", "pierwsze pietro"),
        ("lampa nad stołem", "light/onTable/kitchen", "kuchnia", "drugie pietro"),

        ("lampa na oknie", "groundFloor/light/OnWindow/livingroom", "salon", "parter"),
        ("lampa na oknie", "groundFloor/light/OnWindow/kitchen", "kuchnia", "parter"),

        ("oświetlenie sufitu", "groundFloor/light/ceiling/kitchen", "kuchnia", "parter"),
        ("oświetlenie sufitu", "secondFloor/light/ceiling/kitchen", "kuchnia", "drugie pietro"),

        ("oświetlenie nocne", "secondFloor/night/light/bedroom", "sypialnia", "drugie pietro"),
        ("oświetlenie nocne", "firstFloor/night/light/bedroom", "sypialnia", "pierwsze pietro"),

        ("oświetlenie nad szafkami", "groundFloor/light/upCupboards/kitchen", "kuchnia", "parter"),
        ("oświetlenie pod szafkami", "groundFloor/light/ceiling/bathroom", "łazienka", "parter"),
        ("oświetlenie pod szafkami", "firstFloorlight/ceiling/bathroom", "łazienka", "pierwsze pietro"),
        ("oświetlenie pod szafkami", "secondFloor/light/ceiling/bathroom", "łazienka", "drugie pietro"),
    ]

    storeys = ["parter", "pierwsze pietro", "drugie pietro"]

    state_on_all = ["wszystkie", "wszedzie", "calkowicie"]
    # states
    state_on = ["wlacz", "włącz", "odpal", "zapal", "zalacz", "wlaczaj", "zalaczaj", "uruchom", "zaswiec"]

    state_off = ["wylacz", "wyłącz", "wyelminuj", "wyklucz", "wywal", "pozbyc sie", "odetnij", "powylaczaj", "odlacz",
                 "oddziel"]

    state_toogle = ["toggle", "zmien stan", "modyfikuj", "zmodyfikuj", "zmien", "przelacz", "transformuj"]

    while True:
        listen(places, devices, storeys, state_on_all, state_on, state_off, state_toogle)


print(controller())