import type { HomePayload, PageSection, Project } from "@/lib/types";
import { getSection } from "@/lib/content";
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

function isVisible(section: PageSection | undefined): section is PageSection {
  return Boolean(section && section.is_visible !== false);
}

function resolveFeaturedProject(data: HomePayload): Project | undefined {
  if (data.featured_project_slug) {
    const bySlug = data.projects.find((p) => p.slug === data.featured_project_slug);
    if (bySlug) return bySlug;
  }
  const byFlag = data.projects.find((p) => p.show_in_detail_section);
  if (byFlag) return byFlag;
  return data.projects.find((p) => p.stages.length > 0);
}

export default function Site({ data }: SiteProps) {
  const featured = resolveFeaturedProject(data);
  const projectsSection = getSection(data.sections, "projects");
  const photographySection = getSection(data.sections, "photography");
  const materialsSection = getSection(data.sections, "materials");
  const processSection = getSection(data.sections, "process");
  const workshopSection = getSection(data.sections, "workshop");
  const drawingSection = getSection(data.sections, "drawing");
  const beforeAfterSection = getSection(data.sections, "before_after");
  const contactSection = getSection(data.sections, "contact");

  return (
    <>
      <JsonLd settings={data.settings} />
      <Header settings={data.settings} navigation={data.navigation} />
      <main>
        <Hero settings={data.settings} stats={data.hero_stats} />
        {isVisible(projectsSection) ? (
          <Projects
            section={projectsSection}
            projects={data.projects}
            settings={data.settings}
          />
        ) : null}
        {isVisible(projectsSection) && featured ? (
          <ProjectDetail project={featured} settings={data.settings} />
        ) : null}
        {isVisible(photographySection) ? (
          <Photography section={photographySection} details={data.craft_details} />
        ) : null}
        {isVisible(drawingSection) ? (
          <DrawingReality settings={data.settings} section={drawingSection} />
        ) : null}
        {isVisible(materialsSection) ? (
          <Materials section={materialsSection} materials={data.materials} />
        ) : null}
        {isVisible(processSection) ? (
          <Process section={processSection} steps={data.process_steps} />
        ) : null}
        {isVisible(workshopSection) ? (
          <Workshop
            section={workshopSection}
            settings={data.settings}
            stats={data.workshop_stats}
            images={data.workshop_images}
          />
        ) : null}
        {isVisible(beforeAfterSection) ? (
          <BeforeAfter settings={data.settings} section={beforeAfterSection} />
        ) : null}
        {isVisible(contactSection) ? (
          <Contact
            section={contactSection}
            settings={data.settings}
            roomTypes={data.room_types}
          />
        ) : null}
      </main>
      <Footer settings={data.settings} navigation={data.navigation} />
    </>
  );
}
