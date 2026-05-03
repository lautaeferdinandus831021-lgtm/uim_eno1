"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [checking, setChecking] = useState(true);

  // Auto-login check on mount
  useEffect(() => {
    const token = api.getToken();
    if (token) {
      router.replace("/setup");
      return;
    }

    // Try auto-login with dev credentials
    api.login("dev@bgbot.local", "dev123456")
      .then(() => {
        router.replace("/setup");
      })
      .catch(() => {
        setChecking(false); // Show login form
      });
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.login(email, password);
      router.push("/setup");
    } catch (err: any) {
      setError(err.message);
    }
    setLoading(false);
  };

  // Show loading while checking auto-login
  if (checking) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-bold text-t1 mb-2">
            BG-BOT <span className="text-acc">v5</span>
          </div>
          <div className="text-t3 text-sm">Connecting...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-t1">BG-BOT <span className="text-acc">v5</span></h1>
          <p className="text-t3 text-sm mt-1">Sign in to your account</p>
        </div>

        {error && (
          <div className="bg-red/10 border border-red/30 text-red text-sm rounded-md px-4 py-2.5 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Button type="submit" loading={loading} className="w-full">Sign In</Button>
        </form>

        <p className="text-t3 text-xs mt-6 text-center">
          No account? <a href="/register" className="text-acc hover:underline">Register</a>
        </p>
      </div>
    </div>
  );
}
