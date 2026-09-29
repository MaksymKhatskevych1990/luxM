import { fetchHome } from "@/lib/api";
import { fallbackHome } from "@/lib/fallback";
import { metadataFromSettings } from "@/lib/seo";
import Site from "@/components/Site";

export async function generateMetadata() {
  try {
    const data = await fetchHome();
    return metadataFromSettings(data.settings);
  } catch {
    return metadataFromSettings(fallbackHome.settings);
  }
}

export default async function HomePage() {
  let data = fallbackHome;

  try {
    data = await fetchHome();
  } catch {
    data = fallbackHome;
  }

  return <Site data={data} />;
}
