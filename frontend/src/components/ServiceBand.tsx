import Link from "next/link";
import { services } from "@/lib/services";

export default function ServiceBand() {
  return (
    <section className="service-band" aria-labelledby="service-band-title">
      <div className="wrap">
        <p className="label label--oak">Послуги в Дніпрі</p>
        <h2 id="service-band-title" className="font-serif service-band-title">
          Меблі на замовлення в Дніпрі
        </h2>
        <p className="service-band-lead">
          Кухні, шафи та гардеробні: прорахунок, замовлення виготовлення і збірка на місці.
          Оберіть, що потрібно порахувати.
        </p>
        <ul className="service-band-grid">
          {services.map((service) => (
            <li key={service.slug}>
              <Link href={`/${service.slug}`} className="service-band-card">
                <span className="label">{service.navLabel}</span>
                <strong className="font-serif">{service.h1}</strong>
                <span className="service-band-more">Дивитись →</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
