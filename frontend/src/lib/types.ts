export type SiteSettings = {
  brand_name: string;
  tagline: string;
  founded_year: number;
  phone: string;
  email: string;
  telegram: string;
  address: string;
  instagram_url: string;
  telegram_url: string;
  seo_title: string;
  seo_description: string;
  seo_keywords: string;
  stats_projects: string;
  stats_years: string;
  stats_masters: string;
  stats_production: string;
  workshop_quote: string;
  workshop_author: string;
  workshop_text: string;
  before_image_url: string;
  after_image_url: string;
};

export type ProjectStage = {
  id: number;
  title: string;
  image_url: string;
  order: number;
};

export type Project = {
  id: number;
  title: string;
  slug: string;
  subtitle: string;
  description: string;
  materials_label: string;
  category: string;
  year: number | null;
  area: string;
  duration: string;
  location: string;
  image_url: string;
  detail_image_url: string;
  is_featured: boolean;
  order: number;
  seo_title: string;
  seo_description: string;
  stages: ProjectStage[];
};

export type Material = {
  id: number;
  name_uk: string;
  name_en: string;
  description: string;
  image_url: string;
  order: number;
};

export type ProcessStep = {
  id: number;
  title: string;
  description: string;
  duration: string;
  image_url: string;
  order: number;
};

export type CraftDetail = {
  id: number;
  title: string;
  image_url: string;
  order: number;
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
  projects: Project[];
  materials: Material[];
  process_steps: ProcessStep[];
  craft_details: CraftDetail[];
  workshop_stats: WorkshopStat[];
  workshop_images: WorkshopImage[];
};
