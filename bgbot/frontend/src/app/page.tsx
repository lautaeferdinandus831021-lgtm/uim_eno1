"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Dev mode: auto-login, go straight to setup
    const token = api.getToken();
    if (token) {
      router.replace("/setup");
    } else {
      // Try auto-login with dev credentials
      api.login("dev@bgbot.local", "dev123456")
        .then(() => router.replace("/setup"))
        .catch(() => router.replace("/login"));
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="text-2xl font-bold text-t1 mb-2">
          BG-BOT <span className="text-acc">v5</span>
        </div>
        <div className="text-t3 text-sm">Starting...</div>
      </div>
    </div>
  );
}
