# developer: https://t.me/n3rz4_bloody_phoenix

from loader import Module, Moon
from random import choice
from typing import List
from types import ModuleType


class Generator(Module):
    def __init__(self) -> None:
        self.init()
        self.logger: Moon = self.get_logger()
        self.aiofiles: ModuleType = self.req("aiofiles", _importlib=True)
        self.phrases: List[str] = ['ты сынуля шлюхи ебаной', 'порвем тебе рыгалище', 'жалкий ты кусок говна', 'ты терпила будешь старадать тут', 'я тебе и шанса на выживание не дам жалкий сын бляди','ты никому не известный сынок говна','детина побляди рванный терпеть тебе велено','ты щенок ебаный не представляющий ничего из себя','я буду ебать и ебать рылище твоей матери пока ты сын шлюхи в себя не придешь','разорвм пездачело твоей мамаши', ' а ну хуесос ебаный не терпи','твою мамашу ебал',' ты сынок шельмы нищий','поблядь рванная на хую тут не сдыхай', ' ты разве что насадка для хуяцэм моего',' пиздак твой в ошметки мяса превратим','поблядь ебаная не утруждайся ты так а лишь прими позор','гортань твоей матери шлюхи перережу','слабая ты ни на что не способная дочь шлюхи не терпеть', 'сынище шлюхи пожирай говно', 'ты терпильный сын говнища не откинь копытца тут мне', 'а ну дерьмоед ебаный не сдавайся тут на хуе моем', 'ты сынок побляди ебаной ты что тут в себя поверила или что я раскромсаю рылище твое ты понял', 'не убегай отсюда шушваль ебаная', 'твою мамашу на хуй натяну пока ты сын бляди тут потеешь', 'тварина ебаная может ты уже перестанешь терпеть тут', 'сыняра грязи ты будешь разве что дыркой для хуя моего', 'я членом пройдусь по твоему рылу попутно разрывая его сынуля ты шлюхи слабой', 'хуесоска чернорылая ты так и будешь будто бы застривать на хуе', 'ты слабая проблядь а ну пошла отсюда', 'я твою мамашу порву тут просто ты сын хуйни ахуел в край', 'детище блядины ебаной а ну соси тут', 'харканем в рылище твоей матери с такой силой что уж прорвем ей черепицу', ' ты сын плесени ебаной поешл нахуй отсюда' , 'сын уличной урны ты ебаный тебе разве не было сказано терпеть и помирать на хуях наших', 'сынок ты шалавы ебаной ты ведь просто насадница на хуец не более', ' терпила будем гасить тебя шлюху слабейшую', 'зарезанный моим хуем','убитый моим членом', 'избитый мною', 'раздербаненный моим хуйцем', 'изпидорашенный моим пенисом', 'изуродованный мною', 'выебанная моим агрегатом', 'изнасилованная мною', 'уторпедированная моим елдаком', 'истребленная моим членищем', 'я тебе мать ебал тут осознавай', 'рыльце твое размажу нахуй вникаешь тут', 'трахну твое никому не всравшее пиздалище',  'на моем члене ты подохший',  'изпидорасю тебе рыгло', 'в рыльце тебе нассым', 'использовал твою пизду кстати как аналог писсуара', 'твой анал исключительно моему хую подлежит', 'не тухни тут ебта', 'не помирай на моем члентаке', 'не пытайся убежать от меня', 'я тебе мамашу ебал ведь тут',  'я являюсь богом ебырем твоей матери шлюхи', 'не терпи ибо я могу заебашить твое пиздалище', 'твоя пезда является для менее не более чем одноразовым презервативом помни', 'своим хуэм тебе дыхательные пути порвал внатуре', 'скальпел тебе срежу хуэм что бы ты понимало', 'я тебе мамашу ебал лул вникай в данное', 'я поочередно тебе состав зубной выбивал хуэм',  'я твою мать буду ебать до сей поры пока это не надоест меня', 'мне свойственно насиловать тушак твоей матери шлюхи', 'я на твоем рыгле свои инициалы оставлю', 'своим члентаком всех представителей твоей семьи зарежу', 'сиди терпи пока я тебе еблище не поломал тут окончательным счетом', 'не вздумай с моего хуя убежать', 'не сумел мне ничего против моего хуя сопоставить мдам', 'забавно лицезреть как ты всеми силами тужишься дабы от моего хуя царского убежать', 'ану сбежал отсюда покуда я тебе все твои кости не переломал', 'передвигай свои копытца резче с моего хуя', 'я кстати ковыряюсь своим хуйцем в уретральных прослойках твоей мамщели', 'что ты там мне в хуй хрюкаешь эм', 'я кстати попросто напросто разрезал пездак твоей матери', 'мне привыкать утилизировать туши тебе подобных свиней', 'всевозможные усчелия анальные твоей матери ебал кстати','ты вникай что от моего хуя не сбежать никак нахуй', 'все попытки трусливо убежать с моего агрегата увенчаны на гибель как и жизнь твоей матери шлюхи', 'не сдавайся тут ебта я только разогрелся', 'ты кому тут свои односторонные потуги отправлять пытаешься', 'я же твое пиздалище вобью сука в асфальт эу нахуй', 'твои гланды повырываю своим хуэм дете шлюхи что бы ты вследствий не мог потом хрукать что то в сторону моего пениса', 'не дам тебе шансы на реаблитацию на моем хуе тут лул', 'раб пидорас сука', 'хуегрыз', 'членологрыз', 'насадка хуя', 'маломощный', 'сын бляди', 'раб хуя', 'черныш', 'сын хуйни', 'сынок говна', 'сынуля дерьма', 'дете шлюхи', 'вафля', 'подсос', 'олигофрен', 'шизофренник','рабопидорас', 'терпиленок', 'терпилоид', 'вафлежуй', 'сынишка шелухи', 'свин', 'поросенок', 'дете бляди', 'фанат', 'заморыш', 'унтерменш', 'унтерье', 'убожество', 'никчемныш', 'омежка', 'амежка', 'лалочка', 'лоускилл', 'шлюханок', 'дитя швали', 'профурсетыш', 'профура', 'потешный', 'заготовочный', 'генераторный', 'педик', 'пледовыш', 'абортыш','челядь', 'копрофаг', 'говноед', 'копрофил', 'чурок', 'хаченок', 'раб пидорас', 'хомяк', 'хуесос', 'членосос', 'хуелиз', 'проблядь', 'ошизофреневший', 'опидоревший', 'ошлюхоневший', 'обдегенератевший', 'обпрофурсетевший', 'охуевший', 'опрошмандевший', 'облядевший', 'ошалавевший', 'отруханевший', 'ошкуреневший', 'оговнотроллевший', 'офанатевший', 'опутаноневший', 'ошмаровевший', 'обаребуханевший', 'одерьмевевший', 'орабопидорассовевший', 'охуесосовевший', 'охуелизовевший','охуегрызовевший', 'отерпилевевший', 'одыревший', 'ожерлоневший', 'одырконевший', 'осуфлерший', 'опониковевший', 'убожественный', 'никчемный', 'мнимый', 'прещырылый', 'свинорылый', 'пиздаеблый', 'дуропездный', 'свинопездый', 'хуегрызный', 'манямирочный', 'черноеблый', 'омежливый', 'девственномежнопидорасный', 'шлюхообразный', 'оскотиневший', 'безталантливый', 'анскильный', 'лоускильный', 'свиноеблый', 'примитивный', 'униженный','одырчастый', 'косорылый', 'косоеблый', 'криворылый', 'кривокопытный', 'убожественный', 'облевовычный', 'окровавленный', 'распотрошенный', 'изтраханный', 'манямирочный', 'червивый', 'червеообразный', 'опарышевидный', 'поросячий', 'плешивый', 'олигофренический', 'триперный', 'тривиальный', 'рабопидорассовский', 'терпилоидный', 'терпилевший', 'атрофированный', 'скудодумный', 'дефектный', 'шлюхоподобный', 'свиноподобный', 'псинообразный', 'тухлощекий', 'тухлодырый', 'отребуханевший', 'обухший', 'перегнивший', 'нафалеточный','побрякушный', 'блядевидный', 'черномазый', 'чернорылый','зарезанный', 'располовинутый','недееспособный','небоеспособный', 'негодный', 'померший', 'опездевший', 'потнющий', 'вегеативный', 'нелепый', 'несуразный', 'софистический', 'лоботомизированный', 'нахуйнный', 'начленный', 'выкошанный','вытребуха' ]
        self.handlers()

    async def result_generate_handler(self, msg, file_name, result_generate):
        result_text = ' '.join(result_generate)
        async with self.aiofiles.open(file_name, mode="w") as file:
            await file.write(result_text)

        await msg.respond("by n3rz4", file=file_name)

    async def generator_handler(self, msg, args):
        if not args:
            return await msg.edit("<b>Укажите аргументы</b>", parse_mode="html")

        reply_message = await msg.get_reply_message()
        if not reply_message:
            return await msg.edit("<b>Укажите реплай на файл</b>", parse_mode="html")

        target_file = reply_message
        current_number = int(args[0])
        result_generate = []
        generated_text = []

        file_name = await self.client.download_media(target_file, f"{current_number}.txt")

        for _ in range(current_number * 2):
            random_choice = choice(self.phrases)
            if random_choice not in generated_text:
                generated_text.append(random_choice)
                result_generate.append(random_choice)

                if len(result_generate) >= current_number:
                    await self.result_generate_handler(msg, file_name, result_generate)
                    result_generate = []
                    generated_text = []
                    break

    def handlers(self):
        @self.strict_owner_command
        async def generate(event):
            args = await self.get_args(event)
            await self.generator_handler(event, args)

Generator()
