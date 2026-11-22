"""
Interactive Cultural & Everyday Scenarios for Levantine / Lebanese Arabic Practice.
"""
from typing import List, Dict, Any

SCENARIOS_DATA: List[Dict[str, Any]] = [
    {
        "id": "beirut_cafe",
        "title_ar": "قهوة بيروت - Ahwet Beirut",
        "title_en": "At a Beirut Café",
        "icon": "☕",
        "category": "Daily Life & Dining",
        "level": "A1-A2",
        "location": "Hamra Street, Beirut",
        "description": "Step into a cozy café in Beirut. Order authentic Lebanese coffee, grab a hot manousheh, chat with the waiter, and ask for the bill.",
        "initial_tutor_message": "أهلاً وسهلاً يا هلا! تفضّل عود وين ما بدك. شو بتحب تشرب أو تاكل اليوم؟",
        "initial_transliteration": "Ahlan w sahlan ya hala! Tfaddal 3oud wein ma baddak. Shou bte7eb tishrab aw tekol el yom?",
        "initial_translation": "Welcome, welcome! Please have a seat wherever you like. What would you like to drink or eat today?",
        "objectives": [
            {"id": "obj_greet", "text_en": "Greet the waiter politely and say you want a table or are ready to order", "text_ar": "رحّب بالويتر وقلّه شو بدك تطلب", "completed": False},
            {"id": "obj_order_drink", "text_en": "Order a Lebanese coffee with your sweetness preference (wasat, bala soukar, etc.)", "text_ar": "اطلب فنجان قهوة وحدد السكر", "completed": False},
            {"id": "obj_order_food", "text_en": "Order a fresh Manousheh (zaatar or cheese)", "text_ar": "اطلب منقوشة زعتر أو جبنة سخنة", "completed": False},
            {"id": "obj_ask_bill", "text_en": "Ask for the check politely and thank the staff (Yislamo / Merci)", "text_ar": "اطلب الحساب واشكرهم", "completed": False}
        ],
        "starter_hints": [
            {"arabic": "يعطيك العافية! بدي فنجان قهوة وسط لو سمحت.", "translit": "Ya3tik el 3afye! Baddi fenjen ahwe wasat law sama7et.", "english": "May God give you health! I want a medium-sweet coffee, please."},
            {"arabic": "بدي كمان منقوشة زعتر سخنة مع كبّاية ماي.", "translit": "Baddi kaman manousheh zaatar sokhne ma3 kebbeyet may.", "english": "I also want a warm zaatar manousheh with a glass of water."},
            {"arabic": "قديش الحساب لو سمحت؟ ويسلمو إيديك!", "translit": "Addeish el hseib law sama7et? W yislamo ideik!", "english": "How much is the bill, please? And thank you so much!"}
        ]
    },
    {
        "id": "souk_bargaining",
        "title_ar": "البازار وسوق الحرف - El Souq",
        "title_en": "Bargaining at the Old Souk",
        "icon": "🛍️",
        "category": "Shopping & Culture",
        "level": "A2-B1",
        "location": "Old Souks of Byblos (Jbeil)",
        "description": "Explore the historic market stalls. Inquire about handmade cedar souvenirs and practice the art of friendly Lebanese price bargaining.",
        "initial_tutor_message": "أهلاً يا مية هلا! تفضل تفرّج على أحلى تحف وشغلات خشب أرز شغل إيد. عجبك شي؟",
        "initial_transliteration": "Ahlan ya miyet hala! Tfaddal tfarraj 3ala a7la to7af w shaghlet khashab arez shoghol eid. 3ajabak shi?",
        "initial_translation": "A hundred welcomes! Please look around at the finest handcrafted cedar wood artifacts. Does anything catch your eye?",
        "objectives": [
            {"id": "obj_inquire", "text_en": "Ask about the price of a cedar wood souvenir or embroidery", "text_ar": "اسأل عن سعر قطعة التذكار", "completed": False},
            {"id": "obj_bargain", "text_en": "Politely ask for a discount using 'Kermeli' or 'Ra3ina chway'", "text_ar": "فاصل بالسعر بلطف وطلب خصم", "completed": False},
            {"id": "obj_agree", "text_en": "Agree on a final price and complete the purchase", "text_ar": "اتفق على السعر النهائي وادفع", "completed": False}
        ],
        "starter_hints": [
            {"arabic": "كتير حلو هيدا! قديش حقه لو سمحت؟", "translit": "Ktiir 7elo heida! Addeish 7a22o law sama7et?", "english": "This is very nice! How much does it cost, please?"},
            {"arabic": "كتير هيك يا خيي، كرمالي راعينا بالسعر شوية!", "translit": "Ktiir heik ya khayye, kermeli ra3ina bel se3er chway!", "english": "That's a bit high my friend, do me a favor and give a little discount!"},
            {"arabic": "يلا اتفقنا، تفضل المصاري ويسلمو إيديك.", "translit": "Yalla ttafa2na, tfaddal el masari w yislamo ideik.", "english": "All right, agreed! Here is the money and thank you!"}
        ]
    },
    {
        "id": "service_taxi",
        "title_ar": "سرفيس بيروت - Beirut Service Taxi",
        "title_en": "Taking a Shared Taxi in Beirut",
        "icon": "🚕",
        "category": "Transportation & Navigation",
        "level": "A1-A2",
        "location": "Sassine Square to Hamra",
        "description": "Hail a Lebanese 'Service' shared taxi, specify your destination street, negotiate the fare, and tell the driver where to pull over.",
        "initial_tutor_message": "سرفيس! وين رايح يا شباب؟ عالحمرا ولا عالمصيطبة؟",
        "initial_transliteration": "Service! Wein rayeh ya shabab? 3al-Hamra wala 3al-Mseitbeh?",
        "initial_translation": "Service taxi! Where are you headed folks? To Hamra or to Msaitbeh?",
        "objectives": [
            {"id": "obj_destination", "text_en": "Tell the driver your destination (e.g. Hamra Street)", "text_ar": "حدّد وجهتك للسائق (شارع الحمرا)", "completed": False},
            {"id": "obj_fare", "text_en": "Ask if it's one 'Service' fare (Addeish el service?)", "text_ar": "اسأل عن تسعيرة السرفيس", "completed": False},
            {"id": "obj_stop", "text_en": "Direct the driver to drop you off on the right (3ala yeminak hon)", "text_ar": "اطلب النزول على اليمين", "completed": False}
        ],
        "starter_hints": [
            {"arabic": "سرفيس على شارع الحمرا لو سمحت؟", "translit": "Service 3ala chere3 el Hamra law sama7et?", "english": "Service to Hamra Street, please?"},
            {"arabic": "سرفيس واحد ولا تنين؟ قديش بتآخد؟", "translit": "Service wa7ad wala tnein? Addeish btekhed?", "english": "Is it a single or double service fare? How much?"},
            {"arabic": "على يمينك هون عند الإشارة لو سمحت! يسلمو.", "translit": "3ala yeminak hon 3ind el eshara law sama7et! Yislamo.", "english": "On your right here by the traffic light, please! Thank you."}
        ]
    },
    {
        "id": "family_dinner",
        "title_ar": "عزيمة عند العيلة - Lebanese Family Feast",
        "title_en": "Visiting a Lebanese Family",
        "icon": "🏡",
        "category": "Hospitality & Social Etiquette",
        "level": "B1-B2",
        "location": "Mount Lebanon Home",
        "description": "You are invited to a Lebanese family dinner. Master essential cultural compliments, polite refusals of 4th helpings, and blessing the hosts ('Deyme').",
        "initial_tutor_message": "أهلاً بحبيب قلبي! نورت بيتنا! تفضل ارتاح، عم نحضّر الطاولة، في تبولة وكبة وورق عنب. شو بتشرب بالأول؟",
        "initial_transliteration": "Ahlan bi 7abib qalbi! Nawwart beitna! Tfaddal irta7, 3am n7adder el tawleh, fi tabbouleh w kebbeh w wara2 3enab. Shou btisrab bel awwal?",
        "initial_translation": "Welcome dear friend! You brought light to our home! Please relax, we're setting the table with tabbouleh, kibbeh, and grape leaves. What will you drink first?",
        "objectives": [
            {"id": "obj_greet_family", "text_en": "Compliment their home and hospitality (Beit 3amer / Nawwart)", "text_ar": "امدح البيت والضيافة", "completed": False},
            {"id": "obj_praise_food", "text_en": "Praise the food and say 'Sahteyn' or 'Yislamo ideiki'", "text_ar": "امدح الأكل اللبناني الشهي", "completed": False},
            {"id": "obj_end_meal", "text_en": "Finish with the traditional blessing 'Deyme' (May your table always be blessed)", "text_ar": "اختم بالدعاء 'دايمة'", "completed": False}
        ],
        "starter_hints": [
            {"arabic": "الله ينوّر عليكن والبيت عامر دايماً بأهله!", "translit": "Allah ynawwer 3laykon w el beit 3amer dayman bi ahlo!", "english": "May God bless you, and may your home always be prosperous and full!"},
            {"arabic": "يسلمو هالإيدين! التبولة والكبة بتعقّد!", "translit": "Yislamo hal eidein! El tabbouleh w el kebbeh bte32od!", "english": "Bless these hands! The tabbouleh and kibbeh are mind-blowing!"},
            {"arabic": "سفرة دايمة يا رب! شبعت كتير وما عاد فيي أكل لقمة!", "translit": "Sofra deyme ya rabb! Shebe3t ktiir w ma 3ad fiyye ekol le2meh!", "english": "May this feast always be blessed! I'm completely full and can't take another bite!"}
        ]
    },
    {
        "id": "beirut_startup_office",
        "title_ar": "شغل ومكتب ببيروت - Beirut Startup Chat",
        "title_en": "Modern Workplace & Colleague Chat",
        "icon": "💼",
        "category": "Professional & Modern Life",
        "level": "B1-B2",
        "location": "Digital District (BDD), Beirut",
        "description": "Experience how modern professionals in Beirut communicate: seamless code-switching between Levantine Arabic, English, and French.",
        "initial_tutor_message": "Bonjour! Ça va? كيف ماشي الشغل معك اليوم؟ جاهز للـ meeting مع الـ team بعد ربع ساعة؟",
        "initial_transliteration": "Bonjour! Sa va? Kif mechi el shoghol ma3ak el yom? Jehez lal-meeting ma3 el team ba3ed rebe3 se3a?",
        "initial_translation": "Good morning! How are you? How is work going with you today? Are you ready for the team meeting in 15 minutes?",
        "objectives": [
            {"id": "obj_office_greet", "text_en": "Respond with the classic Beirut trilingual greeting", "text_ar": "رد بالتحية البيروتية الثلاثية اللغات", "completed": False},
            {"id": "obj_status_update", "text_en": "Give a quick progress update on your work", "text_ar": "أعطِ لمحة سريعة عن تطور الشغل", "completed": False},
            {"id": "obj_coffee_break", "text_en": "Suggest grabbing a quick espresso before the meeting", "text_ar": "اقترح شرب إسبريسو سريع قبل الاجتماع", "completed": False}
        ],
        "starter_hints": [
            {"arabic": "Bonjour! Ça va bien el-hamdillah. الشغل تمام وعم خلّص الـ presentation.", "translit": "Bonjour! Sa va bien el-hamdillah. El shoghol tamam w 3am khalles el presentation.", "english": "Bonjour! Doing well praise God. Work is great and I'm finishing the presentation."},
            {"arabic": "شو رأيك ننزل نجيب قهوة سريعة قبل ما يبلش الـ meeting؟", "translit": "Shou ra2yak ninzal njib ahwe sari3a abel ma yballesh el meeting?", "english": "What do you think about grabbing a quick coffee before the meeting starts?"}
        ]
    }
]

def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    for s in SCENARIOS_DATA:
        if s["id"] == scenario_id:
            return s
    return SCENARIOS_DATA[0]
