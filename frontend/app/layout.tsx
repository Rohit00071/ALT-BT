import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "AI Manim Animator — Generate Math Animations with AI",
  description:
    "Type a math concept, choose a language, and let AI generate beautiful educational animations using Manim. Free and open-source.",
  keywords: [
    "manim",
    "math animation",
    "AI",
    "education",
    "generative AI",
    "Gemini",
    "math video",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`} suppressHydrationWarning={true}>
        {/* Animated background orbs */}
        <div className="bg-orb bg-orb-1" />
        <div className="bg-orb bg-orb-2" />
        <div className="bg-orb bg-orb-3" />
        {children}
      </body>
    </html>
  );
}
