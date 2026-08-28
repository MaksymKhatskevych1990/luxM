import type { HomePayload } from "@/lib/types";
import Header from "./Header";
import Hero from "./Hero";
import Projects from "./Projects";
import ProjectDetail from "./ProjectDetail";
import Photography from "./Photography";
import DrawingReality from "./DrawingReality";
import Materials from "./Materials";
import Process from "./Process";
import Workshop from "./Workshop";
import BeforeAfter from "./BeforeAfter";
import Contact from "./Contact";
import Footer from "./Footer";
import JsonLd from "./JsonLd";

type SiteProps = {
  data: HomePayload;
};

export default function Site({ data }: SiteProps) {
  const featured =
    data.projects.find((p) => p.is_featured && p.stages.length > 0) ??
    data.projects.find((p) => p.stages.length > 0);

  return (
    <>
      <JsonLd settings={data.settings} />
      <Header />
      <main>
        <Hero settings={data.settings} />
        <Projects projects={data.projects} />
        {featured ? <ProjectDetail project={featured} /> : null}
        <Photography details={data.craft_details} />
        <DrawingReality afterImageUrl={data.settings.after_image_url} />
        <Materials materials={data.materials} />
        <Process steps={data.process_steps} />
        <Workshop
          settings={data.settings}
          stats={data.workshop_stats}
          images={data.workshop_images}
        />
        <BeforeAfter
          beforeUrl={data.settings.before_image_url}
          afterUrl={data.settings.after_image_url}
        />
        <Contact settings={data.settings} />
      </main>
      <Footer settings={data.settings} />
    </>
  );
}
