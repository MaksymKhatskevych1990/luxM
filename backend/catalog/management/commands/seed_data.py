from django.core.management.base import BaseCommand

from catalog.models import (
    CraftDetail,
    HeroStat,
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
        self.stdout.write(self.style.SUCCESS("Seed data loaded from Forma Studio mockup."))

    def _seed_settings(self):
        settings = SiteSettings.load()
        settings.brand_name = "Форма Studio"
        settings.tagline = "Унікальні меблі на замовлення. Київ, Україна."
        settings.founded_year = 2018

        settings.header_logo_primary = "Форма"
        settings.header_logo_secondary = "STUDIO"
        settings.header_cta_text = "Обговорити проєкт"
        settings.header_cta_href = "#контакти"

        settings.hero_eyebrow = "Форма Studio · Київ, Україна"
        settings.hero_title_line1 = "Меблі,"
        settings.hero_title_emphasis = "створені"
        settings.hero_title_line2 = "під ваш простір."
        settings.hero_subline = "Проєктування · Виробництво · Монтаж"
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
        settings.address = "Київ · Стара Дарниця, вул. Промислова 14"
        settings.instagram_url = "https://instagram.com/forma_studio"
        settings.telegram_url = "https://t.me/forma_studio"
        settings.whatsapp_url = ""
        settings.contact_label_whatsapp = "WhatsApp"
        settings.contact_label_instagram = "Instagram"

        settings.seo_title = "Форма Studio — меблі на замовлення в Києві"
        settings.seo_description = (
            "Преміальні меблі на замовлення: проєктування, виробництво та монтаж. "
            "Кухні, гардеробні, вітальні та кабінети."
        )
        settings.seo_keywords = (
            "меблі на замовлення, кухні Київ, гардеробні, Forma Studio"
        )
        settings.og_image_url = ""
        settings.jsonld_city = "Київ"
        settings.jsonld_country = "UA"
        settings.jsonld_price_range = "$$$"

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

        settings.detail_eyebrow_prefix = "Проєкт у деталях"
        settings.detail_section_title = "Від ескізу до встановлення"
        settings.detail_number_prefix = "Проєкт №"
        settings.detail_cta_text = "Схожий проєкт →"
        settings.detail_cta_href = "#контакти"
        settings.meta_label_area = "Площа"
        settings.meta_label_materials = "Матеріали"
        settings.meta_label_duration = "Тривалість"
        settings.meta_label_year = "Рік"
        settings.meta_label_location = "Локація"

        settings.drawing_eyebrow = "Від ескізу до реальності"
        settings.drawing_title = "Ідея, що стає простором"
        settings.drawing_body = (
            "Прокрутіть — побачите трансформацію з технічного креслення "
            "в готовий інтер'єр"
        )
        settings.drawing_phase_1_label = "Креслення"
        settings.drawing_phase_2_label = "Ескіз"
        settings.drawing_phase_3_label = "Результат"
        settings.drawing_result_alt = "Готова кухня"
        settings.drawing_sketch_image_url = ""

        settings.ba_eyebrow = "Трансформація простору"
        settings.ba_title = "До і після"
        settings.ba_hint = "Перетягніть повзунок"
        settings.ba_label_before = "ДО"
        settings.ba_label_after = "ПІСЛЯ"
        settings.before_image_url = IMG["before"]
        settings.after_image_url = IMG["after"]

        settings.contact_eyebrow = "Зв'язатися"
        settings.contact_title_line1 = "Розкажіть"
        settings.contact_title_line2 = "про свій"
        settings.contact_title_emphasis = "простір."
        settings.contact_intro = (
            "Надішліть план приміщення, фотографію або просто ідею — "
            "ми зв'яжемося протягом одного робочого дня."
        )
        settings.contact_room_heading = "Що плануєте"
        settings.contact_message_placeholder = "Розкажіть про ваш проєкт…"
        settings.contact_name_placeholder = "Ім'я"
        settings.contact_phone_placeholder = "Телефон"
        settings.contact_email_placeholder = "Email"
        settings.contact_telegram_placeholder = "Telegram"
        settings.contact_submit_text = "Надіслати запит →"
        settings.contact_submit_loading = "Надсилаємо…"
        settings.contact_success_eyebrow = "Надіслано"
        settings.contact_success_title = "Дякуємо, ми отримали ваш запит."
        settings.contact_success_body = (
            "Зв'яжемося протягом одного робочого дня, щоб обговорити ваш простір."
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
        settings.footer_location_tagline = "Київ, Україна · Виготовлено з гордістю"
        settings.save()
        return settings

    def _seed_hero_stats(self):
        HeroStat.objects.all().delete()
        HeroStat.objects.bulk_create(
            [
                HeroStat(value="147", label="Виконаних проєктів", order=1),
                HeroStat(value="08", label="Років досвіду", order=2),
                HeroStat(value="24", label="Майстри в команді", order=3),
                HeroStat(value="100%", label="Власне виробництво", order=4),
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
                    title="Кожен предмет —",
                    title_emphasis="окрема історія.",
                    cta_text="Всі проєкти →",
                    cta_href="#проєкти",
                    order=1,
                ),
                PageSection(
                    key="photography",
                    section_id="фотографія",
                    eyebrow="Деталі майстерності",
                    title="Кожне з'єднання —",
                    title_emphasis="ручна робота.",
                    subtitle=(
                        "Без конвеєра. Кожна деталь — через руки майстра "
                        "від початку до кінця."
                    ),
                    order=2,
                ),
                PageSection(
                    key="materials",
                    section_id="матеріали",
                    eyebrow="Бібліотека матеріалів",
                    title="Матеріали, що",
                    title_emphasis="живуть",
                    subtitle="Тільки натуральне. Перевірено роками.",
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
                    eyebrow="Майстерня",
                    order=5,
                ),
                PageSection(
                    key="drawing",
                    section_id="креслення",
                    eyebrow="Від ескізу до реальності",
                    title="Ідея, що стає простором",
                    subtitle=(
                        "Прокрутіть — побачите трансформацію з технічного "
                        "креслення в готовий інтер'єр"
                    ),
                    order=6,
                ),
                PageSection(
                    key="before_after",
                    section_id="до-після",
                    eyebrow="Трансформація простору",
                    title="До і після",
                    subtitle="Перетягніть повзунок",
                    order=7,
                ),
                PageSection(
                    key="contact",
                    section_id="контакти",
                    eyebrow="Зв'язатися",
                    title="Розкажіть",
                    title_line2="про свій",
                    title_emphasis="простір.",
                    subtitle=(
                        "Надішліть план приміщення, фотографію або просто ідею — "
                        "ми зв'яжемося протягом одного робочого дня."
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
                    label="Майстерня",
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
                    label="Кухні",
                    href="#проєкти",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=1,
                ),
                NavItem(
                    label="Гардеробні",
                    href="#проєкти",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=2,
                ),
                NavItem(
                    label="Вітальні",
                    href="#проєкти",
                    location=NavItem.LOCATION_FOOTER_SERVICES,
                    order=3,
                ),
                NavItem(
                    label="Кабінети",
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
                    label="Майстерня",
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
                RoomType(value="kitchen", label="Кухня", order=1),
                RoomType(value="wardrobe", label="Гардеробна", order=2),
                RoomType(value="living", label="Вітальня", order=3),
                RoomType(value="bedroom", label="Спальня", order=4),
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
                "location": "Приватний будинок · Київ",
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
                "seo_title": "Кухня з натурального дуба на замовлення | Форма Studio",
                "seo_description": (
                    "Острівна кухня з масиву дуба та мармуру Calacatta. "
                    "Проєктування, виробництво та монтаж у Києві."
                ),
                "seo_keywords": "кухня на замовлення, дуб, мармур Calacatta, Київ",
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
                "location": "Квартира · Київ",
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
                "seo_title": "Бібліотека і кабінет з горіха | Форма Studio",
                "seo_description": (
                    "Вбудована бібліотека по всій висоті. Ніжки та ручки — матова сталь."
                ),
                "seo_keywords": "бібліотека на замовлення, кабінет, горіх, Київ",
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
                "location": "Приватний будинок · Київ",
                "image_url": IMG["wardrobe"],
                "detail_image_url": IMG["wardrobe"],
                "video_poster_url": IMG["wardrobe"],
                "short_description": "Гардеробна система зі шпону ясена та матовим склом.",
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 3,
                "seo_title": "Гардеробна зі шпону | Форма Studio",
                "seo_description": (
                    "Гардеробна система зі шпону ясена та матовим склом."
                ),
                "seo_keywords": "гардеробна на замовлення, шпон, скло, Київ",
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
                "location": "Квартира · Київ",
                "image_url": IMG["living"],
                "detail_image_url": IMG["living"],
                "video_poster_url": IMG["living"],
                "short_description": "Тихі форми, натуральний дуб і льон.",
                "is_featured": True,
                "is_published": True,
                "show_in_detail_section": False,
                "order": 4,
                "seo_title": "Вітальня Wabi-Sabi | Форма Studio",
                "seo_description": "Тихі форми, натуральний дуб і льон.",
                "seo_keywords": "вітальня на замовлення, wabi-sabi, дуб, Київ",
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
