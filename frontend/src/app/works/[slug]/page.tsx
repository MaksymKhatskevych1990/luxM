import type { Metadata } from "next";
import { notFound } from "next/navigation";
import WorkArticle from "@/components/WorkArticle";
import {
  absoluteUrl,
  allWorks,
  findWork,
  loadHome,
  workHref,
  workMetaDescription,
  workPageTitle,
} from "@/lib/works";

export const revalidate = 300;

type PageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
  const data = await loadHome();
  return allWorks(data.work_categories).map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const data = await loadHome();
  const found = findWork(data.work_categories, slug);
  if (!found) return {};
  const path = workHref(found.item.slug);
  const description = workMetaDescription(found.item);
  const image = found.item.image_url
    ? absoluteUrl(found.item.image_url)
    : undefined;
  const pageTitle = workPageTitle(found.item);
  return {
    title: pageTitle,
    description,
    alternates: { canonical: path, languages: { uk: path } },
    openGraph: {
      title: `${pageTitle} | ProProstir`,
      description,
      url: path,
      locale: "uk_UA",
      type: "article",
      siteName: "ProProstir",
      images: image ? [{ url: image, alt: found.item.title }] : undefined,
    },
    twitter: {
      card: "summary_large_image",
      title: `${pageTitle} | ProProstir`,
      description,
      images: image ? [image] : undefined,
    },
  };
}

export default async function WorkItemPage({ params }: PageProps) {
  const { slug } = await params;
  const data = await loadHome();
  const found = findWork(data.work_categories, slug);
  if (!found) notFound();
  const related = found.category.items.filter((item) => item.slug !== found.item.slug);

  return (
    <WorkArticle
      item={found.item}
      category={found.category}
      related={related}
      settings={data.settings}
      navigation={data.navigation}
    />
  );
}
