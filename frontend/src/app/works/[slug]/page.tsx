import type { Metadata } from "next";
import { notFound } from "next/navigation";
import WorkArticle from "@/components/WorkArticle";
import {
  findWork,
  loadHome,
  workHref,
  workMetaDescription,
  workPageTitle,
} from "@/lib/works";

export const dynamic = "force-dynamic";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const data = await loadHome();
  const found = findWork(data.work_categories, slug);
  if (!found) return {};
  const path = workHref(found.item.slug);
  const description = workMetaDescription(found.item);
  return {
    title: workPageTitle(found.item),
    description,
    alternates: { canonical: path, languages: { uk: path } },
    openGraph: {
      title: `${workPageTitle(found.item)} | ProProstir`,
      description,
      url: path,
      locale: "uk_UA",
      type: "article",
      images: found.item.image_url
        ? [{ url: found.item.image_url, alt: found.item.title }]
        : undefined,
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
