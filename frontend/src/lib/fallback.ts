import type { HomePayload } from "./types";

/** Fallback content matching Figma Make mockup when API is unavailable */
export const fallbackHome: HomePayload = {
  settings: {
    brand_name: "Форма Studio",
    tagline: "Унікальні меблі на замовлення. Київ, Україна.",
    founded_year: 2018,
    phone: "+38 (044) 555 12 34",
    email: "studio@forma.ua",
    telegram: "@forma_studio",
    address: "Київ · Стара Дарниця, вул. Промислова 14",
    instagram_url: "https://instagram.com/",
    telegram_url: "https://t.me/",
    seo_title: "Форма Studio — меблі на замовлення в Києві",
    seo_description:
      "Преміальні меблі на замовлення: проєктування, виробництво та монтаж. Кухні, гардеробні, вітальні та кабінети.",
    seo_keywords: "меблі на замовлення, кухні Київ, гардеробні, Forma Studio",
    stats_projects: "147",
    stats_years: "08",
    stats_masters: "24",
    stats_production: "100%",
    workshop_quote:
      "Ми не просто виготовляємо меблі. Ми створюємо предмети, які мають існувати саме у вашому просторі.",
    workshop_author: "Андрій Коваль, засновник",
    workshop_text:
      "Наша майстерня площею 800 м² в Старій Дарниці обладнана точними верстатами ЧПУ та ручним інструментом. Кожен виріб — від першого ескізу до встановлення — проходить через руки одного майстра.",
    before_image_url:
      "https://images.unsplash.com/photo-1664995156397-99bd42f5a8ab?w=1400&h=900&fit=crop&auto=format",
    after_image_url:
      "https://images.unsplash.com/photo-1758565811352-a439bd6f956e?w=1400&h=900&fit=crop&auto=format",
  },
  projects: [
    {
      id: 1,
      title: "Кухня для приватного будинку",
      slug: "kukhnya-dlya-pryvatnogo-budynku",
      subtitle: "Кухня з натурального дуба",
      description:
        "Спроєктована з урахуванням геометрії приміщення: L-подібне планування, острів з кам'яною стільницею та інтегрована система зберігання.\n\nФасади — масив дуба з відкритою текстурою. Ніжки та ручки — матова сталь. Стільниця — мармур Calacatta.",
      materials_label: "ДУБ · КАМІНЬ · 2026",
      category: "Кухня",
      year: 2026,
      area: "18 м²",
      duration: "11 тижнів",
      location: "Приватний будинок · Київ",
      image_url:
        "https://images.unsplash.com/photo-1765371515325-b6611765dfad?w=1400&h=900&fit=crop&auto=format",
      detail_image_url:
        "https://images.unsplash.com/photo-1765371515325-b6611765dfad?w=1400&h=900&fit=crop&auto=format",
      is_featured: true,
      order: 1,
      seo_title: "",
      seo_description: "Острівна кухня з масиву дуба. Стільниця з мармуру Calacatta.",
      stages: [
        {
          id: 1,
          title: "Ідея",
          image_url:
            "https://images.unsplash.com/photo-1590880795696-20c7dfadacde?w=1100&h=700&fit=crop&auto=format",
          order: 1,
        },
        {
          id: 2,
          title: "3D-модель",
          image_url:
            "https://images.unsplash.com/photo-1497218770144-3fea6dbc33fe?w=1100&h=700&fit=crop&auto=format",
          order: 2,
        },
        {
          id: 3,
          title: "Виготовлення",
          image_url:
            "https://images.unsplash.com/photo-1631396326838-de37e5f8bcbc?w=1100&h=700&fit=crop&auto=format",
          order: 3,
        },
        {
          id: 4,
          title: "Монтаж",
          image_url:
            "https://images.unsplash.com/photo-1765371515325-b6611765dfad?w=1100&h=700&fit=crop&auto=format",
          order: 4,
        },
      ],
    },
    {
      id: 2,
      title: "Бібліотека і кабінет",
      slug: "biblioteka-i-kabinet",
      subtitle: "",
      description:
        "Вбудована бібліотека по всій висоті. Ніжки та ручки — матова сталь.",
      materials_label: "ГОРІХ · МЕТАЛ · 2025",
      category: "Кабінет",
      year: 2025,
      area: "",
      duration: "",
      location: "",
      image_url:
        "https://images.unsplash.com/photo-1780257563050-0ee78acfeee8?w=800&h=1100&fit=crop&auto=format",
      detail_image_url: "",
      is_featured: true,
      order: 2,
      seo_title: "",
      seo_description: "",
      stages: [],
    },
    {
      id: 3,
      title: "Гардеробна зі шпону",
      slug: "garderobna-zi-shponu",
      subtitle: "",
      description: "",
      materials_label: "ГАРДЕРОБНА · ШПОН · СКЛО · 2025",
      category: "Гардеробна",
      year: 2025,
      area: "",
      duration: "",
      location: "",
      image_url:
        "https://images.unsplash.com/photo-1593173945705-d6451ed5909a?w=800&h=600&fit=crop&auto=format",
      detail_image_url: "",
      is_featured: true,
      order: 3,
      seo_title: "",
      seo_description: "",
      stages: [],
    },
    {
      id: 4,
      title: "Вітальня у стилі Wabi-Sabi",
      slug: "vitalnya-wabi-sabi",
      subtitle: "",
      description: "",
      materials_label: "ВІТАЛЬНЯ · ДУБ · ЛЬОН · 2024",
      category: "Вітальня",
      year: 2024,
      area: "",
      duration: "",
      location: "",
      image_url:
        "https://images.unsplash.com/photo-1594272807311-3ed584a48577?w=1100&h=700&fit=crop&auto=format",
      detail_image_url: "",
      is_featured: true,
      order: 4,
      seo_title: "",
      seo_description: "",
      stages: [],
    },
  ],
  materials: [
    {
      id: 1,
      name_uk: "Дуб",
      name_en: "OAK",
      description: "Масив із відкритою текстурою. Теплий на дотик, зносостійкий.",
      image_url:
        "https://images.unsplash.com/photo-1582055193464-943584223be1?w=400&h=560&fit=crop&auto=format",
      order: 1,
    },
    {
      id: 2,
      name_uk: "Горіх",
      name_en: "WALNUT",
      description:
        "Темна деревина з виразним малюнком волокна. Для бібліотек і кабінетів.",
      image_url:
        "https://images.unsplash.com/photo-1736506159776-22ca388780fa?w=400&h=560&fit=crop&auto=format",
      order: 2,
    },
    {
      id: 3,
      name_uk: "Шпон",
      name_en: "VENEER",
      description: "Натуральний шпон ясена та клена. Рівна текстура, широка палітра.",
      image_url:
        "https://images.unsplash.com/photo-1506689205310-0a29c388691c?w=400&h=560&fit=crop&auto=format",
      order: 3,
    },
    {
      id: 4,
      name_uk: "Камінь",
      name_en: "STONE",
      description:
        "Мармур Calacatta та граніт. Стільниці та острови з унікальним малюнком.",
      image_url:
        "https://images.unsplash.com/photo-1778272617843-bdda47b64bad?w=400&h=560&fit=crop&auto=format",
      order: 4,
    },
    {
      id: 5,
      name_uk: "Метал",
      name_en: "METAL",
      description: "Матова сталь, латунь. Ніжки, ручки, декоративні вставки.",
      image_url:
        "https://images.unsplash.com/photo-1497218770144-3fea6dbc33fe?w=400&h=560&fit=crop&auto=format",
      order: 5,
    },
    {
      id: 6,
      name_uk: "Скло",
      name_en: "GLASS",
      description: "Загартоване матове та прозоре скло. Вітрини, фасади, двері.",
      image_url:
        "https://images.unsplash.com/photo-1593173945705-d6451ed5909a?w=400&h=560&fit=crop&auto=format",
      order: 6,
    },
  ],
  process_steps: [
    {
      id: 1,
      title: "Ідея",
      description:
        "Ви розповідаєте про простір та побажання. Ми слухаємо, вивчаємо, ставимо питання.",
      duration: "1–2 дні",
      image_url:
        "https://images.unsplash.com/photo-1590880795696-20c7dfadacde?w=700&h=900&fit=crop&auto=format",
      order: 1,
    },
    {
      id: 2,
      title: "Заміри",
      description:
        "Виїзд майстра, детальні обміри приміщення, фотофіксація всіх нюансів.",
      duration: "1 день",
      image_url:
        "https://images.unsplash.com/photo-1659930087003-2d64e33181f7?w=700&h=900&fit=crop&auto=format",
      order: 2,
    },
    {
      id: 3,
      title: "Проєктування",
      description:
        "Розробка 3D-моделі, технічних креслень, вибір матеріалів та покриттів.",
      duration: "5–10 днів",
      image_url:
        "https://images.unsplash.com/photo-1497218770144-3fea6dbc33fe?w=700&h=900&fit=crop&auto=format",
      order: 3,
    },
    {
      id: 4,
      title: "Виробництво",
      description:
        "Виготовлення в майстерні вручну. Поетапний контроль якості кожної деталі.",
      duration: "4–8 тижнів",
      image_url:
        "https://images.unsplash.com/photo-1631396326838-de37e5f8bcbc?w=700&h=900&fit=crop&auto=format",
      order: 4,
    },
    {
      id: 5,
      title: "Монтаж",
      description:
        "Встановлення нашою командою майстрів, підключення, регулювання.",
      duration: "1–3 дні",
      image_url:
        "https://images.unsplash.com/photo-1631396326646-c06a935ff3a6?w=700&h=900&fit=crop&auto=format",
      order: 5,
    },
    {
      id: 6,
      title: "Результат",
      description:
        "Фінальна перевірка, фотографування готового простору. Гарантія 5 років.",
      duration: "Назавжди",
      image_url:
        "https://images.unsplash.com/photo-1765371515325-b6611765dfad?w=700&h=900&fit=crop&auto=format",
      order: 6,
    },
  ],
  craft_details: [
    {
      id: 1,
      title: "Точна розмітка",
      image_url:
        "https://images.unsplash.com/photo-1659930087003-2d64e33181f7?w=500&h=680&fit=crop&auto=format",
      order: 1,
    },
    {
      id: 2,
      title: "Ручна обробка",
      image_url:
        "https://images.unsplash.com/photo-1631396326646-c06a935ff3a6?w=500&h=650&fit=crop&auto=format",
      order: 2,
    },
    {
      id: 3,
      title: "Фінішне полірування",
      image_url:
        "https://images.unsplash.com/photo-1712171984530-e25a4aaa46dd?w=500&h=700&fit=crop&auto=format",
      order: 3,
    },
    {
      id: 4,
      title: "Перевірка якості",
      image_url:
        "https://images.unsplash.com/photo-1679797850019-3d0d8659a695?w=500&h=620&fit=crop&auto=format",
      order: 4,
    },
  ],
  workshop_stats: [
    { id: 1, value: "800 м²", label: "Площа майстерні", order: 1 },
    { id: 2, value: "1 майстер", label: "Від ескізу до монтажу", order: 2 },
    { id: 3, value: "ЧПУ + ручне", label: "Комбіноване виробництво", order: 3 },
    { id: 4, value: "5 років", label: "Гарантія на вироби", order: 4 },
  ],
  workshop_images: [
    {
      id: 1,
      title: "Майстер за роботою",
      image_url:
        "https://images.unsplash.com/photo-1547609434-b732edfee020?w=500&h=720&fit=crop&auto=format",
      order: 1,
    },
    {
      id: 2,
      title: "Деталі обробки",
      image_url:
        "https://images.unsplash.com/photo-1679797850019-3d0d8659a695?w=400&h=400&fit=crop&auto=format",
      order: 2,
    },
    {
      id: 3,
      title: "Ручна обробка",
      image_url:
        "https://images.unsplash.com/photo-1631396326646-c06a935ff3a6?w=400&h=400&fit=crop&auto=format",
      order: 3,
    },
  ],
};
