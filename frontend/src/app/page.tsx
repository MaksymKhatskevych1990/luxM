import { fetchHome } from "@/lib/api";
import { fallbackHome } from "@/lib/fallback";
import Site from "@/components/Site";

export default async function HomePage() {
  let data = fallbackHome;

  try {
    data = await fetchHome();
  } catch {
    data = fallbackHome;
  }

  return <Site data={data} />;
}
