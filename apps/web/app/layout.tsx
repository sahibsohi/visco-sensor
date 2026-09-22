import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "Visco-Sensor | Monitoring platform",
  description: "Software platform for the Visco-Sensor med-tech prototype.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
