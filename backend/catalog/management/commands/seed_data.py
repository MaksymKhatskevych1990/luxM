from django.core.management.base import BaseCommand

from catalog.models import (
    CraftDetail,
    Material,
    ProcessStep,
    Project,
    ProjectStage,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)

IMG = {
    "kitchen": (
        "https://images.unsplash.com/photo-1765371515325-b6611765dfad"
        "?w=1400&h=900&fit=crop&auto=format"
    ),
    "library": (
        "https://images.unsplash.com/photo-1780257563050-0ee78acfeee8"
        "?w=800&h=1100&fit=crop&auto=format"
    ),
    "wardrobe": (
        "https://images.unsplash.com/photo-1593173945705-d6451ed5909a"
        "?w=800&h=600&fit=crop&auto=format"
    ),
    "living": (
        "https://images.unsplash.com/photo-1594272807311-3ed584a48577"
        "?w=1100&h=700&fit=crop&auto=format"
    ),
    "idea": (
        "https://images.unsplash.com/photo-1590880795696-20c7dfadacde"
        "?w=1100&h=700&fit=crop&auto=format"
    ),
    "model_3d": (
        "https://images.unsplash.com/photo-1497218770144-3fea6dbc33fe"
        "?w=1100&h=700&fit=crop&auto=format"
    ),
    "production": (
        "https://images.unsplash.com/photo-1631396326838-de37e5f8bcbc"
        "?w=1100&h=700&fit=crop&auto=format"
    ),
    "install": (
        "https://images.unsplash.com/photo-1765371515325-b6611765dfad"
        "?w=1100&h=700&fit=crop&auto=format"
    ),
    "measures": (
        "https://images.unsplash.com/photo-1659930087003-2d64e33181f7"
        "?w=700&h=900&fit=crop&auto=format"
    ),
    "craft_1": (
        "https://images.unsplash.com/photo-1659930087003-2d64e33181f7"
        "?w=500&h=680&fit=crop&auto=format"
    ),
    "craft_2": (
        "https://images.unsplash.com/photo-1631396326646-c06a935ff3a6"
        "?w=500&h=650&fit=crop&auto=format"
    ),
    "craft_3": (
        "https://images.unsplash.com/photo-1712171984530-e25a4aaa46dd"
        "?w=500&h=700&fit=crop&auto=format"
    ),
    "craft_4": (
        "https://images.unsplash.com/photo-1679797850019-3d0d8659a695"
        "?w=500&h=620&fit=crop&auto=format"
    ),
    "oak": (
        "https://images.unsplash.com/photo-1582055193464-943584223be1"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "walnut": (
        "https://images.unsplash.com/photo-1736506159776-22ca388780fa"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "veneer": (
        "https://images.unsplash.com/photo-1506689205310-0a29c388691c"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "stone": (
        "https://images.unsplash.com/photo-1778272617843-bdda47b64bad"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "metal": (
        "https://images.unsplash.com/photo-1497218770144-3fea6dbc33fe"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "glass": (
        "https://images.unsplash.com/photo-1593173945705-d6451ed5909a"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "workshop_1": (
        "https://images.unsplash.com/photo-1547609434-b732edfee020"
        "?w=500&h=720&fit=crop&auto=format"
    ),
    "workshop_2": (
        "https://images.unsplash.com/photo-1679797850019-3d0d8659a695"
        "?w=400&h=400&fit=crop&auto=format"
    ),
    "workshop_3": (
        "https://images.unsplash.com/photo-1631396326646-c06a935ff3a6"
        "?w=400&h=400&fit=crop&auto=format"
    ),
    "before": (
        "https://images.unsplash.com/photo-1664995156397-99bd42f5a8ab"
        "?w=1400&h=900&fit=crop&auto=format"
    ),
    "after": (
        "https://images.unsplash.com/photo-1758565811352-a439bd6f956e"
        "?w=1400&h=900&fit=crop&auto=format"
    ),
}


class Command(BaseCommand):
    help = "Seed catalog content from the Forma Studio mockup."

    def handle(self, *args, **options):
        self._seed_settings()
        self._seed_projects()
        self._seed_materials()
        self._seed_process_steps()
        self._seed_craft_details()
        self._seed_workshop()
        self.stdout.write(self.style.SUCCESS("Seed data loaded from Forma Studio mockup."))

    def _seed_settings(self):
        settings = SiteSettings.load()
        settings.brand_name = "Форма Studio"
        settings.tagline = "Унікальні меблі на замовлення. Київ, Україна."
        settings.founded_year = 2018
        settings.phone = "+38 (044) 555 12 34"
        settings.email = "studio@forma.ua"
        settings.telegram = "@forma_studio"
        settings.address = "Київ · Стара Дарниця, вул. Промислова 14"
        settings.instagram_url = "https://instagram.com/"
        settings.telegram_url = "https://t.me/"
        settings.seo_title = "Форма Studio — меблі на замовлення в Києві"
        settings.seo_description = (
            "Преміальні меблі на замовлення: проєктування, виробництво та монтаж. "
            "Кухні, гардеробні, вітальні та кабінети."
        )
        settings.seo_keywords = (
            "меблі на замовлення, кухні Київ, гардеробні, Forma Studio"
        )
        settings.stats_projects = "147"
        settings.stats_years = "08"
        settings.stats_masters = "24"
        settings.stats_production = "100%"
        settings.workshop_quote = (
            "Ми не просто виготовляємо меблі. Ми створюємо предмети, "
            "які мають існувати саме у вашому просторі."
        )
        settings.workshop_author = "Андрій Коваль, засновник"
        settings.workshop_text = (
            "Наша майстерня площею 800 м² в Старій Дарниці обладнана точними "
            "верстатами ЧПУ та ручним інструментом. Кожен виріб — від першого "
            "ескізу до встановлення — проходить через руки одного майстра."
        )
        settings.before_image_url = IMG["before"]
        settings.after_image_url = IMG["after"]
        settings.save()

    def _seed_projects(self):
        kitchen, _ = Project.objects.update_or_create(
            slug="kuhnya-pryvatnyy-budynok",
            defaults={
                "title": "Кухня для приватного будинку",
                "subtitle": (
                    "Острівна кухня з масиву дуба. Стільниця з мармуру Calacatta."
                ),
                "description": (
                    "Спроєктована з урахуванням геометрії приміщення: "
                    "L-подібне планування, острів з кам'яною стільницею "
                    "та інтегрована система зберігання.\n\n"
                    "Фасади — масив дуба з відкритою текстурою. "
                    "Ніжки та ручки — матова сталь. Стільниця — мармур Calacatta."
                ),
                "materials_label": "ДУБ · КАМІНЬ · 2026",
                "category": "Кухня",
                "year": 2026,
                "area": "18 м²",
                "duration": "11 тижнів",
                "location": "Приватний будинок · Київ",
                "image_url": IMG["kitchen"],
                "detail_image_url": IMG["install"],
                "is_featured": True,
                "is_published": True,
                "order": 1,
                "seo_title": "Кухня з натурального дуба",
                "seo_description": (
                    "L-подібне планування, острів з кам'яною стільницею "
                    "та інтегрована система зберігання."
                ),
            },
        )
        kitchen.stages.all().delete()
        ProjectStage.objects.bulk_create(
            [
                ProjectStage(
                    project=kitchen,
                    title="Ідея",
                    image_url=IMG["idea"],
                    order=1,
                ),
                ProjectStage(
                    project=kitchen,
                    title="3D-модель",
                    image_url=IMG["model_3d"],
                    order=2,
                ),
                ProjectStage(
                    project=kitchen,
                    title="Виготовлення",
                    image_url=IMG["production"],
                    order=3,
                ),
                ProjectStage(
                    project=kitchen,
                    title="Монтаж",
                    image_url=IMG["install"],
                    order=4,
                ),
            ]
        )

        Project.objects.update_or_create(
            slug="biblioteka-i-kabinet",
            defaults={
                "title": "Бібліотека і кабінет",
                "subtitle": (
                    "Вбудована бібліотека по всій висоті. "
                    "Ніжки та ручки — матова сталь."
                ),
                "description": (
                    "Вбудована бібліотека по всій висоті стіни з відкритими "
                    "полицями та закритими секціями. Каркас і фасади — горіх "
                    "з виразним малюнком волокна. Ніжки та ручки — матова сталь."
                ),
                "materials_label": "ГОРІХ · МЕТАЛ · 2025",
                "category": "Кабінет",
                "year": 2025,
                "area": "22 м²",
                "duration": "9 тижнів",
                "location": "Квартира · Київ",
                "image_url": IMG["library"],
                "detail_image_url": IMG["library"],
                "is_featured": True,
                "is_published": True,
                "order": 2,
                "seo_title": "Бібліотека і кабінет",
                "seo_description": (
                    "Вбудована бібліотека по всій висоті. Ніжки та ручки — матова сталь."
                ),
            },
        )

        Project.objects.update_or_create(
            slug="garderobna-zi-shponu",
            defaults={
                "title": "Гардеробна зі шпону",
                "subtitle": "Гардеробна система зі шпону ясена та матовим склом.",
                "description": (
                    "Простора гардеробна зі шпону ясена: відкриті рейли, "
                    "висувні ящики та вітрини із загартованого матового скла. "
                    "Рівна текстура, м'яке світло, точна фурнітура."
                ),
                "materials_label": "ШПОН · СКЛО · 2025",
                "category": "Гардеробна",
                "year": 2025,
                "area": "14 м²",
                "duration": "7 тижнів",
                "location": "Приватний будинок · Київ",
                "image_url": IMG["wardrobe"],
                "detail_image_url": IMG["wardrobe"],
                "is_featured": True,
                "is_published": True,
                "order": 3,
                "seo_title": "Гардеробна зі шпону",
                "seo_description": (
                    "Гардеробна система зі шпону ясена та матовим склом."
                ),
            },
        )

        Project.objects.update_or_create(
            slug="vitalnya-wabi-sabi",
            defaults={
                "title": "Вітальня у стилі Wabi-Sabi",
                "subtitle": "Тихі форми, натуральний дуб і льон.",
                "description": (
                    "Вітальня у стилі Wabi-Sabi: низький меблевий ряд з масиву дуба, "
                    "м'які лляні текстури та відкриті полиці без зайвого декору. "
                    "Простір, у якому матеріал важливіший за орнамент."
                ),
                "materials_label": "ДУБ · ЛЬОН · 2024",
                "category": "Вітальня",
                "year": 2024,
                "area": "28 м²",
                "duration": "8 тижнів",
                "location": "Квартира · Київ",
                "image_url": IMG["living"],
                "detail_image_url": IMG["living"],
                "is_featured": True,
                "is_published": True,
                "order": 4,
                "seo_title": "Вітальня у стилі Wabi-Sabi",
                "seo_description": "Тихі форми, натуральний дуб і льон.",
            },
        )

    def _seed_materials(self):
        materials = [
            {
                "name_uk": "Дуб",
                "name_en": "OAK",
                "description": (
                    "Масив із відкритою текстурою. Теплий на дотик, зносостійкий."
                ),
                "image_url": IMG["oak"],
                "order": 1,
            },
            {
                "name_uk": "Горіх",
                "name_en": "WALNUT",
                "description": (
                    "Темна деревина з виразним малюнком волокна. "
                    "Для бібліотек і кабінетів."
                ),
                "image_url": IMG["walnut"],
                "order": 2,
            },
            {
                "name_uk": "Шпон",
                "name_en": "VENEER",
                "description": (
                    "Натуральний шпон ясена та клена. Рівна текстура, широка палітра."
                ),
                "image_url": IMG["veneer"],
                "order": 3,
            },
            {
                "name_uk": "Камінь",
                "name_en": "STONE",
                "description": (
                    "Мармур Calacatta та граніт. Стільниці та острови "
                    "з унікальним малюнком."
                ),
                "image_url": IMG["stone"],
                "order": 4,
            },
            {
                "name_uk": "Метал",
                "name_en": "METAL",
                "description": (
                    "Матова сталь, латунь. Ніжки, ручки, декоративні вставки."
                ),
                "image_url": IMG["metal"],
                "order": 5,
            },
            {
                "name_uk": "Скло",
                "name_en": "GLASS",
                "description": (
                    "Загартоване матове та прозоре скло. Вітрини, фасади, двері."
                ),
                "image_url": IMG["glass"],
                "order": 6,
            },
        ]
        for item in materials:
            Material.objects.update_or_create(
                name_uk=item["name_uk"],
                defaults={
                    "name_en": item["name_en"],
                    "description": item["description"],
                    "image_url": item["image_url"],
                    "order": item["order"],
                    "is_published": True,
                },
            )

    def _seed_process_steps(self):
        steps = [
            {
                "title": "Ідея",
                "description": (
                    "Ви розповідаєте про простір та побажання. "
                    "Ми слухаємо, вивчаємо, ставимо питання."
                ),
                "duration": "1–2 дні",
                "image_url": IMG["idea"],
                "order": 1,
            },
            {
                "title": "Заміри",
                "description": (
                    "Виїзд майстра, детальні обміри приміщення, "
                    "фотофіксація всіх нюансів."
                ),
                "duration": "1 день",
                "image_url": IMG["measures"],
                "order": 2,
            },
            {
                "title": "Проєктування",
                "description": (
                    "Розробка 3D-моделі, технічних креслень, "
                    "вибір матеріалів та покриттів."
                ),
                "duration": "5–10 днів",
                "image_url": IMG["model_3d"],
                "order": 3,
            },
            {
                "title": "Виробництво",
                "description": (
                    "Виготовлення в майстерні вручну. "
                    "Поетапний контроль якості кожної деталі."
                ),
                "duration": "4–8 тижнів",
                "image_url": IMG["production"],
                "order": 4,
            },
            {
                "title": "Монтаж",
                "description": (
                    "Встановлення нашою командою майстрів, підключення, регулювання."
                ),
                "duration": "1–3 дні",
                "image_url": IMG["install"],
                "order": 5,
            },
            {
                "title": "Результат",
                "description": (
                    "Фінальна перевірка, фотографування готового простору. "
                    "Гарантія 5 років."
                ),
                "duration": "Назавжди",
                "image_url": IMG["install"],
                "order": 6,
            },
        ]
        for item in steps:
            ProcessStep.objects.update_or_create(
                order=item["order"],
                defaults={
                    "title": item["title"],
                    "description": item["description"],
                    "duration": item["duration"],
                    "image_url": item["image_url"],
                    "is_published": True,
                },
            )

    def _seed_craft_details(self):
        details = [
            ("Точна розмітка", IMG["craft_1"], 1),
            ("Ручна обробка", IMG["craft_2"], 2),
            ("Фінішне полірування", IMG["craft_3"], 3),
            ("Перевірка якості", IMG["craft_4"], 4),
        ]
        for title, image_url, order in details:
            CraftDetail.objects.update_or_create(
                title=title,
                defaults={
                    "image_url": image_url,
                    "order": order,
                    "is_published": True,
                },
            )

    def _seed_workshop(self):
        stats = [
            ("800 м²", "Площа майстерні", 1),
            ("1 майстер", "Від ескізу до монтажу", 2),
            ("ЧПУ + ручне", "Комбіноване виробництво", 3),
            ("5 років", "Гарантія на вироби", 4),
        ]
        for value, label, order in stats:
            WorkshopStat.objects.update_or_create(
                order=order,
                defaults={"value": value, "label": label},
            )

        images = [
            ("Майстерня", IMG["workshop_1"], 1),
            ("Деталь виробу", IMG["workshop_2"], 2),
            ("Ручна робота", IMG["workshop_3"], 3),
        ]
        for title, image_url, order in images:
            WorkshopImage.objects.update_or_create(
                order=order,
                defaults={"title": title, "image_url": image_url},
            )
