/**
 * Utilities for resolving asset image URLs consistently across
 * Vite development server, backend static mounts, and production builds.
 */

export function resolveImageUrl(url?: string | null): string {
  if (!url) return '';
  
  // Return absolute URLs as is
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
    return url;
  }

  // If URL starts with /static/ or /uploads/, return directly so Vite proxy or production root serves it
  if (url.startsWith('/static/') || url.startsWith('/uploads/') || url.startsWith('/furniture/')) {
    return url;
  }

  // Fallback to ensuring leading slash
  return url.startsWith('/') ? url : `/${url}`;
}
