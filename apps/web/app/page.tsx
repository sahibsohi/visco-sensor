const foundationItems = [
  { number: "01", title: "Connected architecture", text: "Independent services for the interface, API, messaging, and data layers." },
  { number: "02", title: "Typed contracts", text: "TypeScript and Pydantic establish dependable boundaries before telemetry arrives." },
  { number: "03", title: "Reproducible locally", text: "Docker Compose starts the application, database, API, and MQTT broker together." },
];

export default function Home() {
  return (
    <main>
      <nav className="nav" aria-label="Primary navigation">
        <a className="brand" href="#top" aria-label="Visco-Sensor home">
          <span className="brandMark">V</span>
          <span>VISCO-SENSOR</span>
        </a>
        <div className="navMeta">
          <span className="statusDot" aria-hidden="true" />
          Foundation online
        </div>
      </nav>

      <section id="top" className="hero">
        <div className="eyebrow">Med-tech software platform · Day 01</div>
        <h1>Turning sensor data into an earlier signal.</h1>
        <p className="lede">
          Visco-Sensor is an end-to-end IoT platform being built to ingest synthetic wearable telemetry,
          validate time-series data, and surface real-time insights for patients and clinicians.
        </p>
        <div className="actions">
          <a className="button primary" href="#foundation">Explore the foundation</a>
          <a className="button secondary" href="http://localhost:8000/docs">View API docs</a>
        </div>
      </section>

      <section className="signalStrip" aria-label="Project metrics">
        <div><strong>205+</strong><span>qualitative interviews</span></div>
        <div><strong>4</strong><span>service boundaries</span></div>
        <div><strong>100%</strong><span>synthetic demo data</span></div>
      </section>

      <section id="foundation" className="foundation">
        <div className="sectionHeading">
          <span>Engineering foundation</span>
          <h2>Built to grow one verified layer at a time.</h2>
        </div>
        <div className="cards">
          {foundationItems.map((item) => (
            <article className="card" key={item.number}>
              <span className="cardNumber">{item.number}</span>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="nextStep">
        <div>
          <span className="eyebrow">Next milestone</span>
          <h2>Simulated device telemetry</h2>
        </div>
        <p>A deterministic Python service will publish versioned viscosity events through MQTT.</p>
      </section>

      <footer>
        <p>Educational prototype · Not for diagnosis or patient care</p>
        <p>Developed by Sahib Sohi and another founder</p>
      </footer>
    </main>
  );
}
