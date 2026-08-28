export type SiteSettings = {
  id?: number;
  brand_name: string;
  tagline: string;
  founded_year: number;

  header_logo_primary: string;
  header_logo_secondary: string;
  header_cta_text: string;
  header_cta_href: string;

  hero_eyebrow: string;
  hero_title_line1: string;
  hero_title_emphasis: string;
  hero_title_line2: string;
  hero_subline: string;
  hero_cta_primary_text: string;
  hero_cta_primary_href: string;
  hero_cta_secondary_text: string;
  hero_cta_secondary_href: string;
  hero_floorplan_caption: string;
  hero_scroll_hint: string;
  hero_founded_prefix: string;
  hero_background_image_url: string;

  phone: string;
  email: string;
  telegram: string;
  address: string;
  instagram_url: string;
  telegram_url: string;

  seo_title: string;
  seo_description: string;
  seo_keywords: string;
  og_image_url: string;
  jsonld_city: string;
  jsonld_country: string;
  jsonld_price_range: string;

  stats_projects: string;
  stats_years: string;
  stats_masters: string;
  stats_production: string;

  workshop_quote: string;
  workshop_author: string;
  workshop_text: string;

  detail_eyebrow_prefix: string;
  detail_section_title: string;
  detail_number_prefix: string;
  detail_cta_text: string;
  detail_cta_href: string;
  meta_label_area: string;
  meta_label_materials: string;
  meta_label_duration: string;
  meta_label_year: string;
  meta_label_location: string;
  featured_project?: number | null;

  drawing_eyebrow: string;
  drawing_title: string;
  drawing_body: string;
  drawing_phase_1_label: string;
  drawing_phase_2_label: string;
  drawing_phase_3_label: string;
  drawing_result_alt: string;
  drawing_sketch_image_url: string;

  ba_eyebrow: string;
  ba_title: string;
  ba_hint: string;
  ba_label_before: string;
  ba_label_after: string;
  before_image_url: string;
  after_image_url: string;

  contact_eyebrow: string;
  contact_title_line1: string;
  contact_title_line2: string;
  contact_title_emphasis: string;
  contact_intro: string;
  contact_room_heading: string;
  contact_message_placeholder: string;
  contact_name_placeholder: string;
  contact_phone_placeholder: string;
  contact_email_placeholder: string;
  contact_telegram_placeholder: string;
  contact_submit_text: string;
  contact_submit_loading: string;
  contact_success_eyebrow: string;
  contact_success_title: string;
  contact_success_body: string;
  contact_validation_message: string;
  contact_label_address: string;
  contact_label_phone: string;
  contact_label_email: string;
  contact_label_telegram: string;

  footer_services_heading: string;
  footer_studio_heading: string;
  footer_contacts_heading: string;
  footer_copyright_suffix: string;
  footer_location_tagline: string;
};

export type HeroStat = {
  id: number;
  value: string;
  label: string;
  order: number;
};

export type PageSection = {
  id?: number;
  key: string;
  section_id: string;
  eyebrow: string;
  title: string;
  title_line2: string;
  title_emphasis: string;
  subtitle: string;
  cta_text?: string;
  cta_href?: string;
  is_visible: boolean;
  order: number;
};

export type NavItem = {
  id: number;
  label: string;
  href: string;
  location: "header" | "footer_services" | "footer_studio" | string;
  order: number;
  is_visible?: boolean;
};

export type RoomType = {
  id?: number;
  value: string;
  label: string;
  order: number;
  is_active?: boolean;
};

export type ProjectStage = {
  id: number;
  title: string;
  image_url: string;
  order: number;
};

export type ProjectGalleryImage = {
  id: number;
  url: string;
  caption: string;
  order: number;
};

export type Project = {
  id: number;
  title: string;
  slug: string;
  subtitle: string;
  description: string;
  short_description?: string;
  materials_label: string;
  category: string;
  year: number | null;
  area: string;
  duration: string;
  location: string;
  image_url: string;
  detail_image_url: string;
  video_src?: string;
  video_poster?: string;
  is_featured: boolean;
  is_published?: boolean;
  show_in_detail_section?: boolean;
  order: number;
  seo_title: string;
  seo_description: string;
  seo_keywords?: string;
  stages: ProjectStage[];
  gallery: ProjectGalleryImage[];
};

export type Material = {
  id: number;
  name_uk: string;
  name_en: string;
  description: string;
  image_url: string;
  order: number;
  is_published?: boolean;
};

export type ProcessStep = {
  id: number;
  title: string;
  description: string;
  duration: string;
  image_url: string;
  order: number;
  is_published?: boolean;
};

export type CraftDetail = {
  id: number;
  title: string;
  image_url: string;
  order: number;
  is_published?: boolean;
};

export type WorkshopStat = {
  id: number;
  value: string;
  label: string;
  order: number;
};

export type WorkshopImage = {
  id: number;
  title: string;
  image_url: string;
  order: number;
};

export type HomePayload = {
  settings: SiteSettings;
  hero_stats: HeroStat[];
  sections: PageSection[];
  navigation: NavItem[];
  room_types: RoomType[];
  featured_project_slug: string | null;
  projects: Project[];
  materials: Material[];
  process_steps: ProcessStep[];
  craft_details: CraftDetail[];
  workshop_stats: WorkshopStat[];
  workshop_images: WorkshopImage[];
};
