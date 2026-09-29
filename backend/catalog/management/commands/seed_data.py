from django.core.management.base import BaseCommand

from catalog.models import (
    CraftDetail,
    HeroScene,
    HeroStat,
    HeroZone,
    HERO_BACKGROUND_DEFAULT,
    Material,
    NavItem,
    PageSection,
    ProcessStep,
    Project,
    ProjectImage,
    ProjectStage,
    RoomType,
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
    "craft_1": "/craft/craft-1-survey.jpg",
    "craft_2": "/craft/craft-2-drawing.jpg",
    "craft_3": "/craft/craft-3-renovation.jpg",
    "craft_4": "/craft/craft-4-assembly.jpg",
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
    "before": "/before-after/before.jpg",
    "after": "/before-after/after.jpg",
}


class Command(BaseCommand):
    help = "Seed catalog content for ProProstir."

    def handle(self, *args, **options):
        settings = self._seed_settings()
        self._seed_hero_stats()
        self._seed_sections()
        self._seed_nav()
        self._seed_room_types()
        kitchen = self._seed_projects()
        settings.featured_project = kitchen
        settings.save(update_fields=["featured_project", "updated_at"])
        self._seed_materials()
        self._seed_process_steps()
        self._seed_craft_details()
        self._seed_workshop()
        self._seed_hero_scene()
        self.stdout.write(self.style.SUCCESS("Seed data loaded for ProProstir."))

    def _seed_settings(self):
        settings = SiteSettings.load()
        settings.brand_name = "ProProstir"
        settings.tagline = "Ми знаємо про простір все"
        settings.founded_year = 2018

        settings.header_logo_primary = "ProProstir"
        settings.header_logo_secondary = "Ми знаємо про простір все"
        settings.header_cta_text = "Розповісти бачення"
        settings.header_cta_href = "#контакти"

        settings.hero_eyebrow = "ProProstir · Повний цикл"
        settings.hero_title_line1 = "Від дизайну"
        settings.hero_title_emphasis = "до ключів."
        settings.hero_title_line2 = "Заходь і живи."
        settings.hero_subline = "Дизайн · Ремонт · Оздоблення · Комплектація"
        settings.hero_cta_primary_text = "Дивитись проєкти"
        settings.hero_cta_primary_href = "#проєкти"
        settings.hero_cta_secondary_text = "Про процес"
        settings.hero_cta_secondary_href = "#процес"
        settings.hero_floorplan_caption = "Технічне креслення · Масштаб 1:25"
        settings.hero_scroll_hint = "Гортати"
        settings.hero_founded_prefix = "Заснована"
        settings.hero_background_image_url = HERO_BACKGROUND_DEFAULT

        settings.phone = "+38 (044) 555 12 34"
        settings.email = "studio@forma.ua"
        settings.telegram = "@forma_studio"
        settings.whatsapp = "+38 (050) 555 12 34"
        settings.address = "Дніпро · працюємо по всій Україні"
        settings.instagram_url = "https://instagram.com/forma_studio"
        settings.telegram_url = "https://t.me/forma_studio"
        settings.whatsapp_url = ""
        settings.contact_label_whatsapp = "WhatsApp"
        settings.contact_label_instagram = "Instagram"

        settings.seo_title = "Дизайн і ремонт під ключ у Дніпрі | ProProstir"
        settings.seo_description = (
            "ProProstir — повний цикл від дизайну інтер'єру до «заходь і живи». "
            "База в Дніпрі, працюємо також по інших містах України. "
            "Редизайн квартир і будинків, оздоблення, меблі, монтаж."
        )
        settings.seo_keywords = (
            "ремонт під ключ Дніпро, дизайн інтер'єру, редизайн квартири, "
            "ремонт будинку, кахель, гіпсокартон, стелі, "
            "меблі на замовлення, ProProstir"
        )
        settings.seo_author = "ProProstir"
        settings.seo_canonical_path = "/"
        settings.seo_robots = "noindex, nofollow"
        settings.seo_html_lang = "uk"
        settings.seo_locale = "uk_UA"
        settings.seo_geo_region = "UA-12"
        settings.seo_geo_placename = "Дніпро"
        settings.og_title = "ProProstir — Ми знаємо про простір все"
        settings.og_description = (
            "Повний цикл: дизайн, ремонт, оздоблення й комплектація. "
            "Ви ділитеся баченням комфорту — ми втілюємо його до ключів."
        )
        settings.og_type = "website"
        settings.og_image_url = ""
        settings.og_image_alt = (
            "ProProstir: від дизайну інтер'єру до готового простору"
        )
        settings.twitter_card = "summary_large_image"
        settings.jsonld_name = "ProProstir"
        settings.jsonld_type = "HomeAndConstructionBusiness"
        settings.jsonld_description = (
            "ProProstir — повний цикл від дизайну до здачі. "
            "База в Дніпрі, виїжджаємо в інші міста України."
        )
        settings.jsonld_city = "Дніпро"
        settings.jsonld_country = "UA"
        settings.jsonld_street = "Дніпро"
        settings.jsonld_area_served = "Дніпро та інші міста України"
        settings.jsonld_opening_hours = "Mo-Fr 10:00-18:00"
        settings.jsonld_price_range = "$$$"
        settings.jsonld_services = (
            "Дизайн інтер'єру\nРемонт під ключ\nРедизайн квартир і будинків\n"
            "Кахель і оздоблення\nГіпсокартон і стелі\nМеблі та комплектація\nМонтаж"
        )

        settings.stats_projects = "147"
        settings.stats_years = "08"
        settings.stats_masters = "24"
        settings.stats_production = "100%"

        settings.workshop_quote = (
            "Довірте нам своє бачення комфорту. Від найкращого дизайнера "
            "до кахлю, гіпсу, стель і збірки меблів — ми втілимо його так, "
            "щоб ви просто зайшли і жили."
        )
        settings.workshop_author = "Команда ProProstir"
        settings.workshop_text = (
            "Ми ведемо весь цикл: слухаємо ваше бачення, проєктуємо інтер'єр "
            "і реалізуємо його на об'єкті. База в Дніпрі — виїжджаємо в інші міста. "
            "Нові квартири й будинки, перепроєктування старих просторів, "
            "оздоблення та комплектація — одна команда відповідає від ескізу до ключів."
        )

        settings.detail_eyebrow_prefix = "Проєкт у деталях"
        settings.detail_section_title = "Від ескізу до здачі"
        settings.detail_number_prefix = "Проєкт №"
        settings.detail_cta_text = "Схожий проєкт →"
        settings.detail_cta_href = "#контакти"
        settings.meta_label_area = "Площа"
        settings.meta_label_materials = "Матеріали"
        settings.meta_label_duration = "Тривалість"
        settings.meta_label_year = "Рік"
        settings.meta_label_location = "Локація"

        settings.drawing_eyebrow = "Від ескізу до реальності"
        settings.drawing_title = "Бачення, що стає домом"
        settings.drawing_body = (
            "Прокрутіть — побачите, як креслення й ескіз перетворюються "
            "на простір, у який можна зайти і жити"
        )
        settings.drawing_phase_1_label = "Креслення"
        settings.drawing_phase_2_label = "Ескіз"
        settings.drawing_phase_3_label = "Результат"
        settings.drawing_result_alt = "Готовий інтер'єр"
        settings.drawing_sketch_image_url = ""

        settings.ba_eyebrow = "Редизайн і нове життя"
        settings.ba_title = "До і після"
        settings.ba_hint = "Перетягніть повзунок"
        settings.ba_label_before = "ДО"
        settings.ba_label_after = "ПІСЛЯ"
        settings.before_image_url = IMG["before"]
        settings.after_image_url = IMG["after"]
        settings.before_image = None
        settings.after_image = None

        settings.contact_eyebrow = "Зв'язатися"
        settings.contact_title_line1 = "Розкажіть"
        settings.contact_title_line2 = "про своє"
        settings.contact_title_emphasis = "бачення."
        settings.contact_intro = (
            "Надішліть план, фото «до» або просто слова про комфорт, "
            "який хочете відчути вдома — у Дніпрі чи в іншому місті. "
            "Зв'яжемося протягом одного робочого дня."
        )
        settings.contact_room_heading = "Тип об'єкта"
        settings.contact_message_placeholder = "Опишіть своє бачення комфорту…"
        settings.contact_name_placeholder = "Ім'я"
        settings.contact_phone_placeholder = "Телефон"
        settings.contact_email_placeholder = "Email"
        settings.contact_telegram_placeholder = "Telegram"
        settings.contact_submit_text = "Надіслати запит →"
        settings.contact_submit_loading = "Надсилаємо…"
        settings.contact_success_eyebrow = "Надіслано"
        settings.contact_success_title = "Дякуємо, ми отримали ваш запит."
        settings.contact_success_body = (
            "Зв'яжемося протягом одного робочого дня, щоб зрозуміти ваше бачення і шлях до нього."
        )
        settings.contact_validation_message = "Будь ласка, вкажіть ім'я та телефон."
        settings.contact_label_address = "Адреса"
        settings.contact_label_phone = "Телефон"
        settings.contact_label_email = "Email"
        settings.contact_label_telegram = "Telegram"

        settings.footer_services_heading = "Послуги"
        settings.footer_studio_heading = "Студія"
        settings.footer_contacts_heading = "Контакти"
        settings.footer_copyright_suffix = "Всі права захищено"
        settings.footer_location_tagline = "Дніпро · працюємо по всій Україні"
        settings.save()
        return settings

    def _seed_hero_stats(self):
        HeroStat.objects.all().delete()
        HeroStat.objects.bulk_create(
            [
                HeroStat(value="147", label="Виконаних проєктів", order=1),
                HeroStat(value="08", label="Років досвіду", order=2),
                HeroStat(value="24", label="Майстри в команді", order=3),
                HeroStat(value="100%", label="Повний цикл", order=4),
            ]
        )

    def _seed_sections(self):
        PageSection.objects.all().delete()
        PageSection.objects.bulk_create(
            [
                PageSection(
                    key="projects",
                    section_id="проєкти",
                    eyebrow="Вибрані роботи",
                    title="Кожен простір —",
                    title_emphasis="окрема історія.",
                    cta_text="Всі проєкти →",
                    cta_href="#проєкти",
                    order=1,
                ),
                PageSection(
                    key="photography",
                    section_id="фотографія",
                    eyebrow="Деталі реалізації",
                    title="Кожен шар —",
                    title_emphasis="своя майстерність.",
                    subtitle=(
                        "Дизайн, оздоблення, столярка й фініш — "
                        "одна команда веде простір до ключів."
                    ),
                    order=2,
                ),
                PageSection(
                    key="materials",
                    section_id="матеріали",
                    eyebrow="Матеріали простору",
                    title="Те, з чого",
                    title_emphasis="народжується дім",
                    subtitle=(
                        "Від дерева й каменю до кахлю, скла та металу — "
                        "обираємо те, що витримає життя."
                    ),
                    order=3,
                ),
                PageSection(
                    key="process",
                    section_id="процес",
                    eyebrow="Процес",
                    title="Як це відбувається",
                    order=4,
                ),
                PageSection(
                    key="workshop",
                    section_id="майстерня",
                    eyebrow="Команда",
                    order=5,
                ),
                PageSection(
                    key="drawing",
                    section_id="креслення",
                    eyebrow="Від ескізу до реальності",
                    title="Бачення, що стає домом",
                    subtitle=(
                        "Прокрутіть — побачите, як креслення й ескіз "
                        "перетворюються на простір, у який можна зайти і жити"
                    ),
                    order=6,
                ),
                PageSection(
                    key="before_after",
                    section_id="до-після",
                    eyebrow="Редизайн і нове життя",
                    title="До і після",
                    subtitle="Перетягніть повзунок",
                    order=7,
                ),
                PageSection(
                    key="contact",
                    section_id="контакти",
                    eyebrow="Зв'язатися",
                    title="Розкажіть",
                    title_line2="про своє",
                    title_emphasis="бачення.",
                    subtitle=(
                        "Надішліть план, фото «до» або просто слова про комфорт, "
                        "який хочете відчути вдома — у Дніпрі чи в іншому місті. "
                        "Зв'яжемося протягом одного робочого дня."
                    ),
                    order=8,
                ),
            ]
        )

    def _seed_nav(self):
        NavItem.objects.all().delete()
        NavItem.objects.bulk_create(
            [
                NavItem(
                    label="Проєкти",
                    href="#проєкти",
                    location=NavItem.LOCATION_HEADER,
                    order=1,
                ),
                NavItem(
                    label="Процес",
                    href="#процес",
                    location=NavItem.LOCATION_HEADER,
                    order=2,
                ),
                NavItem(
                    label="Про нас",
                    href="#майстерня",
                    location=NavItem.LOCATION_HEADER,
                    order=3,
                ),
                NavItem(
                    label="Контакти",
                    href="#контакти",
                    location=NavItem.LOCATION_HEADER,
                    order=4,
                ),
                NavItem(
                    label="Дизайн інтер'єру",
                    href="#процес",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=1,
                ),
                NavItem(
                    label="Ремонт і редизайн",
                    href="#до-після",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=2,
                ),
                NavItem(
                    label="Оздоблення",
                    href="#матеріали",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=3,
                ),
                NavItem(
                    label="Меблі та комплектація",
                    href="#проєкти",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=4,
                ),
                NavItem(
                    label="Про нас",
                    href="#майстерня",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=1,
                ),
                NavItem(
                    label="Команда",
                    href="#майстерня",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=2,
                ),
                NavItem(
                    label="Процес",
                    href="#процес",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=3,
                ),
                NavItem(
                    label="Проєкти",
                    href="#проєкти",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=4,
                ),
            ]
        )

    def _seed_room_types(self):
        RoomType.objects.all().delete()
        RoomType.objects.bulk_create(
            [
                RoomType(value="apartment", label="Квартира", order=1),
                RoomType(value="house", label="Будинок", order=2),
                RoomType(value="redesign", label="Редизайн", order=3),
                RoomType(value="newbuild", label="Нове житло", order=4),
                RoomType(value="other", label="Інше", order=5),
            ]
        )

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
                    "Ніжки та ручки — матова сталь. Стільниця — мармур Calacatta.\n\n"
                    "Процес почався з обмірів і технічного креслення, далі — 3D-модель, "
                    "виготовлення в майстерні та фінальний монтаж на об'єкті. "
                    "Кожна деталь пройшла контроль якості одним майстром."
                ),
                "materials_label": "ДУБ · КАМІНЬ · 2026",
                "category": "Кухня",
                "year": 2026,
                "area": "18 м²",
                "duration": "11 тижнів",
                "location": "Приватний будинок · Дніпро",
                "image_url": IMG["kitchen"],
                "detail_image_url": IMG["install"],
                "video_poster_url": IMG["kitchen"],
                "short_description": (
                    "L-подібне планування, острів з кам'яною стільницею "
                    "та інтегрована система зберігання."
                ),
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": True,
                "order": 1,
                "seo_title": "Кухня з натурального дуба на замовлення | ProProstir",
                "seo_description": (
                    "Острівна кухня з масиву дуба та мармуру Calacatta. "
                    "Проєктування, виробництво та монтаж у Дніпрі та інших містах."
                ),
                "seo_keywords": "кухня на замовлення, дуб, мармур Calacatta, Дніпро",
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
        self._seed_gallery(
            kitchen,
            [
                (IMG["kitchen"], "Готова кухня", 1),
                (IMG["idea"], "Ескіз / ідея", 2),
                (IMG["model_3d"], "3D-модель", 3),
                (IMG["production"], "Виготовлення", 4),
                (IMG["install"], "Монтаж", 5),
                (IMG["after"], "Деталі фінішу", 6),
            ],
        )

        library, _ = Project.objects.update_or_create(
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
                    "з виразним малюнком волокна. Ніжки та ручки — матова сталь.\n\n"
                    "Проєкт поєднує робочу зону кабінету та бібліотеку в єдину "
                    "архітектурну композицію під геометрію кімнати."
                ),
                "materials_label": "ГОРІХ · МЕТАЛ · 2025",
                "category": "Кабінет",
                "year": 2025,
                "area": "22 м²",
                "duration": "9 тижнів",
                "location": "Квартира · Дніпро",
                "image_url": IMG["library"],
                "detail_image_url": IMG["library"],
                "video_poster_url": IMG["library"],
                "short_description": (
                    "Вбудована бібліотека по всій висоті. Ніжки та ручки — матова сталь."
                ),
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 2,
                "seo_title": "Бібліотека і кабінет з горіха | ProProstir",
                "seo_description": (
                    "Вбудована бібліотека по всій висоті. Ніжки та ручки — матова сталь."
                ),
                "seo_keywords": "бібліотека на замовлення, кабінет, горіх, Дніпро",
            },
        )
        self._seed_gallery(
            library,
            [
                (IMG["library"], "Бібліотека", 1),
                (IMG["metal"], "Металеві деталі", 2),
                (IMG["walnut"], "Текстура горіха", 3),
                (IMG["craft_2"], "Ручна обробка", 4),
            ],
        )

        wardrobe, _ = Project.objects.update_or_create(
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
                "location": "Приватний будинок · Дніпро",
                "image_url": IMG["wardrobe"],
                "detail_image_url": IMG["wardrobe"],
                "video_poster_url": IMG["wardrobe"],
                "short_description": "Гардеробна система зі шпону ясена та матовим склом.",
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 3,
                "seo_title": "Гардеробна зі шпону | ProProstir",
                "seo_description": (
                    "Гардеробна система зі шпону ясена та матовим склом."
                ),
                "seo_keywords": "гардеробна на замовлення, шпон, скло, Дніпро",
            },
        )
        self._seed_gallery(
            wardrobe,
            [
                (IMG["wardrobe"], "Гардеробна", 1),
                (IMG["veneer"], "Шпон", 2),
                (IMG["glass"], "Скло", 3),
            ],
        )

        living, _ = Project.objects.update_or_create(
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
                "location": "Квартира · Дніпро",
                "image_url": IMG["living"],
                "detail_image_url": IMG["living"],
                "video_poster_url": IMG["living"],
                "short_description": "Тихі форми, натуральний дуб і льон.",
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 4,
                "seo_title": "Вітальня Wabi-Sabi | ProProstir",
                "seo_description": "Тихі форми, натуральний дуб і льон.",
                "seo_keywords": "вітальня на замовлення, wabi-sabi, дуб, Дніпро",
            },
        )
        self._seed_gallery(
            living,
            [
                (IMG["living"], "Вітальня", 1),
                (IMG["oak"], "Дуб", 2),
                (IMG["before"], "До", 3),
                (IMG["after"], "Після", 4),
            ],
        )
        return kitchen

    def _seed_gallery(self, project, items):
        project.gallery.all().delete()
        ProjectImage.objects.bulk_create(
            [
                ProjectImage(
                    project=project,
                    image_url=url,
                    caption=caption,
                    order=order,
                    is_published=True,
                )
                for url, caption, order in items
            ]
        )

    def _seed_materials(self):
        materials = [
            {
                "name_uk": "Дуб",
                "name_en": "OAK",
                "description": (
                    "Масив і столярка: кухні, шафи, панелі. "
                    "Теплий на дотик, зносостійкий."
                ),
                "image_url": IMG["oak"],
                "order": 1,
            },
            {
                "name_uk": "Горіх",
                "name_en": "WALNUT",
                "description": (
                    "Темна деревина з виразним малюнком волокна. "
                    "Для кабінетів, бібліотек і теплих зон дому."
                ),
                "image_url": IMG["walnut"],
                "order": 2,
            },
            {
                "name_uk": "Шпон",
                "name_en": "VENEER",
                "description": (
                    "Фасади, панелі, двері. Рівна текстура й широка палітра "
                    "під будь-який інтер'єр."
                ),
                "image_url": IMG["veneer"],
                "order": 3,
            },
            {
                "name_uk": "Камінь",
                "name_en": "STONE",
                "description": (
                    "Камінь, кераміка, кахель. Підлоги, стіни, стільниці — "
                    "матеріал, який тримає щодень."
                ),
                "image_url": IMG["stone"],
                "order": 4,
            },
            {
                "name_uk": "Метал",
                "name_en": "METAL",
                "description": (
                    "Профілі, фурнітура, деталі світла. "
                    "Точність, яка збирає простір докупи."
                ),
                "image_url": IMG["metal"],
                "order": 5,
            },
            {
                "name_uk": "Скло",
                "name_en": "GLASS",
                "description": (
                    "Перегородки, фасади, душові. Світло проходить — простір дихає."
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
                "title": "Бачення",
                "description": (
                    "Ви ділитеся тим, як хочете жити. "
                    "Ми слухаємо без поспіху, ставимо питання "
                    "і беремо на себе відповідальність за довіру."
                ),
                "duration": "1–2 дні",
                "image_url": IMG["idea"],
                "order": 1,
            },
            {
                "title": "Обміри",
                "description": (
                    "Виїзд на квартиру чи будинок: обміри, фото, "
                    "аудит старих планувань і прихованих нюансів."
                ),
                "duration": "1 день",
                "image_url": IMG["measures"],
                "order": 2,
            },
            {
                "title": "Дизайн",
                "description": (
                    "Дизайнер розгортає ваше бачення в планування, 3D і матеріали — "
                    "так, щоб комфорт було видно ще до ремонту."
                ),
                "duration": "1–3 тижні",
                "image_url": IMG["model_3d"],
                "order": 3,
            },
            {
                "title": "Реалізація",
                "description": (
                    "Гіпс, стелі, кахель, електрика, столярка, збірка меблів — "
                    "усе, що потрібно, щоб простір став готовим."
                ),
                "duration": "за проєктом",
                "image_url": IMG["production"],
                "order": 4,
            },
            {
                "title": "Здача",
                "description": (
                    "Фінішне прибирання, перевірка кожної зони, "
                    "ключі у ваших руках. Заходьте і живіть."
                ),
                "duration": "1–3 дні",
                "image_url": IMG["install"],
                "order": 5,
            },
            {
                "title": "Життя",
                "description": (
                    "Простір працює щодня. Гарантія на роботи й підтримка, "
                    "якщо щось потрібно підкрутити."
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
            ("Огляд приміщення", IMG["craft_1"], 1),
            ("Креслення", IMG["craft_2"], 2),
            ("Ремонт", IMG["craft_3"], 3),
            ("Збірка меблів", IMG["craft_4"], 4),
        ]
        for title, image_url, order in details:
            CraftDetail.objects.update_or_create(
                order=order,
                defaults={
                    "title": title,
                    "image_url": image_url,
                    "is_published": True,
                },
            )

    def _seed_workshop(self):
        stats = [
            ("Повний цикл", "Від дизайну до здачі", 1),
            ("Одна команда", "Дизайнери та майстри", 2),
            ("Квартири й будинки", "Нове та редизайн", 3),
            ("5 років", "Гарантія на роботи", 4),
        ]
        for value, label, order in stats:
            WorkshopStat.objects.update_or_create(
                order=order,
                defaults={"value": value, "label": label},
            )

        images = [
            ("Робота на об'єкті", IMG["workshop_1"], 1),
            ("Деталі оздоблення", IMG["workshop_2"], 2),
            ("Столярка на об'єкті", IMG["workshop_3"], 3),
        ]
        for title, image_url, order in images:
            WorkshopImage.objects.update_or_create(
                order=order,
                defaults={"title": title, "image_url": image_url},
            )

    def _seed_hero_scene(self):
        scene, _ = HeroScene.objects.update_or_create(
            title="Вітальня",
            defaults={
                "image_url": (
                    "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6"
                    "?w=2000&h=1400&fit=crop&auto=format"
                ),
                "hint": (
                    "Наведіть курсор — дізнайтеся, які роботи ми пропонуємо "
                    "для кожної зони простору."
                ),
                "idle_eyebrow": "Зона простору",
                "idle_title": "Оберіть деталь інтер'єру",
                "idle_body": (
                    "Стеля, стіни, стелаж, м’які меблі, вікно чи підлога — наведіть "
                    "на елемент і побачите, що саме ми реалізуємо."
                ),
                "is_active": True,
                "is_published": True,
                "order": 1,
            },
        )
        zones = [
            ("Стеля", "Трекове світло та натяжні системи", "Гіпсокартон · LED · натяг", "Стелі", 0, 0, 100, 16, 1),
            ("Підлога", "Паркет, плитка, кахель", "Дуб · кераміка · камінь", "Підлога", 0, 82, 100, 18, 2),
            ("Ліва стіна", "Оздоблення стін", "Штукатурка · фарба · панелі", "Стіни", 0, 12, 18, 70, 3),
            ("Двері", "Столярка та приховані двері", "Шпон · прихована коробка · фурнітура", "Столярка", 5, 12, 11, 68, 4),
            ("Стелаж", "Корпусні меблі на замовлення", "Шпон · фасади · LED-підсвіт", "Меблі", 22, 8, 36, 52, 5),
            ("Диван", "М'які меблі під простір", "Тканина · наповнення · текстиль", "Меблі", 19, 52, 25, 36, 6),
            ("Журнальний стіл", "Предмети з каменю, металу, скла", "Метал · камінь · скло", "Меблі", 39, 66, 15, 22, 7),
            ("Крісло", "М'які меблі під простір", "Тканина · каркас · наповнення", "Меблі", 54, 50, 11, 28, 8),
            ("Вікно", "Віконна зона, штори та підвіконня", "Штори · римські · підвіконня", "Вікна", 65, 8, 20, 70, 9),
            ("Права стіна", "Рейкові панелі та акцентне світло", "Рейки · шпон · бра", "Стіни", 84, 0, 16, 100, 10),
            ("Декор", "Аксесуари, рослини та світло", "Вази · текстиль · бра", "Декор", 78, 38, 14, 42, 11),
        ]
        scene.zones.all().delete()
        HeroZone.objects.bulk_create(
            [
                HeroZone(
                    scene=scene,
                    name=name,
                    service=service,
                    materials=materials,
                    tag=tag,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    order=order,
                    is_published=True,
                )
                for name, service, materials, tag, x, y, width, height, order in zones
            ]
        )
