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
    WorkCategory,
    WorkItem,
    WorkItemImage,
    WorkshopImage,
    WorkshopStat,
)
from catalog.work_gallery import create_work_gallery

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
        "https://images.unsplash.com/photo-1761105439888-86c6e50d7af8"
        "?w=400&h=560&fit=crop&auto=format"
    ),
    "glass": (
        "https://images.unsplash.com/photo-1497366216548-37526070297c"
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
    "before": "/works/before/before-walnut-kitchen.jpg",
    "after": "/works/2024-10-08-a.jpg",
    "walnut_kitchen": "/works/2024-10-08-a.jpg",
    "white_kitchen": "/works/2026-06-29.jpg",
    "tv_stand": "/works/2024-10-08-b.jpg",
    "wardrobe_real": "/works/2024-09-07.jpg",
}


class Command(BaseCommand):
    help = "Seed catalog content for ProProstir."

    def handle(self, *args, **options):
        settings = self._seed_settings()
        self._seed_hero_stats()
        self._seed_sections()
        self._seed_nav()
        self._seed_room_types()
        self._seed_works()
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
        settings.tagline = "Меблі будь-якої складності"
        settings.founded_year = 2018

        settings.header_logo_primary = "ProProstir"
        settings.header_logo_secondary = "Меблі будь-якої складності"
        settings.header_cta_text = "Замовити прорахунок"
        settings.header_cta_href = "#contacts"

        settings.hero_eyebrow = "Меблі на замовлення · Дніпро"
        settings.hero_title_line1 = "Меблі"
        settings.hero_title_emphasis = "будь-якої"
        settings.hero_title_line2 = "складності."
        settings.hero_subline = "Прорахунок · Замовлення · Збірка"
        settings.hero_cta_primary_text = "Замовити прорахунок"
        settings.hero_cta_primary_href = "#contacts"
        settings.hero_cta_secondary_text = "Дивитись проєкти"
        settings.hero_cta_secondary_href = "#projects"
        settings.hero_floorplan_caption = "Технічне креслення · Масштаб 1:25"
        settings.hero_scroll_hint = "Гортати"
        settings.hero_founded_prefix = "Заснована"
        settings.hero_background_image_url = HERO_BACKGROUND_DEFAULT

        settings.phone = "+38 (097) 208 00 74"
        settings.email = "proprostirua@gmail.com"
        settings.telegram = ""
        settings.whatsapp = "+38 (097) 208 00 74"
        settings.address = "Дніпро · працюємо по всій Україні"
        settings.instagram_url = ""
        settings.telegram_url = ""
        settings.whatsapp_url = ""
        settings.contact_label_whatsapp = "WhatsApp"
        settings.contact_label_instagram = "Instagram"

        settings.seo_title = "Кухні та меблі на замовлення в Дніпрі | ProProstir"
        settings.seo_description = (
            "Кухні, шафи та гардеробні на замовлення в Дніпрі. Якісні корпусні "
            "меблі будь-якої складності: прорахунок, замовлення і збірка на місці. "
            "Тел. 097 208 00 74."
        )
        settings.seo_keywords = (
            "меблі на замовлення Дніпро, кухні на замовлення Дніпро, "
            "кухня на замовлення, шафи на замовлення Дніпро, шафа-купе на замовлення, "
            "гардеробна на замовлення Дніпро, корпусні меблі Дніпро, "
            "вбудовані меблі Дніпро, кухонні меблі на замовлення, якісні меблі Дніпро, "
            "індивідуальні меблі, нестандартні меблі Дніпро, прорахунок меблів, "
            "прорахунок кухні Дніпро, замовлення меблів Дніпро, збірка меблів Дніпро, "
            "меблевий майстер Дніпро, меблі з МДФ, меблі будь-якої складності, "
            "тумба під телевізор на замовлення, ProProstir"
        )
        settings.seo_author = "ProProstir"
        settings.seo_canonical_path = "/"
        settings.seo_robots = "index, follow"
        settings.seo_html_lang = "uk"
        settings.seo_locale = "uk_UA"
        settings.seo_geo_region = "UA-12"
        settings.seo_geo_placename = "Дніпро"
        settings.og_title = "Якісні меблі на замовлення в Дніпрі — ProProstir"
        settings.og_description = (
            "Прорахую вартість, замовлю виготовлення і зберу кухню, шафу чи "
            "гардеробну в Дніпрі. Якісні меблі будь-якої складності — "
            "від кошторису до встановлення."
        )
        settings.og_type = "website"
        settings.og_image_url = "https://proprostir.com.ua/works/2024-10-08-a.jpg"
        settings.og_image_alt = (
            "Кухня на замовлення в Дніпрі: горіх, білі фасади, "
            "кам'яна стільниця і вітрина — ProProstir"
        )
        settings.twitter_card = "summary_large_image"
        settings.twitter_title = "Кухні, шафи і гардеробні на замовлення в Дніпрі"
        settings.twitter_description = (
            "Якісні меблі будь-якої складності в Дніпрі: прорахунок, "
            "замовлення виготовлення і збірка на місці. ProProstir."
        )
        settings.jsonld_name = "ProProstir"
        settings.jsonld_type = "FurnitureStore"
        settings.jsonld_description = (
            "ProProstir: кухні, шафи, гардеробні та корпусні меблі на замовлення "
            "в Дніпрі. Прорахунок вартості, замовлення виготовлення і збірка на місці. "
            "Виїзд по місту та в інші міста України."
        )
        settings.jsonld_city = "Дніпро"
        settings.jsonld_country = "UA"
        settings.jsonld_street = ""
        settings.jsonld_area_served = (
            "Дніпро, Кам'янське, Новомосковськ, Павлоград та інші міста України"
        )
        settings.jsonld_opening_hours = "Mo-Fr 10:00-18:00"
        settings.jsonld_price_range = "$$"
        settings.jsonld_latitude = "48.4647"
        settings.jsonld_longitude = "35.0462"
        settings.jsonld_services = (
            "Кухні на замовлення в Дніпрі\n"
            "Шафи та шафи-купе на замовлення\n"
            "Гардеробні на замовлення\n"
            "Корпусні меблі на замовлення\n"
            "Вбудовані меблі\n"
            "Нестандартні меблі будь-якої складності\n"
            "Прорахунок вартості меблів\n"
            "Замовлення виготовлення меблів\n"
            "Збірка та встановлення меблів\n"
            "Меблі для вітальні та кабінету"
        )

        settings.stats_projects = "147"
        settings.stats_years = "08"
        settings.stats_masters = ""
        settings.stats_production = ""

        settings.workshop_quote = (
            "Прораховую меблі будь-якої складності, замовляю виготовлення "
            "і збираю на місці — від кухні до вбудованої бібліотеки."
        )
        settings.workshop_author = "ProProstir"
        settings.workshop_text = (
            "Один фахівець веде замовлення від обміру до готових меблів. "
            "Спочатку точний прорахунок: матеріали, фурнітура, терміни і вартість. "
            "Потім замовлення виготовлення і комплектуючих. Далі збірка на об'єкті. "
            "Кухні, шафи, гардеробні, кабінети і нестандартні вбудови — "
            "у Дніпрі та інших містах України."
        )

        settings.detail_eyebrow_prefix = "Проєкт у деталях"
        settings.detail_section_title = "Від прорахунку до збірки"
        settings.detail_number_prefix = "Проєкт №"
        settings.detail_cta_text = "Схожий проєкт →"
        settings.detail_cta_href = "#contacts"
        settings.meta_label_area = "Площа"
        settings.meta_label_materials = "Матеріали"
        settings.meta_label_duration = "Тривалість"
        settings.meta_label_year = "Рік"
        settings.meta_label_location = "Локація"

        settings.drawing_eyebrow = "Від креслення до меблів"
        settings.drawing_title = "Прорахунок, що стає меблями"
        settings.drawing_body = (
            "Прокрутіть — побачите, як креслення і кошторис "
            "перетворюються на зібрані меблі"
        )
        settings.drawing_phase_1_label = "Креслення"
        settings.drawing_phase_2_label = "Прорахунок"
        settings.drawing_phase_3_label = "Збірка"
        settings.drawing_result_alt = "Зібрані меблі"
        settings.drawing_sketch_image_url = ""

        settings.ba_eyebrow = "Місце і готові меблі"
        settings.ba_title = "До і після збірки"
        settings.ba_hint = "Оберіть роботу і перетягніть повзунок"
        settings.ba_label_before = "ДО"
        settings.ba_label_after = "ПІСЛЯ"
        settings.before_image_url = IMG["before"]
        settings.after_image_url = IMG["after"]
        settings.before_image = None
        settings.after_image = None

        settings.contact_eyebrow = "Зв'язатися"
        settings.contact_title_line1 = "Розкажіть"
        settings.contact_title_line2 = "які меблі"
        settings.contact_title_emphasis = "потрібні."
        settings.contact_intro = (
            "Надішліть розміри, ескіз або фото ніші — у Дніпрі чи в іншому місті. "
            "Прорахую вартість і напишу, що замовляємо і як збираємо. "
            "Відповідь протягом одного робочого дня."
        )
        settings.contact_room_heading = "Які меблі"
        settings.contact_message_placeholder = "Опишіть меблі: кухня, шафа, нестандарт…"
        settings.contact_name_placeholder = "Ім'я"
        settings.contact_phone_placeholder = "Телефон"
        settings.contact_email_placeholder = "Email"
        settings.contact_telegram_placeholder = "Telegram"
        settings.contact_submit_text = "Надіслати запит →"
        settings.contact_submit_loading = "Надсилаємо…"
        settings.contact_success_eyebrow = "Надіслано"
        settings.contact_success_title = "Дякуємо, ми отримали ваш запит."
        settings.contact_success_body = (
            "Зв'яжуся протягом одного робочого дня, щоб уточнити розміри і підготувати прорахунок."
        )
        settings.contact_validation_message = "Будь ласка, вкажіть ім'я та телефон."
        settings.contact_label_address = "Адреса"
        settings.contact_label_phone = "Телефон"
        settings.contact_label_email = "Email"
        settings.contact_label_telegram = "Telegram"

        settings.footer_services_heading = "Послуги"
        settings.footer_studio_heading = "Майстерня"
        settings.footer_contacts_heading = "Контакти"
        settings.footer_copyright_suffix = "Всі права захищено"
        settings.footer_location_tagline = "Дніпро · працюємо по всій Україні"
        settings.save()
        return settings

    def _seed_hero_stats(self):
        HeroStat.objects.all().delete()
        HeroStat.objects.bulk_create(
            [
                HeroStat(value="147", label="Зібраних замовлень", order=1),
                HeroStat(value="8", label="Років досвіду", order=2),
            ]
        )

    def _seed_sections(self):
        PageSection.objects.all().delete()
        PageSection.objects.bulk_create(
            [
                PageSection(
                    key="projects",
                    section_id="projects",
                    eyebrow="Майстерність",
                    title="Збірка",
                    title_emphasis="зблизька.",
                    subtitle=(
                        "Наведіть на фото — побачите руку збирача: "
                        "зазори фасадів, фурнітуру і підгонку до стіни."
                    ),
                    cta_text="",
                    cta_href="",
                    order=1,
                ),
                PageSection(
                    key="gallery",
                    section_id="gallery",
                    eyebrow="Галерея робіт",
                    title="Різні варіанти —",
                    title_emphasis="під вашу кімнату.",
                    subtitle=(
                        "Оберіть тип меблів і відкрийте картку: "
                        "кілька фото і те, чим цей варіант відрізняється."
                    ),
                    order=2,
                ),
                PageSection(
                    key="photography",
                    section_id="photography",
                    eyebrow="Деталі збірки",
                    title="Кожна деталь —",
                    title_emphasis="своя точність.",
                    subtitle=(
                        "Прорахунок, замовлення і збірка — "
                        "меблі доводяться до місця одним фахівцем."
                    ),
                    order=2,
                ),
                PageSection(
                    key="materials",
                    section_id="materials",
                    eyebrow="Матеріали меблів",
                    title="Те, з чого",
                    title_emphasis="збираються меблі",
                    subtitle=(
                        "Дерево, шпон, камінь, метал і скло — "
                        "підбираю під завдання і закладаю в прорахунок."
                    ),
                    order=3,
                ),
                PageSection(
                    key="process",
                    section_id="process",
                    eyebrow="Процес",
                    title="Як це відбувається",
                    order=4,
                ),
                PageSection(
                    key="workshop",
                    section_id="workshop",
                    eyebrow="Майстер",
                    order=5,
                ),
                PageSection(
                    key="drawing",
                    section_id="drawing",
                    eyebrow="Від креслення до меблів",
                    title="Прорахунок, що стає меблями",
                    subtitle=(
                        "Прокрутіть — побачите, як креслення і кошторис "
                        "перетворюються на зібрані меблі"
                    ),
                    order=6,
                ),
                PageSection(
                    key="before_after",
                    section_id="before-after",
                    eyebrow="Місце і готові меблі",
                    title="До і після збірки",
                    subtitle="Оберіть роботу і перетягніть повзунок",
                    order=7,
                ),
                PageSection(
                    key="contact",
                    section_id="contacts",
                    eyebrow="Зв'язатися",
                    title="Розкажіть",
                    title_line2="які меблі",
                    title_emphasis="потрібні.",
                    subtitle=(
                        "Надішліть розміри, ескіз або фото ніші — у Дніпрі чи в іншому місті. "
                        "Прорахую вартість і напишу, що замовляємо і як збираємо. "
                        "Відповідь протягом одного робочого дня."
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
                    href="#projects",
                    location=NavItem.LOCATION_HEADER,
                    order=1,
                ),
                NavItem(
                    label="Галерея",
                    href="/works",
                    location=NavItem.LOCATION_HEADER,
                    order=2,
                ),
                NavItem(
                    label="Процес",
                    href="#process",
                    location=NavItem.LOCATION_HEADER,
                    order=3,
                ),
                NavItem(
                    label="Про роботу",
                    href="#workshop",
                    location=NavItem.LOCATION_HEADER,
                    order=4,
                ),
                NavItem(
                    label="Контакти",
                    href="#contacts",
                    location=NavItem.LOCATION_HEADER,
                    order=5,
                ),
                NavItem(
                    label="Прорахунок",
                    href="#process",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=1,
                ),
                NavItem(
                    label="Замовлення",
                    href="#process",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=2,
                ),
                NavItem(
                    label="Збірка",
                    href="#projects",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=3,
                ),
                NavItem(
                    label="Меблі будь-якої складності",
                    href="#projects",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=4,
                ),
                NavItem(
                    label="Про роботу",
                    href="#workshop",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=1,
                ),
                NavItem(
                    label="Матеріали",
                    href="#materials",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=2,
                ),
                NavItem(
                    label="Процес",
                    href="#process",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=3,
                ),
                NavItem(
                    label="Проєкти",
                    href="#projects",
                    location=NavItem.LOCATION_FOOTER_STUDIO,
                    order=4,
                ),
            ]
        )

    def _seed_room_types(self):
        RoomType.objects.all().delete()
        RoomType.objects.bulk_create(
            [
                RoomType(value="kitchen", label="Кухня", order=1),
                RoomType(value="wardrobe", label="Шафа або гардеробна", order=2),
                RoomType(value="living", label="Вітальня", order=3),
                RoomType(value="office", label="Кабінет", order=4),
                RoomType(value="other", label="Інше", order=5),
            ]
        )

    def _seed_works(self):
        WorkCategory.objects.all().delete()
        create_work_gallery(WorkCategory, WorkItem, WorkItemImage)

    def _seed_projects(self):
        Project.objects.all().delete()
        kitchen, _ = Project.objects.update_or_create(
            slug="kuhnya-z-horikha",
            defaults={
                "title": "Кухня з горіха та каменю",
                "subtitle": (
                    "Кутова кухня: горіх, білі фасади, темний камінь і відкрита вітрина."
                ),
                "description": (
                    "Кутова кухня під геометрію кімнати: високі пенали з горіха, "
                    "білі верхні фасади і темна кам'яна стільниця.\n\n"
                    "Праворуч — відкрита вітрина з підсвіткою. "
                    "Техніка вбудована в колонку.\n\n"
                    "Спочатку обміри і прорахунок: фасади, фурнітура, стільниця, терміни. "
                    "Далі замовлення виготовлення і комплектуючих. "
                    "На об'єкті — збірка і встановлення."
                ),
                "materials_label": "ГОРІХ · КАМІНЬ · 2024",
                "category": "Кухня",
                "year": 2024,
                "area": "",
                "duration": "",
                "location": "Дніпро",
                "image_url": IMG["walnut_kitchen"],
                "detail_image_url": IMG["walnut_kitchen"],
                "video_poster_url": IMG["walnut_kitchen"],
                "short_description": (
                    "Горіх, білі фасади, темний камінь і вітрина з підсвіткою."
                ),
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": True,
                "order": 1,
                "seo_title": "Кухня з горіха на замовлення в Дніпрі | ProProstir",
                "seo_description": (
                    "Кутова кухня з горіха, білих фасадів і каменю в Дніпрі. "
                    "Прорахунок, замовлення виготовлення і збірка на місці."
                ),
                "seo_keywords": (
                    "кухня на замовлення Дніпро, кухні на замовлення, "
                    "кухонний гарнітур Дніпро, кухня з горіха, стільниця з каменю, "
                    "якісна кухня, прорахунок кухні, збірка кухні Дніпро"
                ),
            },
        )
        kitchen.stages.all().delete()
        ProjectStage.objects.bulk_create(
            [
                ProjectStage(
                    project=kitchen,
                    title="До",
                    image_url="/works/before/before-walnut-kitchen.jpg",
                    order=1,
                ),
                ProjectStage(
                    project=kitchen,
                    title="Після",
                    image_url=IMG["walnut_kitchen"],
                    order=2,
                ),
            ]
        )
        self._seed_gallery(
            kitchen,
            [
                (IMG["walnut_kitchen"], "Готова кухня", 1),
                ("/works/before/before-walnut-kitchen.jpg", "Порожня кімната", 2),
            ],
        )

        white, _ = Project.objects.update_or_create(
            slug="bila-kuhnya-z-ostrovom",
            defaults={
                "title": "Біла кухня з барною стійкою",
                "subtitle": (
                    "Білі фасади, дубова стільниця і барна стійка біля вікна."
                ),
                "description": (
                    "Кухня вздовж двох стін: білі фасади, дубова стільниця, "
                    "відкриті полиці і вбудована техніка.\n\n"
                    "Барна стійка на металевому каркасі з трьома табуретами "
                    "стоїть біля вікна."
                ),
                "materials_label": "ДУБ · БІЛИЙ · 2026",
                "category": "Кухня",
                "year": 2026,
                "area": "",
                "duration": "",
                "location": "Дніпро",
                "image_url": IMG["white_kitchen"],
                "detail_image_url": IMG["white_kitchen"],
                "video_poster_url": IMG["white_kitchen"],
                "short_description": (
                    "Білі фасади, дубова стільниця і барна стійка біля вікна."
                ),
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 2,
                "seo_title": "Біла кухня на замовлення в Дніпрі | ProProstir",
                "seo_description": (
                    "Біла кухня з дубовою стільницею і барною стійкою в Дніпрі. "
                    "Прорахунок, замовлення і збірка кухонних меблів."
                ),
                "seo_keywords": (
                    "біла кухня на замовлення Дніпро, кухня з барною стійкою, "
                    "кухонні меблі Дніпро, кухня біля вікна, прорахунок кухні, "
                    "збірка кухні, якісні кухні Дніпро"
                ),
            },
        )
        self._seed_gallery(
            white,
            [
                (IMG["white_kitchen"], "Готова кухня", 1),
                ("/works/before/before-white-kitchen.jpg", "Порожня кімната", 2),
            ],
        )

        wardrobe, _ = Project.objects.update_or_create(
            slug="garderobna-zi-shponu",
            defaults={
                "title": "Гардеробна з горіха",
                "subtitle": "Відкриті секції з підсвіткою і колона ящиків.",
                "description": (
                    "Гардеробна з горіха: відкриті ніші з рейками, "
                    "світлодіодна підсвітка і висока колона ящиків."
                ),
                "materials_label": "ГОРІХ · 2024",
                "category": "Гардеробна",
                "year": 2024,
                "area": "",
                "duration": "",
                "location": "Дніпро",
                "image_url": IMG["wardrobe_real"],
                "detail_image_url": IMG["wardrobe_real"],
                "video_poster_url": IMG["wardrobe_real"],
                "short_description": "Відкриті секції з підсвіткою і колона ящиків.",
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 3,
                "seo_title": "Гардеробна на замовлення в Дніпрі | ProProstir",
                "seo_description": (
                    "Гардеробна з горіха на замовлення в Дніпрі: відкриті секції, "
                    "підсвітка і ящики. Прорахунок і збірка шафи."
                ),
                "seo_keywords": (
                    "гардеробна на замовлення Дніпро, шафа на замовлення, "
                    "гардеробна кімната, шафа з горіха, вбудована гардеробна, "
                    "збірка шафи Дніпро, якісні меблі"
                ),
            },
        )
        self._seed_gallery(
            wardrobe,
            [
                (IMG["wardrobe_real"], "Гардеробна", 1),
            ],
        )

        living, _ = Project.objects.update_or_create(
            slug="vitalnya-wabi-sabi",
            defaults={
                "title": "Підвісна тумба під телевізор",
                "subtitle": "Біла підвісна тумба з рейками і продовженням у стіл.",
                "description": (
                    "Підвісна тумба під телевізор: рейкові фасади, ящики "
                    "і нижча секція, що переходить у вузький стіл."
                ),
                "materials_label": "БІЛИЙ · 2024",
                "category": "Вітальня",
                "year": 2024,
                "area": "",
                "duration": "",
                "location": "Дніпро",
                "image_url": IMG["tv_stand"],
                "detail_image_url": IMG["tv_stand"],
                "video_poster_url": IMG["tv_stand"],
                "short_description": "Біла підвісна тумба з рейками і продовженням у стіл.",
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 4,
                "seo_title": "Тумба під телевізор на замовлення в Дніпрі | ProProstir",
                "seo_description": (
                    "Підвісна тумба під телевізор на замовлення в Дніпрі. "
                    "Рейкові фасади, прорахунок, замовлення і збірка меблів для вітальні."
                ),
                "seo_keywords": (
                    "тумба під телевізор на замовлення, меблі для вітальні Дніпро, "
                    "підвісна тумба, корпусні меблі Дніпро, збірка меблів, "
                    "меблі на замовлення"
                ),
            },
        )
        self._seed_gallery(
            living,
            [
                (IMG["tv_stand"], "Тумба", 1),
                ("/works/before/before-tv-wall.jpg", "Порожня стіна", 2),
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
                    "Фасади, панелі, дверцята. Рівна текстура під кухні, "
                    "шафи і стінові системи."
                ),
                "image_url": IMG["veneer"],
                "order": 3,
            },
            {
                "name_uk": "Камінь",
                "name_en": "STONE",
                "description": (
                    "Стільниці та вставки. Мармур, кварц, керамограніт — "
                    "під кухні, столи і тумби."
                ),
                "image_url": IMG["stone"],
                "order": 4,
            },
            {
                "name_uk": "Метал",
                "name_en": "METAL",
                "description": (
                    "Каркаси, ніжки, петлі і напрямні. "
                    "Те, на чому тримається збірка."
                ),
                "image_url": IMG["metal"],
                "order": 5,
            },
            {
                "name_uk": "Скло",
                "name_en": "GLASS",
                "description": (
                    "Фасади, вітрини, полиці. Матове і прозоре скло в корпусних меблях."
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
                "title": "Запит",
                "description": (
                    "Ви описуєте меблі: кухня, шафа, вбудова чи нестандарт. "
                    "Я уточнюю побажання, матеріали і бюджет."
                ),
                "duration": "1–2 дні",
                "image_url": IMG["idea"],
                "order": 1,
            },
            {
                "title": "Обміри",
                "description": (
                    "Виїзд на місце: розміри ніш, стін і комунікацій, фото. "
                    "Без цього прорахунок не буде точним."
                ),
                "duration": "1 день",
                "image_url": IMG["measures"],
                "order": 2,
            },
            {
                "title": "Прорахунок",
                "description": (
                    "Кошторис із розкладкою: корпуси, фасади, фурнітура, "
                    "стільниці, терміни і підсумкова вартість. "
                    "Затверджуєте його до замовлення."
                ),
                "duration": "2–5 днів",
                "image_url": IMG["model_3d"],
                "order": 3,
            },
            {
                "title": "Замовлення",
                "description": (
                    "Замовляю виготовлення і комплектуючі під затверджений кошторис. "
                    "Контролюю терміни і комплектацію."
                ),
                "duration": "за проєктом",
                "image_url": IMG["production"],
                "order": 4,
            },
            {
                "title": "Збірка",
                "description": (
                    "Збираю і встановлюю меблі на місці: підганяю до стін, "
                    "виставляю фасади, підключаю техніку там, де вона частина меблів."
                ),
                "duration": "3–10 днів",
                "image_url": IMG["install"],
                "order": 5,
            },
            {
                "title": "Здача",
                "description": (
                    "Перевірка кожної секції, регулювання фурнітури "
                    "і гарантія на збірку."
                ),
                "duration": "1 день",
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
            ("Обміри", IMG["craft_1"], 1),
            ("Прорахунок", IMG["craft_2"], 2),
            ("Замовлення", IMG["production"], 3),
            ("Збірка", IMG["craft_4"], 4),
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
            ("Прорахунок", "Кошторис до старту", 1),
            ("Замовлення", "Виготовлення і фурнітура", 2),
            ("Збірка", "На об'єкті, будь-яка складність", 3),
            ("5 років", "Гарантія на збірку", 4),
        ]
        for value, label, order in stats:
            WorkshopStat.objects.update_or_create(
                order=order,
                defaults={"value": value, "label": label},
            )

        images = [
            ("Збірка на об'єкті", IMG["workshop_1"], 1),
            ("Фурнітура і деталі", IMG["workshop_2"], 2),
            ("Корпус перед встановленням", IMG["workshop_3"], 3),
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
                    "Наведіть курсор — побачите, які меблі тут можна "
                    "прорахувати, замовити і зібрати."
                ),
                "idle_eyebrow": "Меблі в кадрі",
                "idle_title": "Оберіть предмет",
                "idle_body": (
                    "Стелаж, тумби, диван, стіл, крісло чи тумба — "
                    "наведіть і побачите, що це за предмет."
                ),
                "is_active": True,
                "is_published": True,
                "order": 1,
            },
        )
        zones = [
            ("Стелаж", "Корпусні меблі на замовлення", "Полиці · корпус · підсвітка", "Меблі", 16, 10, 57, 40, 1),
            ("Нижні тумби", "Шафи під стелаж", "Фасади · петлі · доводчики", "Шафи", 20, 50, 53, 12, 2),
            ("Тумба під вікном", "Тумби та полиці під вікно", "Корпус · стільниця · фасади", "Меблі", 77, 55, 23, 16, 4),
            ("Диван", "Диван у зоні відпочинку", "Поруч — тумби і стелаж на замовлення", "Меблі", 0, 50, 39, 48, 5),
            ("Крісло", "Крісло біля вікна", "Поруч — тумба під вікно", "Меблі", 60, 48, 17, 33, 6),
            ("Журнальний стіл", "Столи на замовлення", "Стільниця · опора", "Столи", 40, 59, 22, 31, 7),
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
