import type { Metadata } from "next";
import { notFound } from "next/navigation";
import ServicePage from "@/components/ServicePage";
import { fetchHome } from "@/lib/api";
import { fallbackHome } from "@/lib/fallback";
import { getService, services } from "@/lib/services";
import { SITE_URL } from "@/lib/site";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return services.map((service) => ({ slug: service.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const service = getService(slug);
  if (!service) return {};
  const url = `${SITE_URL}/${service.slug}`;
  return {
    title: { absolute: service.title },
    description: service.description,
    alternates: { canonical: url },
    openGraph: {
      title: service.title,
      description: service.description,
      url,
      locale: "uk_UA",
      type: "website",
      images: [{ url: service.image, alt: service.imageAlt }],
    },
  };
}

export default async function LandingPage({ params }: PageProps) {
  const { slug } = await params;
  const service = getService(slug);
  if (!service) notFound();

  let data = fallbackHome;
  try {
    data = await fetchHome();
  } catch {
    data = fallbackHome;
  }

  return (
    <ServicePage service={service} settings={data.settings} navigation={data.navigation} />
  );
}
