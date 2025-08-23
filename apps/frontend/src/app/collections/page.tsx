"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * Collections page that redirects to /library
 * This maintains backward compatibility with navigation links
 */
export default function CollectionsPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/library");
  }, [router]);

  return (
    <div className="min-h-screen bg-gamer-dark flex items-center justify-center">
      <div className="text-gamer-text">
        <p>Redirecting to your library...</p>
      </div>
    </div>
  );
}
